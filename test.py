from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from database import *
from fastapi.encoders import jsonable_encoder

app = FastAPI()


def read_production_areas():
    """Получаем все данные из хранимой функции GetFailedEquipment()."""
    db = next(get_db())
    try:
        # Выполняем хранимую функцию
        result = db.execute(text("SELECT GetFailedEquipment();")).fetchone()

        # Проверяем, вернул ли результат что-либо
        if result:
            print(result)
            return jsonable_encoder(result[0])  # result[0] - это результат JSON из БД
        else:
            return {"error": "No data found"}
    except Exception as e:
        return {"error": str(e)}

print(read_production_areas())