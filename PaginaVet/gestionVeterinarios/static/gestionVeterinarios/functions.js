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