from kafka import KafkaConsumer
from kafka import KafkaProducer


def consumer_kafka():
    # 消耗kafka数据
    consumer = KafkaConsumer('EQS-TASK-JD-SKU-DETAIL', group_id='eqs-task', bootstrap_servers=['192.168.6.11:9092'])
    for msg in consumer:
        pass


# 向kafka推送数据
def push_kafka():
    import uuid
    import time
    import json
    # producer = KafkaProducer(bootstrap_servers=["192.168.6.11:9092"], client_id="eqs")
    producer = KafkaProducer(bootstrap_servers=["10.1.21.9:9092", "10.1.21.19:9092", "10.1.21.44:9092"],
                             client_id="eqs")
    # sku = "100004619587"
    # task = {
    #     "id": str(uuid.uuid4()),
    #     "task_type": "JD_SKU_DETAIL",
    #     "sku": sku,
    #     "root_url": f"",
    #     "batch_no": time.strftime(f"%Y%m%d001"),
    #     "dispatched_at": int(time.time() * 1000),
    # }
    task = {
        "id": str(uuid.uuid4()),
        "task_type": "TMALL_SPU_LIST_M_ALL",
        "batch_no": time.strftime(f"%Y%m%d001"),
        "keyword": "",
        "root_url": "",
        "brand_id": "",
        "cat_id": "50936008",
        "limit": -1,
        "condition_id": "Objectid_hex",
        "dispatched_at": int(time.time() * 1000),
    }
    print(task)
    producer.send("EQS-TASK-GOODS-LIST", value=json.dumps(task, ensure_ascii=False).encode("utf-8")).get(20)
    # producer.send("EQS-TASK-JD-SKU-DETAIL", value=json.dumps(task, ensure_ascii=False).encode("utf-8")).get(20)


if __name__ == '__main__':
    push_kafka()
    # consumer_kafka()
