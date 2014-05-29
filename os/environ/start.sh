#!/bin/bash

#
# bash注册环境变量, 然后python模块通过os.environ取得环境变量。
#

export SOURCE=first

python ./foo.py
