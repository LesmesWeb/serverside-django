console.log("ingresa")

$(document).ready(() => {

    $('.tag-select').select2({
        dropdownAutoWidth: false,
        allowClear: true,
        ajax: {
        url: '/ingestion_medios/SearchTag/',
        processResults: function (data) {
            console.log(data);
            return {
            results: $.map(data, function (item, index) {
                return {
                text: item.name_tag,
                id: item.id
                }
            })
            };
        }
        }
    });



    $('.tema-select').select2({
        dropdownAutoWidth: false,
        allowClear: true,
        ajax: {
        url: '/ingestion_medios/SearchTema/',
        processResults: function (data) {
            console.log(data);
            return {
            results: $.map(data, function (item, index) {
                return {
                text: item.name_tema,
                id: item.id
                }
            })
            };
        }
        }
    });

    $('.pasivo-select').select2({
        dropdownAutoWidth: false,
        allowClear: true,
        ajax: {
        url: '/ingestion_medios/SearchPasiveActive/',
        processResults: function (data) {
            console.log(data);
            return {
            results: $.map(data, function (item, index) {
                return {
                text: item.name_autor,
                id: item.id
                }
            })
            };
        }
        }
    });


    $('.active-select').select2({
        dropdownAutoWidth: false,
        allowClear: true,
        ajax: {
        url: '/ingestion_medios/SearchPasiveActive/',
        processResults: function (data) {
            console.log(data);
            return {
            results: $.map(data, function (item, index) {
                return {
                text: item.name_autor,
                id: item.id
                }
            })
            };
        }
        }
    });
    });
    

    /**
     * Envia la categorización realizada por el usuario.
     * {objeto} dataFragment - capturta el objecto de la localStorage del fragmento. 
     * {form} form - Categorización de fragmento (Tag - Tema - Entidades)
     * 
     */
    function saveCategorization() {
    var dataFragment = localStorage.getItem('fragmentSelect'); //validacion de fragmento
    let tags = $(".tag-fragment-select").val()

    if (tags.length > 0) {

        var form = $('#form_categorization');
        var popDiv = document.getElementById('povDivform')
        popDiv.remove()
        localStorage.setItem('fragmentSelect', ""); //Limpiar la localStorage

        $.ajax({
        url: form.attr("action"),
        method: "POST",
        data: {
            form: form.serialize(),
            dataFragment: dataFragment,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        
        success: function (fragment_id) {
            //asigna el id del formulario al span
            spanAtive = document.getElementById("active-span" + spanActivo).firstChild.setAttribute('data-custom',fragment_id)


        },  
        error: function (xhr, errmsg, err) {
            console.log("Hay un error")
        }
        });

    } else {
        $(".tag-fragment-select").select2('open');
    }
    }

    function deleteCategorization() {
    console.log("Elimina")
    var id_fragment = document.getElementById("delete_form")
    
    id_fragment = id_fragment.dataset.idfragment  

    if (id_fragment.length > 0) {
        $.ajax({
        url: '/categorizacion_medios/delete_fragment/',
        method: "POST",
        data: {
            idFragment: id_fragment,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },

        success: function () {
            console.log("Entra al succes de eliminar")
            var event_delete = new CustomEvent("delete_span");
            let elem = document.querySelector("#delete_form");
            elem.dispatchEvent(event_delete);
        },
        error: function (xhr, errmsg, err) {
            console.log("Hay un error")
        }
        });
    } else {
        console.log("No se guardo el fragmento previamente")
    }


    }