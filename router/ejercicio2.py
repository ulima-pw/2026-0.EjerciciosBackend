from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(
    prefix = "",
    tags = ["Ejercicio 2"]
)

class ConvertRequest(BaseModel):
    category : str
    from_unit : str
    to_unit : str
    value : float

@router.post("/convert")
async def convert(req : ConvertRequest):
    if req.category == "temperature":
        resp = None
        formula = None
        if req.from_unit == "F" and req.to_unit == "C":
            resp = (req.value - 32) * (5/9)
            formula = "valor - 32 * (5/9)"
        if req.from_unit == "C" and req.to_unit == "F":
            resp = (req.value * (9/5)) + 32
            formula = "valor * (9/5) + 32"

        if resp == None:
            raise HTTPException(
                status_code=400,
                detail={
                    "msg" : "Unidades de temperatura invalidas"
                }
            )
        else:
            return {
                "result" : resp,
                "formula" : formula
            }
    else:
        raise HTTPException(
                status_code=400,
                detail={
                    "msg" : "Categoria incorrecta"
                }
            )