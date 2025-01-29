from django.contrib import admin
from .models import Venue, VenueSet, Course, CourseSet, Department, ExamTimeTablePlan

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')
    search_fields = ('name',)
    list_filter = ('capacity',)

@admin.register(VenueSet)
class VenueSetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('venues',)  # To make it easier to manage the ManyToMany field

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'department', 'num_students', 'units', 'level')
    search_fields = ('title', 'code')
    list_filter = ('num_students', 'department', 'level', 'code')

@admin.register(CourseSet)
class CourseSetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('courses',)  # To make it easier to manage the ManyToMany field

# @admin.register(Exam)
# class ExamAdmin(admin.ModelAdmin):
#     list_display = ('course', 'date', 'time', 'venue')
#     search_fields = ('course__title', 'venue__name')
#     list_filter = ('date', 'venue', 'course')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department',)


@admin.register(ExamTimeTablePlan)
class ExamTimeTablePlanAdmin(admin.ModelAdmin):
    list_display = ('title',)