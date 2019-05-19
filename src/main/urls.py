from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, AssignmentViewSet, TaskViewSet, ResultCreateAPIView, \
    ApproveCourseParticipant, AssignmentsList, SubmissionListView, GradeSubmissionView, CreateSubmissionView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='Course')
router.register(r'assignments', AssignmentViewSet, basename='Assignment')
router.register(r'tasks', TaskViewSet, basename='Task')

urlpatterns = [
                  path('submission_result/', ResultCreateAPIView.as_view()),
                  path('approve_participant/', ApproveCourseParticipant.as_view(), name='approve-participant'),
                  path('submissions/', SubmissionListView.as_view(), name='retrieve-submissions'),
                  path('grade_submission/<int:pk>', GradeSubmissionView.as_view(), name='grade-submission'),
                  path('submissions/', CreateSubmissionView.as_view(), name='submit'),
                  path('my_assignments/', AssignmentsList.as_view(), name='my-submissions'),
              ] + router.urls
