let spanActivo = 0; //Ultimo span creado
let spanText = [] //Guarda los span
let counterSpans = 0; //conteo de span
let stateFragment = 0 //estado del fragmento
localStorage.setItem('fragmentSelect', ""); //Limpiar la localStorage


/**
* Captura el resumen y lo separa por c.
*/
// let str = document.getElementById("texto-resumen").textContent;
// let res = str.replace(/\.\s\s/g, '. <br>');
// document.getElementById("texto-resumen").innerHTML = res;


// Funciones de busqueda en Select2
$(".select2").select2({
  placeholder: "Buscar y Selecionar",
  dropdownAutoWidth: false,
  allowClear: true,
  selectOnClose: false,
  width: '100%',

});

$('.js-example-basic-multiple-medio').select2({
  placeholder: "Buscar y Selecionar",
  dropdownAutoWidth: false,
  allowClear: true,
  ajax: {
    url: '/ingestion_medios/SearchMedia/',
    processResults: function (data) {
      return {
        results: $.map(data, function (item, index) {
          return {
            text: item.name_medio,
            id: item.id
          }
        })
      };
    }
  }
});

$('.js-example-basic-multiple-autor').select2({
  placeholder: "Buscar y Selecionar",
  dropdownAutoWidth: false,
  allowClear: true,
  ajax: {
    url: '/ingestion_medios/SearchAutor/',
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

$('.js-basic-multiple-tag').select2({
  placeholder: "Buscar y Selecionar",
  dropdownAutoWidth: false,
  allowClear: true,
  ajax: {
    url: '/ingestion_medios/SearchTag/',
    processResults: function (data) {
      console.log(data);
      return {
        results: $.map(data, function (item, index) {
          console.log("Prueba--", item);
          return {
            text: item.name_tag,
            id: item.id
          }
        })
      };
    }
  }
});

$('.js-basic-multiple-tema').select2({
  placeholder: "Buscar y Selecionar",
  dropdownAutoWidth: false,
  allowClear: true,
  ajax: {
    url: '/ingestion_medios/SearchTema/',
    processResults: function (data) {
      console.log(data);
      return {
        results: $.map(data, function (item, index) {
          console.log("Prueba--", item);
          return {
            text: item.name_tema,
            id: item.id
          }
        })
      };
    }
  }
});

//Datapicker Fecha
jQuery(document).ready(function () {
  'use strict';
  jQuery('#picker').datetimepicker({
    dateFormat: 'dd/mm/yy',
  });
});

/**
* Captura y renderiza el formulario - Encabezado del articulo.
*/
;
document.getElementById("button-header").addEventListener("click", function () {
  let form = $('#form-header');
  let formHeader = form.serialize()
  console.log("holaaaaaaaaaaa",form)

  $("#tipo-publicacion").prop('disabled', true);
  $(".js-example-basic-multiple-autor").prop('disabled', true);
  $(".js-example-basic-multiple-medio").prop('disabled', true);
  $("#picker").prop('disabled', true);
  $("#programa").prop('disabled', true);

  $.ajax({
    url: form.attr("action"),
    method: "POST",
    data: {
      form_header: formHeader,
      csrfmiddlewaretoken: '{{ csrf_token }}'
    }, //
    success: function (json) {
      form: $('form_header').val(' ');
    },
    error: function (xhr, errmsg, err) { }
  });
});

/**
* Captura y renderiza el formulario - Categorizacion general del articulo.
*/
document.getElementById("article-button-general").addEventListener("click", function () {
  let form_article = $('#form_article');
  $.ajax({
    url: form_article.attr("action"),
    method: "POST",
    data: {
      form_article: form_article.serialize(),
      csrfmiddlewaretoken: '{{ csrf_token }}'
    }, //
    success: function (json) {
      form_article: $('#form_article').val(' ');
    },
    error: function (xhr, errmsg, err) { }
  });
});



//Funciones de categorizaciòn del articulo
activateFunction()

/**
 * Funciones que se ejecutan una vez se ejecuta el codigo
 * Valida los estados del articulo
 * */
function activateFunction() {
  let stateArticle = document.getElementById("texto");
  let state = stateArticle.dataset.state;

  if (state == 'True') {
      fragmentPosition() //Activa las categorizaciones anteriores
      console.log("Entra a categorizados")
  } else {     
      
      // let str = document.getElementById("texto").innerHTML;
      // let res = str.replace(/\.\s\s/g,'.<br>');
      // document.getElementById("texto").innerHTML = res;

      $(".loading-w").hide("20");
      //predictionFragment() //Realiza la prediccion (porque no hay categorizacion previa)
  }

}

/**
 * Predicción de fragmentos al cargar la pagina. 
 * @param {Array} datos_fragment - Posicion de fragmentos.
 * @return {Array} - Posiciones del fragmento.
 */
function colorPhrase(datos_fragment,dataFragment) {
  let range = new Range();
  let nodeArticle = document.getElementsByClassName("article_text")[0];
 
  dataFragment = datos_fragment.sort((a, b) => (a.end < b.end) ? 1 : -1); //
  let ultimoDato = dataFragment.length - 1;
  for (var i = 0; i < dataFragment.length; i++) {
      
      console.log(dataFragment[0])
      let newNode = null
      range.setStart(nodeArticle.firstChild, dataFragment[i].start);
      range.setEnd(nodeArticle.firstChild, dataFragment[i].end);
      

      var spanChild = document.createElement("span");
      spanChild.setAttribute("onclick", "updateCategorization()");
      spanChild.setAttribute("data-custom", dataFragment[i].id_fragment);
      range.surroundContents(spanChild);

      newNode = document.createElement("span");
      newNode.setAttribute("class", "selectedText");
      newNode.setAttribute("id", "active-span" + counterSpans);
      newNode.setAttribute("data-counter", counterSpans);
      range.surroundContents(newNode)
      counterSpans = counterSpans + 1;
      spanText.push({
          position: counterSpans
      })  


  }
}

/**El articulo esta categorizado posteriormente.
* Se realiza un parseo de del dato que se captura para convertirlo
* en un objecto. 
*/
function fragmentPosition() {

  var fragment = document.getElementById("texto");
  info = fragment.dataset.context

  var info = eval(info)
  dateFragment = info[0]

  var nodeArticle = document.getElementById("texto");

  info.sort((a, b) => (a.end < b.end) ? 1 : -1)
  let newArray = [];
  info.map((elemento) => {
      newArray.push({
          id: elemento.id,
          start_index: parseInt(elemento.start_index),
          end_index: parseInt(elemento.end_index)
      })
  })
  info = newArray;

  function compare(a, b) {
      if (a.end_index > b.end_index) {
          return -1;
      }
      if (a.end_index < b.end_index) {
          return 1;
      }
      return 0;
  }

  info.sort(compare);
  let ultimoDatoTwo = info.length - 1;



  var nodeArticle = nodeArticle.firstChild
  var nodorango = nodeArticle.length

  for (var i = 0; i < info.length; i++) {
      let range = new Range();
      let newNode = null;

      startOffset = info[i]['start_index']
      endOffset = info[i]['end_index']


      isCollapsed = range.collapsed;

      range.setStart(nodeArticle, startOffset);
      range.setEnd(nodeArticle, endOffset);
      var positionTrue = isCollapsed

      var spanChild = document.createElement("span");
      spanChild.setAttribute("onclick", "updateCategorization()");
      spanChild.setAttribute("data-custom", info[i]['id']);
      range.surroundContents(spanChild);

      newNode = document.createElement("span");
      newNode.setAttribute("class", "selectedText");
      newNode.setAttribute("id", "active-span" + counterSpans);
      newNode.setAttribute("data-counter", counterSpans);
      range.surroundContents(newNode)
      counterSpans = counterSpans + 1;
      spanText.push({
          position: counterSpans
      })

     

      if (i == ultimoDatoTwo) {
          $(".loading-w").hide("20");
          console.log("Esto entra", i)
      }
  }


}

var parentContainerId = "textDescription"  //Declarar el nodo que sera utilizado.

if (!window.CurrentSelection) {
      CurrentSelection = {}
}
CurrentSelection.Selector = {}

/**
 * Captura la selección realizada por el usuario.
 * @returns {object} sel - rango de la selección
 */
CurrentSelection.Selector.getSelected = function (event) {
  var sel = "";

  if (window.getSelection) {
      sel = window.getSelection()
  } else if (document.getSelection) {
      sel = document.getSelection()
  } else if (document.selection) {
      sel = document.selection.createRange()
  }
  return sel
}

/**
 * Creación etiqueta <span> en donde se encapsula la seleccion realizada por el usuario. 
 * Se almacena en el localStorage la seleccion.
 */

CurrentSelection.Selector.mouseup = function createSpan(event) {  
  var st = window.getSelection()
  if (document.selection && !window.getSelection) {
      var range = st
      range.pasteHTML("<span class='selectedText'>" + range.htmlText + "</span>");
  } else if (window.getSelection().toString().length > 0) {

      try {

          //Validación del formulario, si ya existe
          if(document.getElementById('povDivform')){
              console.log("Ya existe el formulario")
          }
          else{
              
              var nodeArticle = document.getElementById("texto")
              var nodeArticle = nodeArticle.firstChild
              var nodorango = nodeArticle.length
  
              let fragmentSelect = window.getSelection().toString() //seleccion realizada por el 
           
              var range = st.getRangeAt(0);   //rango que se selecciona
              let indexStart = range.startOffset
              let indexEnd = range.endOffset
  
              counterSpans = counterSpans + 1
              spanActivo = counterSpans;
             
  
              spanText.push({  //validar si ese elemento ya existe en el array de lo contrario se puede agregar
                  position: counterSpans,
                  textClean: window.getSelection().toString()
              })
  
              //crea el span que contiene el texto
  
  
              var spanChild = document.createElement("span");
              spanChild.setAttribute("onclick", "updateCategorization()");
              range.surroundContents(spanChild);
  
  
              var newNode = document.createElement("span");
              newNode.setAttribute("class", "selectedText");
              newNode.setAttribute("id", "active-span" + counterSpans);
              newNode.setAttribute("data-counter", counterSpans);
              range.surroundContents(newNode)
  
  
  
              //crea el separador para obtener el indexStart
              newNode.innerHTML = "|" + newNode.innerHTML; //Separado al inciar el <SPAN> aqui lo iniciamos 
  
              let noditos = document.getElementById("texto").childNodes;
              let initPosition = 0;
              let endPosition = 0;
              let finded = false;
              for (let index = 0; index < noditos.length; index++) {
                  let nodoCompleto = document.getElementById("texto").childNodes[index];
                  if (!finded) {
                      if (nodoCompleto.textContent.includes('|')) {
                          let suma = newNode.textContent.substring(1, newNode.textContent.length);
                          endPosition = initPosition + suma.length;
                          finded = true;
                          break;
                      } else {
                          if (nodoCompleto.length > -1) { // aqui valida si es mayor a menos uno porque ocasiones cuando seleccionas así: no lo antecede nada entonces puede ser 0 o undefined -Rusia 2020
                              initPosition += nodoCompleto.length
                          } else if (nodoCompleto.textContent.length > -1) {
                              initPosition += nodoCompleto.textContent.length
                          }
                      }
                  }
              }
              newNode.innerHTML = newNode.innerHTML.replace("|", "")
  
              var dataFragment = {
                  'text': fragmentSelect,
                  'indexStart': initPosition,
                  'indexEnd': endPosition
              }
  
              //Seleccion limpia
  
              localStorage.setItem('fragmentSelect', JSON.stringify(dataFragment));
  
              //Crea la etiqueta <span> para insertar la barra de categorizacion
              var popDiv = document.createElement('div');
              popDiv.setAttribute('class', 'popDiv');
              popDiv.setAttribute('id', 'povDivform'); // 
  
              //aqui le di el evento
  
  
              var containerSelected = document.getElementById('povDivform');
  
              popDiv.innerHTML = '';
              popDiv.focus();
           
              if (newNode.innerHTML.length > 0) {
  
                  //capturar datos del parametro de proyecto y articulo
                  var parameter = window.location.pathname.split('/');
  
                  newNode.appendChild(popDiv);
                  var containerSelected = document.getElementById('povDivform');
                  containerSelected.focus();
                  
                  var parameter = window.location.pathname.split('/');

                  url = '/categorizacion_medios/form_categorization/proyecto/' + parameter[4] + '/articulo/' + parameter[6]
                  $('#povDivform').load(url, function () {
                      $("#popDivform").ready(() => {
  
                          $(document).mouseup(function (e) {
                              var container = $("#custom");
  
                              if (!container.is(e.target) && container.has(e.target).length === 0 && e.target.classList[0] != "select2-results__option") {
                                  if (document.getElementById("custom")) {
                                      document.getElementById("povDivform").remove()
                                      localStorage.setItem('fragmentSelect', ""); //Limpiar la localStorage
                                 
                                      if (stateFragment == 0 && document.getElementById("active-span" + spanActivo)) { //
                                          let lastSpan = spanText[spanActivo - 1],
                                              texto = document.getElementById("texto").innerHTML;
                                          document.getElementById("texto").innerHTML = texto.toString();
                                          $("#active-span" + spanActivo).replaceWith(lastSpan.textClean)
                                        
                                      }
                                  }
                              }
                          })
                      })
                  });
  
              }
          }
      } catch {
          console.error("No hay seleccion")
      }

      if (window.getSelection) {
          window.getSelection().removeAllRanges();
      } else if (document.selection) {
          document.selection.empty();
      }


  }

  var getText = newNode;
}

//Cerrar el formulario popDiv solo se activa se se da afuera de la ventana emergente
$(function () {
  $("#" + parentContainerId).bind("mouseup", CurrentSelection.Selector.mouseup);
})


/*
 *   Abre nuevamente el formulario categorizado para realizar el update
 */
function updateCategorization(e) {
  if(document.getElementById('povDivform')){
      console.log("El formulario de categorización ya esta creado")
  }
  else{
      var parameter = window.location.pathname.split('/');
      var project = parameter[4]
      //Captura el elemnto cla cual se le da onclick
      spanSelection = event.srcElement
      console.log('spanSelection',spanSelection)
      spanParent = spanSelection.parentNode //padre del nodo de la selección
      fragment_id = spanSelection.dataset.custom //https://developer.mozilla.org/es/docs/Web/API/HTMLElement/dataset
  
      var popDiv = document.createElement('span');
      popDiv.setAttribute('class', 'popDiv');
      popDiv.setAttribute('id', 'povDivform');
      popDiv.setAttribute('height', '442');
      spanParent.appendChild(popDiv); //se agrega el formulario al SPAN
  
      
      console.log('fragment_id',fragment_id)
      url = '/categorizacion_medios/update_fragment/proyecto/' + project + '/id_fragment/' + fragment_id
      $('#povDivform').load(url, function () {
  
          $("#popDivform").ready(() => {
              //agrega el id del fragmento al boton eliminar
              document.getElementById("delete_form").setAttribute("data-idfragment", fragment_id)
  
              //Funcion para desaparecer el popDiv
              let activeCustom = false;
              $(document).mouseup(function (e) {
  
                  var container = $("#custom");
  
                  if (!container.is(e.target) && container.has(e.target).length === 0 && e.target.classList[0] != "select2-results__option") {
                      if (document.getElementById("custom")) {
                          document.getElementById("povDivform").remove()
                          if (stateFragment == 0 && document.getElementById("active-span" + spanActivo)) { //
                              let lastSpan = spanText[spanActivo - 1],
                                  texto = document.getElementById("texto").innerHTML;
                              console.log("lastSpan----", lastSpan)
                              document.getElementById("texto").innerHTML = texto.toString();
                              //$("#active-span" + spanActivo).replaceWith(lastSpan.textClean) //
                          }
                      }
                  }
              })
          })
      });
  }
}

/*
Formulario de categorizacion
*/
document.getElementById("save-form").addEventListener("click", function () {
 console.log("Esta ingresandooooooooooooo")
});