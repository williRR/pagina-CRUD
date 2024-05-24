let minusBtn = document.getElementById('minus');
let plusBtn = document.getElementById('plus');
let cantidadInput = document.getElementById('cantidad');
let cantidad = 1;

console.log('El archivo JavaScript se ha cargado correctamente.');

function plus() {
    cantidad += 1;
    cantidadInput.value = cantidad;
}

 