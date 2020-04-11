import env as env
from django_remote_submission.models import Server, Job, Interpreter
from django_remote_submission.tasks import submit_job_to_server, copy_key_to_server
from rest_framework import request
from django_remote_submission.tasks import copy_key_to_server
from django_remote_submission.tasks import delete_key_from_server

server = Server.objects.get_or_create(
    title='LAPTOPWT0312',
    hostname='LAPTOPWT0312.uninet.unitel.co.ao',
    port=8085,
)[0]

python2_interpreter = Interpreter.objects.get_or_create(
    name = 'python2',
    path = '/usr/bin/python2.7 -u',
)[0]

python3_interpreter = Interpreter.objects.get_or_create(
    name = 'python3',
    path = '/usr/bin/python3.5 -u',
)[0]

server.interpreters.set([python2_interpreter,
                         python3_interpreter])

job = Job.objects.get_or_create(
    title='My Job Title',
    program='print("hello world")',
    remote_directory='/tmp/',
    remote_filename='test.py',
    owner=request.user,
    server=server,
    interpreter=python2_interpreter,
)[0]

# Using delay calls celery:
modified_files = submit_job_to_server.delay(
    job_pk=job.pk,
    password=request.POST.get('password'),
    remote=False,
)

copy_key_to_server(
    username=env.remote_user,
    password=env.remote_password,
    hostname=env.server_hostname,
    port=env.server_port,
    public_key_filename=None, # finds it automaticaly
)


delete_key_from_server(
    username=env.remote_user,
    password=env.remote_password,
    hostname=env.server_hostname,
    port=env.server_port,
    public_key_filename=None,
)