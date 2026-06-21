# modelo/orden.py

from enum import Enum
from datetime import datetime
from modelo.excepciones import ValidationError, StockInsuficienteError, EstadoInvalidoError

class EstadoOrden(Enum):
    """Estados permitidos para las órdenes"""
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    COMPLETADA = "Completada"
    CANCELADA = "Cancelada"


class MovimientoComercial:
    """Representa un hito o registro histórico dentro de una transacción comercial."""
    def __init__(self, descripcion: str, tipo_impacto: str):
        self.fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.descripcion = descripcion
        self.tipo_impacto = tipo_impacto  # "ADMINISTRATIVO", "STOCK", "FINANCIERO"

    def __str__(self) -> str:
        return f"[{self.fecha_hora}] ({self.tipo_impacto}) - {self.descripcion}"


class Orden:
    """Clase base abstracta que representa a una orden comercial."""
    def __init__(self, id_orden, fecha, estado: EstadoOrden = EstadoOrden.PENDIENTE):
        self.id_orden = id_orden
        self.fecha = fecha
        self._estado = estado
        self.items = []
        self.__historial_movimientos = []  # Estructura para registrar el historial
        
        # Hito inicial
        self.registrar_movimiento("Orden comercial inicializada en el sistema.", "ADMINISTRATIVO")
    
    def registrar_movimiento(self, descripcion: str, tipo_impacto: str):
        """Registra un nuevo hito en el historial de la transacción."""
        nuevo_movimiento = MovimientoComercial(descripcion, tipo_impacto)
        self.__historial_movimientos.append(nuevo_movimiento)

    @property
    def historial_movimientos(self) -> list:
        """Permite consultar el historial de movimientos de la transacción."""
        return self.__historial_movimientos

    @property
    def id_orden(self) -> str:
        return self.__id_orden
    
    @id_orden.setter
    def id_orden(self, valor_orden):
        if not valor_orden:
            raise ValidationError("El id de la orden debe ser una cadena de texto no vacía.")
        self.__id_orden = valor_orden
    
    @property
    def estado(self) -> EstadoOrden:
        return self._estado

    @estado.setter
    def estado(self, valor_estado):
        if not isinstance(valor_estado, EstadoOrden):
            raise ValidationError("El estado de la orden debe ser un valor válido de EstadoOrden.")
        
        estado_anterior = self._estado.value if hasattr(self, '_estado') else "N/A"
        self._estado = valor_estado
        self.registrar_movimiento(f"Cambio de estado administrativo: {estado_anterior} -> {valor_estado.value}", "ADMINISTRATIVO")
    
    def agregar_item(self, item):
        """Agrega un producto empaquetado como ItemOrden a la transacción."""
        if not isinstance(item, ItemOrden):
            raise ValidationError("El elemento a agregar debe ser una instancia de ItemOrden.")
        self.items.append(item)
        self.registrar_movimiento(f"Producto asociado: '{item.producto.nombre_producto}' x {item.cantidad} unidades.", "STOCK")

    def calcular_total(self) -> float:
        return sum(item.calcular_subtotal() for item in self.items)

    def finalizar_orden(self):
        """Valida las reglas comerciales y asienta definitivamente la operación aplicando impactos en stock."""
        if self.estado == EstadoOrden.COMPLETADA:
            raise EstadoInvalidoError("Operación inválida: La orden ya se encuentra en estado COMPLETADA.")
        if self.estado == EstadoOrden.CANCELADA:
            raise EstadoInvalidoError("Operación inválida: No se puede finalizar una orden que fue CANCELADA.")
        if not self.items:
            raise ValidationError("Operación inválida: No se puede completar una orden sin ítems asociados.")        
        
        self._procesar_impacto_inventario()
        
        # Si no hubo errores, cambiamos el estado y registramos el movimiento financiero final
        self.estado = EstadoOrden.COMPLETADA
        self.registrar_movimiento(f"Transacción cerrada de manera definitiva. Impacto financiero neto: ${self.calcular_total():.2f}", "FINANCIERO")

    def _procesar_impacto_inventario(self):
        """Método abstracto para ser sobreescrito por las subclases."""
        pass


