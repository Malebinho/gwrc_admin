from django.db import models


class Utilizador(models.Model):
    id_utiizador = models.IntegerField()
    nome = models.CharField(max_length=255)
    utilizador = models.CharField(max_length=255)
    senha = models.IntegerField(primary_key=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now_add=True)


class Config_propertie(models.Model):

    class Meta:
        unique_together = (('module', 'module_id'),)

    module = models.CharField(max_length=255, primary_key=True)
    module_id = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    version = models.CharField(max_length=255)

    def __str__(self):
        return self.key

    class Meta:
        db_table = 'config_properties'


class Alarm(models.Model):
    alarm_id = models.IntegerField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=255)
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'alarms'


class Eai_cdr(models.Model):

    class Meta:
        unique_together = (('eai_cdr_history_id', 'eai_cdr_id'),)

    eai_cdr_id = models.IntegerField(primary_key=True)
    process_id = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    request_id = models.CharField(max_length=255)
    eai_error_code = models.CharField(max_length=255)
    eai_error_message = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    processor_id = models.CharField(max_length=255)
    operation_id = models.IntegerField()
    eai_cdr_history_id = models.CharField(max_length=255)
    guid = models.CharField(max_length=255)

    def __str__(self):
        return self.eai_error_code

    class Meta:
        db_table = 'eai_cdr'


class Mobile_propertie(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    value = models.IntegerField()

    def __str__(self):
        return self.key

    class Meta:
        db_table = 'mobile_properties'


class Operation(models.Model):
    class Meta:
        unique_together = (('operation_history_id', 'operation_id'),)

    operation_id = models.IntegerField(primary_key=True)
    process_id = models.IntegerField()
    operation_type = models.CharField(max_length=255)
    retry_count = models.IntegerField()
    retry_interval = models.IntegerField()
    base_request_id = models.CharField(max_length=255)
    id_processor = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    operation_history_id = models.CharField(max_length=255)

    def __str__(self):
        return self.operation_type

    class Meta:
        db_table = 'operation'


class Processe(models.Model):

    class Meta:
        unique_together = (('process_history_id', 'process_id'),)

    process_id = models.IntegerField(primary_key=True)
    end_of_upload_received = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)
    sim_status = models.IntegerField()
    sim_type = models.IntegerField()
    lrw_session_id = models.CharField(max_length=255)
    urd_session_id = models.CharField(max_length=255)
    doc_type = models.CharField(max_length=255)
    doc_number = models.CharField(max_length=255)
    doc_name = models.CharField(max_length=255)
    alternative_contact = models.CharField(max_length=255)
    lrw_lac = models.CharField(max_length=255)
    urd_lac = models.CharField(max_length=255)
    lrw_cell_id = models.CharField(max_length=255)
    urd_cell_id = models.CharField(max_length=255)
    agent_sap_reference = models.CharField(max_length=255)
    guid_gwrc = models.CharField(max_length=255)
    guid_kta = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    sim_msisdn = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    process_history_id = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return self.doc_name

    class Meta:
        db_table = 'processes'


class Sms(models.Model):
    class Meta:
        unique_together = (('sms_history_id', 'sms_id'),)

    sms_id = models.IntegerField(primary_key=True)
    process_id = models.IntegerField()
    date_received = models.DateTimeField(auto_now_add=True)
    date_replyed = models.DateTimeField(auto_now_add=True)
    originator_msisdn = models.CharField(max_length=255)
    originator_ip = models.CharField(max_length=255)
    proxy_id = models.CharField(max_length=255)
    network_node_id = models.CharField(max_length=255)
    operation_type = models.CharField(max_length=255)
    request = models.CharField(max_length=255)
    reply = models.CharField(max_length=255)
    error_code = models.CharField(max_length=255)
    sms_history_id = models.CharField(max_length=255)
    imei = models.CharField(max_length=255)
    app_version = models.CharField(max_length=255)

    def __str__(self):
        return self.originator_msisdn

    class Meta:
        db_table = 'sms'


class Agente_unitel(models.Model):
    agent_sap_reference = models.CharField(max_length=255)
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'AGENTE_UNITEL'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'


