let minusBtn = document.getElementById('minus');
  let plusBtn = document.getElementById('plus');
  let cantidadInput = document.getElementById('cantidad');
  let cantidad = 1;


  function plus() {
    cantidad+= 1;
    cantidadInput.value = cantidad;
  }

  function minus() {
    if (cantidad > 1) {
      cantidad -= 1;
      cantidadInput.value = cantidad;
    }
  }

  minusBtn.addEventListener('click', minus);
  plusBtn.addEventListener('click', plus);

  
  var link = document.getElementById('linkToOtherPage');
  link.href = "/otra_pagina.html?cantidad=" + cantidad;

  let alertMsg = document.getElementById('eliminar');

  function eliminar() {
    var confirmacion = confirm("¿Estás seguro de que quieres eliminar este producto?");
    if (confirmacion) {
        // Aquí va el código para eliminar el producto si el usuario confirma
    } else {
        // Aquí va el código para cancelar la eliminación si el usuario no confirma
        event.preventDefault();
    }
}