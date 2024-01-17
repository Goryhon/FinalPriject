import sqlite3
import data
# Создание подключения к базе данных
conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
cursor = conn.cursor()

# Создание таблицы admin
cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin(
        master_full_name VARCHAR(90),
        phone_num VARCHAR(11)
    );
''')

# Создание таблицы employees
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employees_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employees_full_name VARCHAR(90),
        phone_number VARCHAR(11),
        age INTEGER
    );
''')

# Создание таблицы timetable_date
cursor.execute('''
    CREATE TABLE IF NOT EXISTS timetable_date (
        employees_id INTEGER,
        start_date DATE,
        start_time TIME,
        end_date DATE,
        end_time TIME,
        worked_hours REAL,
        FOREIGN KEY (employees_id) REFERENCES employees(employees_id) ON DELETE CASCADE
    );
''')

# Создание таблицы salary
cursor.execute('''
    CREATE TABLE IF NOT EXISTS salary(
        employees_id INTEGER,
        work_count INTEGER,
        hour_cost INTEGER,
        full_salary REAL,
        FOREIGN KEY (employees_id) REFERENCES employees(employees_id) ON DELETE CASCADE
    );
''')

# Создание таблицы bonuses_and_penalties
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bonuses_and_penalties(
        employees_id INTEGER,
        status BOOLEAN,
        summ INTEGER,
        FOREIGN KEY (employees_id) REFERENCES employees(employees_id) ON DELETE CASCADE
    );
''')

# Создание триггера для автоматического вычисления full_salary
cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS calculate_full_salary
    AFTER UPDATE OF work_count, hour_cost ON salary
    FOR EACH ROW
    BEGIN
        UPDATE salary
        SET full_salary = NEW.work_count * NEW.hour_cost
        WHERE employees_id = NEW.employees_id;
    END;
''')

# Создание триггера для автоматического обновления work_count в salary
cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS update_work_count
    AFTER INSERT ON timetable_date
    FOR EACH ROW
    BEGIN
        UPDATE salary
        SET work_count = work_count + NEW.worked_hours
        WHERE employees_id = NEW.employees_id;
    END;
''')

# Создание триггера для автоматического вычисления worked_hours
#cursor.execute('''
#    CREATE TRIGGER IF NOT EXISTS calculate_worked_hours
#    BEFORE INSERT ON timetable_date
#    FOR EACH ROW
#    BEGIN
#        -- Вычисление разницы в часах между start_date + start_time и end_date + end_time
#        NEW.worked_hours = (julianday(NEW.end_date || ' ' || NEW.end_time) - julianday(NEW.start_date || ' ' || NEW.start_time)) * 24;
#    END;
#''')

# Удаление существующих данных из таблиц перед вставкой
cursor.execute('DELETE FROM employees')
cursor.execute('DELETE FROM timetable_date')
cursor.execute('DELETE FROM salary')
cursor.execute('DELETE FROM bonuses_and_penalties')

# Вставка данных в таблицу employees
cursor.executemany('INSERT INTO employees (employees_id, employees_full_name, phone_number, age) VALUES (?, ?, ?, ?)', data.employees_data)

# Вставка данных в таблицу timetable_date
cursor.executemany('INSERT INTO timetable_date (employees_id, start_date, start_time, end_date, end_time, worked_hours) VALUES (?, ?, ?, ?, ?, ?)', data.timetable_data)

# Вставка данных в таблицу salary
cursor.executemany('INSERT INTO salary (employees_id, work_count, hour_cost, full_salary) VALUES (?, ?, ?, ?)', data.salary_data)

# Вставка данных в таблицу bonuses_and_penalties
cursor.executemany('INSERT INTO bonuses_and_penalties (employees_id, status, summ) VALUES (?, ?, ?)', data.bonuses_data)


cursor.execute('SELECT * FROM salary')
print(cursor.fetchall())

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
