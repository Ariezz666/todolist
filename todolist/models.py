from django.db import models
from django.contrib import admin


#create the class which will be description your to-do list
class TodoList(models.Model):

    #title the job
    title = models.CharField(max_length=200)

    #is the job finished?
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class DoneJobs(models.Model):

	#counts how many jobs is done
	is_done = models.IntegerField(default=0)


admin.site.register(TodoList)
admin.site.register(DoneJobs)
