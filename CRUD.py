from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from database import *
from fastapi.encoders import jsonable_encoder
import datetime
import json


#CREATE
def add_production_area(number_area: int, name: str):
    db = next(get_db())
    try:
        db.execute(text("CALL AddProductionArea(:number_area,:name);"),
                   {"number_area": number_area, "name": name})
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def add_equip(prod_id: int, number_equip: int, type_eq: str, name: str):
    db = next(get_db())
    try:
        db.execute(text("CALL AddEquipment(:prod_id, :number_equip, :type_eq, :name);"),
        {   "prod_id": prod_id,
            "number_equip": number_equip,
            "type_eq": type_eq,
            "name": name})
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def add_tech_inspection(equip_id: int, date: datetime.date, equip_cond: str, reason: str, type_inspection: str):
    db = next(get_db())
    try:
        db.execute(text("CALL ADDTechInspection(:equip_id, :date, :equip_cond, :reason, :type_inspection);" ),
            {   "equip_id": equip_id,
                "date": date,
                "equip_cond": equip_cond,
                "reason": reason,
                "type_inspection": type_inspection})
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def add_employee(tech_id: int, number: int, name: str, position: str):
    db = next(get_db())
    try:
        db.execute(text("CALL AddEmployee(:tech_id, :number, :name, :position);"),
            {   "tech_id": tech_id,
                "number": number,
                "name": name,
                "position": position})
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


#READ
def get_failed_equipment():
    db = next(get_db())
    try:
        # Выполняем хранимую функцию
        result = db.execute(text("SELECT GetFailedEquipment();")).fetchone()

        # Проверяем, вернул ли результат что-либо
        if result and result[0]:  # Проверяем, что результат существует и содержит JSON
            data = json.loads(result[0])  # Парсим JSON строку
            return data
 # result[0] - это результат JSON из БД
        else:
            return {"error": "No data found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def get_equipment_inspection_history(p_inventory_number: int):
    db = next(get_db())
    try:
        # Выполняем хранимую функцию
        result = db.execute(text(f"SELECT GetEquipmentInspectionHistory({p_inventory_number});")).fetchone()

        # Проверяем, вернул ли результат что-либо
        if result and result[0]:  # Проверяем, что результат существует и содержит JSON
            data = json.loads(result[0])  # Парсим JSON строку
            return data# result[0] - это результат JSON из БД
        else:
            return {"error": "No data found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def get_employees_on_date(date: str):
    db = next(get_db())
    try:
        # Выполняем хранимую функцию
        result = db.execute(text("SELECT GetEmployeesOnDate(:date);"), {"date": date}).fetchone()

        # Проверяем, вернул ли результат что-либо
        if result and result[0]:  # Проверяем, что результат существует и содержит JSON
            data = json.loads(result[0])  # Парсим JSON строку
            return data  # result[0] - это результат JSON из БД
        else:
            return {"error": "No data found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def get_tech_inspection():
    db = next(get_db())
    try:
        result = db.execute(text("SELECT * FROM Техосмотр")).fetchall()
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def get_employees():
    db = next(get_db())
    try:
        result = db.execute(text("SELECT * FROM Сотрудники")).fetchall()
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def get_production_area():
    db = next(get_db())
    try:
        result = db.execute(text("SELECT * FROM Производственный_участок")).fetchall()
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def get_equip():
    db = next(get_db())
    try:
        result = db.execute(text("SELECT * FROM Оборудование")).fetchall()
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()
def get_production_area_by_id(id: int):
    db = next(get_db())
    try:
        result = db.execute(text("SELECT * FROM Производственный_участок WHERE production_area_id= :id"), {"id": id}).fetchone()
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def get_equip_by_id(id: int):
    db = next(get_db())
    try:
        result = db.execute(text("SELECT * FROM Оборудование WHERE equipment_id= :id"), {"id": id}).fetchone()
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def get_tech_by_id(id: int):
    db = next(get_db())
    try:
        result = db.execute(text("SELECT * FROM Техосмотр WHERE tech_inspection_id= :id"), {"id": id}).fetchone()
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def get_employee_by_id(id: int):
    db = next(get_db())
    try:
        result = db.execute(text("SELECT * FROM Сотрудники WHERE personal_id= :id"), {"id": id}).fetchone()
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


#UPDATE
def update_production_area(prod_id: int, number_area: int, name: str):
    db = next(get_db())
    try:
        db.execute(text("CALL UpdateProductionArea(:id,:number_area,:name);"),
                   {"id": prod_id, "number_area": number_area, "name": name})
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def update_equip(equip_id: int, prod_id: int, number_equip: int, type_eq: str, name: str):
    db = next(get_db())
    try:
        db.execute(text("CALL UpdateEquipment(:equip_id, :prod_id, :number_equip, :type_eq, :name);"),
        {"equip_id": equip_id,
            "prod_id": prod_id,
            "number_equip": number_equip,
            "type_eq": type_eq,
            "name": name})
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def update_tech_inspection(tech_id: int, equip_id: int, date: datetime.date, equip_cond: str, reason: str, type_inspection: str):
    db = next(get_db())
    try:
        db.execute(text("CALL UpdateTechInspection(:tech_id, :equip_id, :date, :equip_cond, :reason, :type_inspection);" ),
            {  "tech_id": tech_id,
                "equip_id": equip_id,
                "date": date,
                "equip_cond": equip_cond,
                "reason": reason,
                "type_inspection": type_inspection})
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def update_employee(employee_id: int, tech_id: int, personal_num: int, name: str, position: str):
    db = next(get_db())
    try:
        db.execute(text("CALL UpdateEmployee(:employee_id, :tech_id, :personal_num, :name, :position);"),
            {  "employee_id": employee_id,
                "tech_id": tech_id,
                "personal_num": personal_num,
                "name": name,
                "position": position})
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


#DELETE
def delete_tech_inspection(id: int):
    db = next(get_db())
    try:
        db.execute(text("CALL DeleteTechInspection(:id);"), {"id": id})
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def delete_equip(id: int):
    db = next(get_db())
    try:
        db.execute(text("CALL DeleteEquipment(:id);"), {"id": id})
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def delete_production_area(id: int):
    db = next(get_db())
    try:
        db.execute(text("CALL DeleteProductionArea(:id);"), {"id": id})
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def delete_employee(Num_id: int):
    db = next(get_db())
    try:
        db.execute(text("CALL DeleteEmployee(:id);"), {"id": Num_id})
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


if __name__ == "__main__":
    print(get_tech_inspection())
    print(add_tech_inspection(5, datetime.date(2024, 8, 12), 'Неисправно', None, 'Аварийный'))
    print(get_tech_inspection())
    print(get_failed_equipment())