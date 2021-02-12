var $ = jQuery.noConflict();

/* ----------------------------------------
    funciones Reutilizables 
 ---------------------------------------- */
// está opción es para diseñar la tabla con ajax
function listadoReglas(){

    //$ (define que es una instancia jquery)
    // la ruta debe tener "/" al inicio para que busque a través del dominio
    $.ajax({
        url: "/stakeholders/reglas/",
        type:"get",
        dataType: "json",
        // que pasa si la petición es correcta, la función recibe la respuesta
        success: function(response){
            // Validamos que existe el data table con el proposito de que no genere error por el hecho que se repita, asi que se valida para quitar y volver a poner
            if($.fn.DataTable.isDataTable('#tabla_listar_reglas')){
                //si existe una instancia datatable con el id tabla detruir
                $('#tabla_listar_reglas').DataTable().destroy();
            }

            $('#tabla_listar_reglas tbody').html("");
            for (let i = 0; i < response.length; i++) {
                let fila = '<tr>';
                fila += '<td><input type="checkbox" class="input-chk check"></td>';
                fila += '<td>' + (i + 1) + '</td>';
                fila += '<td>' + response[i]["fields"]['actor'] + '</td>';
                fila += '<td>' + response[i]["fields"]['nombre'] + '</td>';
                fila += '<td>' + response[i]["fields"]['created_at'] + '</td>';
                fila += '<td>' + response[i]["fields"]['updated_at'] + '</td>';
                fila += '<td>';
                fila += '<div class="row">';
                fila += '<div class="col-6 col-xl-6 col-lg-6 col-sm-6 p-0 text-right">';
                fila += '<button onclick = "abrir_modal_edicion_regla(\'/stakeholders/editar_regla/' + response[i]['pk'] + '/\');"'
                fila += 'class="btn btn-info"><i class="fa fa-edit fa-1x"> </i> </button></div>';

                fila += '<div class="col-6 col-xl-6 col-lg-6 col-sm-6 pl-1 text-left">';
                fila += '<button onclick = "abrir_modal_eliminacion(\'/stakeholders/eliminar_regla/' + response[i]['pk'] + '/\');"'

                fila += 'class="btn btn-danger"><i class="feather icon-edit-2 fa-1x"> </i> </button></div>';

                fila += '</div></div>';
                fila += '</td>';
                fila += '</tr>';
                $('#tabla_listar_reglas tbody').append(fila);
            }
            
            //Traducción del dataTable
            $('#tabla_listar_reglas').DataTable({
                searchDelay: 350,
                language: {
                    decimal: "",
                    emptyTable: "No hay información",
                    info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                    infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
                    infoFiltered: "(Filtrado de _MAX_ total entradas)",
                    infoPostFix: "",
                    thousands: ",",
                    lengthMenu: "Mostrar _MENU_ Entradas",
                    loadingRecords: "Cargando...",
                    processing: "Procesando...",
                    search: "Buscar:",
                    zeroRecords: "Sin resultados encontrados",
                    paginate: {
                      first: "Primero",
                      last: "Ultimo",
                      next: "Siguiente",
                      previous: "Anterior",
                    },
                  },
            });
            
        },
        error: function(error){
            console.log("error --> ", error);
        }
    });
}

function BuscarPorNombreModelo(id_input,url_django) {

    $(id_input).select2({
        placeholder: "Buscar y Selecionar",
        //dropdownParent: $("#creacion"),
        dropdownAutoWidth: false,
        allowClear: true,
        selectOnClose: false,
        width: '100%',
        minimumInputLength: 2, //https://github.com/select2/select2/issues/2561
    
        ajax: {
            url: url_django,
            processResults: function (data) {
                console.log(data);
                return {
                results: $.map(data, function (item, index) {
                    return {
                        text: item.name,
                        id: item.id
                    }
                })
                };
            }
        }

    }); 



    //soluciòn al problema del placeholder en los select multiples
    $('.select2-search__field').css('width', '100%');

    //soluciòn al problema del scroll dentro de los modales
    $('select.select2:not(.normal)').each(function () {
        $(this).select2({
            dropdownParent: $(this).parent().parent()
        });
    });

}

function ValidarNombreActorAjax(id_input,url_django,id_form) {
        //Begin: Función para validar nombre repetido y borrarlo
        $(id_input).change(function(){
            var data = { 
                username: $(id_input).val() 
            }
        
            $.ajax({
                url : url_django,
                method : "POST", 
                data : { nombre_data_ajax:  data[Object.keys(data)[0]],
                        csrfmiddlewaretoken: '{{ csrf_token }}' },
                    success: function(response) {
                            // response, es el diccionario que envias desde python
                            if (response['valido']==false){
                                console.log("Sin repetir")
                                $(id_form +" "+ id_input).removeClass( "is-invalid" ).addClass( "is-valid" );                                
                                return true; // esto quiere decir que el formulario se enviara correctamente para guardar los datos en la base de datos
                            } else{ // si no enviamos desde el servidor que la respuesta está valida, entra aca
                                notificacionError("El nombre ya existe")
                                //event.preventDefault(); // este event, se supone es el que viene cuando haces $('form').submit(function(**event**){/... aqui se supone va el codigo que estoy escribiendo .../})
                                //location.href='{% url 'proyecto:lista_proyecto_filtros' %}';
                                $(id_input).val('')
                                $(id_form +" "+ id_input).addClass('is-invalid'); // Añado una clase para que el input que de color rojo

                                return false;
                            }
                    }
            }); 
        
    }); 
    //End: Función para validar nombre repetido y borrarlo
}

