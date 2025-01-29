# from django.test import TestCase

# # Create your tests here.

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import re
# import ast
# from io import BytesIO
# from django.core.files.base import ContentFile
# from g4f.client import Client
# import pandas as pd
# from rest_framework import generics

# from .models import (
#     Venue,
#     VenueSet,
#     Course,
#     CourseSet,
#     Department,
#     ExamTimeTablePlan,
# )
# from .serializers import (
#     VenueSerializer,
#     VenueSetSerializer,
#     CourseSetSerializer,
#     CourseSerializer,
#     DepartmentSerializer,
#     PlanDataSerializer,
#     ExamTimeTablePlanSerializer,
# )


# class VenueListCreateView(generics.ListCreateAPIView):
#     # permission_classes = IsAuthenticated
#     queryset = Venue.objects.all()
#     serializer_class = VenueSerializer


# class VenueSetListView(generics.ListAPIView):
#     queryset = VenueSet.objects.all()
#     serializer_class = VenueSetSerializer


# class CourseListCreateView(generics.ListCreateAPIView):
#     # permission_classes = IsAuthenticated
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer


# class CourseSetListView(generics.ListAPIView):
#     queryset = CourseSet.objects.all()
#     serializer_class = CourseSetSerializer


# class DepartmentListView(generics.ListAPIView):
#     queryset = Department.objects.all()
#     serializer_class = DepartmentSerializer


# def create_excel_file(data_dict_string):
#     # Convert the string representation of the dictionary to an actual dictionary
#     data_dict = ast.literal_eval(data_dict_string.split("=", 1)[1].strip())

#     # Create a DataFrame from the dictionary
#     df = pd.DataFrame(data_dict)

#     # Create an in-memory Excel file
#     excel_buffer = BytesIO()
#     df.to_excel(excel_buffer, index=False, engine="openpyxl")
#     excel_buffer.seek(0)

#     return excel_buffer


# class ProcessVenueDetails(APIView):
#     def post(self, request):
#         serializer = PlanDataSerializer(data=request.data)
#         if serializer.is_valid():
#             # Extract data
#             venue_details = serializer.validated_data["venueDetails"]
#             course_details = serializer.validated_data["courseDetails"]
#             start_date = serializer.validated_data["startDate"]
#             end_date = serializer.validated_data["endDate"]
#             title = serializer.validated_data["title"]
#             venue_set = serializer.validated_data["venue_set_name"]
#             course_set = serializer.validated_data["course_set_name"]
#             const = serializer.validated_data["constraints"]

#             print(course_details)

#             # Example client call (ensure you have correct client setup)
#             client = Client()
#             try:
#                 print("Sending request to g4f client...")
#                 response = client.chat.completions.create(
#                     model="gpt-4o",
#                     messages=[
#                         {
#                             "role": "system",
#                             "content": (
#                                 "You are an experienced academic scheduler tasked with creating efficient examination timetables for "
#                                 "tertiary institutions. Your goal is to optimize the schedule while considering various constraints "
#                                 "and requirements."
#                             ),
#                         },
#                         {
#                             "role": "user",
#                             "content": (
#                                 "I have the following data for scheduling exams:\n\n"
#                                 f"Course Details:\n{course_details}\n\n"
#                                 f"Venue Details:\n{venue_details}\n\n"
#                                 f"The exam period is {start_date} to {end_date}. Please schedule the exams considering the following constraints:\n"
#                                 "1. Distribute courses evenly across the entire examination period ensuring that no course appears more than once.\n"
#                                 "2. Allocate venues based on course enrollment, ensuring venue capacity is not exceeded.\n"
#                                 "3. Avoid scheduling exams for the same department or year group simultaneously when possible.\n\n"
#                                 "Duration guide.\n\n"
#                                 "2 units courses: 2 hours and 30 minutes "
#                                 "3 units courses: 3 hours"
#                                 "4 units courses: 3 hours"
#                                 f"4.{const}\n\n"
#                                 "Please provide the output in a pandas DataFrame format. Use this format:\n"
#                                 "data = {\n"
#                                 '    "Date": ["date", "date", "date", "date"],\n'
#                                 '    "Start Time": ["start time", "start time", "start time", ""],\n'
#                                 '    "End Time": ["end time", "end time", "end time", ""],\n'
#                                 '    "Course Code": ["code", "code", "code", ""],\n'
#                                 '    "Venue": ["venue", "venue", "venue", ""]\n'
#                                 "}"
#                             ),
#                         },
#                     ],
#                 )
#                 print("Received response from g4f client.")

#                 if response and response.choices:
#                     # Extract the timetable from the model's response
#                     timetable = response.choices[0].message.content

#                     # Regular expression to capture the 'data' dictionary
#                     pattern = r"data\s*=\s*\{[\s\S]*?\}"
#                     match = re.search(pattern, timetable)

#                     if match:
#                         # Extracted 'data' dictionary
#                         data_dict_string = match.group(0)
#                         print("Captured Data Dictionary:")

#                         print(data_dict_string)
#                         excel_buffer = create_excel_file(data_dict_string)

#                         # Save to model

#                         exam_plan = ExamTimeTablePlan(
#                             title=title,
#                             venue_set_name=venue_set,
#                             course_set_name=course_set,
#                             constraints=const,
#                         )

#                         exam_plan.excel_file.save(
#                             "exam_timetable.xlsx", ContentFile(excel_buffer.getvalue())
#                         )
#                         exam_plan.save()

#                         # Optionally, you can return the data dictionary as a response
#                         return Response(
#                             {"data_dict": data_dict_string}, status=status.HTTP_200_OK
#                         )
#                     else:
#                         print("Data dictionary not found.")
#                         return Response(
#                             {"error": "Data dictionary not found in the response"},
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                         )
#                 else:
#                     print("No response content received from the model.")
#                     return Response(
#                         {"error": "No timetable generated by the model"},
#                         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                     )
#             except Exception as e:
#                 print(f"An error occurred: {str(e)}")
#                 return Response(
#                     {"error": "An error occurred while processing the request"},
#                     status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ExamTimeTablePlanListView(generics.ListAPIView):
#     queryset = ExamTimeTablePlan.objects.all()
#     serializer_class = ExamTimeTablePlanSerializer
