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

cd /mnt/mongodb-linux-x86_64-rhel70-4.2.10/
./mongostat --port 28018
./bin/mongod --dbpath /mnt/mongo/00/data/ --logpath /mnt/mongo/00/logs/monog.log --bind_ip 0.0.0.0 --port 28018 --fork --replSet rs
./bin/mongod --dbpath /mnt/mongo/00/data/ --logpath /mnt/mongo/00/logs/monog.log --bind_ip 0.0.0.0 --port 28018 --fork --replSet rs


# 新建mongo复制集
`./bin/mongod --dbpath /home/mnt/mongo/00/data --logpath /home/mnt/mongo/00/logs/monog.log --bind_ip 0.0.0.0 --port 28018 --fork --replSet rs`
`./bin/mongod --dbpath /home/mnt/mongo/01/data --logpath /home/mnt/mongo/01/logs/monog.log --bind_ip 0.0.0.0 --port 28019 --fork --replSet rs`
`./bin/mongod --dbpath /home/mnt/mongo/02/data --logpath /home/mnt/mongo/02/logs/monog.log --bind_ip 0.0.0.0 --port 28020 --fork --replSet rs`
`./bin/mongod --dbpath /home/mnt/mongo/00/data --logpath /home/mnt/mongo/00/logs/monog.log --bind_ip 0.0.0.0 --port 28018 --shutdown`
`./bin/mongod --dbpath /home/mnt/mongo/01/data --logpath /home/mnt/mongo/01/logs/monog.log --bind_ip 0.0.0.0 --port 28019 --shutdown`
`./bin/mongod --dbpath /home/mnt/mongo/02/data --logpath /home/mnt/mongo/02/logs/monog.log --bind_ip 0.0.0.0 --port 28020 --shutdown`
`./bin/mongo --host 127.0.0.1 --port 28019`
`shell:`
`cfg={"_id":"rs","members":[{"_id":0,"host":"192.168.110.252:28018"},{"_id":1,"host":"192.168.110.252:28019"},{"_id":2,"host":"192.168.110.252:28020"}]}`
`rs.initiate(cfg)`
`rs.remove("192.168.110.252:28019")`
`rs.status()`
`rs.add("192.168.110.252:28019")` 
`rs.conf()`
`firewall-cmd --query-port=28018/tcp`
`firewall-cmd --add-port=28018/tcp --permanent`
`firewall-cmd --reload`
`firewall-cmd --query-port=28018/tcp`