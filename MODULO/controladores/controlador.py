# controladores/controlador.py

from modelo.cliente import Cliente
from modelo.proveedor import Proveedor, RubroProveedor
from modelo.producto import Producto, CategoriaProducto
from modelo.orden import Orden, OrdenCompra, OrdenVenta, EstadoOrden
from modelo.excepciones import EntidadDuplicadaError, ValidationError

class GestorSistema:
    """Clase del Controlador (Controller) encargada de gestionar las colecciones globales,
    coordinar las operaciones comerciales y aplicar reglas de negocio del dominio."""

    def __init__(self):
        self.__productos = []
        self.__personas = [] 
        self.__ordenes = []
        self.__contador_ordenes = 0  

    @property
    def productos(self) -> list:
        """Retorna la lista de productos registrados en el sistema."""
        return self.__productos

    @property
    def personas(self) -> list:
        """Retorna la lista de actores (clientes y proveedores) registrados."""
        return self.__personas

    @property
    def ordenes(self) -> list:
        """Retorna la lista de órdenes registradas en el sistema."""
        return self.__ordenes

    # --- Gestión de Productos ---
    def registrar_producto(self, codigo: str, nombre: str, descripcion: str, precio: float, stock: int, categoria_str: str) -> Producto:
        """Registra un nuevo producto, asegurando la unicidad del código identificador."""
        for prod in self.__productos:
            if prod.id_producto == codigo:
                raise EntidadDuplicadaError(f"Error funcional: Ya existe un producto registrado bajo el código '{codigo}'.")
        
        # Mapeo y validación de la categoría ingresada por string hacia su tipo Enum
        try:
            categoria_enum = CategoriaProducto[categoria_str.upper()]
        except KeyError:
            valores_validos = [c.name for c in CategoriaProducto]
            raise ValidationError(f"La categoría '{categoria_str}' no es válida. Opciones: {', '.join(valores_validos)}")

        nuevo_prod = Producto(codigo, nombre, descripcion, precio, stock, categoria_enum)
        self.__productos.append(nuevo_prod)
        return nuevo_prod

    # --- Gestión de Actores (Clientes y Proveedores) ---
    def registrar_cliente(self, id_cliente: str, nombre: str, email: str, telefono: str, direccion: str) -> Cliente:
        """Registra un nuevo cliente en el sistema, controlando duplicados mediante excepción propia."""
        for p in self.__personas:
            if isinstance(p, Cliente) and p.id_cliente == id_cliente:
                raise EntidadDuplicadaError(f"Error funcional: Ya existe un cliente registrado bajo el ID '{id_cliente}'.")
        
        nuevo_cliente = Cliente(id_cliente, nombre, email, telefono, direccion)
        self.__personas.append(nuevo_cliente)
        return nuevo_cliente

    def registrar_proveedor(self, id_proveedor: str, cuit: str, razon_social: str, email: str, telefono: str, direccion: str, rubro_str: str) -> Proveedor:
        """Registra un nuevo proveedor en el sistema, controlando duplicados y mapeando su Enum."""
        for p in self.__personas:
            if isinstance(p, Proveedor) and p.id_proveedor == id_proveedor:
                raise EntidadDuplicadaError(f"Error funcional: Ya existe un proveedor registrado bajo el ID '{id_proveedor}'.")
        
        # Mapeo y validación del rubro ingresado por string hacia su tipo Enum
        try:
            rubro_enum = RubroProveedor[rubro_str.upper()]
        except KeyError:
            valores_validos = [r.name for r in RubroProveedor]
            raise ValidationError(f"El rubro '{rubro_str}' no es válido. Opciones: {', '.join(valores_validos)}")

        nuevo_prov = Proveedor(id_proveedor, cuit, razon_social, email, telefono, direccion, rubro_enum)
        self.__personas.append(nuevo_prov)
        return nuevo_prov

    # --- Gestión de Órdenes Transaccionales ---
    def crear_orden_compra(self, fecha: str, id_proveedor: str) -> OrdenCompra:
        """Genera una nueva Orden de Compra vinculada a un proveedor existente."""
        proveedor = next((p for p in self.__personas if isinstance(p, Proveedor) and p.id_proveedor == id_proveedor), None)
        if not proveedor:
            raise ValidationError(f"No se encontró ningún proveedor registrado bajo el ID '{id_proveedor}'.")
        
        self.__contador_ordenes += 1
        nueva_orden = OrdenCompra(self.__contador_ordenes, fecha, proveedor)
        self.__ordenes.append(nueva_orden)
        return nueva_orden

    def crear_orden_venta(self, fecha: str, id_cliente: str) -> OrdenVenta:
        """Genera una nueva Orden de Venta vinculada a un cliente existente."""
        cliente = next((p for p in self.__personas if isinstance(p, Cliente) and p.id_cliente == id_cliente), None)
        if not cliente:
            raise ValidationError(f"No se encontró ningún cliente registrado bajo el ID '{id_cliente}'.")
        
        self.__contador_ordenes += 1
        nueva_orden = OrdenVenta(self.__contador_ordenes, fecha, cliente)
        self.__ordenes.append(nueva_orden)
        return nueva_orden

    # --- Estadísticas del Sistema ---
    def obtener_estadisticas(self) -> dict:
        """Calcula y retorna estadísticas analíticas completas sobre el inventario,
        las operaciones, estados administrativos y movimientos comerciales financieros."""
        clientes = [p for p in self.__personas if isinstance(p, Cliente)]
        proveedores = [p for p in self.__personas if isinstance(p, Proveedor)]
        
        # 1. AUDITORÍA DE ESTADOS ADMINISTRATIVOS
        pendientes = [o for o in self.__ordenes if o.estado == EstadoOrden.PENDIENTE]
        activas = [o for o in self.__ordenes if o.estado == EstadoOrden.EN_PROCESO]
        finalizadas = [o for o in self.__ordenes if o.estado == EstadoOrden.COMPLETADA]
        canceladas = [o for o in self.__ordenes if o.estado == EstadoOrden.CANCELADA]
        
        # 2. AUDITORÍA POR TIPOS DE OPERACIONES 
        ordenes_compra = [o for o in self.__ordenes if isinstance(o, OrdenCompra)]
        ordenes_venta = [o for o in self.__ordenes if isinstance(o, OrdenVenta)]
        
        # 3. MOVIMIENTOS COMERCIALES (Flujos financieros monetarios de transacciones concretadas)
        monto_compras = sum(o.calcular_total() for o in ordenes_compra if o.estado == EstadoOrden.COMPLETADA)
        monto_ventas = sum(o.calcular_total() for o in ordenes_venta if o.estado == EstadoOrden.COMPLETADA)
        
        # Búsqueda de extremos volumétricos
        orden_mayor = max(self.__ordenes, key=lambda o: o.calcular_total(), default=None)
        orden_menor = min(self.__ordenes, key=lambda o: o.calcular_total(), default=None)

        stats = {
            "total_productos_en_catalogo": len(self.__productos),
            "total_clientes_registrados": len(clientes),
            "total_proveedores_registrados": len(proveedores),
            
            # Desglose de Estados
            "ordenes_en_estado_pendiente": len(pendientes),
            "ordenes_en_estado_en_proceso": len(activas),
            "ordenes_en_estado_completada": len(finalizadas),
            "ordenes_en_estado_cancelada": len(canceladas),
            
            # Desglose de Operaciones
            "total_ordenes_de_compra_emitidas": len(ordenes_compra),
            "total_ordenes_de_venta_emitidas": len(ordenes_venta),
            
            # Movimientos de Caja / Financieros Concretados
            "monto_total_compras_concretadas": f"${monto_compras:.2f}",
            "monto_total_ventas_concretadas": f"${monto_ventas:.2f}",
            
            "orden_de_mayor_volumen_monetario": f"Orden N° {orden_mayor.id_orden} (${orden_mayor.calcular_total():.2f})" if orden_mayor else "N/A",
            "orden_de_menor_volumen_monetario": f"Orden N° {orden_menor.id_orden} (${orden_menor.calcular_total():.2f})" if orden_menor else "N/A",
        }
        return stats