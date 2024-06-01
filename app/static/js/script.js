document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;

    if (name && email && subject && message) {
        if (subject !== "") {
            alert('El formulario ha sido enviado con éxito.');
            // Aquí podrías agregar la lógica para enviar los datos a un servidor.
        } else {
            alert('Por favor, seleccione un asunto.');
        }
    }
});
