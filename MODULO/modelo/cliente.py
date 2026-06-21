# modelos/cliente.py
import re
from MODULO.interfaz.constantes import PATRON_TELEFONO, PATRON_EMAIL



class Cliente:
    """Clase que representa a un cliente en el sistema de gestión de ventas."""
    def __init__(self, id_cliente, nombre, email, telefono, direccion):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
    
    @property
    def id_cliente(self) -> str:
        """Obtiene el ID del cliente."""
        return self.__id_cliente
    
    @id_cliente.setter
    def id_cliente(self, valor_cliente):
        if not valor_cliente or not isinstance(valor_cliente, str):
            raise ValueError("El id del cliente debe ser una cadena de texto no vacía")
        self.__id_cliente = valor_cliente
    
    @property
    def nombre(self) -> str:
        """Obtiene el nombre del cliente."""
        return self.__nombre
    
    @nombre.setter
    def nombre(self, valor_nombre):
        if not valor_nombre or len(valor_nombre.strip()) < 3:
            raise ValueError("El nombre del cliente debe tener al menos 3 caracteres")
        self.__nombre = valor_nombre.strip()
    
    @property
    def email(self) -> str:
        """Obtiene el email del cliente."""
        return self.__email
    
    @email.setter
    def email(self, valor_email):        
        if not valor_email or not re.fullmatch(PATRON_EMAIL, valor_email):
            raise ValueError("El email del cliente debe ser una dirección de correo electrónico válida")
        self.__email = valor_email    
        
    @property
    def telefono(self) -> str:
        """Obtiene el teléfono del cliente."""
        return self.__telefono
    
    @telefono.setter
    def telefono(self, valor_telefono):        
        if not valor_telefono or not re.fullmatch(PATRON_TELEFONO, valor_telefono):
            raise ValueError("El teléfono del cliente debe tener al menos 10 dígitos.")
        self.__telefono = valor_telefono
    
    @property
    def direccion(self) -> str:
        """Obtiene la dirección del cliente."""
        return self.__direccion
    
    @direccion.setter
    def direccion(self, valor_direccion):
        if not valor_direccion or len(valor_direccion.strip()) < 5:
            raise ValueError("La dirección del cliente debe tener al menos 5 caracteres")
        self.__direccion = valor_direccion.strip()
    
    def __str__(self) -> str:
        return f"[Cliente] ID: {self.id_cliente} | Nombre: {self.nombre} | Email: {self.email} | Teléfono: {self.telefono} | Dirección: {self.direccion}"
    
    def __repr__(self) -> str:
        return f"Cliente(id_cliente='{self.id_cliente}', nombre='{self.nombre}', email='{self.email}', telefono='{self.telefono}', direccion='{self.direccion}')"