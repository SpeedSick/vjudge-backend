from django.contrib import admin

from main.models import Task, Assignment, Course, Result, Submission, CourseParticipant, News

admin.site.register(Task)
admin.site.register(Assignment)
admin.site.register(Course)
admin.site.register(Result)
admin.site.register(Submission)
admin.site.register(CourseParticipant)
admin.site.register(News)
