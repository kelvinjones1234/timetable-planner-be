from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re
import ast
from io import BytesIO
from django.core.files.base import ContentFile
from g4f.client import Client
import pandas as pd
from anthropic import Anthropic

from rest_framework import generics

from .models import (
    Venue,
    VenueSet,
    Course,
    CourseSet,
    Department,
    ExamTimeTablePlan,
)
from .serializers import (
    VenueSerializer,
    VenueSetSerializer,
    CourseSetSerializer,
    CourseSerializer,
    DepartmentSerializer,
    PlanDataSerializer,
    ExamTimeTablePlanSerializer,
)


class VenueListCreateView(generics.ListCreateAPIView):
    # permission_classes = IsAuthenticated
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class VenueSetListView(generics.ListAPIView):
    queryset = VenueSet.objects.all()
    serializer_class = VenueSetSerializer


class CourseListCreateView(generics.ListCreateAPIView):
    # permission_classes = IsAuthenticated
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseSetListView(generics.ListAPIView):
    queryset = CourseSet.objects.all()
    serializer_class = CourseSetSerializer


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


def create_excel_file(data_dict_string):
    # Convert the string representation of the dictionary to an actual dictionary
    data_dict = ast.literal_eval(data_dict_string.split("=", 1)[1].strip())

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data_dict)

    # Create an in-memory Excel file
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine="openpyxl")
    excel_buffer.seek(0)

    return excel_buffer


