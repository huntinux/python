#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: huntinux@gmail.com
# Create Date: 2014年 06月 03日 星期二 10:33:08 CST
# Description: redis使用示例

from db import connectRedis



def main():
    machine_repo_dict = {
        "host1":"code1,code2",
        "host2":"code1,code2",
        "host3":"code1,code2",
    }

    # 增
    redis_conn = connectRedis()
    redis_conn.hmset('Deploy', machine_repo_dict)

    # 查
    hostname = "host1"
    repo = redis_conn.hget("Deploy", hostname)
    print repo

    # 删
    redis_conn.hdel("Deploy", hostname)

    # 改
    hostname = "host2"
    redis_conn.hset('Deploy', hostname, "code1")
    repo = redis_conn.hget("Deploy", hostname)
    print repo
    
    # 查询所有
    print redis_conn.hgetall("Deploy")

    # 删除全部
    redis_conn.delete("Deploy")

if __name__ == "__main__":
    main()


# 参考资料
# http://redis.io/ 
# http://redis.readthedocs.org/en/latest/index.html 
# http://www.redis.cn/
