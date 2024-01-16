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
    # url = "https://sis.rutgers.edu/soc/api/courses.json?year=2023&term=1&campus=NB"
    url = "https://sis.rutgers.edu/soc/api/courses.json?year=2024&term=1&campus=NB"
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


#convert from 24 hour format to 12 hour format
def convert_time(time_str):
    parts = time_str.split(' - ')
    new_parts = []

    for part in parts:
        # Adjusting to handle time format without colon
        hour = int(part[:2])
        minute = int(part[2:])
        am_pm = "am" if hour < 12 else "pm"
        hour = hour % 12
        hour = 12 if hour == 0 else hour
        new_parts.append(f"{hour}:{minute:02d}{am_pm}")

    return " - ".join(new_parts)

#convert from 24 hour format to 12 hour format
def update_times_in_file():
    with open('data.txt', 'r') as file:
        lines = file.readlines()

    with open('data.txt', 'w') as file:
        for line in lines:
            if "Title:::Instructor" in line:
                file.write(line)  # Write the header line as-is
                continue

            parts = line.strip().split(':::')
            if len(parts) == 6:
                parts[3] = convert_time(parts[3])  # Convert the time
                updated_line = ':::'.join(parts)
                file.write(updated_line + '\n')
            else:
                file.write(line)  # Write non-standard lines as-is


# this is where the website searches for data
def save_to_file(class_data):
    with open("data.txt", "w") as file:
        # Writing the header
        file.write("Title:::Instructor:::Day:::Time:::Campus:::Building & Room\n")

        # Writing each entry
        for entry in class_data:
            line = f"{entry['title']}:::{entry['instructor']}:::{entry['day']}:::{entry['time']}:::{entry['campus']}:::{entry['building_and_room']}\n"
            file.write(line)


# Main Execution
if __name__ == "__main__":
    course_data = fetch_course_data()
    print("Fetched course data:", course_data)  # Diagnostic print

    class_data = updated_parse_class_details(course_data)
    print("Parsed class data:", class_data)  # Diagnostic print

    print("Calling updated_save_to_file...")  # Diagnostic print
    updated_save_to_file(class_data)

    print("Calling save_to_file...")  # Diagnostic print
    save_to_file(class_data)
    
    #convert from 24 hour format to 12 hour format
    update_times_in_file()



