import requests
import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox



# Define the Campus Mapping
campus_mapping = {
    "Cook/Douglass": "Cook/Douglass",
    "College Avenue": "College Avenue",
    "LIVINGSTON": "Livingston",
    "Busch": "Busch"
}

# Mapping for day abbreviations to full words
day_mapping = {
    "M": "Monday",
    "T": "Tuesday",
    "W": "Wednesday",
    "H": "Thursday",  # H is probably Thursday
    "F": "Friday",
    "S": "Saturday",
    "Su": "Sunday"
}

# Fetch Course Data from the API
def fetch_course_data():
    url = "https://sis.rutgers.edu/soc/api/courses.json?year=2023&term=1&campus=NB"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

# Parse the Data
def updated_parse_class_details(data):
    class_details = []
    for course in data:
        course_title = course.get("title", "Unknown Title")
        for section in course.get("sections", []):
            instructor_name = section.get("instructorsText", "Unknown Instructor")
            for meeting in section.get("meetingTimes", []):
                day = day_mapping.get(meeting.get("meetingDay", ""), "")
                start_time = meeting.get("startTimeMilitary", "")
                end_time = meeting.get("endTimeMilitary", "")
                campus = campus_mapping.get(meeting.get("campusName", "").lower(), meeting.get("campusName", ""))
                building_room = f"{meeting.get('buildingCode', '')}-{meeting.get('roomNumber', '')}"
                if not day or not start_time or not end_time:
                    continue
                class_detail = {
                    "title": course_title,
                    "instructor": instructor_name,
                    "day": day,
                    "time": f"{start_time} - {end_time}",
                    "campus": campus,
                    "building_and_room": building_room
                }
                class_details.append(class_detail)
    sorted_class_details = sorted(class_details, key=lambda x: x['title'])
    return sorted_class_details

def updated_save_to_file(class_data):
    with open("testt.txt", "w") as file:
        header = "| Title                         | Instructor                    | Day                            | Time                           | Campus                         | Building & Room                 |"
        separator = "|-------------------------------|-------------------------------|--------------------------------|--------------------------------|--------------------------------|---------------------------------|"
        file.write(header + "\n" + separator + "\n")
        for entry in class_data:
            line = f"| {entry['title']:<29} | {entry['instructor']:<29} | {entry['day']:<30} | {entry['time']:<30} | {entry['campus']:<30} | {entry['building_and_room']:<30} |"
            file.write(line + "\n")


# Main Execution
if __name__ == "__main__":
    course_data = fetch_course_data()
    class_data = updated_parse_class_details(course_data)
    updated_save_to_file(class_data)
