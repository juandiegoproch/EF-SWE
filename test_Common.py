import unittest
from unittest.mock import patch, mock_open
from io import StringIO

import unittest
from datetime import datetime
from Common import *


class TestController(unittest.TestCase):

    def setUp(self):
        """Setup for each test case."""
        self.controller = Controller()
        self.controller.dataHandler.usuarios.append(Usuario("Alicia", "alicea24"))
        self.controller.dataHandler.usuarios.append(Usuario("Gustavo", "gustagustavogustitos"))

    def test_list_contactos(self):
        """Test listing contacts for a user."""
        self.controller.add_contactos("alicea24", "gustagustavogustitos", "Gus")
        contactos = self.controller.list_contactos("alicea24")
        self.assertEqual(len(contactos), 1)
        self.assertEqual(contactos[0].alias, "gustagustavogustitos")

    def test_add_contactos(self):
        """Test adding a contact."""
        self.controller.add_contactos("alicea24", "charlie789", "Charlie")
        contactos = self.controller.list_contactos("alicea24")
        self.assertEqual(len(contactos), 1)
        self.assertEqual(contactos[0].alias, "charlie789")

        usuario = next((u for u in self.controller.dataHandler.usuarios if u.alias == "charlie789"), None)
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre, "Charlie")

    def test_enviarMensaje(self):
        self.controller.add_contactos("alicea24", "gustagustavogustitos", "Gus")
        self.controller.enviarMensaje("alicea24", "gustagustavogustitos", "Hello Gus!")

        alice = next(u for u in self.controller.dataHandler.usuarios if u.alias == "alicea24")
        self.assertEqual(len(alice.mensajesEnviados), 1)
        self.assertEqual(alice.mensajesEnviados[0].mensaje, "Hello Gus!")

        bob = next(u for u in self.controller.dataHandler.usuarios if u.alias == "gustagustavogustitos")
        self.assertEqual(len(bob.mensajesRecibidos), 1)
        self.assertEqual(bob.mensajesRecibidos[0].mensaje, "Hello Gus!")

    def test_getMensajes(self):
        """Test retrieving received messages."""
        self.controller.add_contactos("alicea24", "gustagustavogustitos", "Gus")
        self.controller.enviarMensaje("alicea24", "gustagustavogustitos", "Hello Gus!")

        mensajes = self.controller.getMensajes("gustagustavogustitos")
        self.assertEqual(len(mensajes), 1)
        self.assertEqual(mensajes[0].mensaje, "Hello Gus!")

    def test_enviarMensaje_no_contact(self):
        """Test sending a message to a non-contact."""
        with self.assertRaises(Exception) as context:
            self.controller.enviarMensaje("alicea24", "nonexistent", "Hello!")
        self.assertEqual(str(context.exception), "El usuario destinatario no es tu contacto")

    def test_getMensajes_no_user(self):
        """Test retrieving messages for a nonexistent user."""
        with self.assertRaises(Exception) as context:
            self.controller.getMensajes("nonexistent")
        self.assertEqual(str(context.exception), "El usuario no existe")

    def test_add_contacto_no_existe(self):
        with self.assertRaises(Exception) as context:
            self.controller.add_contactos("nonexistent","noimporta","Noimporta")
        self.assertEqual(str(context.exception), "El usuario no existe")

if __name__ == '__main__':
    unittest.main()
