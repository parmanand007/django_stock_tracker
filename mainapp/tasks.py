from celery import shared_task
from yahoo_fin.stock_info import *
from django.http import HttpResponse
import time
import queue
from threading import Thread
@shared_task(bind=True)
def update_stock(self,stockpicker):
    data={}
    available_stocks=tickers_nifty50()
    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            stockpicker.remove(i)
    #we use threading  when line 25 run for single stock then our cpu is id le
    n_threads = len(stockpicker)
    thread_list=[]
    que = queue.Queue()

    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}), args = (que, stockpicker[i]))
        thread_list.append(thread)  #list need to join later
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result= que.get()
        data.update(result)
    
    return "Done"

 