import tkinter as tk
from tkinter import ttk
from datetime import datetime
import re

# Class periods definition
class_periods = [
    ["8:30am – 9:50am", "8:45am – 9:40am", "8:30am – 11:30am"],
    ["10:20am – 11:40am", "10:35am – 11:30am", "10:20am – 1:20pm"],
    ["12:10pm – 1:30pm", "12:25pm – 1:20pm", "12:10pm – 3:10pm"],
    ["2:00pm – 3:20pm", "2:15pm – 3:10pm", "2:00pm – 5:00pm"],
    ["3:50pm – 5:10pm", "4:05pm – 5:00pm", "3:50pm – 6:50pm"],
    ["5:40pm – 7:00pm", "5:55pm – 6:50pm", "5:40pm – 8:40pm"],
    ["7:30pm – 8:50pm", "7:45pm – 8:40pm", "6:00pm – 9:00pm"],
    ["9:20pm – 10:40pm", "9:35pm – 10:30pm", "7:30pm – 10:30pm"]
]

# Parsing class details from the text file
def parse_class_details(lines):
    class_details = []
    pattern = r"\| (?P<day>\w+day)\s+\| (?P<start_time>\d+:\d+ [APM]{2}) - (?P<end_time>\d+:\d+ [APM]{2})\s+\| (?P<campus>\w+)\s+\| (?P<building_and_room>[^|]+)\s+\|"
    for line in lines:
        match = re.match(pattern, line)
        if match:
            details = match.groupdict()
            class_details.append(details)
    return class_details

with open("extracted_class_details.txt", "r") as file:
    extracted_class_details = file.readlines()

class_data = parse_class_details(extracted_class_details)

# function to group by campus and sort alphabetically
def search_unoccupied_classes():
    selected_day = day_var.get()
    selected_period = period_var.get()
    
    # Extract start and end times from the selected period
    start_time_str, end_time_str = selected_period.split(" – ")
    start_time = datetime.strptime(start_time_str, "%I:%M%p")
    end_time = datetime.strptime(end_time_str, "%I:%M%p")
    
    all_rooms = {f"{detail['campus']} - {detail['building_and_room'].strip()}" for detail in class_data}
    occupied_rooms = set()
    
    for detail in class_data:
        if detail["day"] == selected_day:
            class_start_time = datetime.strptime(detail["start_time"], "%I:%M %p")
            class_end_time = datetime.strptime(detail["end_time"], "%I:%M %p")
            
            # Check if there's an overlap between the selected period and the class timings
            if (start_time <= class_start_time <= end_time) or (start_time <= class_end_time <= end_time):
                occupied_rooms.add(f"{detail['campus']} - {detail['building_and_room'].strip()}")
    
    unoccupied_rooms = all_rooms - occupied_rooms

    # Group and sort the rooms
    def sort_key(room_str):
        campus, room = room_str.split(" - ")
        return (campus, room)

    occupied_rooms_sorted = sorted(list(occupied_rooms), key=sort_key)
    unoccupied_rooms_sorted = sorted(list(unoccupied_rooms), key=sort_key)

    occupied_text.delete(1.0, tk.END)
    unoccupied_text.delete(1.0, tk.END)

    if occupied_rooms_sorted:
        occupied_text.insert(tk.END, "\n".join(occupied_rooms_sorted))
    else:
        occupied_text.insert(tk.END, "No rooms are occupied during the specified period.")
    
    if unoccupied_rooms_sorted:
        unoccupied_text.insert(tk.END, "\n".join(unoccupied_rooms_sorted))
    else:
        unoccupied_text.insert(tk.END, "All classes are occupied during the specified period.")


# UI setup for side by side view
root = tk.Tk()
root.title("Class Search")
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
day_var = tk.StringVar()
day_dropdown = ttk.Combobox(frame, textvariable=day_var, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], state="readonly")
day_dropdown.set("Monday")
day_dropdown.grid(row=0, column=1, sticky=tk.W, pady=5)
day_label = ttk.Label(frame, text="Select Day:")
day_label.grid(row=0, column=0, sticky=tk.W, pady=5)
period_var = tk.StringVar()
period_dropdown_values = [period for sublist in class_periods for period in sublist]
period_dropdown = ttk.Combobox(frame, textvariable=period_var, values=period_dropdown_values, state="readonly", width=25)
period_dropdown.set(period_dropdown_values[0])
period_dropdown.grid(row=1, column=1, sticky=tk.W, pady=5)
period_label = ttk.Label(frame, text="Select Period:")
period_label.grid(row=1, column=0, sticky=tk.W, pady=5)
search_button = ttk.Button(frame, text="Search", command=search_unoccupied_classes)
search_button.grid(row=2, column=0, columnspan=2, pady=10)
occupied_label = ttk.Label(frame, text="OCCUPIED Rooms:")
occupied_label.grid(row=3, column=0, pady=5)
unoccupied_label = ttk.Label(frame, text="UNOCCUPIED Rooms:")
unoccupied_label.grid(row=3, column=1, pady=5)
occupied_text = tk.Text(frame, wrap=tk.WORD, width=30, height=15)
occupied_text.grid(row=4, column=0, pady=5)
unoccupied_text = tk.Text(frame, wrap=tk.WORD, width=30, height=15)
unoccupied_text.grid(row=4, column=1, pady=5)
root.mainloop()
