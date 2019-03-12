import os,time,stat

path='D:\projects\major\images'


while True:
    for d in os.listdir(path):
        d=os.path.join(path,d)
        if os.path.isdir(d):
            for f in os.listdir(d):
                f=os.path.join(d,f)
                print('deleting',f)
                os.remove(f)
    time.sleep(1000)    