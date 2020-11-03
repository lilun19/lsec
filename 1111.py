import time
start_stamp=time.mktime(time.strptime('2020-09-14 00:00:00', '%Y-%m-%d %H:%M:%S'))
end_stamp=time.mktime(time.strptime('2020-09-14 23:59:59', '%Y-%m-%d %H:%M:%S'))
print(start_stamp)
print(end_stamp)