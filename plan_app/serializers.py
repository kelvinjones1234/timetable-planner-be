from rest_framework import serializers
from .models import Venue, VenueSet, Course, CourseSet, Department, ExamTimeTablePlan


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"


class VenueSetSerializer(serializers.ModelSerializer):
    venues = VenueSerializer(many=True, read_only=True)

    class Meta:
        model = VenueSet
        fields = ["id", "name", "venues"]


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "code", "num_students", "department", "units", "department_name", "level"]

    def get_department_name(self, obj):
        return obj.department.department


class CourseSetSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSet
        fields = ["name", "courses"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class PlanDataSerializer(serializers.Serializer):
    title = serializers.CharField()
    course_set_name = serializers.CharField()
    venue_set_name = serializers.CharField()
    constraints = serializers.CharField(allow_blank=True)
    venueDetails = serializers.CharField()
    courseDetails = serializers.CharField()
    startDate = serializers.CharField()
    endDate = serializers.CharField()

class ExamTimeTablePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamTimeTablePlan
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'excel_file' in representation and representation['excel_file']:
            # Modify the URL to include `/api/`
            representation['excel_file'] = representation['excel_file'].replace('/media/', '/api/media/')
        return representation
