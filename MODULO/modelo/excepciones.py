# modelo/excepciones.py

class GestionError(Exception):
    """Clase base para todas las excepciones del sistema de gestión."""
    pass

class ValidationError(GestionError, ValueError):
    """Lanzada cuando un formato, tipo de dato o restricción de longitud falla.
    Hereda también de ValueError para mantener compatibilidad hacia atrás."""
    pass

class StockInsuficienteError(GestionError):
    """Lanzada cuando una orden de venta intenta retirar más stock del disponible."""
    pass

class EstadoInvalidoError(GestionError):
    """Lanzada cuando se intenta realizar una transición de estado no permitida 
    (ej. finalizar una orden ya completada o cancelada)."""
    pass

class EntidadDuplicadaError(GestionError):
    """Lanzada cuando se intenta registrar un producto, cliente o proveedor con un ID ya existente."""
    pass    