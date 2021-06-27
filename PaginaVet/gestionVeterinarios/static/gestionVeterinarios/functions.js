var regionactual;

function getRegion(tag, regiones) {
    let x = 0;
    regionactual = tag.options[tag.selectedIndex].text;
    $.getJSON(regiones, function(obj) {
        $.each(obj.datos, function (key, value) {
            if(value.region == regionactual){
                $("#comuna").empty();
                $("#comuna").append('<option value="" selected="selected" disabled = "disabled">Seleccione una comuna</option>');
                for (let i = 0; i<this.comunas.length; i++){
                    let comuna_i = value.comunas[i];
                    $("#comuna").append('<option value="' + comuna_i + '">' + comuna_i + '</option>');
                }
            }
            x++;
        });

    });
}

function check() {
    var pass1= document.getElementById('password').value;
    var pass2= document.getElementById('repeat_password').value;
    if(pass1 == pass2) {
        document.getElementById('message').innerHTML = "Las contraseñas coinciden";
        document.getElementById('message').style.color = "white";
        document.getElementById('message').style.fontSize = "20px";
    } else {
        document.getElementById('message').innerHTML = "Las contraseñas no coinciden";
        document.getElementById('message').style.color = "#ffed80";
        document.getElementById('message').style.fontSize = "20px";
    }
}
