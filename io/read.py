

# 方法1 
try:
    f = open('/path/to/file', 'r')
    print f.read()
finally: # 记得close关闭文件，释放资源。
    if f:
        f.close()

# 方法2
# with 会帮助我们，自动调用close
# 所以更方便
with open('/path/to/file', 'r') as f:
	print f.read()
