#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Author    : KK
# @Time     : 2019/10/22

from kafka import KafkaProducer, KafkaConsumer, TopicPartition, OffsetAndMetadata
import random
import threading


class KafkaTemplate:
    """
    实现 kafka 连接，可直接创建生产者、消费者
    """

    # 生产者配置
    __DEFAULT_PRODUCER_CONFIG = {
        "key_serializer": lambda m: m.encode('utf-8') if m else None,
        "value_serializer": lambda m: m.encode('utf-8'),
        'max_request_size': 5242880,
        'receive_buffer_bytes': 5242880,
        'send_buffer_bytes': 5242880
    }

    # 消费者配置
    __DEFAULT_CONSUMER_CONFIG = {
        "key_deserializer": lambda m: m.decode('utf-8') if m else None,
        "value_deserializer": lambda m: m.decode('utf-8'),
        'fetch_max_wait_ms': 500,
        'fetch_min_bytes': 1,
        'fetch_max_bytes': 5242880,
        'max_partition_fetch_bytes': 1048576,
        'request_timeout_ms': 40 * 1000,
        'retry_backoff_ms': 100,
        'reconnect_backoff_ms': 50,
        'reconnect_backoff_max_ms': 1000,
        'max_in_flight_requests_per_connection': 5,
        'auto_offset_reset': 'latest',
        'auto_commit_interval_ms': 3000,
        'default_offset_commit_callback': lambda offsets, response: True,
        'check_crcs': True,
        'metadata_max_age_ms': 5 * 60 * 1000,
        'heartbeat_interval_ms': 3000,
        'session_timeout_ms': 30000,
        'max_poll_records': 100,
        'receive_buffer_bytes': 5242880,
        'send_buffer_bytes': 5242880
    }

    def __init__(self, bootstrap_server, client_id=None):
        self.bootstrap_server = bootstrap_server
        self.client_id = client_id if client_id else "".join(random.sample('abcderghijklmnopqrstuvwxyz', 6))
        # 生产者懒加载
        self.producer = None

    def consume(self, topic, group, func, async_param=False, **config):
        """
        创建消费者，通过 async 可设置异步消费
        :param topics: 消费主题
        :param group: 消费者组
        :param func: 消息处理函数
        :param async: 异步消费
        :param config: 消费者配置
        :return:
        """
        conf = {
            'bootstrap_servers': self.bootstrap_server,
            'client_id': self.client_id,
            'group_id': group
        }
        conf = {**self.__DEFAULT_CONSUMER_CONFIG, **conf, **config}

        def handler():
            consumer = None
            topics = [topic] if isinstance(topic, str) else topic.copy()
            try:
                consumer = KafkaConsumer(*topics, **conf)
                for message in consumer:
                    func(message.key, message.value, message.topic, message.partition, message.offset)
                    # 控制 kafka topic 偏移量，
                    if 'enable_auto_commit' in conf and not conf['enable_auto_commit']:
                        consumer.commit_async(
                            {TopicPartition(message.topic, message.partition): OffsetAndMetadata(message.offset, None)})
            finally:
                if consumer:
                    consumer.close()

        # 不异步执行，会阻塞在当前方法
        if async_param:
            thread = threading.Thread(target=handler)
            thread.setDaemon(True)
            thread.start()
        else:
            handler()

    def produce(self, topic, value, key=None, partition=None, timeout=10, **config):
        """
        创建生产者
        :param topic:
        :param value:
        :param key:
        :param partition:
        :param timeout: 默认10秒
        :return:
        """
        if not self.producer:
            conf = {
                'bootstrap_servers': self.bootstrap_server,
                'client_id': self.client_id
            }
            conf = {**self.__DEFAULT_PRODUCER_CONFIG, **conf, **config}
            self.producer = KafkaProducer(**conf)
        self.producer.send(topic, value=value, key=key, partition=partition).get(timeout)


def one_test(key, value, topic, partition, offset):
    print(key, value, topic, partition, offset)


if __name__ == '__main__':
    import time
    # kafka_template = KafkaTemplate(['10.1.6.25:9092', '10.1.6.24:9092'])
    kafka_template = KafkaTemplate('192.168.0.158:9092')
    kafka_template.consume("SPIDER_SAVE_BAIDU_KAFKA", "amazing",
                           one_test,
                           async_param=True)
    for i in range(10):
        kafka_template.produce("SPIDER_SAVE_BAIDU_KAFKA", f"{i}: sefsefesfesggsgsegesgsegsegsegse")
    time.sleep(6000)