class ProcessTimeTable(APIView):
    def post(self, request):
        serializer = PlanDataSerializer(data=request.data)
        if serializer.is_valid():
            # Extract data
            venue_details = serializer.validated_data["venueDetails"]
            course_details = serializer.validated_data["courseDetails"]
            start_date = serializer.validated_data["startDate"]
            end_date = serializer.validated_data["endDate"]
            title = serializer.validated_data["title"]
            venue_set = serializer.validated_data["venue_set_name"]
            course_set = serializer.validated_data["course_set_name"]
            const = serializer.validated_data["constraints"]


            print(course_details)
            ANTHROPIC_API_KEY = "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"

            # Example client call (ensure you have correct client setup)
            client = Anthropic(
                api_key=ANTHROPIC_API_KEY
            )  # Replace with your actual API key
            try:
                print("Sending request to anthrope client...")
                response = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=1000,
                    messages=[
                        {
                            "role": "user",
                            "content": f"""You are an experienced academic scheduler tasked with creating efficient examination timetables for 
                    tertiary institutions. Your goal is to create an optimized exam time table while considering various constraints 
                    and requirements ensuring all courses are scheduled. Provide only the dataframe with no explanation.
                    I have the following data for scheduling exams:
                    Course Details:
                    {course_details}
                    Venue Details:
                    {venue_details}
                    The exam period is from {start_date} to {end_date}. Schedule the exams considering the following constraints:
                    1. Distribute courses evenly across the entire examination period ensuring that courses scheduled twice for the same department.
                    2. Allocate venues making sure the number of students doesnt exceed venue capacity.
                    3. If course units is <= 2 allocate 2 hours 30 minutes else allocate 3 hours
                    4. {const}
                    Please provide the output in a pandas DataFrame format. Use this format:
                    data = {{
                    "DATE": "3/05/24",
                    "DAY": "FRIDAY", 
                    "TIME": "9:00 - 12:00",
                    "NDI OTM": "COM211 (allocated venue)",
                    "NDII OTM": "SWD311 (allocated venue)", 
                    "HNDI OTM": "NCC312 (allocated venue)",
                    "HNDII OTM": "MAC3118 (allocated venue)",
                    "NDI MAC": "COM211 (allocated venue)",
                    "NDII MAC": "SWD311 (allocated venue)", 
                    "HNDI MAC": "NCC312 (allocated venue)",
                    "HNDII MAC": "MAC3118 (allocated venue)",
                    "NDI CS": "COM211 (allocated venue)",
                    "NDII CS": "SWD311 (allocated venue)", 
                    "HNDI CS": "NCC312 (allocated venue)",
                    "HNDII CS": "MAC3118 (allocated venue)",
    
                    }}
                    """,
                        }
                    ],
                )
                print("Received response from anthrope client.")
                timetable = response.content[0].text
                pattern = r"data\s*=\s*\{[\s\S]*?\}"
                match = re.search(pattern, timetable)

                if not match:
                    return Response(
                        {"error": "Data dictionary not found in the response"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                data_dict_string = match.group(0)
                print("This is the constraints: " + const)
                excel_buffer = create_excel_file(data_dict_string)
                exam_plan = ExamTimeTablePlan(
                    title=title,
                    venue_set_name=venue_set,
                    course_set_name=course_set,
                    constraints=const,
                )
                exam_plan.excel_file.save(
                    "exam_timetable.xlsx", ContentFile(excel_buffer.getvalue())
                )
                exam_plan.save()

                # Optionally, you can return the data dictionary as a response
                return Response(
                    {"data_dict": data_dict_string}, status=status.HTTP_200_OK
                )

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return Response(
                    {"error": "An error occurred while processing the request"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamTimeTablePlanListView(generics.ListAPIView):
    queryset = ExamTimeTablePlan.objects.all()
    serializer_class = ExamTimeTablePlanSerializer



# above has been proven to work well
# below is still under review




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re
import ast
from io import BytesIO
from django.core.files.base import ContentFile
from g4f.client import Client
import pandas as pd
from anthropic import Anthropic

from rest_framework import generics

from .models import (
    Venue,
    VenueSet,
    Course,
    CourseSet,
    Department,
    ExamTimeTablePlan,
)
from .serializers import (
    VenueSerializer,
    VenueSetSerializer,
    CourseSetSerializer,
    CourseSerializer,
    DepartmentSerializer,
    PlanDataSerializer,
    ExamTimeTablePlanSerializer,
)


class VenueListCreateView(generics.ListCreateAPIView):
    # permission_classes = IsAuthenticated
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class VenueSetListView(generics.ListAPIView):
    queryset = VenueSet.objects.all()
    serializer_class = VenueSetSerializer


class CourseListCreateView(generics.ListCreateAPIView):
    # permission_classes = IsAuthenticated
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseSetListView(generics.ListAPIView):
    queryset = CourseSet.objects.all()
    serializer_class = CourseSetSerializer


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


def create_excel_file(data_dict_string):
    # Convert the string representation of the dictionary to an actual dictionary
    data_dict = ast.literal_eval(data_dict_string.split("=", 1)[1].strip())

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data_dict)

    # Create an in-memory Excel file
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine="openpyxl")
    excel_buffer.seek(0)

    return excel_buffer


class ProcessTimeTable(APIView):
    def post(self, request):
        serializer = PlanDataSerializer(data=request.data)
        if serializer.is_valid():
            # Extract data
            venue_details = serializer.validated_data["venueDetails"]
            course_details = serializer.validated_data["courseDetails"]
            start_date = serializer.validated_data["startDate"]
            end_date = serializer.validated_data["endDate"]
            title = serializer.validated_data["title"]
            venue_set = serializer.validated_data["venue_set_name"]
            course_set = serializer.validated_data["course_set_name"]
            const = serializer.validated_data["constraints"]


            print(course_details)
            ANTHROPIC_API_KEY = "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"

            # Example client call (ensure you have correct client setup)
            client = Anthropic(
                api_key=ANTHROPIC_API_KEY
            )  # Replace with your actual API key
            try:
                print("Sending request to anthrope client...")
                response = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=1000,
                    messages=[
                        {
                            "role": "user",
                            "content": f"""You are tasked with professionally planning an exam timetable for a tertiary institution. 
                            This is a complex task that requires careful consideration of multiple factors to ensure a fair and 
                            efficient schedule for all students and courses. Follow these instructions to create the exam timetable:
                            Course Details:
                            1. First, you will receive the following input information:
                                <courses>
                                {course_set}
                                </courses>
                                This contains a list of code as course code, department_name, level, num_students as number of students, title, units as course units.
                            {start_date} - {end_date} {const}
                            This specifies the start and end dates of the exam period, as well as other constraints.
                                <venues>
                                {venue_set}
                                </venues>
                            This lists the available exam venues and their seating capacities.
                            2. Analyze the course information:
                                a. Sort courses by the number of enrolled students, from highest to lowest.
                                b. Identify courses with the largest enrollments, as these may need special consideration.

                            3. Consider student schedules:
                                a. Create a matrix of course conflicts, showing which courses have overlapping student enrollments.
                                b. Prioritize scheduling exams for courses with fewer conflicts earlier in the exam period.

                            4. Allocate exam slots:
                                a. Start with the courses having the highest enrollment and fewest conflicts.
                                b. Assign exam slots, ensuring at least one day between exams for courses with significant overlap in student enrollment.
                                c. Try to schedule more difficult or time-consuming exams earlier in the day and earlier in the exam period.

                            5. Assign venues:
                                a. Match courses to appropriate venues based on enrollment numbers and venue capacities.
                                b. For large courses, consider splitting the exam across multiple venues if necessary.

                            6. Avoid conflicts:
                                a. Ensure no student has more than one exam scheduled at the same time.
                                b. Try to avoid scheduling more than two exams per day for any student.
                                c. Allow sufficient time between exams on the same day for students to move between venues.
                                d. If course units is <= 2 allocate 2 hours 30 minutes else allocate 3 hours

                            7. Balance the schedule:
                                a. Distribute exams evenly across the exam period to avoid clustering.
                                b. Ensure fair distribution of morning, afternoon, and (if applicable) evening exam slots.

                            8. Create the exam timetable output in the following format:
                                data = {{
                                            "DATE": "3/05/24",
                                            "DAY": "FRIDAY", 
                                            "TIME": "9:00 - 12:00",
                                            "NDI OTM": "COM211 (allocated venue)",
                                            "NDII OTM": "SWD311 (allocated venue)", 
                                            "HNDI OTM": "NCC312 (allocated venue)",
                                            "HNDII OTM": "MAC3118 (allocated venue)",
                                            "NDI MAC": "COM211 (allocated venue)",
                                            "NDII MAC": "SWD311 (allocated venue)", 
                                            "HNDI MAC": "NCC312 (allocated venue)",
                                            "HNDII MAC": "MAC3118 (allocated venue)",
                                            "NDI CS": "COM211 (allocated venue)",
                                            "NDII CS": "SWD311 (allocated venue)", 
                                            "HNDI CS": "NCC312 (allocated venue)",
                                            "HNDII CS": "MAC3118 (allocated venue)",
                            
                                        }}

                            9. After creating the initial timetable, perform the following checks and optimizations:
                                a. Verify that no student has conflicting exams.
                                b. Ensure that no venue is overbooked.
                                c. Check for any unassigned courses and fit them into the schedule.
                                d. Look for opportunities to improve the schedule by swapping exam times or venues to reduce student stress or improve resource utilization.
                            
                            """,
                        }
                    ],
                )
                print("Received response from anthrope client.")
                timetable = response.content[0].text
                pattern = r"data\s*=\s*\{[\s\S]*?\}"
                match = re.search(pattern, timetable)

                if not match:
                    return Response(
                        {"error": "Data dictionary not found in the response"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                data_dict_string = match.group(0)
                print("This is the constraints: " + const)
                excel_buffer = create_excel_file(data_dict_string)
                exam_plan = ExamTimeTablePlan(
                    title=title,
                    venue_set_name=venue_set,
                    course_set_name=course_set,
                    constraints=const,
                )
                exam_plan.excel_file.save(
                    "exam_timetable.xlsx", ContentFile(excel_buffer.getvalue())
                )
                exam_plan.save()

                # Optionally, you can return the data dictionary as a response
                return Response(
                    {"data_dict": data_dict_string}, status=status.HTTP_200_OK
                )

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return Response(
                    {"error": "An error occurred while processing the request"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamTimeTablePlanListView(generics.ListAPIView):
    queryset = ExamTimeTablePlan.objects.all()
    serializer_class = ExamTimeTablePlanSerializer