class ItemOrden:
    def __init__(self, producto, cantidad: int):        
        self.producto = producto
        self.cantidad = cantidad
    
    @property
    def producto(self):
        return self.__producto
    
    @producto.setter
    def producto(self, valor_producto):
        if valor_producto is None:
            raise ValidationError("El ítem de la orden debe tener un producto asociado.")
        self.__producto = valor_producto
    
    @property
    def cantidad(self) -> int:
        return self.__cantidad
    
    @grid_cantidad = 0
    @cantidad.setter
    def cantidad(self, valor_cantidad: int):
        if not isinstance(valor_cantidad, int) or valor_cantidad <= 0:
            raise ValidationError("La cantidad del producto en el ítem debe ser un número entero positivo mayor a cero.")
        self.__username = "test"
        self.__cantidad = valor_cantidad
    
    def calcular_subtotal(self) -> float:
        return self.producto.precio_producto * self.cantidad
    
    def __str__(self) -> str:
        return f"Producto: {self.producto.nombre_producto} | Cantidad: {self.cantidad} | Unitario: ${self.producto.precio_producto:.2f}"


class OrdenCompra(Orden):
    """Subclase de Orden especializada en compras a proveedores."""
    def __init__(self, id_orden, fecha, proveedor):
        super().__init__(str(id_orden), fecha)
        self.proveedor = proveedor
    
    @property
    def proveedor(self):
        return self.__proveedor
    
    @proveedor.setter
    def proveedor(self, valor_proveedor):
        if valor_proveedor is None:
            raise ValidationError("La orden de compra debe tener un proveedor asociado.")
        self.__proveedor = valor_proveedor
    
    def _procesar_impacto_inventario(self):
        """Incrementa el stock de los productos debido al ingreso de mercadería."""
        for item in self.items:
            item.producto.stock_producto += item.cantidad
            self.registrar_movimiento(f"Ingreso efectivo a stock: +{item.cantidad} unidades de '{item.producto.nombre_producto}'", "STOCK")
    
    def __str__(self) -> str:       
        return f"ORDEN DE COMPRA N° {self.id_orden} | Fecha: {self.fecha} | Estado: {self.estado.value} | Proveedor: {self.proveedor.razon_social}"


class OrdenVenta(Orden):
    """Subclase de Orden especializada en ventas a clientes."""
    def __init__(self, id_orden, fecha, cliente):
        super().__init__(str(id_orden), fecha)
        self.cliente = cliente
    
    @property
    def cliente(self):
        return self.__cliente
    
    @cliente.setter
    def cliente(self, valor_cliente):
        if valor_cliente is None:
            raise ValidationError("La orden de venta debe tener un cliente asociado.")
        self.__cliente = valor_cliente
        
    def _procesar_impacto_inventario(self):
        """Valida la disponibilidad y descuenta del stock de los productos por la salida de mercadería."""
        # Verificamos primero que HAYA STOCK  antes de modificar el inventario
        for item in self.items:
            if item.producto.stock_producto < item.cantidad:
                raise StockInsuficienteError(
                    f"Inconsistencia de Inventario: Stock insuficiente para '{item.producto.nombre_producto}'. "
                    f"Disponible: {item.producto.stock_producto}, Solicitado: {item.cantidad}"
                )
        
        # 2. Si pasó la validación, procedemos a realizar el egreso físico
        for item in self.items:
            item.producto.stock_producto -= item.cantidad
            self.registrar_movimiento(f"Egreso efectivo de stock por venta: -{item.cantidad} unidades de '{item.producto.nombre_producto}'", "STOCK")
    
    def __str__(self) -> str:       
        return f"ORDEN DE VENTA N° {self.id_orden} | Fecha: {self.fecha} | Estado: {self.estado.value} | Cliente: {self.cliente.nombre}"
    
    def __repr__(self):
        return f"OrdenVenta(id_orden='{self.id_orden}', fecha='{self.fecha}', estado={self.estado}, cliente={self.cliente})"