function abrir_modal_creacion(url) {
    $('#creacion').load(url, function()
    {
        $(this).modal('show');
    
    });
}

function abrir_modal_edicion(url) {

    $('#edicion').load(url, function()
    {
        $(this).modal('show');

    });

}

function abrir_modal_eliminacion(url) {

    $('#eliminacion').load(url, function()
    {
        $(this).modal('show');

    });

}

function cerrar_modal_creacion(){
    $('#creacion').modal('hide');
}

function cerrar_modal_edicion(){
    $('#edicion').modal('hide');
}

function cerrar_modal_eliminacion(){
    $('#eliminacion').modal('hide');
}

function notificacionError(mensaje){
	Swal.fire({
		title: 'Error!',
		text: mensaje,
		icon: 'error',
        allowOutsideClick: false,
	})
}

function notificacionSuccess(mensaje) {
	Swal.fire({
		title: 'Buen Trabajo!',
		text: mensaje,
		icon: 'success',
        timer: 5000, //milisegundos = 5
	})
}

// está función me permite no enviar dos veces el formulario ya lleno deshabilitando el botón
function activarBoton(){
    if($('#boton_creacion').prop('disabled')){
        $('#boton_creacion').prop('disabled',false);
    }else{
        $('#boton_creacion').prop('disabled',true);
    }

}

function mostrarErrorCreacionForm(id_form,errores){
	
    //Limpiamos los errores que le asignamos la clase help-block
	$("div.help-block").remove();
    $("select,textarea, input").removeClass('is-invalid')
    //Recorremos el Json que almacena el error de form.erros
	for(var error in errores.responseJSON.error){
         $(id_form+' #'+error+ "_crear").addClass('is-invalid'); // Añado una clase para que el input que de color rojo
         $(id_form+' #'+error+ "_crear").append('<div class="help-block text-danger">'+errores.responseJSON.error[error]+'</div>'); //pintar el error a interior del div creado
        
        //$('#form_creacion .error_message #nombre').css( "border", "3px solid red" ); //Test para validar el campo en la consola del navegador
	}
  

}

function mostrarErrorEdicionForm(id_form,errores){
	
    //Limpiamos los errores que le asignamos la clase help-block
	$("div.help-block").remove();
    $("select,textarea, input").removeClass('is-invalid')

    //Recorremos el Json que almacena el error de form.erros
	for(var error in errores.responseJSON.error){
         $(id_form+' #'+error+ "_editar").addClass('is-invalid'); // Añado una clase para que el input que de color rojo
         $(id_form+' #'+error+ "_editar").append('<div class="help-block text-danger">'+errores.responseJSON.error[error]+'</div>'); //pintar el error a interior del div creado
        
        //$('#form_creacion .error_message #nombre').css( "border", "3px solid red" ); //Test para validar el campo en la consola del navegador
	}
  

}

// eliminar con sweetAlert2
function eliminarRegla(url_django_eliminar,id){
    console.log(id)
    console.log(url_django_eliminar)
    Swal.fire({
        "title":"¿Estas seguro?",
        "text": "Esto Eliminara la Reglas permanentemente",
        "icon":"question",
        "showCancelButton":true,
        "cancelButtonText":"No, Cancelar",
        "cancelButtonClass":"btn-primary",
        "confirmButtonText":"Si, Eliminar",
        "reverseButtons":true,
        "confirmButtonColor":"#dc3545"
    })
    //cuando se ejecute va generar un resultado
    .then(function(result){
        if(result.isConfirmed){
            document.location.href= url_django_eliminar+id+"/";
        }
    })
}



/* ----------------------------------------
    funciones de la la plantilla de proyecto
 ---------------------------------------- */



/* ----------------------------------------
    funciones especificas Reglas
 ---------------------------------------- */

// Permite abrir el modal y que se activen los ajax de buscar actor y validar el campo de nombre
function abrir_modal_creacion_regla(url_modal){
    $('#creacion').load(url_modal, function()
    {
        $(this).modal('show');
        BuscarPorNombreModelo('#actor_crear','/stakeholders/buscar_actor/');
        //ValidarNombreActorAjax('#nombre_crear','/stakeholders/validar_input_regla/','#form_creacion');
    });
}

function abrir_modal_edicion_regla(url) {

    $('#edicion').load(url, function()
    {
        $(this).modal('show');
        BuscarPorNombreModelo('#actor_editar','/stakeholders/buscar_actor/');
        //ValidarNombreActorAjax('#nombre_editar','/stakeholders/validar_input_regla/','#form_edicion');
    });

}

