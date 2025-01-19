from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from database import *
from CRUD import *
from fastapi.encoders import jsonable_encoder
import json
import logging
import datetime
from typing import Optional


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def menu_page(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})


@app.get("/production_area", response_class=HTMLResponse)
async def view_production_area(request: Request):
    data = get_production_area()
    return templates.TemplateResponse("production_area_view.html", {"request": request, "areas": data})


@app.get("/production_area/put/{area_id}")
async def edit_area_page(request: Request, area_id: int):
    area = get_production_area_by_id(area_id)

    if area is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return templates.TemplateResponse("production_area_edit.html", {"request": request, "area": area})


@app.post("/production_area/put/{area_id}")
async def edit_area(request: Request, area_id: int, number_area: int = Form(...), name:str = Form(...)):
    try:
        update_production_area(area_id, number_area,name)
        return RedirectResponse(url="/production_area", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/production_area/add")
async def add_area(number_area: int = Form(...), name: str = Form(...)):
    try:
        add_production_area(number_area, name)
        return RedirectResponse(url="/production_area", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/production_area/delete/{area_id}")
async def delete_area(request: Request, area_id: int):
    try:
        delete_production_area(area_id)
        return RedirectResponse(url="/production_area", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/equip", response_class=HTMLResponse)
async def view_equip(request: Request):
    data = get_equip()
    return templates.TemplateResponse("equip_view.html", {"request": request, "equips": data})


@app.get("/equip/put/{equip_id}")
async def edit_equip_page(request: Request, equip_id: int):
    equip = get_equip_by_id(equip_id)

    if equip is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return templates.TemplateResponse("equip_edit.html", {"request": request, "equip": equip})


@app.post("/equip/put/{equip_id}")
async def edit_equip(request: Request, equip_id: int, prod_id: int = Form(...),
                    number: int = Form(...), type: str = Form(...), name: str = Form(...)):
    try:
        update_equip(equip_id, prod_id, number, type, name)
        return RedirectResponse(url="/equip", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/equip/add")
async def addr_equip(prod_id: int = Form(...), number: int = Form(...),
                   type: str = Form(...), name: str = Form(...)):
    try:
        add_equip(prod_id, number, type, name)
        return RedirectResponse(url="/equip", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/equip/delete/{equip_id}")
async def delete_equipr(request: Request, equip_id: int):
    try:
        delete_equip(equip_id)
        return RedirectResponse(url="/equip", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tech", response_class=HTMLResponse)
async def view_tech(request: Request):
    data = get_tech_inspection()
    return templates.TemplateResponse("tech_view.html", {"request": request, "techs": data})


@app.get("/tech/put/{tech_id}")
async def edit_tech_page(request: Request, tech_id: int):
    tech = get_tech_by_id(tech_id)

    if tech is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return templates.TemplateResponse("tech_edit.html", {"request": request, "tech": tech})


@app.post("/tech/put/{tech_id}")
async def edit_tech(request: Request, tech_id: int, equip_id: int = Form(...), date: datetime.date = Form(...), equip_cond: str = Form(...),
                  reason: str = Form(...), type: str = Form(...)):
    try:
        if reason =="" or reason =="None":
            reason = None
        update_tech_inspection(tech_id, equip_id, date, equip_cond, reason, type)
        return RedirectResponse(url="/tech", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tech/add")
async def add_tech(equip_id: int = Form(...), date: datetime.date = Form(...), equip_cond: str = Form(...),
                  reason: str = Form(...), type: str = Form(...)):
    try:
        if reason =="" or reason =="None":
            reason = None
        add_tech_inspection(equip_id, date, equip_cond, reason, type)
        return RedirectResponse(url="/tech", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tech/delete/{tech_id}")
async def delete_tech(request: Request, tech_id: int):
    try:
        delete_tech_inspection(tech_id)
        return RedirectResponse(url="/tech", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/employee", response_class=HTMLResponse)
async def view_employee(request: Request):
    data = get_employees()
    return templates.TemplateResponse("employee_view.html", {"request": request, "employees": data})


@app.get("/employee/put/{employee_id}")
async def edit_employee_page(request: Request, employee_id: int):
    employee = get_employee_by_id(employee_id)

    if employee is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return templates.TemplateResponse("employee_edit.html", {"request": request, "employee": employee})


@app.post("/employee/put/{employee_id}")
async def edit_employee(request: Request, employee_id: int, tech_id: int = Form(...), number: int = Form(...),
                    name: str = Form(...), position: str = Form(...)):
    try:
        update_employee(employee_id, tech_id, number, name, position)
        return RedirectResponse(url="/employee", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/employee/add")
async def add_employeer(tech_id: int = Form(...), number: int = Form(...),
                    name: str = Form(...), position: str = Form(...)):
    try:
        add_employee(tech_id, number, name, position)
        return RedirectResponse(url="/employee", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/employee/delete/{employee_id}")
async def delete_employeer(request: Request, employee_id: int):
    try:
        delete_employee(employee_id)
        return RedirectResponse(url="/employee", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/equip/history", response_class=HTMLResponse)
async def equip_history_page(request: Request):
    histories = list(set([i[2] for i in get_equip()]))
    return templates.TemplateResponse("equip_history_input.html", {"request": request, "histories": histories})


@app.post("/equip/history")
async def equip_history(request: Request, equip_number: int = Form(...)):
    try:
        histories = get_equipment_inspection_history(equip_number)
        return templates.TemplateResponse("equip_history.html", {"request": request, "histroies": histories})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/employee/date", response_class=HTMLResponse)
async def equip_history(request: Request):
    dates = list(set(i[2] for i in get_tech_inspection()))
    return templates.TemplateResponse("employee_input.html", {"request": request, "dates": dates})


@app.post("/employee/date")
async def equip_history(request: Request, date: str = Form(...)):
    try:
        data = get_employees_on_date(date)
        return templates.TemplateResponse("employee_output.html", {"request": request, "datas": data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/equip/failed", response_class=HTMLResponse)
async def equip_history(request: Request):
    data = get_failed_equipment()
    return templates.TemplateResponse("failed.html", {"request": request, "datas": data})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


