from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', sms_functions, name="list"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('login/submit', login_submit, name="login_submit"),
    path('proxies/', proxies_list, name="proxies_list"),
    path('gateways/', gataways_list, name="gataways_list"),
    path('process/', processes_list, name="processes_list"),
    path('operation/', operation_list, name="operation_list"),
    path('request/', request_list, name="request_list"),
    path('alarms/', alarms_list, name="alarms_list"),
    path('propriedades/', propriedade_list, name="propriedade_list"),
    path('chart_operations/', chart_operations, name="chart_operations"),
    path('grafico_proxy/', grafico_proxy, name="grafico_proxy"),
    path('chart_operations_gw/', chart_operations_gw, name="chart_operations_gw"),
    path('grafico_gwrc/', grafico_gwrc, name="grafico_gwrc"),
    path('search_gwrc/', search_gwrc, name="search_gwrc"),
    path('csv_export/', csv_export, name="csv_export"),
    path('excel_export/', excel_export, name="excel_export"),
    path('teste/', teste, name="teste"),
    path('search_mobile/', search_mobile, name="search_mobile"),
    path('search_agente/', search_agente, name="search_agente"),
    path('search_mobileMsisdn/', search_mobileMsisdn, name="search_mobileMsisdn"),
    path('search_msisdn/', search_msisdn, name="search_msisdn"),
    path('search_duplicate/', search_duplicate, name="search_duplicate"),
    path('search_agente_reg/', search_agente_reg, name="search_agente_reg"),
    path('search_vinte_mais/', search_vinte_mais, name="search_vinte_mais"),
    path('config_list/', config_list, name="config_list"),
    path('white_list/', white_list, name="white_list"),
    path('detail_agente/', detail_agente, name="detail_agente"),
    path('detail_subAgent/', detail_subAgent, name="detail_subAgent"),
    path('detail_msisdn/', detail_msisdn, name="detail_msisdn"),

    # ------------------- Trabalhar com as password --------------
    path('password/', change_password, name='change_password'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"),
         name="password_reset_complete"),
]
