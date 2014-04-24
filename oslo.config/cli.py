#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from oslo.config import cfg

# 每个文件都可以加这行
CONF = cfg.CONF # 对本文件的参数做配置
common_opts = [
    cfg.StrOpt('bind-host',
               default='0.0.0.0',
               help='IP address to listen on'),
    cfg.IntOpt('bind-port',
               default=9292,
               help='Port number to listen on')
]
web_opts = [
    cfg.StrOpt('run-mode',
               default="local",
               choices=('gunicorn', 'local'),
               help="Run server use the specify mode.")
]

# 注册配置
CONF.register_cli_opts(common_opts)
CONF.register_cli_opts(web_opts, "web")

# 匹配sys.argv
CONF(sys.argv[1:], version="v1.0")

# 输出结果
print "bind-host:", CONF.bind_host
print "bind-port:", CONF.bind_port
print "web-run-mode:", CONF.web.run_mode
