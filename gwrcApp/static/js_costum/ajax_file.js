$(document).ready(function(){
 $("#buscar").click(function(){
     var imei = $("input[name='pesquisa[]']").val();
        $.ajax({
        url: '/search_mobile/',
        dataType: 'json',
        type: 'GET',
        data: 'imei='+imei,

        success: function(data){
            console.log(data)
            tableFromResponse(data);
        }
    });
});

 $("#agente").click(function(){
     var agente = $("input[name='agente[]']").val();
        $.ajax({
        url: '/search_agente/',
        dataType: 'json',
        type: 'GET',
        data: 'agente='+agente,

        success: function(data){
            console.log(data)
            tableFromAgente(data);
        }
    });
});



 $("#msisdn").click(function(){
     var msisdn = $("input[name='msisdn[]']").val();
        $.ajax({
        url: '/search_msisdn/',
        dataType: 'json',
        type: 'GET',
        data: 'msisdn='+msisdn,

        success: function(data){
            console.log(data)
            tableFromMsisdn(data);
        }
    });
});



$("#mobileMsisdn").click(function(){
     var mobileMsisdn = $("input[name='mobileMsisdn[]']").val();
        $.ajax({
        url: '/search_mobileMsisdn/',
        dataType: 'json',
        type: 'GET',
        data: 'mobileMsisdn='+mobileMsisdn,

        success: function(data){
            console.log(data)
            tableFromMobilemsisdn(data);
        }
    });
});


});

function tableFromResponse(responseData) {
        var mainObj = JSON.parse(responseData.mobileData);
        var k = '<tbody>'
        var m = '<tfoot>'
        if(mainObj == ""){
           m+='<tr>'
           m+='<td colspan="8" align="center"><div class="alert alert-warning alert-dismissible">Alerta de Pesquisa: Não existem dados para mostrar sobre esta pesquisa...</div></td>'
           m+='</tr>'
        }
        for(i = 0;i < mainObj.length; i++){
            k+= '<tr>';
            k+= '<td>' + mainObj[i]["fields"]["imei"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["date_received"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["originator_msisdn"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["proxy_id"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["operation_type"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["error_code"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["sms_history_id"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["app_version"] + '</td>';
            k+= '</tr>';
        }
        k+='</tbody>';
        m+='</tfoot>'
        document.getElementById('tableData1').innerHTML = m;
        document.getElementById('tableData').innerHTML = k;
}


function tableFromAgente(responseData) {
        var mainObj = JSON.parse(responseData.agenteData);
        var k = '<tbody>'
        var m = '<tfoot>'
        if(mainObj == ""){
           m+='<tr>'
           m+='<td colspan="9" align="center"><div class="alert alert-warning alert-dismissible">Alerta de Pesquisa: Não existem dados para mostrar sobre esta pesquisa...</div></td>'
           m+='</tr>'
        }
        for(i = 0;i < mainObj.length; i++){
            k+= '<tr>';
            k+= '<td>' + mainObj[i]["fields"]["agent_sap_reference"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["created_date"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["end_of_upload_received"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["sim_msisdn"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["guid_kta"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["process_history_id"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["user_id"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["urd_cell_id"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["status"] + '</td>';
            k+= '</tr>';
        }
        k+='</tbody>';
        m+='</tfoot>'
        document.getElementById('tableData2').innerHTML = m;
        document.getElementById('tableAgente').innerHTML = k;
}


function tableFromMsisdn(responseData) {
        var mainObj = JSON.parse(responseData.msisdnData);
        var k = '<tbody>'
        var m = '<tfoot>'
        if(mainObj == ""){
           m+='<tr>'
           m+='<td colspan="9" align="center"><div class="alert alert-warning alert-dismissible">Alerta de Pesquisa: Não existem dados para mostrar sobre esta pesquisa...</div></td>'
           m+='</tr>'
        }
        for(i = 0;i < mainObj.length; i++){
            k+= '<tr>';
            k+= '<td>' + mainObj[i]["fields"]["agent_sap_reference"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["created_date"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["end_of_upload_received"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["sim_msisdn"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["guid_kta"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["process_history_id"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["user_id"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["urd_cell_id"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["status"] + '</td>';
            k+= '</tr>';
        }
        k+='</tbody>';
        m+='</tfoot>'
        document.getElementById('tableData3').innerHTML = m;
        document.getElementById('tableMsisdn').innerHTML = k;
}

function tableFromMobilemsisdn(responseData) {
        var mainObj = JSON.parse(responseData.mobileMsisdnData);
        var k = '<tbody>'
        var m = '<tfoot>'
        if(mainObj == ""){
           m+='<tr>'
           m+='<td colspan="8" align="center"><div class="alert alert-warning alert-dismissible">Alerta de Pesquisa: Não existem dados para mostrar sobre esta pesquisa...</div></td>'
           m+='</tr>'
        }
        for(i = 0;i < mainObj.length; i++){
            k+= '<tr>';
            k+= '<td>' + mainObj[i]["fields"]["originator_msisdn"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["date_received"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["imei"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["proxy_id"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["operation_type"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["error_code"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["sms_history_id"] + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["app_version"] + '</td>';
            k+= '</tr>';
        }
        k+='</tbody>';
        m+='</tfoot>'
        document.getElementById('tableData4').innerHTML = m;
        document.getElementById('tablemobileMsisdn').innerHTML = k;
}