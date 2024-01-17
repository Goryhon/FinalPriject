import datetime
import re

from fastapi.responses import JSONResponse
from Authorization.authorization import KeycloakJWTBearerHandler, HTTPException
import sqlite3
from fastapi import APIRouter, Depends
import json
from Models.models import employeer_model, timetable_model,salary_model,bonuses_model
admin_router = APIRouter(
    tags=["Administrator"]
)
#employees
@admin_router.post("/employees")
def post_employees(employeer_info:employeer_model,role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})
    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT employees_id FROM employees WHERE
        employees_id = {employeer_info.employees_id};
    ''')
    data = cursor.fetchall()
    print(data)
    if len(data)!=0:
        return JSONResponse(status_code=404, content={"message": "Работник с таким id уже существует"})
    if employeer_info.employees_full_name == "":
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    if employeer_info.age <18:
        return JSONResponse(status_code=404, content={"message": "Работник не достиг 18 лет"})
    if not is_valid_custom_phone_number(employeer_info.phone_number):
        return JSONResponse(status_code=404, content={"message": "Номер не соответствует формату 7**********"})
    cursor.execute(f'INSERT INTO employees (employees_id, employees_full_name, phone_number, age) VALUES ({employeer_info.employees_id},"{employeer_info.employees_full_name}","{employeer_info.phone_number}",{employeer_info.age})')
    conn.commit()
    conn.close()
    return("Пользователь усепшно добавлен")

@admin_router.get("/employees")
def get_employees(role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})
    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM employees;
    ''')
    result = json.loads(json.dumps(cursor.fetchall()))
    conn.close()
    return result

@admin_router.put("/employees")
def put_employee(employeer_info:employeer_model, role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})

    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()

    # Проверка существования работника с указанным ID
    cursor.execute(f'SELECT employees_id FROM employees WHERE employees_id = {employeer_info.employees_id};')
    data = cursor.fetchall()
    if len(data) == 0:
        return JSONResponse(status_code=404, content={"message": "Работник с таким ID не найден"})

    # Проверки на обновление данных
    if employeer_info.employees_full_name == "":
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    if employeer_info.age < 18:
        return JSONResponse(status_code=404, content={"message": "Работник не достиг 18 лет"})
    if not is_valid_custom_phone_number(employeer_info.phone_number):
        return JSONResponse(status_code=404, content={"message": "Номер не соответствует формату 7**********"})

    # Обновление данных о работнике
    cursor.execute(f'''
        UPDATE employees
        SET employees_full_name = "{employeer_info.employees_full_name}",
            phone_number = "{employeer_info.phone_number}",
            age = {employeer_info.age}
        WHERE employees_id = {employeer_info.employees_id};
    ''')
    conn.commit()
    conn.close()
    return {"message": f"Данные работника с ID {employeer_info.employees_id} успешно обновлены"}

@admin_router.delete("/employees")
def delete_employee(employeer_info:employeer_model,role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})

    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()

    # Проверка существования работника с указанным ID
    cursor.execute(f'SELECT employees_id FROM employees WHERE employees_id = {employeer_info.employees_id};')
    data = cursor.fetchall()
    if len(data) == 0:
        return JSONResponse(status_code=404, content={"message": "Работник с таким ID не найден"})

    # Удаление данных о работнике
    cursor.execute(f'DELETE FROM employees WHERE employees_id = {employeer_info.employees_id};')
    conn.commit()
    conn.close()
    return {"message": f"Данные работника с ID {employeer_info.employees_id} успешно удалены"}


