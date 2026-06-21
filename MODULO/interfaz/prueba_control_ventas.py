# interfaz/prueba_control_ventas
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controladores.controlador import GestorSistema
from constantes import OPCIONES_MENU, MSG_BIENVENIDA, MSG_DESPEDIDA
from modelo.orden import EstadoOrden
from modelo.orden import ItemOrden
from modelo.excepciones import (
    GestionError,
    ValidationError,
    StockInsuficienteError,
    EstadoInvalidoError,
    EntidadDuplicadaError
)

class VistaConsola:
    def __init__(self):
        self.controlador = GestorSistema()

    def ejecutar(self):
        """Ejecuta el bucle principal de la interfaz de consola, mostrando el menú y procesando las opciones seleccionadas por el usuario."""
        print(MSG_BIENVENIDA)
        while True:
            print("\n" + "="*40)
            print("             MENÚ PRINCIPAL")
            print("="*40)
            for clave, opcion in OPCIONES_MENU.items():
                print(f"{clave}. {opcion}")
            print("="*40)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "10":
                print(MSG_DESPEDIDA)
                break

            try:
                self.procesar_opcion(opcion)
            except ValidationError as e:
                print(f"\n[ERROR DE VALIDACIÓN] -> {e}")
            except StockInsuficienteError as e:
                print(f"\n[ERROR DE INVENTARIO] -> {e}")
            except EstadoInvalidoError as e:
                print(f"\n[ERROR ADMINISTRATIVO] -> {e}")
            except EntidadDuplicadaError as e:
                print(f"\n[ERROR DE DUPLICIDAD] -> {e}")
            except GestionError as e:
                print(f"\n[ERROR DE NEGOCIO] -> {e}")
            except ValueError as e:
                print(f"\n[ERROR DE DATO] -> {e}")
            except Exception as e:
                print(f"\n[ERROR INESPERADO] -> {e}")

    def procesar_opcion(self, opcion: str):
        """Procesa la opción seleccionada por el usuario, ejecutando la acción correspondiente en el sistema."""
        if opcion == "1":
            print("\n--- REGISTRAR PRODUCTO ---")
            codigo = input("Código (Format: PROD-XXXX): ")
            nombre = input("Nombre del producto: ")
            desc = input("Descripción: ")
            try:
                precio = float(input("Precio: "))
                stock = int(input("Stock inicial: "))
            except ValueError as exc:
                raise ValueError("El precio debe ser un número y el stock un número entero.") from exc
            print("Categorías válidas: ELECTRONICA, ALIMENTOS, ROPA, HOGAR, INDUMENTARIA, INFORMATICA")
            cat = input("Categoría: ")
            prod = self.controlador.registrar_producto(codigo, nombre, desc, precio, stock, cat)
            print(f"¡Éxito! Producto registrado: {prod}")

        elif opcion == "2":
            print("\n--- REGISTRAR ACTOR ---")
            print("1. Registrar Cliente\n2. Registrar Proveedor")
            tipo_actor = input("Seleccione (1/2): ")
            id_persona = input("Identificación única: ")
            nombre = input("Nombre / Razón Social: ")
            email = input("Correo electrónico: ")
            tel = input("Teléfono: ")
            dire = input("Dirección: ")
            
            if tipo_actor == "1":
                persona = self.controlador.registrar_cliente(id_persona, nombre, email, tel, dire)
            elif tipo_actor == "2":
                cuit = input("CUIT (Format: XX-XXXXXXXX-X): ")
                print("Rubros válidos: ELECTRONICA, ALIMENTOS, ROPA, HOGAR, INDUMENTARIA, INFORMATICA")
                rubro = input("Rubro: ")
                persona = self.controlador.registrar_proveedor(id_persona, cuit, nombre, email, tel, dire, rubro)
            else:
                raise ValueError("Opción de registro inválida.")
            print(f"¡Éxito! Registrado correctamente: {persona}")

        elif opcion == "3":
            print("\n--- CREAR ÓRDEN DE COMPRA ---")
            id_prov = input("Identificación del Proveedor: ")
            fecha = input("Fecha (DD/MM/AAAA): ")
            orden = self.controlador.crear_orden_compra(id_prov, fecha)
            print(f"¡Éxito! {orden}")

        elif opcion == "4":
            print("\n--- CREAR ÓRDEN DE VENTA ---")
            id_cli = input("Identificación del Cliente: ")
            fecha = input("Fecha (DD/MM/AAAA): ")
            orden = self.controlador.crear_orden_venta(id_cli, fecha)
            print(f"¡Éxito! {orden}")

        elif opcion == "5":
            print("\n--- ASOCIAR PRODUCTO A ÓRDEN ---")            
            nro_o = input("Número de la orden: ").strip()
            
            # Buscamos la orden en el controlador            
            orden = next((o for o in self.controlador.ordenes if o.id_orden == nro_o), None)
            if not orden:
                raise ValidationError(f"No se encontró ninguna orden con el número {nro_o}")
            
            cod_p = input("Código del producto (PROD-XXXX): ").strip()
            # Buscamos el producto
            producto = next((p for p in self.controlador.productos if p.id_producto == cod_p), None)
            if not producto:
                raise ValidationError(f"No se encontró ningún producto con el código {cod_p}")
            
            try:
                cant = int(input(f"Cantidad de '{producto.nombre_producto}': "))
            except ValueError as exc:
                raise ValidationError("La cantidad debe ser un número entero.") from exc
            
            # Creamos el ítem y lo agregamos a la orden
            nuevo_item = ItemOrden(producto, cant)
            orden.agregar_item(nuevo_item)
            
            print(f"¡Éxito! Producto asociado. Total actual de la orden: ${orden.calcular_total():.2f}")

        elif opcion == "6":
            print("\n--- MODIFICAR ESTADO DE LA ORDEN ---")

            try:
                nro_o = int(input("Número de la orden: "))
            except ValueError as exc:
                raise ValueError("El número de la orden debe ser un número entero.") from exc

            orden = self.controlador.buscar_orden(nro_o)

            print(f"Estado actual: {orden.estado.value}")
            print("1. EN PROCESO")
            print("2. COMPLETADA")
            print("3. CANCELADA")

            est_opc = input("Seleccione una opción: ")

            if est_opc == "1":
                orden.estado = EstadoOrden.EN_PROCESO
                print("Estado modificado correctamente.")

            elif est_opc == "2":
                orden.finalizar_orden()
                print("La orden fue completada correctamente.")

            elif est_opc == "3":
                orden.estado = EstadoOrden.CANCELADA
                print("La orden fue cancelada.")

            else:
                raise ValueError("La opción ingresada no es válida.")

        elif opcion == "7":
            print("\n--- CONSULTAR OPERACIONES ---")
            if not self.controlador.ordenes:
                print("No hay órdenes registradas en el sistema.")
            else:
                for o in self.controlador.ordenes:
                    print("\n" + "-"*60)
                    print(o)
                    print("--> HISTORIAL DE MOVIMIENTOS COMERCIALES:")
                    for mov in o.historial_movimientos:
                        print(f"    {mov}")
                print("-"*60)

        elif opcion == "8":
            print("\n--- ESTADÍSTICAS GENERALES ---")
            stats = self.controlador.obtener_estadisticas()
            for k, v in stats.items():
                print(f" * {k.replace('_', ' ').capitalize()}: {v}")

        elif opcion == "9":
            print("\n--- LISTAR ELEMENTOS DEL SISTEMA ---")
            print("\n>> PRODUCTOS:")
            if not self.controlador.productos:
                print("No hay productos registrados.")
            else:
                for p in self.controlador.productos:
                    print(p)
            print("\n>> ACTORES REGISTRADOS:")
            for pers in self.controlador.personas:
                print(pers)
        else:
            raise ValueError("La opción elegida no es válida.")

if __name__ == "__main__":
    vista = VistaConsola()
    vista.ejecutar()