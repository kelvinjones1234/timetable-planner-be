from django.db import models


class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.department


class Venue(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class VenueSet(models.Model):
    name = models.CharField(max_length=100)
    venues = models.ManyToManyField(Venue)

    def __str__(self):
        return self.name


class Course(models.Model):

    CHOICE_SET = (
    ('HNDI', 'HNDI'),
    ('HNDII', 'HNDII'),
    ('NDI', 'NDI'),
    ('NDII', 'NDII'),
)

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    num_students = models.IntegerField()
    level = models.CharField(max_length=5, choices=CHOICE_SET)
    units = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return self.title


class CourseSet(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name


class ExamTimeTablePlan(models.Model):
    title = models.CharField(max_length=500, default="exam time table tester")
    excel_file = models.FileField(upload_to="exam_files/", blank=True, null=True)
    course_set_name = models.CharField(max_length=200)
    venue_set_name = models.CharField(max_length=200)
    constraints = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
