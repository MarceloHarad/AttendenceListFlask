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
        }
        if (radios[i].value == "aluno"){
          document.getElementById("register_std2").style.display= 'block' ;
        }
        break;
    }
  }
  document.getElementById("register1").style.display= 'none';
}
