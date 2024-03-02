from django.shortcuts import render
from yahoo_fin.stock_info import *
from django.http import HttpResponse
import time
import queue
from threading import Thread
# Create your views here.


def stockPicker(request):
    stock_picker=tickers_nifty50()
    print(stock_picker)
    return render(request,'mainapp/stockpicker.html',{'stockpicker':stock_picker})
    ...

def stockTracker(request):
    stockpicker=request.GET.getlist('stockpicker')
    print(stockpicker)
    data={}
    available_stocks=tickers_nifty50()
    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            return HttpResponse("Error")
    #we use threading  when line 25 run for single stock then our cpu is id le
    n_threads = len(stockpicker)
    thread_list=[]
    que = queue.Queue()
    start=time.time()
    # for i in stockpicker:
    #     details = get_quote_table(i)
    #     data.update({i:details})
    for i in range(n_threads):
        thread = thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}), args = (que, stockpicker[i]))
    end = time.time()
    time_taken= end-start

    print("time taken is",time_taken)
    print(data)
    return render(request,"mainapp/stocktracker.html")