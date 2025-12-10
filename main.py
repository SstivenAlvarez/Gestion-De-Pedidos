from fastapi import FastAPI, HTTPException
from modelos import Producto, NuevaOrden, Actualizar_Pedido, Respuesta
from arbol_binario import ArbolBusqueda
from list_pedidos import ListaDePedidos
import uvicorn

app = FastAPI(
    title="Gestión de Pedidos BY Stiven Alvarez",
    description="API REST para gestionar productos y pedidos con estructuras avanzadas UEM",
    version="1.0.0"
)

arbol_productos = ArbolBusqueda()
lista_pedidos = ListaDePedidos()

@app.get("/")
async def raiz():
    return {
        "mensaje": "Bienvenido a la API de Gestión de Pedidos UEM",
        "endpoints": {
            "productos": {
                "crear": "POST /productos",
                "obtener": "GET /productos/{id}",
                "listar": "GET /productos"
            },
            "pedidos": {
                "crear": "POST /pedidos",
                "obtener": "GET /pedidos/{id}",
                "actualizar": "PUT /pedidos/{id}",
                "eliminar": "DELETE /pedidos/{id}",
                "listar": "GET /pedidos"
            }
        }
    }

@app.post("/productos")
async def crear_producto(producto: Producto):
    if arbol_productos.insertar(producto):
        return {
            "mensaje": "Producto creado",
            "producto_id": producto.id,
            "nombre": producto.nombre
        }
    else:
        raise HTTPException(
            status_code=400,
            detail=f"El producto con ID {producto.id} ya existe"
        )

@app.get("/productos/{producto_id}")
async def obtener_producto(producto_id: int):
    producto = arbol_productos.buscar(producto_id)
    
    if producto is None:
        raise HTTPException(
            status_code=404,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "cantidad": producto.cantidad,
        "descripcion": producto.descripcion
    }

@app.get("/productos")
async def listar_productos():
    productos = arbol_productos.obtener_todos_productos()
    
    if not productos:
        return {
            "total": 0,
            "productos": []
        }
    
    return {
        "total": len(productos),
        "productos": [
            {
                "id": p.id,
                "nombre": p.nombre,
                "precio": p.precio,
                "cantidad": p.cantidad,
                "descripcion": p.descripcion
            }
            for p in productos
        ]
    }

@app.post("/pedidos")
async def crear_pedido(orden: NuevaOrden):
    for item in orden.productos:
        if arbol_productos.buscar(item.producto_id) is None:
            raise HTTPException(
                status_code=404,
                detail=f"Producto con ID {item.producto_id} no existe"
            )
    respuesta = lista_pedidos.insertar(orden)
    
    return {
        "mensaje": "Pedido creado exitosamente",
        "orden_id": respuesta.orden_id,
        "total": respuesta.total,
        "fecha": respuesta.fecha
    }

@app.get("/pedidos/{orden_id}")
async def obtener_pedido(orden_id: int):
    nodo = lista_pedidos.buscar(orden_id)
    
    if nodo is None:
        raise HTTPException(
            status_code=404,
            detail=f"Pedido con ID {orden_id} no encontrado"
        )
    
    return {
        "orden_id": nodo.orden_id,
        "nombre_Cliente": nodo.nombre_cliente,
        "Email_Cliente": nodo.email_cliente,
        "productos": nodo.productos,
        "total": nodo.total_pedido,
        "fecha": nodo.fecha_creacion
    }

@app.get("/pedidos")
async def listar_pedidos():
    pedidos = lista_pedidos.obtener_todos_pedidos()
    
    return {
        "total_pedidos": lista_pedidos.cantidad_pedidos,
        "pedidos": [
            {
                "orden_id": p.orden_id,
                "nombre_Cliente": p.nombre_Cliente,
                "Email_Cliente": p.Email_Cliente,
                "productos": p.items,
                "total": p.total,
                "fecha": p.fecha
            }
            for p in pedidos
        ]
    }

@app.put("/pedidos/{orden_id}")
async def actualizar_pedido(orden_id: int, orden_actualizada: Actualizar_Pedido):
    if orden_actualizada.productos:
        for item in orden_actualizada.productos:
            if arbol_productos.buscar(item.producto_id) is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Producto con ID {item.producto_id} no existe"
                )
    nueva_orden = NuevaOrden(
        nombre_Cliente=orden_actualizada.nombre_Cliente or lista_pedidos.buscar(orden_id).nombre_cliente,
        Email_Cliente=orden_actualizada.Email_Cliente or lista_pedidos.buscar(orden_id).email_cliente,
        productos=orden_actualizada.productos or lista_pedidos.buscar(orden_id).productos
    )
    respuesta = lista_pedidos.actualizar(orden_id, nueva_orden)
    
    if respuesta is None:
        raise HTTPException(
            status_code=404,
            detail=f"Pedido con ID {orden_id} no encontrado"
        )
    return {
        "mensaje": "Pedido actualizado exitosamente",
        "orden_id": respuesta.orden_id,
        "total": respuesta.total
    }

@app.delete("/pedidos/{orden_id}")
async def eliminar_pedido(orden_id: int):
    if lista_pedidos.eliminar(orden_id):
        return {
            "mensaje": "Pedido eliminado exitosamente",
            "orden_id": orden_id
        }
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Pedido con ID {orden_id} no encontrado"
        )

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False
    )
