from fastapi.responses import JSONResponse
from Authorization.authorization import KeycloakJWTBearerHandler, HTTPException
import sqlite3
from fastapi import APIRouter, Depends
import json
from Models.models import employeer_model
worker_router = APIRouter(
    tags=["Employeer"]
)

@worker_router.get("/employees_w")
def get_employees(role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_worker(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})
    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM employees;
    ''')
    result = json.loads(json.dumps(cursor.fetchall()))
    conn.close()
    return result

@worker_router.get("/timetable_date_w")
def get_timetable_date(role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_worker(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})
    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM timetable_date;
    ''')
    result = json.loads(json.dumps(cursor.fetchall()))
    conn.close()
    return result

@worker_router.get("/salary_w")
def get_salary(role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_worker(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})
    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM salary;
    ''')
    result = json.loads(json.dumps(cursor.fetchall()))
    conn.close()
    return result

@worker_router.get("/bonuses_and_penalties_w")
def get_bonuses_and_penalties(role=Depends(KeycloakJWTBearerHandler())):
    # Проверка авторизации
    if not verify_worker(role):
        raise HTTPException(status_code=403, detail={"message": "Доступ запрещен"})
    conn = sqlite3.connect('C:\\Users\\ssdeg\\PycharmProjects\\DateBaseWeb\\Database\\coffee_shop.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM bonuses_and_penalties;
    ''')
    result = json.loads(json.dumps(cursor.fetchall()))
    conn.close()
    return result

def verify_worker(role) -> bool:
    if role == "worker":
        return True
    else:
        return False