import sqlite3
from datetime import datetime, timedelta

# Устанавливаем соединение с базой данных
conn = sqlite3.connect('instance/schedule.db')
cursor = conn.cursor()

# Создаем таблицу, если она еще не существует, с указанием значений по умолчанию для строковых полей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY,
        date TEXT,
        hour TEXT,
        is_available BOOLEAN,
        user_id INTEGER DEFAULT 0,
        username TEXT DEFAULT '',
        first_name TEXT DEFAULT '',
        last_name TEXT DEFAULT '',
        phonenumber TEXT DEFAULT '',
        last_haircut TEXT DEFAULT ''
    )
''')

# Генерируем и добавляем записи в базу данных
start_date = datetime.strptime('2023-12-19', '%Y-%m-%d').date()
end_date = datetime(2030, 1, 1).date()

current_date = start_date
insert_count = 0  # Добавим переменную для отслеживания количества вставок

while current_date <= end_date:
    for hour in range(10, 22):
        schedule_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=hour)
        try:
            cursor.execute('''
                INSERT INTO schedule (date, hour, is_available, user_id, username, first_name, last_name, phonenumber, last_haircut)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (current_date.strftime('%Y-%m-%d'), schedule_time.strftime('%H:%M'), 1, 0, '', '', '', '', ''))  # Заполнение пустыми значениями
            insert_count += 1  # Увеличим счетчик вставок
        except Exception as e:
            print(f"Ошибка при вставке данных: {e}")

    current_date += timedelta(days=1)

# Выведем информацию о количестве вставок
print(f"Количество вставок: {insert_count}")

# Фиксируем изменения и закрываем соединение с базой данных
try:
    conn.commit()
    print("Изменения успешно зафиксированы в базе данных")
except Exception as e:
    print(f"Ошибка при фиксации изменений: {e}")

conn.close()