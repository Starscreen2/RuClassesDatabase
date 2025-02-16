import json
import csv
import requests
from datetime import datetime  # <-- Import for time conversion

# Function to convert military time to AM/PM format
def convert_to_am_pm(military_time):
    if not military_time or military_time == "N/A":  # Handle missing values
        return "N/A"
    try:
        return datetime.strptime(military_time, "%H%M").strftime("%I:%M %p")
    except ValueError:
        return "N/A"  # Handle incorrect time format gracefully

# Fetch course data from Rutgers API
response = requests.get("https://classes.rutgers.edu/soc/api/courses.json?year=2024&term=9&campus=NB")
courses = response.json()

# Sort courses by "courseString"
sorted_courses = sorted(courses, key=lambda c: c.get("courseString", ""))

# Define day mapping
day_mapping = {
    "M": "Monday",
    "T": "Tuesday",
    "W": "Wednesday",
    "H": "Thursday",  # H is Thursday
    "F": "Friday",
    "S": "Saturday",
    "Su": "Sunday"
}

# Open CSV file for writing
with open("courses_export.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    
    # Updated header row with military & AM/PM time
    writer.writerow([
        "Course Code",
        "Title",
        "Subject",
        "Course Number",
        "Credits",
        "School",
        "Campus Locations",
        "Prerequisites",
        "Core Requirements",
        "Section #",
        "Instructors",
        "Status",
        "Comments",
        "Military Time",  # Original military time
        "AM/PM Time",      # Converted AM/PM format
        "Weekdays",
        "Meeting Times"
    ])
    
    # Process each course in sorted order
    for course in sorted_courses:
        base_info = [
            course.get("courseString", ""),
            course.get("title", ""),
            f"{course.get('subject', '')} - {course.get('subjectDescription', '')}",
            course.get("courseNumber", ""),
            f"{course.get('credits', '')} ({course.get('creditsObject', {}).get('description', '')})",
            course.get("school", {}).get("description", ""),
            "; ".join([loc.get("description", "") for loc in course.get("campusLocations", [])]),
            course.get("preReqNotes", ""),
            (", ".join([
                f"{core.get('coreCode', '')}: {core.get('coreCodeDescription', '')}"
                for core in course.get("coreCodes", [])
            ]) if course.get("coreCodes") else "None")
        ]
        
        # For each section in the course, write a row
        for section in course.get("sections", []):
            if section.get("meetingTimes"):
                first_meeting = section.get("meetingTimes")[0]
                
                start_time_military = first_meeting.get("startTimeMilitary", "N/A")
                end_time_military = first_meeting.get("endTimeMilitary", "N/A")
                
                start_time_am_pm = convert_to_am_pm(start_time_military)
                end_time_am_pm = convert_to_am_pm(end_time_military)
                
                extra_time_military = f"{start_time_military}-{end_time_military}"
                extra_time_am_pm = f"{start_time_am_pm}-{end_time_am_pm}"
                
                weekdays = day_mapping.get(first_meeting.get('meetingDay', ''), 'N/A')
            else:
                extra_time_military = "N/A"
                extra_time_am_pm = "N/A"
                weekdays = "N/A"
            
            section_info = [
                section.get("number", ""),
                ", ".join([instr.get("name", "") for instr in section.get("instructors", [])]),
                section.get("openStatusText", ""),
                section.get("commentsText", ""),
                extra_time_military,  # Military time
                extra_time_am_pm,      # AM/PM time
                weekdays,              # Weekday
                "; ".join([
                    f"{meeting.get('meetingDay', '')}: {meeting.get('startTimeMilitary', 'N/A')} ({convert_to_am_pm(meeting.get('startTimeMilitary', 'N/A'))}) - "
                    f"{meeting.get('endTimeMilitary', 'N/A')} ({convert_to_am_pm(meeting.get('endTimeMilitary', 'N/A'))}) "
                    f"at {meeting.get('buildingCode', 'N/A')} {meeting.get('roomNumber', 'N/A')} ({meeting.get('meetingModeDesc', 'N/A')})"
                    for meeting in section.get("meetingTimes", [])
                ])
            ]
            
            # Write a complete row: course info + section info
            writer.writerow(base_info + section_info)

print("Export complete! CSV saved as 'courses_export.csv'.")
