import os
import re

def extract_class_details(filename):
    with open(filename, 'r') as file:
        content = file.read()
        
    #search
    pattern = r'(?P<day>\w+day)</span><span[^>]*>(?P<time>[\d:]+ [APM]{2} - [\d:]+ [APM]{2})</span><span[^>]*>(?P<campus>\w+)</span><span[^>]*><a[^>]*>(?P<building_and_room>[^<]+)</a>'
    matches = re.findall(pattern, content)
    
    return matches

def save_to_file(details, output_filename):
    with open(output_filename, 'w') as file:
        #Chart
        file.write("| Day                            | Time                           | Campus                         | Building & Room                |\n")
        file.write("|--------------------------------|--------------------------------|--------------------------------|--------------------------------|\n")
        
        for detail in details:
            file.write("| {:30} | {:30} | {:30} | {:30} |\n".format(detail[0], detail[1], detail[2], detail[3]))

#put the path to the txt file below called "FullArtsAndSciences.txt"
if os.path.exists("###FullArtsAndSciences.txt"):
    class_details = extract_class_details("FullArtsAndSciences.txt")#<<< same here, put the location where you want the files extracted
    save_to_file(class_details, "extracted_class_details.txt")
    print("saved! extracted_class_details.txt")
else:
    print("'FullArtsAndSciences.txt' is not found in the specified directory")

# class periods
#schedule = [
# 1   ["8:30am – 9:50am", "8:45am – 9:40am", "8:30am – 11:30am"],
# 2   ["10:20am – 11:40am", "10:35am – 11:30am", "10:20am – 1:20pm"],
# 3   ["12:10pm – 1:30pm", "12:25pm – 1:20pm", "12:10pm – 3:10pm"],
# 4   ["2:00pm – 3:20pm", "2:15pm – 3:10pm", "2:00pm – 5:00pm"],
# 5   ["3:50pm – 5:10pm", "4:05pm – 5:00pm", "3:50pm – 6:50pm"],
# 6   ["5:40pm – 7:00pm", "5:55pm – 6:50pm", "5:40pm – 8:40pm"],
# 6   ["7:30pm – 8:50pm", "7:45pm – 8:40pm", "6:00pm – 9:00pm"],
# 7   ["9:20pm – 10:40pm", "9:35pm – 10:30pm", "7:30pm – 10:30pm"]
#]
