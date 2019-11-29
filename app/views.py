from django.shortcuts import render
from django.http import HttpResponse
import sys
import json
from .models import Raspi_data
import datetime
import RPi.GPIO as GPIO


sys.path.append("/home/pi/python/django/temprature/tool/max31855")
from max31855 import MAX31855

# Create your views here.

def index(request):
    return render(request, 'app/index.html')

def camera(request):
    return render(request, 'app/camera.html')

today = datetime.date.today()

def show_graph(request,y=today.year, m=today.month, d=today.day):
    data = get_data(y,m,d)
    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    return HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=None)

def throw_sensor_data(request,y=today.year, m=today.month, d=today.day):
    data = get_sensor_data(y,m,d)
    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    return HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=None)

def throw_one_sensor_data(request):
    data = direct_get_sensor_data()
    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    return HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=None)


def get_data(y=today.year, m=today.month, d=today.day):

    labels = []
    ds = []

    datas = Raspi_data.objects.filter(date__year=y, date__month=m, date__day=d)

    title = "{0:%Y%m%d}".format(datas[1].date)


    for data in datas:
        labels.append("{0:%H:%M:%S}".format(data.date))
        ds.append(data.data1)
        

    data = {
        'type': 'line',
        'data': {
            'labels': labels,
            'datasets': [
            {
                'label': '温度',
                'data': ds,
                'borderColor': "rgba(255,0,0,1)",
                'backgroundColor': "rgba(0,0,0,0)"
            }
            ],
        },
        'options': {
            'title': {
            'display': 'true',
            'text': title + '室温'
            },
            'scales': {
            'xAxes': [{
                'type': 'realtime',
                'realtime': {
                    'delay':'2000',
                },
            }],
            'yAxes': [{
                'ticks': {
                'suggestedMax': 40,
                'suggestedMin': 0,
                'stepSize': 10,
                }
            }]
            },
        }
    }
    return data

#def get_graph(request):


def get_sensor_data(y=today.year, m=today.month, d=today.day):
    '''
    データベースから指定した日付の温度データを取得する
    '''

    labels = []
    ds = []

    datas = Raspi_data.objects.filter(date__year=y, date__month=m, date__day=d)

    title = "{0:%Y%m%d}".format(datas[1].date)


    for data in datas:
        labels.append("{0:%H:%M:%S}".format(data.date))
        ds.append(data.data1)
        

    data = {
        'temp': ds,
        'rec_time': labels,
        'graph_title': title,
    }
                
    return data

def direct_get_sensor_data():
    '''
    温度センサーから直接温度データを取得
    '''
    cs_pins =[24,] #CS(CS黄)
    clock_pin = 23 #SCLK(CLK青)
    data_pin = 21  #MOSI(DO緑)22
    units = "c"
    thermocouples = []
    for cs_pin in cs_pins:
        thermocouples.append(MAX31855(cs_pin, clock_pin, data_pin, units, board=GPIO.BOARD))
    
        try:
            for thermocouple in thermocouples:
                rj = thermocouple.get_rj()
                try:
                    tc = thermocouple.get()
                except MAX31855Error as e:
                    tc = "Error: "+ e.value
                    running = False
                #print("tc: {} and rj: {}".format(tc, rj))

        except KeyboardInterrupt:
            pass
    for thermocouple in thermocouples:
        thermocouple.cleanup()
    data = {
        'temp': tc,
    }

    return data
    