#timetable_date
@admin_router.get("/timetable_date")
def get_timetable_date(role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})
    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM timetable_date;
    ''')
    result = json.loads(json.dumps(cursor.fetchall()))
    conn.close()
    return result

@admin_router.post("/timetable_date")
def post_timetable_date(timetable_info:timetable_model,role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})
    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT employees_id FROM timetable_date WHERE employees_id = {timetable_info.employees_id} INTERSECT SELECT start_date FROM timetable_date WHERE start_date = {timetable_info.start_date};')
    data = cursor.fetchall()
    if len(data) == 0:
        return JSONResponse(status_code=404, content={"message": "Работник с таким ID не найден/У данного сотрудника есть смена в этот день"})

    if timetable_info.employees_id == 0:
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    if timetable_info.start_date == "":
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    try:
        datetime.date.fromisoformat(timetable_info.start_date.isoformat())
    except ValueError:
        return JSONResponse(status_code=404, content={"Формат даты должен соответствовать ГГГГ-ММ-ДД"})
    try:
        # Преобразование строки времени в объект datetime.time
        timetable_info.start_time = datetime.time.fromisoformat(str(timetable_info.start_time))
    except ValueError:
        return JSONResponse(status_code=404, content={"Формат времени должен соответствовать ЧЧ:ММ"})
    try:
        datetime.date.fromisoformat(timetable_info.end_date.isoformat())
    except ValueError:
        return JSONResponse(status_code=404, content={"Формат даты должен соответствовать ГГГГ-ММ-ДД"})
    try:
        # Преобразование строки времени в объект datetime.time
        timetable_info.end_time = datetime.time.fromisoformat(str(timetable_info.end_time))
    except ValueError:
        return JSONResponse(status_code=404, content={"Формат времени должен соответствовать ЧЧ:ММ"})
    if timetable_info.worked_hours == 0:
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    cursor.execute(f'INSERT INTO timetable_date (employees_id, start_date, start_time, end_date, end_time, worked_hours) VALUES ({timetable_info.employees_id},"{timetable_info.start_date}","{timetable_info.start_time}","{timetable_info.end_date}","{timetable_info.end_time}",{timetable_info.worked_hours})')
    conn.commit()
    conn.close()
    return("Пользователь усепшно добавлен")

@admin_router.put("/timetable_date")
def put_timetable_date(timetable_info:timetable_model, role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})

    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()

    # Проверка существования работника с указанным ID
    cursor.execute(f'SELECT employees_id FROM timetable_date WHERE employees_id = {timetable_info.employees_id};')
    data = cursor.fetchall()
    if len(data) == 0:
        return JSONResponse(status_code=404, content={"message": "Работник с таким ID не найден"})

    # Проверки на обновление данных
    try:
        datetime.date.fromisoformat(timetable_info.start_date.isoformat())
    except ValueError:
        return JSONResponse(status_code=404, content={"Формат даты должен соответствовать ГГГГ-ММ-ДД"})
    try:
        # Преобразование строки времени в объект datetime.time
        timetable_info.start_time = datetime.time.fromisoformat(str(timetable_info.start_time))
    except ValueError:
        return JSONResponse(status_code=404, content={"Формат времени должен соответствовать ЧЧ:ММ"})
    try:
        datetime.date.fromisoformat(timetable_info.end_date.isoformat())
    except ValueError:
        return JSONResponse(status_code=404, content={"Формат даты должен соответствовать ГГГГ-ММ-ДД"})
    try:
        # Преобразование строки времени в объект datetime.time
        timetable_info.end_time = datetime.time.fromisoformat(str(timetable_info.end_time))
    except ValueError:
        return JSONResponse(status_code=404, content={"Формат времени должен соответствовать ЧЧ:ММ"})
    if timetable_info.worked_hours == 0:
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    # Обновление данных о работнике
    cursor.execute(f'''
        UPDATE employees
        SET start_date = "{timetable_info.start_date}",
            start_time = "{timetable_info.start_time}",
            end_date = "{timetable_info.end_date}",
            end_time = "{timetable_info.end_time}",
            worked_hours = {timetable_info.worked_hours}
        WHERE employees_id = {timetable_info.employees_id};
    ''')
    conn.commit()
    conn.close()
    return {"message": f"Данные работника с ID {timetable_info.employees_id} успешно обновлены"}

@admin_router.delete("/timetable_date")
def delete_timetable_date(timetable_info:timetable_model,role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})

    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()

    # Проверка существования работника с указанным ID
    cursor.execute(f'SELECT employees_id FROM timetable_date WHERE employees_id = {timetable_info.employees_id};')
    data = cursor.fetchall()
    if len(data) == 0:
        return JSONResponse(status_code=404, content={"message": "Работник с таким ID не найден"})

    # Удаление данных о работнике
    cursor.execute(f'DELETE FROM timetable_date WHERE employees_id = {timetable_info.employees_id};')
    conn.commit()
    conn.close()
    return {"message": f"Данные работника с ID {timetable_info.employees_id} успешно удалены"}


#salary
@admin_router.get("/salary")
def get_salary(role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})
    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM salary;
    ''')
    result = json.loads(json.dumps(cursor.fetchall()))
    conn.close()
    return result

