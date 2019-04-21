from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, AssignmentViewSet, TaskViewSet, CourseParticipantViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='Course')
router.register(r'assignments', AssignmentViewSet, basename='Assignment')
router.register(r'tasks', TaskViewSet, basename='Task')
router.register(r'course_participants', CourseParticipantViewSet, basename='CourseParticipant')

urlpatterns = [

              ] + router.urls
