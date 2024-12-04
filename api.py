from Common import *
from flask import Flask, request, jsonify

controller = Controller()

user1 = Usuario("Juan","jperez")
user2 = Usuario("Maria","mmcraft")
user3 = Usuario("Gilberto","filihuili2000")


user1.agregarContacto("mmcraft","Maria")

user2.agregarContacto("jperez","Juan")
user2.agregarContacto("filihuili2000","Gilberto")

user3.agregarContacto("jperez","Juan")

controller.dataHandler.usuarios = [
    user1,user2,user3
]



app = Flask(__name__)

@app.route('/mensajeria/contactos', methods=['GET'])
def getcontactos():
    mialias = request.args.get('mialias', 'default')

    response = ""

    for i in controller.list_contactos(mialias):
        # el contacto no guarda su nombre...
        response += f"{i.alias} "

    return response, 200

@app.route('/mensajeria/contactos', methods=['GET'])
def getmensajes():
    mialias = request.args.get('mialias', 'default')

    response = ""

    for i in controller.getMensajes():
        # el contacto no guarda su nombre...
        response += i.prettyString() + "\n"

    return response, 200

@app.route('/mensajeria/enviar', methods=['POST'])
def sendmsg():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    sender_alias = data["usuario"]
    sendee_alias = data["contacto"]
    contents = data["mensaje"]
    
    controller.enviarMensaje(sender_alias,sendee_alias,contents)

    response = {

    }
    return jsonify(response), 200

@app.route('/mensajeria/contactos/<string:alias>', methods=['POST'])
def addcontacto(alias):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    contacto_alias = data["contacto"]
    contacto_nombre = data["nombre"]

    
    controller.add_contactos(alias,contacto_alias,contacto_nombre)

    response = {

    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
