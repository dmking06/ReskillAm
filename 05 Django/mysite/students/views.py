from django.views import generic

from .models import Student, School, Department, Grade, Faculty, Certificate


class IndexView(generic.ListView):
    template_name = 'students/index.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        return Student.objects.order_by('id')


class StudentView(generic.DetailView):
    model = Student
    template_name = 'students/student.html'


class SchoolView(generic.DetailView):
    model = School
    template_name = 'students/school.html'


class DepartmentView(generic.DetailView):
    model = Department
    template_name = 'students/department.html'


class GradeView(generic.DetailView):
    model = Grade
    template_name = 'students/grade.html'


class CertificateView(generic.DetailView):
    model = Certificate
    template_name = 'students/certificate.html'


class FacultyView(generic.DetailView):
    model = Faculty
    template_name = 'students/faculty.html'
