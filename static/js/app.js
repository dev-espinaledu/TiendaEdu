// Asegúrate de tener SweetAlert2 disponible en tu proyecto.
import Swal from 'sweetalert2';

// Para asegurar que las funciones se usen en un entorno sin módulos
window.visualizarFoto = visualizarFoto;
window.visualizarModalEliminar = visualizarModalEliminar;

/**
 * función que responde al evento
 * change del campo fileFoto y muestra
 * la foto seleccionada en un elemento de tipo
 * image del formulario llamado imagenProducto
 * @param {*} evento
 */
function visualizarFoto(evento) {
    const $fileFoto = document.querySelector('#fileFoto');
    const $imagenPrevisualizacion = document.querySelector("#imagenProducto");

    const files = evento.target.files;
    const archivo = files[0];
    let filename = archivo.name;
    let extension = filename.split('.').pop();
    extension = extension.toLowerCase();

    if (extension !== "jpg" && extension !== "jpeg" && extension !== "png") {
        $fileFoto.value = "";
        // Usando SweetAlert para mostrar el mensaje de error
        Swal.fire("Formato incorrecto", "La imagen debe ser en formato JPG, JPEG o PNG", "error");
    } else {
        const objectURL = URL.createObjectURL(archivo);
        $imagenPrevisualizacion.src = objectURL;
    }
}

function visualizarModalEliminar(id) {
    Swal.fire({
        title: "¿Estás seguro de eliminar?",
        showDenyButton: true,
        confirmButtonText: "Sí",
        denyButtonText: "No"
    }).then((result) => {
        if (result.isConfirmed) {
            location.href = '/eliminar/' + id;
        }
    });
}

// Enlazando el evento 'change' para que funcione correctamente
document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.querySelector('#fileFoto');
    fileInput.addEventListener('change', visualizarFoto);
});

module.exports = {visualizarFoto, visualizarModalEliminar}