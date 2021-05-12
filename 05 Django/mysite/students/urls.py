from django.urls import path

from . import views

app_name = 'students'
urlpatterns = [
    # # Use template/HttpResponse
    # path('', views.index, name='index')

    # Use generic view
    # ex: /students/
    path('', views.IndexView.as_view(), name='index'),

    # ex: /students/1/
    path('<int:pk>/', views.StudentView.as_view(), name='student'),

    # ex: /students/1/school
    path('<int:pk>/school', views.SchoolView.as_view(), name='school'),

    # ex: /students/1/certificate
    path('<int:pk>/certificate', views.CertificateView.as_view(), name='certificate'),

    # ex: /students/1/department
    path('<int:pk>/department', views.DepartmentView.as_view(), name='department'),

    # ex: /students/1/faculty
    path('<int:pk>/faculty', views.FacultyView.as_view(), name='faculty'),

    # ex: /students/1/grade
    path('<int:pk>/grade', views.GradeView.as_view(), name='grade'),
    ]
