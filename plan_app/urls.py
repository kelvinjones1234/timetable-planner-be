from django.urls import path
from .views import VenueListCreateView, ExamTimeTablePlanListView, VenueSetListView, CourseSetListView, CourseListCreateView, DepartmentListView
from .views import ProcessTimeTable
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('venue-sets/', VenueSetListView.as_view(), name='venue-set-list'),
    path('course-sets/', CourseSetListView.as_view(), name='course-set-list'),
    path('venues/', VenueListCreateView.as_view(), name='venue-list-create'),
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('departments/', DepartmentListView.as_view(), name='department-list-create'),
    path('process-time-table/', ProcessTimeTable.as_view(), name='process_time_table'),
    path('exam-time-table/', ExamTimeTablePlanListView.as_view(), name='exam_timetable_plan'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)