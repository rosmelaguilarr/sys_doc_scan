// Redimensionar textarea del formulario RegisterDoc
const $txta = document.querySelector('textarea')
$txta.rows = 2


// Borrar asteriscos de (requerdio) del formulario RegisterDoc
const $asteriskAll = document.querySelectorAll('.asteriskField')
for (let i = 0; i < $asteriskAll.length; i++) {
    $asteriskAll[i].innerHTML = ''
}

// Mover boton Registrar dentro del formulario
const $formRegisterDoc=document.querySelector('.form-registerdoc'),
$btnRegisterDoc=document.querySelector('.btn-registerdoc');
$formRegisterDoc.append($btnRegisterDoc)

