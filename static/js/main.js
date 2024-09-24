function visualizarFoto(event) {
    const file = event.target.files[0];  // Obtener el archivo seleccionado
    if (file) {
        const reader = new FileReader();  // Crear un lector de archivos
        reader.onload = function(e) {
            const preview = document.querySelector('#imagenProducto');  // Seleccionar la imagen por su id que está en el HTML de AgregarProducto
            preview.src = e.target.result;  // Asignar la URL de la imagen
        };
        reader.readAsDataURL(file);  // Leer el archivo como URL de datos
    }
}
// Escuchador de eventos
document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.querySelector('#fileFoto');
    fileInput.addEventListener('change', visualizarFoto);
});