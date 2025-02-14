import json
import csv
import requests  # <-- new import

# Replace file-based JSON loading with API fetch
response = requests.get("https://classes.rutgers.edu/soc/api/courses.json?year=2024&term=9&campus=NB")
courses = response.json()

# Sort courses by a key (here we use "courseString", but you can change it)
sorted_courses = sorted(courses, key=lambda c: c.get("courseString", ""))

# Open a CSV file for writing
with open("courses_export.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    
    # Updated header row with new "Time" column inserted before "Meeting Times"
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
        "Time",             # <-- new column
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
            # Build the core requirements column:
            (", ".join([
                f"{core.get('coreCode', '')}: {core.get('coreCodeDescription', '')}"
                for core in course.get("coreCodes", [])
            ]) if course.get("coreCodes") else "None")
        ]
        
        # For each section in the course, write a row
        for section in course.get("sections", []):
            # Compute extra "Time" column using the first meeting time (if exists)
            if section.get("meetingTimes"):
                first_meeting = section.get("meetingTimes")[0]
                extra_time = f"{first_meeting.get('startTimeMilitary', 'N/A')}-{first_meeting.get('endTimeMilitary', 'N/A')}"
            else:
                extra_time = ""
            
            section_info = [
                section.get("number", ""),
                ", ".join([instr.get("name", "") for instr in section.get("instructors", [])]),
                section.get("openStatusText", ""),
                section.get("commentsText", ""),
                extra_time,   # <-- extra column inserted here
                # Format meeting times (concatenate all meeting times in the section)
                "; ".join([
                    f"{meeting.get('meetingDay', '')}: {meeting.get('startTimeMilitary', 'N/A')}-{meeting.get('endTimeMilitary', 'N/A')} at {meeting.get('buildingCode', 'N/A')} {meeting.get('roomNumber', 'N/A')} ({meeting.get('meetingModeDesc', 'N/A')})"
                    for meeting in section.get("meetingTimes", [])
                ])
            ]
            # Write a complete row: course info + section info
            writer.writerow(base_info + section_info)
