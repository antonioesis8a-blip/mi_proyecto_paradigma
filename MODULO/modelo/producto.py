# Clase Producto

# modelo/producto.py
import re
from enum import Enum

class CategoriaProducto(Enum):
    ELECTRONICA = "Electrónica"
    ALIMENTOS = "Alimentos"
    ROPA = "Ropa"
    HOGAR = "Hogar"
    INDUMENTARIA = "Indumentaria"
    INFORMATICA = "Informática"

class Producto:
    def __init__(self, id_producto, nombre_producto, descripcion_producto, precio_producto, stock_producto, categoria_producto):
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.descripcion_producto = descripcion_producto
        self.precio_producto = precio_producto
        self.stock_producto = stock_producto
        self.categoria_producto = categoria_producto

    @property
    def id_producto(self) -> str:
        return self.__id_producto

    @id_producto.setter
    def id_producto(self, valor_producto):
        patron_id_producto = r"^PROD-\d{4}$"   
        if not valor_producto or not isinstance(valor_producto, str):
            raise ValueError("El id del producto debe ser una cadena de texto no vacía")
        if not re.match(patron_id_producto, valor_producto):
            raise ValueError("El id del producto no cumple con el formato requerido (PROD-XXXX)")
        self.__id_producto = valor_producto

    @property
    def nombre_producto(self) -> str:
        return self.__nombre_producto

    @nombre_producto.setter
    def nombre_producto(self, valor_nombre):
        if not valor_nombre or not isinstance(valor_nombre, str) or valor_nombre.strip() == "":
            raise ValueError("El nombre del producto debe ser una cadena de texto no vacía")
        self.__nombre_producto = valor_nombre.strip()
    
    @property
    def descripcion_producto(self) -> str:
        return self.__descripcion_producto
    
    @descripcion_producto.setter
    def descripcion_producto(self, valor_descripcion):
        if not valor_descripcion or not isinstance(valor_descripcion, str):
            raise ValueError("La descripción del producto debe ser una cadena de texto no vacía")
        self.__descripcion_producto = valor_descripcion
    
    @property
    def precio_producto(self) -> float:
        return self.__precio_producto
    
    @precio_producto.setter
    def precio_producto(self, valor_precio):
        if not isinstance(valor_precio, (int, float)) or valor_precio < 0:
            raise ValueError("El precio del producto debe ser un número positivo")
        self.__precio_producto = float(valor_precio)
    
    @property
    def stock_producto(self) -> int:
        return self.__stock_producto
    
    @stock_producto.setter
    def stock_producto(self, valor_stock):
        if not isinstance(valor_stock, int) or valor_stock < 0:
            raise ValueError("El stock del producto debe ser un número entero positivo")
        self.__stock_producto = valor_stock

    @property
    def categoria_producto(self) -> CategoriaProducto:
        return self.__categoria_producto

    @categoria_producto.setter
    def categoria_producto(self, valor_categoria: CategoriaProducto):
        if not isinstance(valor_categoria, CategoriaProducto):
            raise ValueError(f"Categoría inválida.")
        self.__categoria_producto = valor_categoria     

    def __str__(self):
        return f"[{self.id_producto}] {self.nombre_producto} | Cat: {self.categoria_producto.value} | Precio: ${self.precio_producto:.2f} | Stock: {self.stock_producto} u."