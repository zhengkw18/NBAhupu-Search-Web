from scrapy import cmdline
from multiprocessing import Process
import time
import multiprocessing
import logging
class run:
    def task(self):
        cmdline.execute('scrapy crawl newsspider'.split())
    def main_run(self):
        while True:
            pp=multiprocessing.Process(target=self.task)
            logging.info('pp run ')
            pp.start()
            pp.join()
            time.sleep(60)

if __name__=='__main__':
    obj=run()
    obj.main_run()
