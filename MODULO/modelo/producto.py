# Clase Producto

# modelo/producto.py
import re
from enum import Enum

from MODULO.interfaz.constantes import PATRON_PRODUCTO_ID
from MODULO.modelo.excepciones import ValidationError

class CategoriaProducto(Enum):
    """Enumeración que representa las categorías de productos disponibles en el sistema."""
    ELECTRONICA = "Electrónica"
    ALIMENTOS = "Alimentos"
    ROPA = "Ropa"
    HOGAR = "Hogar"
    INDUMENTARIA = "Indumentaria"
    INFORMATICA = "Informática"

class Producto:
    """Clase que representa a un producto en el sistema de gestión de ventas."""
    def __init__(self, id_producto, nombre_producto, descripcion_producto, precio_producto, stock_producto, categoria_producto):
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.descripcion_producto = descripcion_producto
        self.precio_producto = precio_producto
        self.stock_producto = stock_producto
        self.categoria_producto = categoria_producto
    
    @staticmethod
    def validar_formato_codigo(codigo: str) -> bool:
        """Encargada de verificar si un código cumple con el patrón estructural requerido por el negocio (PROD-XXXX). """
        if not isinstance(codigo, str):
            return False
        return bool(re.match(PATRON_PRODUCTO_ID, codigo))

    @classmethod
    def crear_desde_linea_texto(cls, linea_csv: str):
        """
        Funciona como un Constructor Alternativo (Factory Method).
        Permite instanciar un objeto Producto procesando una línea de texto plana.
        Útil para migraciones de datos, lectura de archivos o inicializaciones masivas.
        Ejemplo de entrada: "PROD-0045,Mouse Óptico,Mouse inalámbrico 1600 DPI,2500.00,40,ELECTRONICA"
        """
        if not linea_csv or not isinstance(linea_csv, str):
            raise ValidationError("La línea de texto provista para procesar el producto es inválida.")
        
        partes = [p.strip() for p in linea_csv.split(",")]
        if len(partes) != 6:
            raise ValidationError("Formato de línea incorrecto. Debe contener exactamente 6 campos separados por comas.")
        
        codigo, nombre, descripcion, precio_str, stock_str, categoria_str = partes
        
        # Conversiones de tipos con manejo de excepciones semánticas
        try:
            precio = float(precio_str)
            stock = int(stock_str)
        except ValueError as exc:
            raise ValidationError("Inconsistencia de tipos: El precio debe ser decimal y el stock un número entero.") from exc
            
        try:
            categoria_enum = CategoriaProducto[categoria_str.upper()]
        except KeyError as exc:
            valores_validos = [c.name for c in CategoriaProducto]
            raise ValidationError(f"Categoría inválida '{categoria_str}'. Opciones permitidas: {', '.join(valores_validos)}") from exc
        
        # Retornamos la instanciación invocando a la clase misma (cls)
        return cls(codigo, nombre, descripcion, precio, stock, categoria_enum)

    @property
    def id_producto(self) -> str:
        """Obtiene el ID del producto."""
        return self.__id_producto

    @id_producto.setter
    def id_producto(self, valor_producto):
        """Valida que el ID del producto cumpla con el formato requerido (PROD-XXXX) y no sea vacío."""
        if not valor_producto or not isinstance(valor_producto, str):
            raise ValueError("El id del producto debe ser una cadena de texto no vacía")
        if not re.match(patron_id_producto, valor_producto):
            raise ValueError("El id del producto no cumple con el formato requerido (PROD-XXXX)")
        self.__id_producto = valor_producto

    @property
    def nombre_producto(self) -> str:
        """Obtiene el nombre del producto."""
        return self.__nombre_producto

    @nombre_producto.setter
    def nombre_producto(self, valor_nombre):
        if not valor_nombre or not isinstance(valor_nombre, str) or valor_nombre.strip() == "":
            raise ValueError("El nombre del producto debe ser una cadena de texto no vacía")
        self.__nombre_producto = valor_nombre.strip()
    
    @property
    def descripcion_producto(self) -> str:
        """Obtiene la descripción del producto."""
        return self.__descripcion_producto
    
    @descripcion_producto.setter
    def descripcion_producto(self, valor_descripcion):
        if not valor_descripcion or not isinstance(valor_descripcion, str):
            raise ValueError("La descripción del producto debe ser una cadena de texto no vacía")
        self.__descripcion_producto = valor_descripcion
    
    @property
    def precio_producto(self) -> float:
        """Obtiene el precio del producto."""
        return self.__precio_producto
    
    @precio_producto.setter
    def precio_producto(self, valor_precio):
        if not isinstance(valor_precio, (int, float)) or valor_precio < 0:
            raise ValueError("El precio del producto debe ser un número positivo")
        self.__precio_producto = float(valor_precio)
    
    @property
    def stock_producto(self) -> int:
        """Obtiene el stock disponible del producto."""
        return self.__stock_producto
    
    @stock_producto.setter
    def stock_producto(self, valor_stock):
        if not isinstance(valor_stock, int) or valor_stock < 0:
            raise ValueError("El stock del producto debe ser un número entero positivo")
        self.__stock_producto = valor_stock

    @property
    def categoria_producto(self) -> CategoriaProducto:
        """Obtiene la categoría del producto."""
        return self.__categoria_producto

    @categoria_producto.setter
    def categoria_producto(self, valor_categoria: CategoriaProducto):
        if not isinstance(valor_categoria, CategoriaProducto):
            raise ValueError(f"Categoría inválida.")
        self.__categoria_producto = valor_categoria     

    def __str__(self):
        """[Representación Pública] Texto amigable para el usuario final."""
        return (f"[{self.id_producto}] {self.nombre_producto} | "
                f"Cat: {self.categoria_producto.value} | "
                f"Precio: ${self.precio_producto:.2f} | Stock: {self.stock_producto}")

    def __repr__(self) -> str:
        """[Representación Técnica] Inequivoca y orientada al desarrollador/debugging."""
        return (f"Producto(id_producto='{self.id_producto}', "
                f"nombre_producto='{self.nombre_producto}', "
                f"descripcion_producto='{self.descripcion_producto}', "
                f"precio_producto={self.precio_producto}, "
                f"stock_producto={self.stock_producto}, "
                f"categoria_producto=CategoriaProducto.{self.categoria_producto.name})")