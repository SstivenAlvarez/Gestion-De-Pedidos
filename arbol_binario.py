from modelos import Producto
from typing import List, Optional


class ArbolNodo:
    """Estructura del arbol binario"""
    def __init__(self, producto: Producto):
        self.producto = producto
        self.derecha = None
        self.izquierda = None

class ArbolBusqueda:
    def __init__(self):
        self.raiz = None
        self.cantidad_productos = 0

    def insertar(self, producto: Producto) -> bool:
        """Se inserta un producto al arbol y estos se iran ordenando por ID 
        si el ID es unico retornara True si se repite algun ID retornara "ID ya existe"""
        if self.raiz is None:
            self.raiz = ArbolNodo(producto)
            self.cantidad_productos += 1
            return True
        
        return self.insertar_recur(self.raiz, producto)
    
    def insertar_recur(self, nodo: ArbolNodo, producto: Producto) -> bool:
        if producto.id == nodo.producto.id:
            return False
        
        if producto.id < nodo.producto.id:
            if nodo.izquierda is None:
                nodo.izquierda = ArbolNodo(producto)
                self.cantidad_productos += 1
                return True
            return self.insertar_recur(nodo.izquierda, producto)
    
        else:
            if nodo.derecha is None:
                nodo.derecha = ArbolNodo(producto)
                self.cantidad_productos += 1
                return True
            return self.insertar_recur(nodo.derecha, producto)
    
    def buscar(self, producto_id: int) -> Optional[Producto]:
        return self.buscar_recurso(self.raiz, producto_id)
    
    def buscar_recurso(self, nodo: ArbolNodo, producto_id: int) -> Optional[Producto]:
        if nodo is None:
            return None
        
        if producto_id == nodo.producto.id:
            return nodo.producto
        
        elif producto_id < nodo.producto.id:
            return self.buscar_recurso(nodo.izquierda, producto_id)
        
        else:
            return self.buscar_recurso(nodo.derecho, producto_id)
    
    def obtener_todos_productos(self) -> List[Producto]:
        productos = []
        self.recorrido_ord(self.raiz, productos)
        return productos


    def recorrido_ord(self, nodo: ArbolNodo, productos: List[Producto]):
        if nodo is None:
            return
        self.recorrido_ord(nodo.izquierda, productos)
        productos.append(nodo.producto) 
        self.recorrido_ord(nodo.derecha, productos)

                           
    def eliminar (self, producto_id: int ) -> bool:
        self.raiz, eliminado = self.eliminar_recur(self.raiz, producto_id)
        if eliminado:
            self.cantidad_productos -=1
        return eliminado
    
    def eliminar_recur(self, nodo: ArbolNodo, producto_id: int) -> tuple:
        if nodo is None:
            return None, False
        
        if producto_id == nodo.producto.id:
            if nodo.izquierda is None and nodo.derecha is None:
                return None, True
            
            if nodo.izquierda is None:
                return nodo.derecha, True
            if nodo.derecha is None:
                return nodo.izquierda, True
            
            nodo_min = self.encontrar_min(nodo.derecha)
            nodo.producto = nodo_min.producto
            nodo.derecha, _ = self.eliminar_recur(nodo.derecha, nodo_min.producto.id)
            return nodo, True

        elif producto_id < nodo.producto.id:
            nodo.izquierda, eliminado = self.eliminar_recur(nodo.izquierda, producto_id)
            return nodo, eliminado

        else:
            nodo.derecha, eliminado = self.eliminar_recur(nodo.derecha, producto_id) 
            return nodo, eliminado
        
    def encontrar_min(self, nodo: ArbolNodo) -> ArbolNodo:
        actual = nodo 
        while actual.izquierda is not None:
            actual = actual.izquierda
            return actual
