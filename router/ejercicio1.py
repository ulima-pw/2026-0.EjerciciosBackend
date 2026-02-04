from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(
    prefix = "",
    tags = ["Tasks"]
)

tasks_repertory : dict[str, "Task"] = {
    "60799464-972d-419b-857e-379664f33b91": {
        "id": "60799464-972d-419b-857e-379664f33b91",
        "title": "Optimizar consultas SQL",
        "description": "Agregar índices a la tabla de usuarios para mejorar el tiempo de respuesta.",
        "priority": 5,
        "complete" : False
    },
    "a1b2c3d4-e5f6-4a5b-bc6d-7e8f9a0b1c2d": {
        "id": "a1b2c3d4-e5f6-4a5b-bc6d-7e8f9a0b1c2d",
        "title": "Corregir estilos CSS",
        "description": "Ajustar el padding del contenedor principal en dispositivos móviles.",
        "priority": 2,
        "complete" : True
    },
    "f1234567-89ab-cdef-0123-456789abcdef": {
        "id": "f1234567-89ab-cdef-0123-456789abcdef",
        "title": "Reunión técnica",
        "description": "Definir la arquitectura de microservicios para el nuevo módulo.",
        "priority": 4,
        "complete" : False
    },
    "99887766-5544-3322-1100-aabbccddeeff": {
        "id": "99887766-5544-3322-1100-aabbccddeeff",
        "title": "Actualizar README",
        "description": "Incluir instrucciones sobre cómo configurar las variables de entorno.",
        "priority": 1,
        "complete" : True
    },
    "550e8400-e29b-41d4-a716-446655440000": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Pruebas de integración",
        "description": "Ejecutar suite de tests en el entorno de staging.",
        "priority": 3,
        "complete" : False
    }
}

class Task(BaseModel):
    id : str
    title : str
    descripton: Optional[str] = None
    priority : int = Field(..., ge = 1, le = 5)
    complete : bool = False

class TaskCreate(BaseModel):
    title : str
    descripton: Optional[str] = None
    priority : int = Field(..., ge = 1, le = 5)

@router.post("/tasks")
async def createTasks(payload : TaskCreate):
    task_id = str(uuid4())

    task = Task(
        id = task_id,
        title = payload.title,
        descripton= payload.descripton,
        priority= payload.priority,
        complete= False
    )

    tasks_repertory[task_id] = task
    return { "msg" : "task created", "data" : task }

@router.get("/tasks/{task_id}")
async def getTask(task_id : str):
    task = tasks_repertory.get(task_id)

    if not task:
        raise HTTPException( status_code= 404 , detail= "Task not found in this repository" )
    
    return {"msg" : "", "data" : task}

@router.get("/tasks")
async def getListTask(
    complete : Optional[bool] = Query(default = None),
    min_priority : Optional[int] = Query(default = None, ge = 1, le = 5), 
    skip : Optional[int] = Query(default= 1, ge = 0),
    limit : Optional[int] = Query(default=1)
):

    tasks = []
    for task in tasks_repertory.values():
        if complete != None:
            if task.complete == complete :
                tasks.append(task)
            else:
                continue
        else:
            tasks.append(task)

        if min_priority != None:
            if task.priority < min_priority :
                tasks.remove(task)

    # if complete != None:
    #     filterTasks = []
    #     for task in tasks:
    #         if task.complete == complete :
    #             filterTasks.append(task)

    #     tasks = filterTasks

    # if min_priority != None:
    #     filterTasks = []
    #     for task in tasks:
    #         if task.priority >= min_priority :
    #             filterTasks.append(task)

    #     tasks = filterTasks

    start = skip * limit
    end = start + limit

    lista_parcial = tasks[start:end]

    total = len(lista_parcial)

    return {
        "msg" : "",
        "meta" : {
            "total" : total,
            "skip" : skip,
            "limit" : limit 
        },
        "data" : lista_parcial
    }
