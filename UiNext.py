import requests

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
def parse_class_details(data):
    class_details = []
    for course in data:
        for section in course["sections"]:
            for meeting in section["meetingTimes"]:
                class_detail = {
                    "day": day_mapping.get(meeting["meetingDay"], meeting["meetingDay"]),
                    "time": f"{meeting['startTimeMilitary']} - {meeting['endTimeMilitary']}",
                    "campus": campus_mapping.get(meeting["campusName"].lower(), meeting["campusName"]),
                    "building_and_room": f"{meeting['buildingCode']}-{meeting['roomNumber']}",
                    "title": course["title"]
                }
                class_details.append(class_detail)
    return class_details

# Save to testt.txt in the new Chart Format
def save_to_file(class_data):
    with open("testt.txt", "w") as file:
        header = "| Day                            | Time                           | Campus                         | Building & Room                |"
        separator = "|--------------------------------|--------------------------------|--------------------------------|--------------------------------|"
        file.write(header + "\n" + separator + "\n")
        for entry in class_data:
            line = f"| {entry['day']:<30} | {entry['time']:<30} | {entry['campus']:<30} | {entry['building_and_room']:<30} |"
            file.write(line + "\n")

# Main Execution
if __name__ == "__main__":
    course_data = fetch_course_data()
    class_data = parse_class_details(course_data)
    save_to_file(class_data)
