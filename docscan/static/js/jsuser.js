const $txta = document.querySelector('textarea.textarea')
if ($txta) $txta.rows = 2

const MAX_FILE_SIZE = 30000000; // 1MB = 1 millón de bytes
const $fileInput = document.querySelector("#id_fileupload");
const $btnSubmit = document.querySelector("#submit-id-submit");

if($fileInput) {
    $fileInput.addEventListener("change", function () {

        if (this.files.length <= 0) return;

        const fileUpload = this.files[0];
        if (fileUpload.size > MAX_FILE_SIZE) {
            const sizeMB = MAX_FILE_SIZE / 1000000;
    
            $alert = `
                        <div class="alert alert-danger py-2 d-flex alert-hide" role="alert">
                            <div class="mx-auto">
                                Tamaño máximo permitido: <strong>${sizeMB}MB</strong>
                            </div>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    `
            $btnSubmit.insertAdjacentHTML('beforebegin',$alert)
            $fileInput.value = "";
        } 

        arrFileName = this.files[0].name.split('.')
        if (arrFileName[arrFileName.length - 1] !== 'pdf') {

            $alert = `
                        <div class="alert alert-danger py-2 d-flex alert-hide" role="alert">
                            <div class="mx-auto">
                                El documento '${arrFileName[arrFileName.length - 1]}' no es <strong>PDF</strong>
                            </div>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    `
            $btnSubmit.insertAdjacentHTML('beforebegin',$alert)

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

window.setTimeout(function() {
    $alert = document.querySelector(".alert-hide")
    if ($alert) $alert.classList.add('d-none')
}, 3000);