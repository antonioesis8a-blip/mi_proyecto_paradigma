# modelos/proveedor.py
import re
from enum import Enum

class RubroProveedor(Enum):
    ELECTRONICA = "Electrónica"
    ALIMENTOS = "Alimentos"
    ROPA = "Ropa"
    HOGAR = "Hogar"
    INDUMENTARIA = "Indumentaria"
    INFORMATICA = "Informática"

class Proveedor:
    def __init__(self, id_proveedor, cuit_proveedor, razon_social, email_proveedor, telefono, direccion, rubro):        
        self.id_proveedor = id_proveedor
        self.cuit_proveedor = cuit_proveedor
        self.razon_social = razon_social
        self.email_proveedor = email_proveedor
        self.telefono = telefono
        self.direccion = direccion
        self.rubro = rubro
    
    @property
    def id_proveedor(self) -> str:
        return self.__id_proveedor
    
    @id_proveedor.setter
    def id_proveedor(self, valor_proveedor):
        if not valor_proveedor or not isinstance(valor_proveedor, str):
            raise ValueError("El id del proveedor debe ser una cadena de texto no vacía")
        self.__id_proveedor = valor_proveedor
    
    @property
    def cuit_proveedor(self) -> str:
        return self.__cuit_proveedor

    @cuit_proveedor.setter
    def cuit_proveedor(self, valor_cuit):
        patron_cuit = r"^\d{2}-\d{8}-\d{1}$"
        if not valor_cuit or not re.fullmatch(patron_cuit, valor_cuit):
            raise ValueError("El CUIT del proveedor debe tener el formato XX-XXXXXXXX-X")
        self.__cuit_proveedor = valor_cuit
    
    @property
    def razon_social(self) -> str:
        return self.__razon_social
    
    @razon_social.setter
    def razon_social(self, valor_razon):
        if not valor_razon or len(valor_razon.strip()) < 2:
            raise ValueError("La razón social del proveedor debe tener al menos 2 caracteres")
        self.__razon_social = valor_razon.strip()
    
    @property
    def email_proveedor(self) -> str:
        return self.__email_proveedor
    
    @email_proveedor.setter
    def email_proveedor(self, valor_email):
        patron_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not valor_email or not re.fullmatch(patron_email, valor_email):
            raise ValueError("El email del proveedor debe ser una dirección válida")
        self.__email_proveedor = valor_email
    
    @property
    def telefono(self) -> str:
        return self.__telefono
    
    @telefono.setter
    def telefono(self, valor_telefono):
        patron_telefono = r"^\+?\d{10,15}$"
        if not valor_telefono or not re.fullmatch(patron_telefono, valor_telefono):
            raise ValueError("El teléfono del proveedor debe tener entre 10 y 15 dígitos.")
        self.__telefono = valor_telefono
    
    @property
    def direccion(self) -> str:
        return self.__direccion
    
    @direccion.setter
    def direccion(self, valor_direccion):
        if not valor_direccion or len(valor_direccion.strip()) < 5:
            raise ValueError("La dirección del proveedor debe tener al menos 5 caracteres")
        self.__direccion = valor_direccion.strip()
    
    @property
    def rubro(self) -> RubroProveedor:
        return self.__rubro
    
    @rubro.setter
    def rubro(self, valor_rubro: RubroProveedor):
        if not isinstance(valor_rubro, RubroProveedor):
            raise ValueError("Rubro inválido.")
        self.__rubro = valor_rubro
    
    def __str__(self):
        return f"[Proveedor] ID: {self.id_proveedor} | Razón Social: {self.razon_social} | Rubro: {self.rubro.value}"