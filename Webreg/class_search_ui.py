import tkinter as tk
from tkinter import ttk
from datetime import datetime
import re

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

def search_classes():
    selected_day = day_var.get()
    input_time_str = time_var.get()
    input_time = datetime.strptime(input_time_str, "%I:%M %p")
    results = []
    for detail in class_data:
        if detail["day"] == selected_day:
            start_time = datetime.strptime(detail["start_time"], "%I:%M %p")
            end_time = datetime.strptime(detail["end_time"], "%I:%M %p")
            if start_time <= input_time <= end_time:
                results.append(f"{detail['start_time']} - {detail['end_time']} at {detail['campus']} in {detail['building_and_room'].strip()}")
    result_text.delete(1.0, tk.END)
    if results:
        result_text.insert(tk.END, "\n".join(results))
    else:
        result_text.insert(tk.END, "No classes found at the specified time.")

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
time_var = tk.StringVar()
time_entry = ttk.Entry(frame, textvariable=time_var)
time_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
time_entry.insert(0, "10:20 AM")
time_label = ttk.Label(frame, text="Enter Time (e.g. 10:20 AM):")
time_label.grid(row=1, column=0, sticky=tk.W, pady=5)
search_button = ttk.Button(frame, text="Search", command=search_classes)
search_button.grid(row=2, column=0, columnspan=2, pady=10)
result_text = tk.Text(frame, wrap=tk.WORD, width=50, height=10)
result_text.grid(row=3, column=0, columnspan=2, pady=5)
root.mainloop()
