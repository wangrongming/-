# -*- coding: utf-8 -*-

import codecs
import json
import sys
import uuid

from xxx import ObjectInfo
from xxxxxx import MessageToDict

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from kafka import KafkaConsumer

consumer = KafkaConsumer('EQS-TASK-TMALL-SPU-PROM', group_id='eqs-task', bootstrap_servers=['10.1.21.19:9092'])
for msg in consumer:
    pass


class ReadKafkaContent(object):
    @staticmethod
    def deserialize(msg):
        """
        反序列化
        :param msg:
        :return:
        """
        pb_obj = ObjectInfo()
        pb_obj.Clear()
        pb_obj.ParseFromString(msg.value)
        return MessageToDict(pb_obj, including_default_value_fields=True, preserving_proto_field_name=True)

    def consume_msg(self, consumer_obj):
        """
        逐条消费，返回反序列化后的内容
        :param consumer_obj:
        :return:
        """
        try:
            while True:
                msg = next(consumer_obj, None)
                if not msg:
                    continue
                content = self.deserialize(msg)
                return content
        except Exception as ex:
            print(u"消费kafka错误,退出测试")
            return None

    def entry(self, topic, ip, count=10, log="log_read_kafka_content.json"):
        """

        :param topic:topic
        :param ip:ip
        :param count:查询kafka数据数量,默认10条
        :param log:内容保存地址,默认
        :return:
        """
        print(u"开始......")
        try:
            # 创建kafka消费对象
            print(u"创建kafka消费对象...")
            consumer = KafkaConsumer(topic, group_id=uuid.uuid4().hex,
                                     bootstrap_servers=[ip],
                                     auto_offset_reset="latest", consumer_timeout_ms=3 * 1000)
        except Exception as ex:
            print(u"连接kafka失败!")
            return False
        print(u"kafka消费对象创建成功.")

        with open(log, "w") as f:
            for i in range(count):
                print(u"开始消费第%s条数据..." % str(i + 1))
                content = self.consume_msg(consumer)
                if not content:
                    return False

                # dict转json保存数据内容
                content_json = json.dumps(content, ensure_ascii=False, indent=4)
                f.write(content_json)
                f.write("\n\n")
                print(u"第%s条数据写入完成." % str(i + 1))

        print(u"完成.")
