from flask import Flask, render_template, request, redirect, url_for, jsonify
from config_db.base_model import init_db, Schedule, db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedule.db'

init_db(app)


@app.route('/')
def index():
    schedule = Schedule.query.all()
    return render_template('index.html', schedule=schedule)


@app.route('/make_appointment', methods=['POST'])
def make_appointment():
    if request.method == 'POST':
        date = request.form['date']
        hour = int(request.form['hour'])
        user_id = request.form['user_id']
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phonenumber = request.form['phonenumber']
        last_haircut = request.form['last_haircut']

        new_appointment = Schedule(date=date, hour=hour, user_id=user_id, username=username,
                                   first_name=first_name, last_name=last_name,
                                   phonenumber=phonenumber, last_haircut=last_haircut)

        db.session.add(new_appointment)
        db.session.commit()

        return redirect(url_for('index'))


@app.route('/get_all_schedule', methods=['GET'])
def get_schedule_for_date():
    try:
        selected_date = request.args.get('date')

        if not selected_date:
            return jsonify({'error': 'Date parameter is missing'}), 400

        all_schedule_data = Schedule.query.filter_by(date=selected_date).all()
        schedule_list = []

        for schedule_data in all_schedule_data:
            schedule_dict = {
                'hour': schedule_data.hour,
                'is_available': schedule_data.is_available,
                'username': schedule_data.username,
            }
            schedule_list.append(schedule_dict)

        return jsonify(schedule_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update_schedule', methods=['POST'])
def update_schedule():
    try:
        updated_data = request.json.get('updatedData')

        updated_schedule = []

        for entry in updated_data:
            hour = entry['hour']
            username = entry['username']
            is_available = entry['is_available']

            schedule_entry = Schedule.query.filter_by(hour=hour).first()

            if schedule_entry:
                schedule_entry.username = username
                schedule_entry.is_available = not bool(username)  # Set is_available to not bool(username)
            else:
                new_schedule_entry = Schedule(hour=hour, username=username, is_available=not bool(username))
                db.session.add(new_schedule_entry)
                updated_schedule.append({
                    'hour': new_schedule_entry.hour,
                    'username': new_schedule_entry.username,
                    'is_available': new_schedule_entry.is_available
                })

        db.session.commit()

        return jsonify({'message': 'Schedule updated successfully', 'updatedSchedule': updated_schedule})
    except Exception as e:
        print(e)  # Выводим ошибку в консоль для отладки
        return jsonify({'error': 'Failed to update schedule: ' + str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='1337')