@admin_router.post("/salary")
def post_salary(salary_info:salary_model,role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})
    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT employees_id FROM salary WHERE
        employees_id = {salary_info.employees_id};
    ''')
    data = cursor.fetchall()
    print(data)
    if len(data)!=0:
        return JSONResponse(status_code=404, content={"message": "Работник с таким id уже существует"})
    if salary_info.work_count == 0:
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    if salary_info.hour_cost == 0:
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    if salary_info.full_salary == 0:
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    cursor.execute(f'INSERT INTO salary (employees_id, work_count, hour_cost, full_salary) VALUES ({salary_info.employees_id},"{salary_info.work_count}","{salary_info.hour_cost}",{salary_info.full_salary})')
    conn.commit()
    conn.close()
    return("Запись усепшно добавлена")

@admin_router.put("/salary")
def put_salary(salary_info:salary_model, role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})

    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()

    # Проверка существования работника с указанным ID
    cursor.execute(f'SELECT employees_id FROM salary WHERE employees_id = {salary_info.employees_id};')
    data = cursor.fetchall()
    if len(data) == 0:
        return JSONResponse(status_code=404, content={"message": "Работник с таким ID не найден"})

    # Проверки на обновление данных
    if salary_info.work_count == 0:
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    if salary_info.hour_cost == 0:
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    if salary_info.full_salary == 0:
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})

    # Обновление данных о работнике
    cursor.execute(f'''
        UPDATE salary
        SET work_count = "{salary_info.work_count}",
            hour_cost = "{salary_info.hour_cost}",
            full_salary = {salary_info.full_salary}
        WHERE employees_id = {salary_info.employees_id};
    ''')
    conn.commit()
    conn.close()
    return {"message": f"Данные работника с ID {salary_info.employees_id} успешно обновлены"}

@admin_router.delete("/salary")
def delete_salary(salary_info:salary_model,role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})

    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()

    # Проверка существования работника с указанным ID
    cursor.execute(f'SELECT employees_id FROM salary WHERE employees_id = {salary_info.employees_id};')
    data = cursor.fetchall()
    if len(data) == 0:
        return JSONResponse(status_code=404, content={"message": "Работник с таким ID не найден"})

    # Удаление данных о работнике
    cursor.execute(f'DELETE FROM salary WHERE employees_id = {salary_info.employees_id};')
    conn.commit()
    conn.close()
    return {"message": f"Данные работника с ID {salary_info.employees_id} успешно удалены"}



#bonuses_and_penalties
@admin_router.get("/bonuses_and_penalties")
def get_bonuses_and_penalties(role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})
    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM bonuses_and_penalties;
    ''')
    result = json.loads(json.dumps(cursor.fetchall()))
    conn.close()
    return result

@admin_router.post("/bonuses_and_penalties")
def post_bonuses_and_penalties(bonuses_info:bonuses_model,role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})
    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT employees_id FROM bonuses_and_penalties WHERE
        employees_id = {bonuses_info.employees_id};
    ''')
    data = cursor.fetchall()
    print(data)
    if len(data)!=0:
        return JSONResponse(status_code=404, content={"message": "Работник с таким id уже существует"})
    if bonuses_info.status is None:
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    if bonuses_info.summ == 0:
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    cursor.execute(f'INSERT INTO bonuses_and_penalties (employees_id, status, summ) VALUES ({bonuses_info.employees_id},"{bonuses_info.status}","{bonuses_info.summ}")')
    conn.commit()
    conn.close()
    return("Запись усепшно добавлена")

@admin_router.put("/bonuses_and_penalties")
def put_bonuses_and_penalties(bonuses_info:bonuses_model, role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})

    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()

    # Проверка существования работника с указанным ID
    cursor.execute(f'SELECT employees_id FROM bonuses_and_penalties WHERE employees_id = {bonuses_info.employees_id};')
    data = cursor.fetchall()
    if len(data) == 0:
        return JSONResponse(status_code=404, content={"message": "Работник с таким ID не найден"})

    # Проверки на обновление данных
    if bonuses_info.status is None:
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})
    if bonuses_info.summ == 0:
        return JSONResponse(status_code=404, content={"message": "Пустое поле"})

    # Обновление данных о работнике
    cursor.execute(f'''
        UPDATE bonuses_and_penalties
        SET status = "{bonuses_info.status}",
            summ = "{bonuses_info.summ}"
        WHERE employees_id = {bonuses_info.employees_id};
    ''')
    conn.commit()
    conn.close()
    return {"message": f"Данные работника с ID {bonuses_info.employees_id} успешно обновлены"}

@admin_router.delete("/bonuses_and_penalties")
def delete_bonuses_and_penalties(bonuses_info:bonuses_model,role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})

    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()

    # Проверка существования работника с указанным ID
    cursor.execute(f'SELECT employees_id FROM bonuses_and_penalties WHERE employees_id = {bonuses_info.employees_id};')
    data = cursor.fetchall()
    if len(data) == 0:
        return JSONResponse(status_code=404, content={"message": "Работник с таким ID не найден"})

    # Удаление данных о работнике
    cursor.execute(f'DELETE FROM bonuses_and_penalties WHERE employees_id = {bonuses_info.employees_id};')
    conn.commit()
    conn.close()
    return {"message": f"Данные работника с ID {bonuses_info.employees_id} успешно удалены"}


def is_valid_custom_phone_number(phone_number):
    # Паттерн для номера телефона в формате 7**********
    pattern = re.compile(r'^7\d{10}$')

    # Проверка соответствия номера паттерну
    match = pattern.match(phone_number)

    return bool(match)

def verify_admin(role) -> bool:
    if role == "admin":
        return True
    else:
        return False
