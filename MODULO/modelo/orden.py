# modelos/orden.py
from enum import Enum
from modelos.producto import Producto



class EstadoOrden(Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    COMPLETADA = "Completada"
    CANCELADA = "Cancelada"

class Orden:
    def __init__(self, id_orden, fecha, estado: EstadoOrden = EstadoOrden.PENDIENTE):
        self.id_orden = id_orden
        self.fecha = fecha
        self.estado = estado
        self.__items = []
    
    @property
    def id_orden(self) -> str:
        return self.__id_orden
    
    @id_orden.setter
    def id_orden(self, valor_orden):
        self.__id_orden = str(valor_orden)
    
    @property
    def estado(self) -> EstadoOrden:
        return self.__estado

    @estado.setter
    def estado(self, valor_estado):
        if not isinstance(valor_estado, EstadoOrden):
            raise ValueError("El estado debe ser un valor válido de EstadoOrden.")

    # Solo verifica si el atributo ya fue creado
        if hasattr(self, "_Orden__estado"):
            if self.__estado == EstadoOrden.COMPLETADA:
                raise ValueError("No se puede modificar una orden que ya está COMPLETADA.")

        self.__estado = valor_estado
    
    @property
    def fecha(self) -> str:
        return self.__fecha
    
    @fecha.setter
    def fecha(self, valor_fecha):
        if not valor_fecha:
            raise ValueError("La fecha no puede estar vacía.")
        self.__fecha = valor_fecha
    
    @property
    def items(self) -> list:
        return self.__items

    def agregar_producto(self, producto: Producto, cantidad: int):

        if producto is None:
            raise ValueError("Debe seleccionar un producto.")

        if self.estado == EstadoOrden.COMPLETADA:
            raise ValueError("No se pueden agregar productos a una orden COMPLETADA.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        self.__items.append({
            "producto": producto,
                "cantidad": cantidad
    })

    def calcular_total(self) -> float:
        total = 0.0
        for item in self.__items:
            total += item["producto"].precio_producto * item["cantidad"]
        return total


class OrdenCompra(Orden):
    def __init__(self, id_orden, fecha, proveedor):
        super().__init__(id_orden, fecha)
        self.proveedor = proveedor
    
    @property
    def proveedor(self):
        return self.__proveedor
    
    @proveedor.setter
    def proveedor(self, valor_proveedor):
        if valor_proveedor is None:
            raise ValueError("La orden de compra debe tener un proveedor asociado.")
        self.__proveedor = valor_proveedor
        
    def finalizar_orden(self):
        """Aumenta el stock al completarse la compra."""

        if not self.items:
            raise ValueError("No se puede completar una orden vacía.")

        self.estado = EstadoOrden.COMPLETADA

        for item in self.items:
            item["producto"].stock_producto += item["cantidad"]
        def __str__(self) -> str:
            return f"[COMPRA N° {self.id_orden}] Fecha: {self.fecha} | Estado: {self.estado.value} | Prov: {self.proveedor.razon_social} | Total: ${self.calcular_total():.2f}"


class OrdenVenta(Orden):
    def __init__(self, id_orden, fecha, cliente):
        super().__init__(id_orden, fecha)
        self.cliente = cliente
    
    @property
    def cliente(self):
        return self.__cliente
    
    @cliente.setter
    def cliente(self, valor_cliente):
        if valor_cliente is None:
            raise ValueError("La orden de venta debe tener un cliente asociado.")
        self.__cliente = valor_cliente

    def agregar_producto(self, producto: Producto, cantidad: int):
        """Verifica la disponibilidad de stock en el momento antes de agregar a la lista"""
        if cantidad > producto.stock_producto:
            raise ValueError(f"Stock insuficiente de '{producto.nombre_producto}'. Disponible: {producto.stock_producto}")
        super().agregar_producto(producto, cantidad)

    def finalizar_orden(self):
        """Disminuye el stock al completarse la venta"""
        if not self.items:
            raise ValueError("No se puede completar una orden vacía.")
        
        # Validación final previa a la transacción
        for item in self.items:
            if item["cantidad"] > item["producto"].stock_producto:
                raise ValueError(f"Falta de stock de último minuto para {item['producto'].nombre_producto}")
        
        self.estado = EstadoOrden.COMPLETADA
        for item in self.items:
            item["producto"].stock_producto -= item["cantidad"]
    
    def __str__(self) -> str:
        return f"[VENTA N° {self.id_orden}] Fecha: {self.fecha} | Estado: {self.estado.value} | Cliente: {self.cliente.nombre} | Total: ${self.calcular_total():.2f}"