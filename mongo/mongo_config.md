# mongoDB 数据库安装
`参考文档 https://www.jianshu.com/p/d8f471bdfa3b`

`mongo文档库 https://www.mongodb.org/dl/linux/x86_64`

`下载 curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.0.6.tgz`
`下载 wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.0.6.tgz`
``
``
``
``
``
`
设置事务等待时间
db.adminCommand( { setParameter: 1, maxTransactionLockRequestTimeoutMillis: 5000 })
`

./bin/mongod --dbpath /mnt/mongo/00/data/ --logpath /mnt/mongo/00/logs/monog.log --bind_ip 0.0.0.0 --port 28018 --fork --replSet rs
