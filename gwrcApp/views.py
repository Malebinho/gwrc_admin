import csv
import json
import datetime
import sys

from django.contrib.auth import authenticate, login as gwrc_login, logout as gwrc_logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import connection
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from .serializers import AlarmSerializer
import xlwt
from django.http import JsonResponse, HttpResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q
from .models import *

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


# ----- Funçoes de login -------------------------
def login(request):
    return render(request, 'login.html')

# ----- Funçoes de logout -------------------------


def logout(request):
    gwrc_logout(request)
    return redirect('/login/')

# ----- Funçoes de login/submit -------------------------
@csrf_protect
def login_submit(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            gwrc_login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Usuário ou Senha inválidos. Tente novamente.')
    return redirect('/login/#')


#------------- Alterar a senha -------------------------------
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Senha atualizada com sucesso')
            return redirect('change_password')
        else:
            messages.error(request, 'Por favor, verificar as senhas inseridas...')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


@login_required(login_url='/login/')
def sms_functions(request):
    # ---------------- Listagen quantidade total de agentes ----------------
    qtd_agentes = Processe.objects.exclude(agent_sap_reference=None). \
        values('agent_sap_reference').distinct().count()

    # ---------------- Listagen quantidade total de subagentes -------------
    qtd_subagentes = Processe.objects.exclude(user_id=None). \
        values('user_id').distinct().count()

    # ---------------- Listagen quantidade total de mobiles -----------------
    qtd_mobiles = Sms.objects.exclude(imei=None).values('imei').distinct().count()

    # ---------------- Listagen quantidade total de msisdns -----------------
    qtd_msisdns = Sms.objects.exclude(originator_msisdn=None). \
        exclude(originator_msisdn="Unknown MSISDN") \
        .values('originator_msisdn').distinct().count()


    # ---------------- Listagen das SMSs recebidas nas GWRC -----------------

    sms_list = Sms.objects.get_queryset().order_by('date_received').reverse()
    paginator = Paginator(sms_list, 20)
    page = request.GET.get('page')
    sms_list = paginator.get_page(page)

    context = {'sms_list': sms_list,
               'qtd_agentes': qtd_agentes,
               'qtd_subagentes': qtd_subagentes,
               'qtd_mobiles': qtd_mobiles,
               'qtd_msisdns': qtd_msisdns
              }
    return render(request, 'gw_sms_list.html', context)


# ----- Funçoes baseadas em views da proxies ------------
@login_required(login_url='/login/')
def proxies_list(request):

    # ---------------- Listagen dos erros nas proxiesRC -----------------
    qtd_error_proxy = Sms.objects.filter(~Q(error_code ='EAI_0_0')).values('error_code','proxy_id').\
        annotate(my_count_proxy=Count('sms_id')).order_by('-my_count_proxy')

    # ---------------- Listagen das contagens dos pedidos por operaçoes - PROXIES 01 -----------------
    count_operation_proxies = Sms.objects.exclude(operation_type=None).filter(Q(proxy_id='sdgw_gwrc_01'), ~Q(operation_type='4'), ~Q(operation_type='0')).\
                                  values('operation_type').annotate(my_count=Count('sms_id')). \
                                  distinct().order_by('-operation_type')[:10]

    # ---------------- Listagen das contagens dos pedidos por operaçoes - PROXIES 02 -----------------
    count_operation_proxies2 = Sms.objects.exclude(operation_type=None).filter(Q(proxy_id='sdgw_gwrc_02'), ~Q(operation_type='4'), ~Q(operation_type='0')). \
                                  values('operation_type').annotate(my_count=Count('sms_id')). \
                                  distinct().order_by('-operation_type')[:10]

    # ---------------- Listagen das contagens dos pedidos por operaçoes - PROXIES 03 -----------------
    count_operation_proxies3 = Sms.objects.exclude(operation_type=None).filter(Q(proxy_id='sdgw_gwrc_03'), ~Q(operation_type='4'), ~Q(operation_type='0')). \
                                   values('operation_type').annotate(my_count=Count('sms_id')). \
                                   distinct().order_by('-operation_type')[:10]

    # ---------------- Listagen das contagens dos pedidos por operaçoes - PROXIES 03 -----------------
    count_operation_proxies4 = Sms.objects.exclude(operation_type=None).filter(Q(proxy_id='sdgw_gwrc_04'), ~Q(operation_type='4'), ~Q(operation_type='0')). \
                                   values('operation_type').annotate(my_count=Count('sms_id')). \
                                   distinct().order_by('-operation_type')[:10]

    context = {
        'count_operation_proxie': count_operation_proxies,
        'count_operation_proxie2': count_operation_proxies2,
        'count_operation_proxie3': count_operation_proxies3,
        'count_operation_proxie4': count_operation_proxies4,
        'row_error_proxy': qtd_error_proxy
    }

    return render(request, 'gw_proxies.html', context)


#----------------------- Funcoes que retornam o JSON para os graficos das proxies ----------------
@login_required(login_url='/login/')
def chart_operations(request):
    count_operations_chart = list(Sms.objects.exclude(operation_type=None).filter(Q(proxy_id='sdgw_gwrc_01'), ~Q(operation_type='4'), ~Q(operation_type='0')).\
                                  values('operation_type').annotate(my_count=Count('sms_id')). \
                                  distinct().order_by('-my_count')[:10])

    count_operations_chart2 = list(Sms.objects.exclude(operation_type=None).filter(Q(proxy_id='sdgw_gwrc_02'), ~Q(operation_type='4'), ~Q(operation_type='0')).\
                                  values('operation_type').annotate(my_count=Count('sms_id')). \
                                  distinct().order_by('-my_count')[:10])

    count_operations_chart3 = list(Sms.objects.exclude(operation_type=None).filter(Q(proxy_id='sdgw_gwrc_03'), ~Q(operation_type='4'), ~Q(operation_type='0')). \
                                   values('operation_type').annotate(my_count=Count('sms_id')). \
                                   distinct().order_by('-my_count')[:10])

    count_operations_chart4 = list(Sms.objects.exclude(operation_type=None).filter(Q(proxy_id='sdgw_gwrc_04'), ~Q(operation_type='4'), ~Q(operation_type='0')). \
                                   values('operation_type').annotate(my_count=Count('sms_id')). \
                                   distinct().order_by('-my_count')[:10])
    data = dict()
    data['count_operations_chart'] = count_operations_chart
    data['count_operations_chart2'] = count_operations_chart2
    data['count_operations_chart3'] = count_operations_chart3
    data['count_operations_chart4'] = count_operations_chart4

    return JsonResponse(data)


@login_required(login_url='/login/')
def grafico_proxy(request):
    return render(request, 'gw_proxies.html')


# ----- Funçoes baseadas em views da gateways ------------
@login_required(login_url='/login/')
def gataways_list(request):

    charts_gwrc1 = Processe.objects.all()

    operations = [obj.agent_sap_reference for obj in charts_gwrc1]
    qtd_operations = [int(obj.process_id) for obj in charts_gwrc1]

       # ---------------- Listagen das contagens dos pedidos por operaçoes - GWRC 01 -----------------
    count_operation_gwrc = Sms.objects.exclude(operation_type=None).filter(Q(sms_history_id='gwrc_02'), ~Q(operation_type='4'), ~Q(operation_type='0')). \
                                  values('operation_type').annotate(my_count=Count('sms_id')). \
                                  distinct().order_by('-operation_type')[:10]

    # ---------------- Listagen das contagens dos pedidos por operaçoes - GWRC 02 -----------------
    count_operation_gwrc2 = Sms.objects.exclude(operation_type=None).filter(Q(sms_history_id='gwrc_03'), ~Q(operation_type='4'), ~Q(operation_type='0')). \
                                   values('operation_type').annotate(my_count=Count('sms_id')). \
                                   distinct().order_by('-operation_type')[:10]

    # ---------------- Listagen das contagens dos pedidos por operaçoes - GWRC 03 -----------------
    count_operation_gwrc3 = Sms.objects.exclude(operation_type=None).filter(Q(sms_history_id='gwrc_04'), ~Q(operation_type='4'), ~Q(operation_type='0')). \
                                   values('operation_type').annotate(my_count=Count('sms_id')). \
                                   distinct().order_by('-operation_type')[:10]

    # ---------------- Listagen das contagens dos pedidos por operaçoes - GWRC 03 -----------------
    count_operation_gwrc4 = Sms.objects.exclude(operation_type=None).filter(Q(sms_history_id='gwrc_05'), ~Q(operation_type='4'), ~Q(operation_type='0')). \
                                   values('operation_type').annotate(my_count=Count('sms_id')). \
                                   distinct().order_by('-operation_type')[:10]

    context = {
        'count_operation_gwrc': count_operation_gwrc,
        'count_operation_gwrc2': count_operation_gwrc2,
        'count_operation_gwrc3': count_operation_gwrc3,
        'count_operation_gwrc4': count_operation_gwrc4,
        'operations': json.dumps(operations),
        'qtd_operations': json.dumps(qtd_operations),
    }

    return render(request, 'gw_gwrc.html', context)


#----------------------- Funcoes que retornam o JSON para os graficos das GWRC ----------------

@login_required(login_url='/login/')
def chart_operations_gw(request):
    count_operations_chart_gw = list(Sms.objects.exclude(operation_type=None).filter(Q(sms_history_id='gwrc_02'), ~Q(operation_type='4'), ~Q(operation_type='0')).\
                                  values('operation_type').annotate(my_count=Count('sms_id')). \
                                  distinct().order_by('-my_count')[:10])

    count_operations_chart_gw2 = list(Sms.objects.exclude(operation_type=None).filter(Q(sms_history_id='gwrc_03'), ~Q(operation_type='4'), ~Q(operation_type='0')).\
                                  values('operation_type').annotate(my_count=Count('sms_id')). \
                                  distinct().order_by('-my_count')[:10])

    count_operations_chart_gw3 = list(Sms.objects.exclude(operation_type=None).filter(Q(sms_history_id='gwrc_04'), ~Q(operation_type='4'), ~Q(operation_type='0')). \
                                   values('operation_type').annotate(my_count=Count('sms_id')). \
                                   distinct().order_by('-my_count')[:10])

    count_operations_chart_gw4 = list(Sms.objects.exclude(operation_type=None).filter(Q(sms_history_id='gwrc_05'), ~Q(operation_type='4'), ~Q(operation_type='0')). \
                                   values('operation_type').annotate(my_count=Count('sms_id')). \
                                   distinct().order_by('-my_count')[:10])
    data = dict()
    data['count_operations_chart_gw'] = count_operations_chart_gw
    data['count_operations_chart_gw2'] = count_operations_chart_gw2
    data['count_operations_chart_gw3'] = count_operations_chart_gw3
    data['count_operations_chart_gw4'] = count_operations_chart_gw4

    return JsonResponse(data)


@login_required(login_url='/login/')
def grafico_gwrc(request):
    return render(request, 'gw_gwrc.html')


# ----- Funçoes baseadas em views dos processos RC ------------
@login_required(login_url='/login/')
def processes_list(request):

    process_list = Processe.objects.get_queryset().order_by('created_date').reverse()
    paginator = Paginator(process_list, 20)
    page = request.GET.get('page')
    process_list = paginator.get_page(page)

    # ---------------- Listagen das contagens dos processos - GWRC 01 -----------------
    count_process_gwrc = Processe.objects.exclude(status=None).filter(Q(process_history_id='gwrc_02')). \
                               values('status').annotate(my_count=Count('process_id')). \
                               distinct().order_by('-status')[:10]

    # ---------------- Listagen das contagens dos processos - GWRC 02 -----------------
    count_process_gwrc2 = Processe.objects.exclude(status=None).filter(Q(process_history_id='gwrc_03')). \
                                values('status').annotate(my_count=Count('process_id')). \
                                distinct().order_by('-status')[:10]

    # ---------------- Listagen das contagens dos processos - GWRC 03 -----------------
    count_process_gwrc3 = Processe.objects.exclude(status=None).filter(Q(process_history_id='gwrc_04')). \
                                values('status').annotate(my_count=Count('process_id')). \
                                distinct().order_by('-status')[:10]

    # ---------------- Listagen das contagens dos processos - GWRC 03 -----------------
    count_process_gwrc4 = Processe.objects.exclude(status=None).filter(Q(process_history_id='gwrc_05')). \
                                values('status').annotate(my_count=Count('process_id')). \
                                distinct().order_by('-status')[:10]

    context = {
        'count_process_gwrc': count_process_gwrc,
        'count_process_gwrc2': count_process_gwrc2,
        'count_process_gwrc3': count_process_gwrc3,
        'count_process_gwrc4': count_process_gwrc4,
        'process_list': process_list,
    }
    return render(request, 'gw_process.html', context)


# ----- Funçoes baseadas em views das operaçoesRC ------------
@login_required(login_url='/login/')
def operation_list(request):

    # ---------------- Listagen agrupadas por operaçoes sRC -----------------
    qtd_operation = Operation.objects.values('operation_type', 'operation_history_id','status'). \
        annotate(my_count_operation=Count('process_id')).order_by('-my_count_operation')

    operation_list = Operation.objects.get_queryset().order_by('created_date').reverse()
    paginator = Paginator(operation_list, 10)
    page = request.GET.get('page')
    operation_list = paginator.get_page(page)

    context = {
               'row_operation_gwrc': qtd_operation,
               'operation_list': operation_list,
    }

    return render(request, 'gw_operation.html', context)


# ----- Funçoes baseadas em views das requisiçoesRC ------------
@login_required(login_url='/login/')
def request_list(request):
    # ---------------- Listagen agrupadas por requisiçoesRC -----------------
    #today = datetime.date.today()
    qtd_request_cdr = Eai_cdr.objects.values('method', 'eai_error_code', 'eai_cdr_history_id'). \
        annotate(my_count_cdr=Count('eai_cdr_id')).order_by('-eai_cdr_history_id')

    request_list = Eai_cdr.objects.get_queryset().order_by('created_date').reverse()
    paginator = Paginator(request_list, 7)
    page = request.GET.get('page')
    request_list = paginator.get_page(page)

    context = {
        'row_request_gwrc': qtd_request_cdr,
        'request_list': request_list,
    }

    return render(request, 'gw_request.html', context)


# ----- Funçoes baseadas em views dos AlarmsRC ------------
@login_required(login_url='/login/')
def alarms_list(request):
    # ---------------- Listagen agrupadas por alarmes -----------------
    qtd_alarms = Alarm.objects.exclude(type=None).values('type').annotate(my_count=Count('alarm_id')). \
                                distinct().order_by('-my_count')[:10]

    # ---------------- Listagen agrupadas por pedidos SMS -----------------
    qtd_pedido_sms = Sms.objects.exclude(error_code=None).values('proxy_id','error_code').annotate(my_count=Count('sms_id')). \
                     distinct().order_by('-my_count')[:10]

    # ---------------- Listagen dos erros nas GatewaysRC -----------------
    qtd_error_gwrc = Sms.objects.values('error_code', 'sms_history_id'). \
        annotate(my_count_gwrc=Count('sms_id')).order_by('-my_count_gwrc')

    context = {
        'qtd_alarms': qtd_alarms,
        'qtd_pedido_sms': qtd_pedido_sms,
        'qtd_error_gwrc': qtd_error_gwrc,
    }

    return render(request, 'gw_alarms.html', context)


# ----- Funçoes baseadas em views dos PropriedadesRC ------------
@login_required(login_url='/login/')
def propriedade_list(request):
    # ---------------- Listagen agrupadas por requisiçoesRC -----------------
    propriedade_list = Mobile_propertie.objects.get_queryset().order_by('value').reverse()

    context = {
        'row_propriedade_list': propriedade_list,
    }

    return render(request, 'gw_propriedade.html', context)


# ----- Funçoes baseadas em views dos PropriedadesRC ------------
@login_required(login_url='/login/')
def search_gwrc(request):
    # ---------------- Listagen agrupadas por requisiçoesRC -----------------
    search_mobile = request.GET.get('pesquisa_msisdn', None)
    mobile_msisdn_list = ''
    if search_mobile:
        mobile_msisdn_list = Sms.objects.filter(originator_msisdn__icontains=search_mobile)

    search_agente = request.GET.get('pesquisa_agente', None)
    sap_reference_list = ''
    if search_agente:
        sap_reference_list = Processe.objects.filter(agent_sap_reference__icontains=search_agente)

    context = {
        'row_mobile_msisdn_list': mobile_msisdn_list,
        'row_sap_reference_list': sap_reference_list,
    }

    return render(request, 'gw_consultas.html', context)

@login_required(login_url='/login/')
def search_duplicate(request):
    # ---------------- Listagen agrupadas por requisiçoesRC -----------------

    context = {

    }

    return render(request, 'gw_duplicado.html', context)


@login_required(login_url='/login/')
def search_agente_reg(request):
    # ---------------- Listagen agrupadas por requisiçoesRC -----------------

    context = {

    }
    return render(request, 'gw_agente_reg.html', context)


@login_required(login_url='/login/')
def search_vinte_mais(request):
    # ---------------- Listagen agrupadas por requisiçoesRC -----------------

    context = {

    }
    return render(request, 'gw_agente_vinte.html', context)


@login_required(login_url='/login/')
def config_list(request):
    # ---------------- Listagen das configurações -----------------
    configure_prot_list = Config_propertie.objects.get_queryset().order_by('value')

    context = {
        'configure_prot_list': configure_prot_list,

    }
    return render(request, 'gw_config_list.html', context)


@login_required(login_url='/login/')
def white_list(request):
    # ---------------- Listagen dos Msisdn a whiteList -----------------
    configure_prot_list = white_list.objects.get_queryset().order_by('value')

    context = {

    }
    return render(request, 'gw_white_list.html', context)


def teste(request):
    if request.POST:
        valor = request.POST.getlist('numero')
        print (dict(request.POST)['numero'])
        print(valor)
    Rainbow = [938067463, 928957637, 933903441]
    for i in range(len(Rainbow)):
        print(Rainbow)
        users = Processe.objects.filter(sim_msisdn__in=Rainbow)
        print(users[i])
        context = {
            'list_user': users,
        }

    return render(request,'teste.html',context)


@login_required(login_url='/login/')
def search_mobile(request):
    # Filtrando os dados do agente
    search_mobiles = request.GET.get('imei', None)
    mobileData = None
    if search_mobiles:
        #print(search_agentes)
        mobileData = serializers.serialize("json", Sms.objects.filter(imei=search_mobiles).order_by('-date_received'))
    return JsonResponse({"mobileData": mobileData})


@login_required(login_url='/login/')
def search_agente(request):
    # Filtrando os dados do agente
    search_agentes = request.GET.get('agente', None)
    agenteData = None
    if search_agentes:
        #print(search_agentes)
        agenteData = serializers.serialize("json", Processe.objects.filter(agent_sap_reference=search_agentes).order_by('-created_date'))
    return JsonResponse({"agenteData": agenteData})


@login_required(login_url='/login/')
def search_msisdn(request):
    # Filtrando os dados do agente
    search_msisdns = request.GET.get('msisdn', None)
    msisdnData = None
    if search_msisdns:
        #print(search_agentes)
        msisdnData = serializers.serialize("json", Processe.objects.filter(sim_msisdn=search_msisdns).order_by('-created_date'))
    return JsonResponse({"msisdnData": msisdnData})


@login_required(login_url='/login/')
def search_mobileMsisdn(request):
    # Filtrando os dados do agente
    search_mobileMsisdns = request.GET.get('mobileMsisdn', None)
    mobileMsisdnData = None
    if search_mobileMsisdns:
        #print(search_agentes)
        mobileMsisdnData = serializers.serialize("json", Sms.objects.filter(originator_msisdn=search_mobileMsisdns).order_by('-date_received'))
    return JsonResponse({"mobileMsisdnData": mobileMsisdnData})


#------------- Apresentar os detalhes do Agente -----------------

@login_required(login_url='/login/')
def detail_agente(request):
    # ---------------- Listagen quantidade total de agentes ----------------
    qtd_agentes = Processe.objects.exclude(agent_sap_reference=None). \
        values('agent_sap_reference').distinct().count()

    sms_list = connection.cursor()
    sms_list.execute(
        "SELECT P.AGENT_SAP_REFERENCE, A.NOME, A.ENDERECO  FROM GWRC.PROCESSES P INNER JOIN  GWRC.AGENTE_UNITEL A ON P.AGENT_SAP_REFERENCE = A.AGENT_SAP_REFERENCE GROUP BY P.AGENT_SAP_REFERENCE,A.NOME, A.ENDERECO")
    list_agentes = sms_list.fetchall()

    context = {'list_agentes': list_agentes,
               'qtd_agentes': qtd_agentes
             }
    return render(request, 'gw_detail_agent.html', context)


@login_required(login_url='/login/')
def detail_subAgent(request):
    # ---------------- Listagen quantidade total de agentes ----------------
    qtd_subagentes = Processe.objects.exclude(user_id=None). \
        values('user_id').distinct().count()

    sms_list = connection.cursor()
    sms_list.execute(
        "SELECT P.AGENT_SAP_REFERENCE, P.USER_ID, A.NOME, A.ENDERECO  FROM GWRC.PROCESSES P INNER JOIN  GWRC.AGENTE_UNITEL A ON P.AGENT_SAP_REFERENCE = A.AGENT_SAP_REFERENCE GROUP BY P.AGENT_SAP_REFERENCE,P.USER_ID,A.NOME, A.ENDERECO")
    list_agentes = sms_list.fetchall()

    context = {'list_agentes': list_agentes,
               'qtd_subagentes': qtd_subagentes
             }
    return render(request, 'gw_detail_subAgent.html', context)


@login_required(login_url='/login/')
def detail_msisdn(request):
    # ---------------- Listagen quantidade total de agentes ----------------
    qtd_mobiles = Sms.objects.exclude(imei=None).values('imei').distinct().count()

    list_mobile = Sms.objects.exclude(imei=None). \
                               values('imei','originator_msisdn', 'app_version'). \
                               distinct().order_by('-imei')

    context = {'list_mobile': list_mobile,
               'qtd_mobiles': qtd_mobiles
             }
    return render(request, 'gw_detail_mobile.html', context)


@login_required(login_url='/login/')
def csv_export(request):
    sms_list_export = Sms.objects.get_queryset().order_by('date_received').reverse()
    paginator = Paginator(sms_list_export, 10)
    page = request.GET.get('page')
    sms_list_export = paginator.get_page(page)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sms_list_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['DATA RECEPCAO', 'ORIGINATOR_MSISDN', 'PROXY_ID', 'OPERATION_TYPE', 'ERROR_CODE', 'SMS_HISTORY_ID', 'IMEI', 'APP_VERSION'])

    for sms_list_exported in sms_list_export:
        writer.writerow([sms_list_exported.date_received,
                         sms_list_exported.originator_msisdn,
                         sms_list_exported.proxy_id,
                         sms_list_exported.operation_type,
                         sms_list_exported.error_code,
                         sms_list_exported.sms_history_id,
                         sms_list_exported.imei,
                         sms_list_exported.app_version])
    return response


@login_required(login_url='/login/')
def excel_export(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sms_list')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['ORIGINATOR_MSISDN', 'PROXY_ID', 'OPERATION_TYPE', 'ERROR_CODE', 'SMS_HISTORY_ID', 'IMEI', 'APP_VERSION', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    sms_list_export = Sms.objects.all().values_list('originator_msisdn', 'proxy_id','operation_type','error_code', 'sms_history_id', 'imei', 'app_version').order_by('date_received').reverse()
    paginator = Paginator(sms_list_export, 10)
    page = request.GET.get('page')
    sms_list_export = paginator.get_page(page)

    for row in sms_list_export:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer





