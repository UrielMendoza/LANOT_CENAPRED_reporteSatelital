$(document).ready(sargazo);

function sargazo(){
        
    
    $('#sargazod').click(function(){
        var imgsargazo = "/static/sargazo/visualizador_sargazo/img/Simbo/Sargazo_dis.png";
        if($(this).is(':checked')){
            map.addLayer(wmsLayersargazo);
            $('#imagen').append('<img src="'+imgsargazo+'" class="imgsard"/>');
        } else {
            map.removeLayer(wmsLayersargazo);
            $('img').remove('.imgsard');
        }
    });
 

/*     $('#estudio').click(function(){
        var imgestudio = "/static/sargazo/visualizador_sargazo/img/Simbo/zona.png";
        if($(this).is(':checked')){
            map.addLayer(wmsLayerzona);
            $('#imagen').append('<img src="'+imgestudio+'" class="imgzona"/>');
        } else {
            map.removeLayer(wmsLayerzona);
            $('img').remove('.imgzona');
        }
    });


    $('#lineacosta').click(function(){
        var imglineacosta = "/static/sargazo/visualizador_sargazo/img/Simbo/lineacosta2021.png";
        if($(this).is(':checked')){
            map.addLayer(wmsLayerlineacosta);
            $('#imagen').append('<img src="'+imglineacosta+'" class="imgzona"/>');
        } else {
            map.removeLayer(wmsLayerlineacosta);
            $('img').remove('.imgzona');
        }
    });
    
    $('#Hycom').click(function(){
        var imgHycom = "/static/sargazo/visualizador_sargazo/img/Simbo/HycomVelvec.png";
        if($(this).is(':checked')){
            map.addLayer(wmsLayerHycom);
            $('#imagen').append('<img src="'+imgHycom+'" class="imgzona"/>');
        } else {
            map.removeLayer(wmsLayerHycom);
            $('img').remove('.imgzona');
        }
    });

    $('#HycomVel').click(function(){
        var imgHycomVel = "/static/sargazo/visualizador_sargazo/img/Simbo/HycomVelvec.png";
        if($(this).is(':checked')){
            map.addLayer(wmsLayerHycomVel);
            $('#imagen').append('<img src="'+imgHycomVel+'" class="imgzona"/>');
        } else {
            map.removeLayer(wmsLayerHycomVel);
            $('img').remove('.imgzona');
        }
    });

    $('#ABI_SST').click(function(){
        var imgABI_SST = "/static/sargazo/visualizador_sargazo/img/Simbo/HycomVelvec.png";
        if($(this).is(':checked')){
            map.addLayer(wmsLayerABI_SST);
            $('#imagen').append('<img src="'+imgABI_SST+'" class="imgzona"/>');
        } else {
            map.removeLayer(wmsLayerABI_SST);
            $('img').remove('.imgzona');
        }
    }); */
}
