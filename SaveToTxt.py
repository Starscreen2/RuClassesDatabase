import sys
import subprocess
import os
import requests  # We will assume requests is already installed after previous fixes
import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
import csv

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests  

campus_mapping = {
    "Cook/Douglass": "Cook/Douglass",
    "College Avenue": "College Avenue",
    "LIVINGSTON": "Livingston",
    "Busch": "Busch"
}

day_mapping = {
    "M": "Monday",
    "T": "Tuesday",
    "W": "Wednesday",
    "H": "Thursday",  # H is probably Thursday
    "F": "Friday",
    "S": "Saturday",
    "Su": "Sunday"
}

def fetch_course_data():
    url = "https://classes.rutgers.edu//soc/api/courses.json?year=2024&term=9&campus=NB"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def updated_parse_class_details(data):
    class_details = []
    for course in data:
        course_title = course.get("title", "Unknown Title")
        for section in course.get("sections", []):
            instructor_name = section.get("instructorsText", "Unknown Instructor")
            for meeting in section.get("meetingTimes", []):
                day = day_mapping.get(meeting.get("meetingDay", ""), "")
                start_time = convert_time(meeting.get("startTimeMilitary", ""))
                end_time = convert_time(meeting.get("endTimeMilitary", ""))
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

def updated_save_to_csv(class_data):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, "classes.csv")

    with open(file_path, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Instructor", "Day", "Time", "Campus", "Building & Room"])

        for entry in class_data:
            writer.writerow([entry['title'], entry['instructor'], entry['day'], entry['time'], entry['campus'], entry['building_and_room']])

    print(f"Data successfully saved to {file_path}")

def convert_time(time_str):
    if not time_str:
        return ""
    hour = int(time_str[:2])
    minute = int(time_str[2:])
    am_pm = "am" if hour < 12 else "pm"
    hour = hour % 12
    hour = 12 if hour == 0 else hour
    return f"{hour}:{minute:02d}{am_pm}"

# def convert_time_military(time_str):
#     parts = time_str.split(' - ')
#     new_parts = []
#
#     for part in parts:
#         hour = int(part[:2])
#         minute = int(part[2:])
#         am_pm = "am" if hour < 12 else "pm"
#         hour = hour % 12
#         hour = 12 if hour == 0 else hour
#         new_parts.append(f"{hour}:{minute:02d}{am_pm}")
#
#     return " - ".join(new_parts)

def update_times_in_file():
    with open('data.txt', 'r') as file:
        lines = file.readlines()

    with open('data.txt', 'w') as file:
        for line in lines:
            if "Title:::Instructor" in line:
                file.write(line)
                continue

            parts = line.strip().split(':::')
            if len(parts) == 6:
                parts[3] = convert_time(parts[3])
                updated_line = ':::'.join(parts)
                file.write(updated_line + '\n')
            else:
                file.write(line)


if __name__ == "__main__":
    course_data = fetch_course_data()
    print("Fetched course data:", course_data)

    class_data = updated_parse_class_details(course_data)
    print("Parsed class data:", class_data)

    print("Calling updated_save_to_csv...")
    updated_save_to_csv(class_data) 

    update_times_in_file()
