// Redimensionar textarea del formulario RegisterDoc
const $txta = document.querySelector('textarea.textarea')
if ($txta) $txta.rows = 2

// Borrar asteriscos de (requerdio) del formulario RegisterDoc
const $asteriskAll = document.querySelectorAll('.asteriskField')
for (let i = 0; i < $asteriskAll.length; i++) {
    $asteriskAll[i].innerHTML = ''
}

// Mover boton Registrar dentro del formulario
const $formRegisterDoc=document.querySelector('.form-registerdoc'),
$btnRegisterDoc=document.querySelector('.btn-registerdoc');
if($btnRegisterDoc) $formRegisterDoc.append($btnRegisterDoc)

// Validar tamaño de PDF
const MAX_FILE_SIZE = 30000000; // 1MB = 1 millón de bytes

const $fileInput = document.querySelector("#id_fileupload");

if($fileInput) {
    $fileInput.addEventListener("change", function () {

        if (this.files.length <= 0) return;

        const fileUpload = this.files[0];
        if (fileUpload.size > MAX_FILE_SIZE) {
            const sizeMB = MAX_FILE_SIZE / 1000000;
    
            $alert = `
                        <div class="alert alert-danger alert-dismissible fade show" role="alert">
                            Tamaño máximo permitido: <strong>${sizeMB}MB</strong>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    `
            $btnRegisterDoc.insertAdjacentHTML('beforebegin',$alert)
            $fileInput.value = "";
        } 

        arrFileName = this.files[0].name.split('.')
        if (arrFileName[arrFileName.length - 1] !== 'pdf') {

            $alert = `
                        <div class="alert alert-danger alert-dismissible fade show" role="alert">
                            El documento '${arrFileName[arrFileName.length - 1]}' no es <strong>PDF</strong>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    `
            $btnRegisterDoc.insertAdjacentHTML('beforebegin',$alert)

            $fileInput.value = "";
        }

    });
}

(function () {
    const $btnDelete = document.querySelectorAll('.btn-delete') 
    $btnDelete.forEach(btn=> {
        btn.addEventListener( 'click', e =>{
            const confirmation = confirm('¿Está seguro de eliminar el documento ?')

            if(!confirmation) e.preventDefault()
        })
    })
}

)();

// Autoclose alert

window.setTimeout(function() {
    $alert = document.querySelector(".alert")
    if ($alert) $alert.classList.add('d-none')
}, 3000);