function registrar(){
    //console.log("$('#form_creacion').attr('action') ",$('#form_creacion').attr('action'))
    activarBoton()
    $.ajax({
        data: $('#form_creacion').serialize(),
        url: $('#form_creacion').attr('action'),
        type: $('#form_creacion').attr('method'),
        success: function(response){
            
            // actualiza el lsitado que se paso como parametro para ver cambios en el datatable despues de guardar
            notificacionSuccess(response.mensaje);
            cerrar_modal_creacion(); 
            //location.reload();
            console.log("paso 1");
            listaReglasServerSide();

        },
        error: function(error){
            console.log("error --> ", error);
            notificacionError(error.responseJSON.mensaje);
            mostrarErrorCreacionForm("#form_creacion",error)
            activarBoton()
            
        },
    })
}

function editar(){
    //console.log("$('#form_edicion').attr('action') ",$('#form_edicion').attr('action'))
    //console.log("$('#form_edicion').attr('method') ",$('#form_edicion').attr('method'))
    //console.log("$('#form_edicion').serialize(),",$('#form_edicion').serialize())

    activarBoton()

    $.ajax({
        data: $('#form_edicion').serialize(),
        url: $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        success: function(response){
            notificacionSuccess(response.mensaje);
            cerrar_modal_edicion(); 
            //location.reload();
            listaReglasServerSide();

        },
        error: function(error){
            console.log("error editar --> ", error);
            notificacionError(error.responseJSON.mensaje);
            mostrarErrorEdicionForm("#form_edicion",error)
            activarBoton()
        },
    })
}

function eliminar(pk) {
	activarBoton()
    $.ajax({
        data:{
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
        },
        url: '/stakeholders/eliminar_regla/'+pk+'/',
        type: 'delete',
        success: function (response) {
            notificacionSuccess(response.mensaje);
            cerrar_modal_eliminacion();
			listaReglasServerSide();
           // listaReglasServerSide();
        },
        error: function (error) {
			console.log("error eliminar--> ", error);
            notificacionError(error.responseJSON.mensaje);
			activarBoton()
        }
    });
}

function listaReglasServerSide(){
    //listadoAutores(); 
    //Destruir la tabla para evitar el error: 
    if ($.fn.DataTable.isDataTable('#tabla_listar_reglas')) {
        $('#tabla_listar_reglas').DataTable().destroy();
        console.log("romper --> ")
    }

    $('#tabla_listar_reglas').DataTable({
        //bloquea el filtro de la columna
        "searchDelay": 350,
        "language": {
            decimal: "",
            emptyTable: "No hay información",
            info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
            infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
            infoFiltered: "(Filtrado de _MAX_ total entradas)",
            infoPostFix: "",
            thousands: ",",
            lengthMenu: "Mostrar _MENU_ Entradas",
            loadingRecords: "Cargando...",
            processing: "Procesando...",
            search: "Buscar:",
            zeroRecords: "Sin resultados encontrados",
            paginate: {
              first: "Primero",
              last: "Ultimo",
              next: "Siguiente",
              previous: "Anterior",
            },
        },

        "columnDefs": [
            { "orderable": false, "targets": 4 },
			{ "orderable": false, "targets": 1 }
        ],
        "serverSide": true,
        "orderCellsTop": false,
        "processing": true,
        "ajax": function(data,callback,settings){
            //seleccionamos el dato de orderby
            var columna_filtro = data.columns[data.order[0].column].data.replace(/\./g,"__"); //limpiamos la url del filtro
            console.log("data --> ",data)
            //al interior del get se capturan todas las acciones
            $.get('/stakeholders/reglas/',{
                //este limite e inicio lo trae de data
                limite: data.length,
                inicio: data.start,
                filtro: data.search.value,
                order_by: columna_filtro
            }, function(res){



                // una vez recibida la respuesta del servidor hacer
                console.log("res --> ",res)
                    callback({
                        //total de elemento que hay en la consulta
                        recordsTotal:res.length,
                        recordsFiltered:res.length,
                        //información
                        data:res.objects
                    });
                },
            );
        },
        //definimos las columnas
        "columns":[
            { "data": "id" },
            { "data": "num" },
            { "data": "actor__nombre" },
            { "data": "nombre" },
            {
                "data": null,
                render:function(data, type, row)
                {
                  return '<div class="row text-center"><div class="col-6 col-xl-6 col-lg-6 col-sm-6 p-0 text-right"><button type="button" class="btn btn-info " onclick="abrir_modal_edicion_regla(\'/stakeholders/editar_regla/'+row.id+'/\');"><i class="fa fa-edit fa-1x"></i></button></div>'
                  + //'&nbsp;&nbsp' +
                  '<div class="col-6 col-xl-6 col-lg-6 col-sm-6 pl-1 text-left"><button type="button" class="btn btn-danger" onclick="abrir_modal_eliminacion(\'/stakeholders/eliminar_regla/'+row.id+'/\');"><i class="feather icon-edit-2 fa-1x"></button></div></div>';

                },

                "targets": -1
            }
        ]
    });
}

// llamar la función para terner resultado en consola del navegador server side 
// apoyo https://riptutorial.com/datatables/example/14618/load-data-using-ajax-with-server-side-processing-
$(document).ready(function() { 
    listaReglasServerSide(); 
});


