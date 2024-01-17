import datetime

from pydantic import BaseModel, Field
class employeer_model(BaseModel):
    employees_id:int
    employees_full_name:str
    phone_number:str
    age:int
class timetable_model(BaseModel):
    employees_id:int
    start_date:datetime.date
    start_time:datetime.time
    end_date:datetime.date
    end_time:datetime.time
    worked_hours:int
class salary_model(BaseModel):
    employees_id: int
    work_count: int
    hour_cost: int
    full_salary: float
class bonuses_model(BaseModel):
    employees_id: int
    status: bool
    summ: int