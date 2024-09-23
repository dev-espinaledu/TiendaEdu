from appWeb import app, usuarios
from flask import render_template, request, redirect, session
import yagmail
import threading

# Ruta para el login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("frmLogin.html")
    else:
        # Obtener los datos del formulario
        username = request.form['username']
        password = request.form['txtPassword']
        # Crear diccionario con las credenciales ingresadas
        usuario = {
            "username": username,
            "password": password
        }
        # Verificar si el usuario existe en la base de datos
        userExiste = usuarios.find_one(usuario)
        if userExiste:
            # Si el usuario existe, crear una sesión
            session['user'] = usuario
            # Configurar el envío de correo con yagmail
            email = yagmail.SMTP("espinalsolarte7@gmail.com", open(".password", "r", encoding="UTF-8").read())
            # Crear asunto y mensaje
            asunto = "Reporte ingreso al sistema de usuario"
            mensaje = f"Se informa que el usuario {username} ha ingresado al sistema"
            destinatario = "espinalsolarte7@gmail.com"  # Direccion de correo válida
            # Iniciar un hilo para enviar el correo de forma asíncrona
            thread = threading.Thread(target=enviarCorreo, args=(email, destinatario, asunto, mensaje))
            thread.start()
            # Redirigir a la lista de productos
            return redirect('/listarProductos')
        else:
            # Si las credenciales no son válidas, mostrar un mensaje de error
            mensaje = "Credenciales de ingreso no válidas"
            return render_template("frmLogin.html", mensaje=mensaje)

# Ruta para cerrar la sesión
@app.route("/salir")
def salir():
    # Eliminar la variable de sesión 'user'
    session.pop('user', None)
    session.clear()  # Limpiar todas las variables de sesión
    # Redirigir al formulario de login con mensaje de confirmación
    return render_template("frmLogin.html", mensaje="Ha cerrado la sesión")

# Función para enviar correo electrónico
def enviarCorreo(email, destinatario, asunto, mensaje):
    email.send(to=destinatario, subject=asunto, contents=mensaje)