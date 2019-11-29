from django.urls import path, register_converter
from . import views, my_converter


app_name = 'app'

register_converter(my_converter.FourDigitConverter, "4_d")
register_converter(my_converter.TwoDigitConverter, "2_d")

urlpatterns = [
    path('index', views.index, name='index'),
    path('graph/<4_d:y>/<2_d:m>/<2_d:d>', views.show_graph, name='graph'),
    path('graphFactor/<4_d:y>/<2_d:m>/<2_d:d>', views.throw_sensor_data, name='graphFactor'),
    path('realTimeData/', views.throw_one_sensor_data, name='realtime'),
    path('camera', views.camera, name='camera'),
]
