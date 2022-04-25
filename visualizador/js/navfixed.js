
function navfixed(){
    // Cambio de coloración de barra de navegación
    var y = window.scrollY;
    
    if(y>0){
        $('nav').css("background","linear-gradient(0deg, rgba(0,0,0,1) 0%, rgba(0,0,0,1) 80%, rgba(255,124,0,1) 100%)");
    }else{
        $('nav').css("background","black");
    }
    
    // Animación de logos
    
    var ey = $("footer").position();
    var ay = ey.top - 500;
    indice=0;
        
        if( y > ay){
            // $('.logos img').css("width", "22%");
            $('.logos img').animate({width: 'show'}, 750);
        }else{
            $('.logos img').animate({width: 'hide'}, 500);
        }
}




