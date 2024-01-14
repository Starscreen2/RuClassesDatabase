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
            parts = line.strip().split(':')
            if len(parts) == 6:
                data.append({
                    'title': parts[0],
                    'instructor': parts[1],
                    'day': parts[2],
                    'time': parts[3],
                    'campus': parts[4],
                    'building_room': parts[5]
                })
    return data

@app.route('/search', methods=['POST'])
def search():
    # Retrieve form data
    title = request.form.get('title', '').lower()
    instructor = request.form.get('instructor', '').lower()
    day = request.form.get('day', '').lower()
    time = request.form.get('time', '').lower()
    campus = request.form.get('campus', '').lower()
    building_room = request.form.get('building_room', '').lower()

    all_data = read_data_file()
    filtered_data = [d for d in all_data if
                     (title in d['title'].lower() or not title) and
                     (instructor in d['instructor'].lower() or not instructor) and
                     (day in d['day'].lower() or not day) and
                     (time in d['time'].lower() or not time) and
                     (campus in d['campus'].lower() or not campus) and
                     (building_room in d['building_room'].lower() or not building_room)]

    return render_template('results.html', data=filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
