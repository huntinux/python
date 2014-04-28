# coding:utf8

#
# 重定向标准输出、错误输出
#

import sys

# 输出会显示在终端上
print "hello world"

# 保存原来的设置
oldstdout = sys.stdout
oldstderr = sys.stderr

# 打开一个文件
f = open("log.out","w")

# 重定向标准输出,标准错误输出到刚才打开的文件
sys.stdout = f
sys.stderr = f

# 下面的输出会输出到log.out文件中
print "hello hongjing"

# 恢复原来的设置
sys.stdout = oldstdout
sys.stderr = oldstderr

# 关闭文件
f.close()
