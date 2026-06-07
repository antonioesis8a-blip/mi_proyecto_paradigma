# controladores
from modelos.cliente import Cliente
from modelos.proveedor import Proveedor, RubroProveedor
from modelos.producto import Producto, CategoriaProducto
from modelos.orden import Orden, OrdenCompra, OrdenVenta, EstadoOrden

class GestorSistema:
    def __init__(self):
        self.__productos = []
        self.__personas = []  # Contiene tanto Clientes como Proveedores
        self.__ordenes = []
        self.__contador_ordenes = 0  

    @property
    def productos(self):
        return self.__productos

    @property
    def personas(self):
        return self.__personas

    @property
    def ordenes(self):
        return self.__ordenes

    # --- Gestión de Productos ---
    def registrar_producto(self, codigo: str, nombre: str, descripcion: str, precio: float, stock: int, categoria_str: str) -> Producto:
        for prod in self.__productos:
            if prod.id_producto == codigo:
                raise ValueError(f"Error: Ya existe un producto con el código '{codigo}'.")
        
        try:
            categoria = CategoriaProducto[categoria_str.upper()]
        except KeyError:
            raise ValueError("Categoría inválida.")

        nuevo_prod = Producto(codigo, nombre, descripcion, precio, stock, categoria)
        self.__productos.append(nuevo_prod)
        return nuevo_prod

    def buscar_producto(self, codigo: str) -> Producto:
        for prod in self.__productos:
            if prod.id_producto == codigo:
                return prod
        raise ValueError(f"Error: El producto '{codigo}' no existe.")

    # --- Gestión de Clientes y Proveedores ---
    def registrar_cliente(self, identificacion: str, nombre: str, email: str, telefono: str, direccion: str) -> Cliente:
        for pers in self.__personas:
            if isinstance(pers, Cliente) and pers.id_cliente == identificacion:
                raise ValueError("Error: Ya existe un cliente con esa identificación.")
        
        nuevo_cli = Cliente(identificacion, nombre, email, telefono, direccion)
        self.__personas.append(nuevo_cli)
        return nuevo_cli

    def registrar_proveedor(self, identificacion: str, cuit: str, razon_social: str, email: str, telefono: str, direccion: str, rubro_str: str) -> Proveedor:
        for pers in self.__personas:
            if isinstance(pers, Proveedor) and pers.id_proveedor == identificacion:
                raise ValueError("Error: Ya existe un proveedor con esa identificación.")
        
        try:
            rubro = RubroProveedor[rubro_str.upper()]
        except KeyError:
            raise ValueError("Rubro inválido de proveedor.")

        nuevo_prov = Proveedor(identificacion, cuit, razon_social, email, telefono, direccion, rubro)
        self.__personas.append(nuevo_prov)
        return nuevo_prov

    def buscar_persona(self, identificacion: str):
        for pers in self.__personas:
            if isinstance(pers, Cliente) and pers.id_cliente == identificacion:
                return pers
            if isinstance(pers, Proveedor) and pers.id_proveedor == identificacion:
                return pers
        raise ValueError(f"La persona con ID '{identificacion}' no existe.")

    # --- Gestión de Órdenes Comerciales ---
    def crear_orden_compra(self, id_proveedor: str, fecha: str) -> OrdenCompra:
        persona = self.buscar_persona(id_proveedor)
        if not isinstance(persona, Proveedor):
            raise ValueError("Error: La identificación no pertenece a un Proveedor.")
        
        self.__contador_ordenes += 1
        nueva_orden = OrdenCompra(self.__contador_ordenes, fecha, persona)
        self.__ordenes.append(nueva_orden)
        return nueva_orden

    def crear_orden_venta(self, id_cliente: str, fecha: str) -> OrdenVenta:
        persona = self.buscar_persona(id_cliente)
        if not isinstance(persona, Cliente):
            raise ValueError("Error: La identificación no pertenece a un Cliente.")
        
        self.__contador_ordenes += 1
        nueva_orden = OrdenVenta(self.__contador_ordenes, fecha, persona)
        self.__ordenes.append(nueva_orden)
        return nueva_orden

    def buscar_orden(self, nro_orden: int) -> Orden:
        for orden in self.__ordenes:
            if int(orden.id_orden) == int(nro_orden):
                return orden
        raise ValueError(f"Error: La orden N° {nro_orden} no existe.")

    # --- Estadísticas del Sistema ---
    def obtener_estadisticas(self) -> dict:
        clientes = [p for p in self.__personas if isinstance(p, Cliente)]
        proveedores = [p for p in self.__personas if isinstance(p, Proveedor)]
        
        activas = [o for o in self.__ordenes if o.estado == EstadoOrden.EN_PROCESO]
        pendientes = [o for o in self.__ordenes if o.estado == EstadoOrden.PENDIENTE]
        finalizadas = [o for o in self.__ordenes if o.estado == EstadoOrden.COMPLETADA]
        
        orden_mayor = max(self.__ordenes, key=lambda o: o.calcular_total(), default=None)
        orden_menor = min(self.__ordenes, key=lambda o: o.calcular_total(), default=None)

        stats = {
            "total_productos": len(self.__productos),
            "total_clientes": len(clientes),
            "total_proveedores": len(proveedores),
            "ordenes_pendientes": len(pendientes),
            "ordenes_activas": len(activas),
            "ordenes_finalizadas": len(finalizadas),
            "orden_mayor_volumen": f"Orden N° {orden_mayor.id_orden} (${orden_mayor.calcular_total():.2f})" if orden_mayor else "N/A",
            "orden_menor_volumen": f"Orden N° {orden_menor.id_orden} (${orden_menor.calcular_total():.2f})" if orden_menor else "N/A",
        }
        return stats