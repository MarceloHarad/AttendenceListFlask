//JavaScript Functions
function show(id){
  //alert("cheked the button - worked");
  document.getElementById(id).style.display= 'block' ;
}

function hide(id){
  //alert("cheked the button - worked");
  document.getElementById(id).style.display= 'none' ;
}

function stdOrProf(){
  var radios = document.getElementsByName('std_prof');

  for (var i = 0, length = radios.length; i < length; i++) {
    if (radios[i].checked) {
      if (radios[i].value == "professor"){
        document.getElementById("register_prof2").style.display= 'block' ;
        document.getElementById("register1").style.display= 'none';
      }
      if (radios[i].value == "aluno"){
        document.getElementById("register_std2").style.display= 'block' ;
        document.getElementById("register1").style.display= 'none';
      }
      break;
    }
  }
}

//JQuery Functions
$(document).ready(function () {
    $('myFormHome').validate({
        rules: {
          email_login: {
            required: true,
            email: true
          },
          password_login: {
            required: true,
          }
        },

        messages: {
          email_login: {
              required: 'Escreva seu email',
              email: 'Escreva um email válido'
          },
          password_login: {
            required: "Escreva sua senha",
            minlength: "Escreva uma senha de 6 dígitos no mínimo"
          }
        }
    });

    $('#myform').validate({ // initialize the plugin
        rules: {
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 6
            },
            name: {
                required: true,
            },
            semestre: {
                required: true,
            },
            curso: {
                required: true,
            },
            file: {
                required: true,
            }
        },
        messages: {
            email: {
                required: 'Escreva seu email',
                email: 'Escreva um email válido'
            },
            password: {
                required: "Escreva sua senha",
                minlength: "Escreva uma senha de 6 dígitos no mínimo"
            },
            name: {
              required: "Escreva seu nome"
            },
            semestre: {
              required: ""
            },
            curso: {
              required: ""
            },
            file: {
              required: ""
            }
        }
    });
    $('#btn_continue').click(function() {
      if ($('#myform').valid()) {
        stdOrProf();
      }
      else {

      }
    });
});

$(".js-example-basic-multiple").select2({
  placeholder: "Escolha suas aulas",
  allowClear: true
});
