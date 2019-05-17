from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, AssignmentViewSet, TaskViewSet, ResultCreateAPIView, \
    ApproveCourseParticipant, AssignmentsList

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='Course')
router.register(r'assignments', AssignmentViewSet, basename='Assignment')
router.register(r'tasks', TaskViewSet, basename='Task')

urlpatterns = [
                  path('submission_result/', ResultCreateAPIView.as_view()),
                  path('approve_participant/', ApproveCourseParticipant.as_view()),
                  path('my_assignments/', AssignmentsList.as_view()),
              ] + router.urls
