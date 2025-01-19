from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# URL для подключения к существующей базе данных
DATABASE_URL = "mysql+mysqlconnector://root:2004@127.0.0.1:3306/lab2"

# Создаем подключение (движок) к существующей БД
engine = create_engine(DATABASE_URL, echo=True)

# Создаем SessionLocal для работы с БД
SessionLocal = sessionmaker(bind=engine)

# Базовый класс для ORM-моделей (но не создаем новые таблицы)
Base = declarative_base()

# Определяем модели в соответствии со структурой БД
class ProductionArea(Base):
    __tablename__ = 'Производственный_участок'

    production_area_id = Column(Integer, primary_key=True, index=True)
    number_area = Column(Integer, nullable=False)
    name = Column(String(45), nullable=False)

    equipment = relationship("Equipment", back_populates="production_area")


class Equipment(Base):
    __tablename__ = 'Оборудование'

    equipment_id = Column(Integer, primary_key=True, index=True)
    number_equip = Column(Integer, nullable=False)
    type_equip = Column(String(45), nullable=False)
    name_equip = Column(String(45), nullable=False)
    production_area_id = Column(Integer, ForeignKey('Производственный_участок.production_area_id'), nullable=False)

    production_area = relationship("ProductionArea", back_populates="equipment")
    inspections = relationship("TechInspection", back_populates="equipment")


class TechInspection(Base):
    __tablename__ = 'Техосмотр'

    tech_inspection_id = Column(Integer, primary_key=True, index=True)
    date_inspection = Column(Date, nullable=False)
    equipment_condition = Column(String(45), nullable=False)
    reason_of_destruction = Column(String(45), nullable=True)
    type_inspection = Column(String(45), nullable=False)
    equipment_id = Column(Integer, ForeignKey('Оборудование.equipment_id'), nullable=False)

    equipment = relationship("Equipment", back_populates="inspections")


class Employee(Base):
    __tablename__ = 'Сотрудники'

    personal_id = Column(Integer, primary_key=True, index=True)
    personal_number = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    position = Column(String(45), nullable=False)
    tech_inspection_id = Column(Integer, ForeignKey('Техосмотр.tech_inspection_id'), nullable=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
