from celery import shared_task
from yahoo_fin.stock_info import *
from django.http import HttpResponse
import time
import queue
from threading import Thread
from channels.layers import get_channel_layer
import asyncio

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
    
    #send date to group
    channel_layer=get_channel_layer()
    loop = asyncio.new_event_loop()

    #set event loop inside in thread
    asyncio.set_event_loop(loop)

    loop.run_until_complete(channel_layer.group_send("stock_track",{
        'type':'send_stock_update',
        'message':data
    }))

    return "Done"

 