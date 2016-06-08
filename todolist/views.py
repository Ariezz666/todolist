from django.http import HttpResponse
from django.shortcuts import render
from todolist.forms import JobForm
from todolist.models import TodoList, DoneJobs
from django.http import QueryDict

import json


def home(request):

    done = len(TodoList.objects.filter(is_finished = True))
    active = len(TodoList.objects.filter(is_finished = False))
    try:
        all_finished = DoneJobs.objects.all()
        for a in all_finished:
            all_finished_jobs = a.is_done
    except:
        all_finished_jobs = False

    tmpl_vars = {
        'jobs': TodoList.objects.all(),
        'form': JobForm(),
        'done': done,
        'active': active,
        'all_finished_job': all_finished_jobs,
    }
    return render(request, 'index.html', tmpl_vars)


def create_job(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')

        response_data = {}

        job = TodoList(title=job_title,)
        job.save()

        all_completed = DoneJobs.objects.all()

        if not all_completed:
            done = DoneJobs(is_done=0,)
            done.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = job.pk
        response_data['title'] = job.title
        response_data['active'] = len(TodoList.objects.filter(is_finished = False))

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def delete_job(request):
    if request.method == 'POST':

        job = TodoList.objects.get(id=QueryDict(request.body).get('job_pk'))

        job.delete()

        response_data = {}
        response_data['msg'] = 'Job is deleted.'
        response_data['active'] = len(TodoList.objects.filter(is_finished=False))
        response_data['done'] = len(TodoList.objects.filter(is_finished=True))

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def done_job(request):
    if request.method == 'POST':

        job = TodoList.objects.get(id=QueryDict(request.body).get('job_done_pk'))

        if job.is_finished:

            all = DoneJobs.objects.all()

            for a in all:
                all_done = a

            all_done.is_done -= 1
            all_done.save()
            all_finished_jobs = all_done.is_done
            job.is_finished = False
        else:
            all = DoneJobs.objects.all()

            for a in all:
                all_done = a
            all_done.is_done += 1
            all_done.save()
            all_finished_jobs = all_done.is_done
            job.is_finished = True


        job.save()

        response_data = {}
        response_data['msg'] = 'Job finished success.'
        response_data['active'] = len(TodoList.objects.filter(is_finished=False))
        response_data['done'] = len(TodoList.objects.filter(is_finished=True))
        response_data['isdone'] = job.is_finished
        response_data['allFinishedJobs'] = all_finished_jobs

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def delete_completed_job(request):
    if request.method == 'POST':
        delete_submit = request.POST.get('confirm')

        response_data = {}

        jobs = TodoList.objects.all()
        deleted_id = []
        for job in jobs:
            if job.is_finished:
                deleted_id.append(job.id)
                job.delete()

        response_data['result'] = 'Delete completed successful!'
        response_data['id'] = deleted_id

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def edit_job(request):
    if request.method == 'POST':

        job = TodoList.objects.get(id=QueryDict(request.body).get('job_edit_pk'))
        job_title = QueryDict(request.body).get('job_title')
        job.title = job_title
        job.save()

        response_data = {}
        response_data['msg'] = 'Job finished success.'
        response_data['isdone'] = job.is_finished
        response_data['title'] = job.title
        response_data['id'] = job.id

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )