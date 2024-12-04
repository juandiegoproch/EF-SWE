from typing import List
from datetime import datetime

class Contacto:
    def __init__(self, alias: str, fecharegistro: datetime):
        self.alias: str = alias
        self.fecha: datetime = fecharegistro

class Mensaje:
    def __init__(self, envia: Contacto, recibe: Contacto, mensaje: str, fecha: datetime):
        self.usuarioRemitente: Contacto = envia
        self.usuarioDestinatario: Contacto = recibe
        self.mensaje: str = mensaje
        self.fechaEnvio: datetime = fecha
    
    def prettyString(self):
        f"{self.usuarioRemitente.alias} te escribió '{self.mensaje}' el {self.fechaEnvio.strftime('%d/%m/%Y')}"

class Usuario:
    def __init__(self, nombre: str, alias: str):
        self.nombre: str = nombre
        self.alias: str = alias

        self.contactos: List[Contacto] = []
        self.mensajesEnviados: List[Mensaje] = []
        self.mensajesRecibidos: List[Mensaje] = []
    
    def agregarContacto(self,alias,nombre):
        self.contactos.append(Contacto(alias,datetime.now()))
    
    def enviarMensaje(self,contactoDestinatario,contenido,momento):
        mensaje = Mensaje(Contacto(self.alias,datetime.now()),
                            contactoDestinatario,contenido,momento)
        self.mensajesEnviados.append(mensaje)
        return mensaje # se usa para que el datahandler lo envie!
    
    def verHistorialMensajes(self):
        return self.mensajesRecibidos
class DataHandler:
    def __init__(self):
        self.usuarios: List[Usuario] = []

class Controller:
    def __init__(self):
        # Este datahandler cumplira la funcion de BD
        self.dataHandler = DataHandler()
    
    def list_contactos(self,alias):
        for i in self.dataHandler.usuarios:
            if i.alias == alias:
                return i.contactos
    def add_contactos(self,alias,contactoAlias,contactoNombre):
        exists = False
        for i in self.dataHandler.usuarios:
            if i.alias == contactoAlias:
                exists = True
                break
        if (not exists):
            self.dataHandler.usuarios.append(Usuario(contactoNombre,contactoAlias))
        for i in self.dataHandler.usuarios:
            if i.alias == alias:
                i.contactos.append(Contacto(contactoAlias,datetime.now()))
                return
        raise Exception("El usuario no existe")
        
    def enviarMensaje(self,aliasremitente,aliasDestinatario,contenido):
        mensaje = None
        for i in self.dataHandler.usuarios:
            if i.alias == aliasremitente:
                destinatario = None
                for cont in i.contactos:
                    if cont.alias == aliasDestinatario:
                        destinatario = cont
                if destinatario == None:
                    raise Exception("El usuario destinatario no es tu contacto")
                mensaje = i.enviarMensaje(destinatario,contenido,datetime.now())
        if mensaje is None:
            raise Exception("El usuario remitente no existe")
        for i in self.dataHandler.usuarios:
            if i.alias == aliasDestinatario:
                i.mensajesRecibidos.append(mensaje)
        
    def getMensajes(self,alias):
        for i in self.dataHandler.usuarios:
            if i.alias == alias:
                return i.verHistorialMensajes()
        raise Exception("El usuario no existe")