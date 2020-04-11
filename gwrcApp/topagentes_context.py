from django.db import connection
from django.db.models import Count
from django.shortcuts import render

from .models import *


def top_registos12(request):
    top_agentes = Agente_unitel.objects.exclude(agent_sap_reference=None). \
             values('agent_sap_reference').annotate(my_count=Count('agent_sap_reference')). \
             distinct().order_by('-my_count')[:10]

    return {'top_agente': top_agentes}


def top_registos(request):
    qtd_error_gwrc = connection.cursor()
    qtd_error_gwrc.execute("SELECT COUNT(P.PROCESS_ID) AS QTD_REGISTO, A.NOME FROM GWRC.PROCESSES P INNER JOIN  GWRC.AGENTE_UNITEL A ON P.AGENT_SAP_REFERENCE = A.AGENT_SAP_REFERENCE GROUP BY A.NOME ORDER BY QTD_REGISTO DESC FETCH NEXT 12 ROWS ONLY")
    top_agentes = qtd_error_gwrc.fetchall()

    return {'top_agente': top_agentes}
















