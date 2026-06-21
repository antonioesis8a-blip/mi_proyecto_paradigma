# constantes.py

OPCIONES_MENU = {
    "1": "Registrar Producto",
    "2": "Registrar Cliente o Proveedor",
    "3": "Crear Órden de Compra",
    "4": "Crear Órden de Venta",
    "5": "Asociar Producto a Órden",
    "6": "Modificar Estado de Órden",
    "7": "Consultar Operaciones Registradas",
    "8": "Mostrar Estadísticas Generales",
    "9": "Listar Productos y Actores registrados",
    "10": "Finalizar Programa"
}

MSG_BIENVENIDA = "=== BIENVENIDO AL SISTEMA DE CONTROL DE ÓRDENES ==="
MSG_DESPEDIDA = "¡Gracias por usar el sistema! Finalizando ejecución..."


# EXPRESIONES REGULARES CENTRALIZADAS

PATRON_PRODUCTO_ID = r"^PROD-\d{4}$"
PATRON_TELEFONO = r"^\+?\d{10,15}$"
PATRON_EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
PATRON_CUIT = r"^\d{2}-\d{8}-\d{1}$" # Formato clásico XX-XXXXXXXX-X