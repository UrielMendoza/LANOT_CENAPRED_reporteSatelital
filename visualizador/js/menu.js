$(document).ready(main);
$(document).ready(maxdate);

var contador = 1;

function main(){
    $('.menu').click(function(){
        if(contador == 1){
            document.getElementById("body-grapper").style.display = "block";
            $('nav').animate({
                left: '0'
            });
            contador = 0;
        } else {
            contador = 1;
            document.getElementById("body-grapper").style.display = "none";
            $('nav').animate({
                left: '-100%'
            });
            
        }

    });

};

function maxdate(){
    //Fecha máxima de consulta en puntos de calor. 
/*     date3.max = new Date().toISOString().split("T")[0];
    date4.max = new Date().toISOString().split("T")[0];
    date5.value = fechapaso;
    date5.max = fechapaso;
    date6.value = fechapaso;
    date6.max = fechapaso; */

    
}
