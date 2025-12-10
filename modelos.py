
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Producto(BaseModel):
    """Modelo general para cada producto del arbol binario"""
    id: int
    nombre: str
    precio: float
    cantidad: int
    descripcion: Optional[str] = None

    class config:
        json_schema_extra = {
            "ejemplo":{
                id: 1,
                "nombre": "Camara",
                "precio": 209900.00,
                "cantidad": 15,
                "descripcion": "Camara Emeet Nova 4k"
            }
        }

class Produc_Orden(BaseModel):
    """Productos que estan dentro de una orden"""
    producto_id: int
    cantidad: int
    precio: float

class NuevaOrden(BaseModel):
    """Modelo general para crear una nueva orden o pedido"""
    nombre_Cliente: str
    Email_Cliente: str
    productos: List[Produc_Orden]

    class config:
        json_schema_extra = {
            "ejemplo": {
                "nombre_Cliente": "STIVEN ALVAREZ",
                "Email_Cliente": "uem@.es",
                "productos": [
                    {"producto_id": 1, "cantida": 2, "precio": 209900.00},
                    {"producto_id": 2, "cantida": 1, "precio": 51900.00}
                ]
            }
        }

class Actualizar_Pedido(BaseModel):
    """Modelo para actualizar un pedido o orden"""
    nombre_Cliente: Optional[str] = None
    Email_Cliente: Optional[str] = None
    productos: Optional[List[Produc_Orden]] = None

class Respuesta(BaseModel):
    """Modelo de las respuesta que recibiremos"""
    orden_id: int
    nombre_Cliente: str
    Email_Cliente: str
    items: List[Produc_Orden]
    total: float
    fecha: str