from django.contrib import admin

from main.models import Task, Assignment, Course, Result, Submission, CourseParticipant

admin.site.register(Task)
admin.site.register(Assignment)
admin.site.register(Course)
admin.site.register(Result)
admin.site.register(Submission)
admin.site.register(CourseParticipant)


