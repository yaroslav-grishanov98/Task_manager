from django.contrib import admin
from .models import Task, Project, Comment


admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Comment)
