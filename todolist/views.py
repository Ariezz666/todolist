from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from todolist.forms import JobForm
from todolist.models import TodoList, DoneJobs
from django.http import QueryDict
import json


class TaskView(View):

    # get method return all tasks
    @staticmethod
    def get(request):

        done = len(TodoList.objects.filter(is_finished=True))
        active = len(TodoList.objects.filter(is_finished=False))
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

    # post method add new ask in db
    @staticmethod
    def post(request):
        if request.method == 'POST':

            # create and save new task
            job_title = request.POST.get('job_title')

            job = TodoList(title=job_title)
            job.save()

            # get how many tasks are finished already
            all_completed = DoneJobs.objects.all()
            if not all_completed:
                done = DoneJobs(is_done=0,)
                done.save()

            # create dictionary for response
            response_data = {}

            response_data['result'] = 'Create post successful!'
            response_data['postpk'] = job.pk
            response_data['title'] = job.title
            response_data['active'] = len(TodoList.objects.filter(is_finished=False))

            # return response
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"error": "error"}),
                content_type="application/json"
            )

    # method to remove task with id or all completed tasks
    @staticmethod
    def delete(request):
        if request.method == 'DELETE':

            id = QueryDict(request.body).get('job_pk')

            # if id exist delete task with this id
            if id:

                # delete task
                job = TodoList.objects.get(id=id)
                job.delete()

                # create dictionary for response
                response_data = {}
                response_data['msg'] = 'Job is deleted.'
                response_data['active'] = len(TodoList.objects.filter(is_finished=False))
                response_data['done'] = len(TodoList.objects.filter(is_finished=True))

                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json")

            # if id not exist delete all completed tasks
            else:

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
                json.dumps({"error": "error"}),
                content_type="application/json"
            )

    # method for update task(edit task's title or finish tasks)
    @staticmethod
    def put(request):
        if request.method == 'PUT':

            # if task's title exist change it
            job_title = QueryDict(request.body).get('job_title')
            if job_title:

                # edit task title
                job = TodoList.objects.get(id=QueryDict(request.body).get('job_edit_pk'))
                job.title = job_title
                job.save()

                # create dictionary for response
                response_data = {}
                response_data['msg'] = 'Job finished success.'
                response_data['isdone'] = job.is_finished
                response_data['title'] = job.title
                response_data['id'] = job.id

                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )

            # # if task title does not exist make this task finished/unfinished
            else:

                id = QueryDict(request.body).get('job_done_pk')
                job = TodoList.objects.get(id=id)

                # if task is finished change in to unfinished
                if job.is_finished:

                    all = DoneJobs.objects.all()

                    for a in all:
                        all_done = a

                    all_done.is_done -= 1
                    all_done.save()
                    all_finished_jobs = all_done.is_done
                    job.is_finished = False

                # else if task is unfinished change it to finished
                else:
                    all = DoneJobs.objects.all()

                    for a in all:
                        all_done = a
                    all_done.is_done += 1
                    all_done.save()
                    all_finished_jobs = all_done.is_done
                    job.is_finished = True


                job.save()

                # create dictionary for response
                response_data = {}
                response_data['msg'] = 'Job finished success.'
                response_data['active'] = len(TodoList.objects.filter(is_finished=False))
                response_data['done'] = len(TodoList.objects.filter(is_finished=True))
                response_data['isdone'] = job.is_finished
                response_data['allFinishedJobs'] = all_finished_jobs
                response_data['title'] = job.title

                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )
        else:
            return HttpResponse(
                json.dumps({"error": "error"}),
                content_type="application/json"
            )

