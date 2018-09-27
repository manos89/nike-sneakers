from scrapy import cmdline
import os


count=0
while True:
    try:
        command='scrapy crawl snkrs'
        os.system(command)
    except Exception as E:
        print(str(E))
    print('DONE '+str(count))
    count+=1