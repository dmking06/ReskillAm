from django.db import models


class School(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name


class Certificate(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Grade(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Faculty(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Student(models.Model):
    fullname = models.CharField(max_length=200)
    grad_year = models.PositiveSmallIntegerField()
    school = models.ForeignKey(School, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    certificate = models.ForeignKey(Certificate, on_delete=models.PROTECT)

    class Meta:
        ordering = ["fullname"]

    def __str__(self):
        return self.fullname
