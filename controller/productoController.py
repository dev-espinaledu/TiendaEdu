from appWeb import app, productos
from flask import request, jsonify, redirect, render_template, session
import pymongo
import os
import pymongo.errors
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import json

@app.route("/listarProductos")
def inicio():
    if "user" in session:  # Verifica si el usuario ha iniciado sesión
        try:
            mensaje = ""
            # Obtener todos los productos de la colección
            listaProductos = productos.find()
        except pymongo.errors as error:
            mensaje = str(error)
            
        return render_template("listarProductos.html", productos=listaProductos, mensaje=mensaje)
    else:
        mensaje = "Debe primero ingresar con sus credenciales"
        return render_template("frmLogin.html", mensaje=mensaje)

@app.route("/agregar", methods=['POST', 'GET'])
def agregar():
    if "user" in session:
        if request.method == 'POST':
            try:
                producto = None
                codigo = int(request.form['txtCodigo'])          
                nombre = request.form['txtNombre']
                precio = int(request.form['txtPrecio'])
                categoria = request.form['cbCategoria']
                foto = request.files['fileFoto']
                nombreArchivo = secure_filename(foto.filename)
                listaNombreArchivo = nombreArchivo.rsplit(".", 1)
                extension = listaNombreArchivo[1].lower()
                # Crear nombre de la foto utilizando el código del producto
                nombreFoto = f"{codigo}.{extension}"        
                producto = {
                    "codigo": codigo, "nombre": nombre, "precio": precio, 
                    "categoria": categoria, "foto": nombreFoto
                }
                # Verificar si el producto ya existe por su código
                existe = existeProducto(codigo)
                if not existe:
                    resultado = productos.insert_one(producto)
                    if resultado.acknowledged:
                        mensaje = "Producto Agregado Correctamente"
                        # Guardar la foto del producto en la ruta
                        foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))
                        return redirect('/listarProductos')
                    else:
                        mensaje = "Problemas al agregar el producto."
                else:
                    mensaje = "Ya existe un producto con ese código"
            except pymongo.errors as error:
                mensaje = str(error)
            return render_template("frmAgregarProducto.html", mensaje=mensaje, producto=producto)
        else:  # Si el método es GET, mostrar el formulario vacío
            return render_template("frmAgregarProducto.html", producto=None)
    else:
        mensaje = "Debe primero ingresar con sus credenciales"
        return render_template("frmLogin.html", mensaje=mensaje)

@app.route("/consultar/<string:id>", methods=["GET"])
def consultar(id):
    if "user" in session:
        if request.method == 'GET':
            try:
                id = ObjectId(id)
                consulta = {"_id": id}
                producto = productos.find_one(consulta)
                return render_template("frmActualizarProducto.html", producto=producto)
            except pymongo.errors as error:
                mensaje = str(error)
                return redirect("/listarProductos")
    else:
        mensaje = "Debe primero ingresar con sus credenciales"
        return render_template("frmLogin.html", mensaje=mensaje)

def existeProducto(codigo):
    try:
        consulta = {"codigo": codigo}
        producto = productos.find_one(consulta)
        return producto is not None
    except pymongo.errors as error:
        print(error)
        return False

@app.route("/actualizar", methods=["POST"])
def actualizarProducto():
    if "user" in session:
        try:
            if request.method == "POST":
                # Recibir los datos del formulario
                codigo = int(request.form["txtCodigo"])
                nombre = request.form["txtNombre"]
                precio = int(request.form["txtPrecio"])
                categoria = request.form["cbCategoria"]
                id = ObjectId(request.form["id"])
                foto = request.files["fileFoto"]
                # Si se ha subido una nueva foto
                if foto.filename != "":
                    nombreArchivo = secure_filename(foto.filename)
                    listaNombreArchivo = nombreArchivo.rsplit(".", 1)
                    extension = listaNombreArchivo[1].lower()
                    nombreFoto = f"{codigo}.{extension}"
                    producto = {
                        "_id": id, "codigo": codigo, "nombre": nombre,
                        "precio": precio, "categoria": categoria, "foto": nombreFoto
                    }
                else:
                    # Si no se sube una nueva foto, mantener la actual
                    producto = {
                        "_id": id, "codigo": codigo, "nombre": nombre,
                        "precio": precio, "categoria": categoria
                    }
                criterio = {"_id": id}
                consulta = {"$set": producto}
                # Verificar si el nuevo código ya existe para otro producto
                existe = productos.find_one({"codigo": codigo, "_id": {"$ne": id}})
                if existe:
                    mensaje = "Producto ya existe con ese código"
                    return render_template("frmActualizarProducto.html", producto=producto, mensaje=mensaje)
                else:
                    resultado = productos.update_one(criterio, consulta)
                    if resultado.acknowledged:
                        mensaje = "Producto Actualizado"
                        # Guardar la nueva foto si se subió
                        if foto.filename != "":
                            foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))
                        return redirect("/listarProductos")
        except pymongo.errors as error:
            mensaje = str(error)
            return redirect("/listarProductos")
    else:
        mensaje = "Debe primero ingresar con sus credenciales"
        return render_template("frmLogin.html", mensaje=mensaje)

@app.route("/eliminar/<string:id>")
def eliminar(id):
    if "user" in session:
        try:
            id = ObjectId(id)
            criterio = {"_id": id}
            producto = productos.find_one(criterio)
            nombreFoto = producto['foto']
            resultado = productos.delete_one(criterio)
            if resultado.acknowledged:
                mensaje = "Producto Eliminado"
                # Eliminar la foto del servidor si existe
                if nombreFoto:
                    rutaFoto = os.path.join(app.config['UPLOAD_FOLDER'], nombreFoto)
                    if os.path.exists(rutaFoto):
                        os.remove(rutaFoto)
        except pymongo.errors as error:
            mensaje = str(error)
        return redirect("/listarProductos")
    else:
        mensaje = "Debe primero ingresar con sus credenciales"
        return render_template("frmLogin.html", mensaje=mensaje)