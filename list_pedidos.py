from modelos import NuevaOrden, Produc_Orden, Respuesta
from typing import Optional, List
from datetime import datetime

class NodoList:
    def __init__(self, orden_id: int, orden: NuevaOrden):
        self.orden_id = orden_id
        self.nombre_cliente = orden.nombre_Cliente
        self.email_cliente = orden.Email_Cliente
        self.productos = orden.productos
        self.total_pedido = sum(item.precio * item.cantidad for item in orden.productos)
        self.fecha_creacio = datetime.now().isoformat()
        self.siguiente = None

class ListaDePedidos:
    def __init__(self):
        self.inicio = None
        self.cantidad_pedidos = 0
        self.proximo_id_orden = 1

    def insertar(self, orden: NuevaOrden) -> Respuesta:
        nuevo_nodo = NodoList(self.proximo_id_orden, orden)
        self.proximo_id_orden += 1

        if self.inicio is None:
            self.inicio = nuevo_nodo

        else:
            actual = self.inicio
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

        return Respuesta(
        orden_id=nuevo_nodo.orden_id,
        nombre_Cliente=nuevo_nodo.nombre_cliente,
        Email_Cliente=nuevo_nodo.email_cliente,
        items=nuevo_nodo.productos,
        total=nuevo_nodo.total_pedido,
        fecha=nuevo_nodo.fecha_creacio
        )
    
    def buscar(self, orden_id: int) -> Optional[NodoList]:
        actual = self.inicio
        while actual is not None:
            if actual.orden_id == orden_id:
                return actual
            actual = actual.siguiente
        return None
    
    def obtener_todos_pedidos(self) -> List[Respuesta]:
        pedidos = []
        actual = self.inicio
        
        while actual is not None:
            pedidos.append(Respuesta(
                orden_id=actual.orden_id,
                nombre_Cliente=actual.nombre_cliente,
                Email_Cliente=actual.email_cliente,
                items=actual.productos,
                total=actual.total_pedido,
                fecha=actual.fecha_creacio
            ))
            actual = actual.siguiente
        
        return pedidos
    
    def actualizar(self, orden_id: int, orden_actualizada: NuevaOrden) -> Optional[Respuesta]:
        nodo = self.buscar(orden_id)
        if nodo is None:
            return None
        
        # Actualizar datos
        nodo.nombre_cliente = orden_actualizada.nombre_Cliente
        nodo.email_cliente = orden_actualizada.Email_Cliente
        nodo.productos = orden_actualizada.productos
        nodo.total_pedido = sum(item.precio * item.cantidad for item in orden_actualizada.productos)
        
        return Respuesta(
            orden_id=nodo.orden_id,
            nombre_Cliente=nodo.nombre_cliente,
            Email_Cliente=nodo.email_cliente,
            items=nodo.productos,
            total=nodo.total_pedido,
            fecha=nodo.fecha_creacio
        )
    
    def eliminar(self, orden_id: int) -> bool:
        if self.inicio is not None and self.inicio.orden_id == orden_id:
            self.inicio = self.inicio.siguiente
            self.cantidad_pedidos -= 1
            return True
        
        # Buscar en el resto de la lista
        actual = self.inicio
        while actual is not None and actual.siguiente is not None:
            if actual.siguiente.orden_id == orden_id:
                actual.siguiente = actual.siguiente.siguiente
                self.cantidad_pedidos -= 1
                return True
            actual = actual.siguiente
        
        return False


