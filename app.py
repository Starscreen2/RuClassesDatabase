from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def read_data_file():
    data = []
    with open('data.txt', 'r') as file:
        next(file)  # Skip the header line
        for line in file:
            parts = line.strip().split(':::')  # Splitting using ':::' as delimiter
            if len(parts) == 6:
                data.append({
                    'title': parts[0].strip(),
                    'instructor': parts[1].strip(),
                    'day': parts[2].strip(),
                    'time': parts[3].strip(),
                    'campus': parts[4].strip(),
                    'building_room': parts[5].strip()
                })
    return data

@app.route('/search', methods=['POST'])
def search():
    # Get form data, no need to convert to lower here, will be done in comparison
    title = request.form.get('title', '')
    instructor = request.form.get('instructor', '')
    day = request.form.get('day', '')
    time = request.form.get('time', '')
    campus = request.form.get('campus', '')
    building_room = request.form.get('building_room', '')

    # Read the data from file
    all_data = read_data_file()

    # Filter the data based on the form input, case insensitive
    filtered_data = [d for d in all_data if
                     (title.lower() in d['title'].lower() or not title) and
                     (instructor.lower() in d['instructor'].lower() or not instructor) and
                     (day.lower() == d['day'].lower() or not day) and
                     (time.lower() == d['time'].lower() or not time) and
                     (campus.lower() == d['campus'].lower() or not campus) and
                     (building_room.lower() in d['building_room'].lower() or not building_room)] #replaced == with in


    # Debug print to check what is being sent to the template
    print("Filtered data:", filtered_data)

    # Render the results template with the filtered data
    return render_template('results.html', data=filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
