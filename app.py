from flask import Flask, request, render_template
import csv
import os

app = Flask(__name__)

# Function to get the path of the CSV file in the same folder as the script
def get_csv_file_path():
    script_directory = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    return os.path.join(script_directory, 'classes.csv')  # Join the directory with 'classes.csv'

# Function to read data from the CSV file
def read_data_file():
    data = []
    csv_file_path = get_csv_file_path()  # Get the full path to 'classes.csv'
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)  # Using DictReader to map CSV headers to dictionary keys
        for row in reader:
            data.append({
                'title': row['Title'].strip(),
                'instructor': row['Instructor'].strip(),
                'day': row['Day'].strip(),
                'time': row['Time'].strip(),
                'campus': row['Campus'].strip(),
                'building_room': row['Building & Room'].strip()
            })
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get form data from the search form
    title = request.form.get('title', '')
    instructor = request.form.get('instructor', '')
    day = request.form.get('day', '')
    time = request.form.get('time', '')
    campus = request.form.get('campus', '')
    building_room = request.form.get('building_room', '')

    # Read the data from the CSV file
    all_data = read_data_file()

    # Filter the data based on the form input, case insensitive
    filtered_data = [d for d in all_data if
                     (title.lower() in d['title'].lower() or not title) and
                     (instructor.lower() in d['instructor'].lower() or not instructor) and
                     (day.lower() == d['day'].lower() or not day) and
                     (time.lower() == d['time'].lower() or not time) and
                     (campus.lower() == d['campus'].lower() or not campus) and
                     (building_room.lower() in d['building_room'].lower() or not building_room)]

    # Debug print to check what is being sent to the template
    print("Filtered data:", filtered_data)

    # Render the results template with the filtered data
    return render_template('results.html', data=filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
