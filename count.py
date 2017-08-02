import time
from config import project

first = 0
old_counts = 0
while True:
    now_counts = project.find().count()
    add_count = now_counts - old_counts
    print(str(first) + ':    现在数据库有 '+ str(now_counts) + ' 条数据' + '  比上次增加了 ' + str(add_count) + ' 条数据')
    old_counts =  now_counts
    first = first + 1
    time.sleep(5)



# import random
# a=random.choice([0.1, 0.2, 0.3])
# print(a)