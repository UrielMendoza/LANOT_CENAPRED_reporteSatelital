// $(document).ready(infolay);
$(document).ready(moreinfo);
$(document).ready(popup);



function infolay(){
    $('input[type=checkbox]').click(function(){
        //Función para actulización del select 
        var ids;
    
        ids = $('input[type=checkbox]:checked').map(function() {
            return $(this).attr('id');
        }).get();
        idS=$('input[type=checkbox]:checked').size();
        // alert(idS);
        // alert('IDS: ' + ids.join(', '));
        $('#selectcapas').html("");
        for(var i=0; i<idS; i++ ){
            switch (true){
                case ids[i]=='sargazod':
                $('#selectcapas').append('<option value="sargazod">Sargazo</option>')
                break;
                case ids[i]=='estados':
                $('#selectcapas').append('<option value="estados">Estados y linea</option>')
                break;
                case ids[i]=='lineacosta':
                $('#selectcapas').append('<option value="estudio">Linea de costa 2021</option>')
                break;
                case ids[i]=='playas':
                $('#selectcapas').append('<option value="estudio">Playas 2021</option>')
                break;
                case ids[i]=='anp':
                $('#selectcapas').append('<option value="anp">Área natural protegida</option>')
                break;
                case ids[i]=='hum':
                $('#selectcapas').append('<option value="hum">Humedales</option>')
                break;
                case ids[i]=='nidos':
                $('#selectcapas').append('<option value="nidos">Nidos de tortugas</option>')
                break;
                case ids[i]=='man':
                $('#selectcapas').append('<option value="man">Manglares</option>')
                break;
                case ids[i]=='insu':
                $('#selectcapas').append('<option value="insu">Islasr</option>')
                break;
                case ids[i]=='estudio':
                $('#selectcapas').append('<option value="estudio">Zona de estudio</option>')
                break;
                case ids[i]=='Hycom':
                $('#selectcapas').append('<option value="Hycom">HYCOM velocidad de corrientes (dirección)</option>')
                break;
                case ids[i]=='HycomVel':
                $('#selectcapas').append('<option value="HycomVel">HYCOM velocidad de corrientes</option>')
                break;
                case ids[i]=='ABI_SST':
                $('#selectcapas').append('<option value="ABI_SST">GOES-16/ABI (Sea Surface Temperature)</option>')
                break;
                case ids[i]=='sentineltc':
                $('#selectcapas').append('<option value="sentineltc">Sentinel TC</option>')
                break;
                case ids[i]=='sentinelfal':
                $('#selectcapas').append('<option value="sentinelfal">Sentinel FC</option>')
                break;
            }
        }

                    
                    
    });

    //Función de selección de capas para información
    $('#elegir').click(function(){
        cap = $('#selectcapas').val();
        swal("Usted eligio la capa:"+cap);
        var infopuntoslayer =  function(){
            /*alert("Si funciona");*/
            
            var view1 = new ol.View({
                center: ol.proj.transform([-90, 20], 'EPSG:4326', 'EPSG:3857'),//Cambiamos proyección a WGS84
            });
            map.on('singleclick', function (evt) {
                document.getElementById('infolay').innerHTML = 'Espere un momento por favor';
                var viewResolution = /** @type {number} **/ (view1.getResolution());

                switch(true){
                    case cap=='sargazod':
                        // infopuntoslayer();
                        var url = wmsSourcesargazo.getFeatureInfoUrl(
                            evt.coordinate,
                            viewResolution,
                            'EPSG:4326',
                            {'INFO_FORMAT': 'text/html', 'FEATURE_COUNT': 50}
                        );
                        // alert(evt.coordinate);
                        document.getElementById('infolay').innerHTML = '<iframe seamless id="24pc" src="' + url + '"></iframe>';
                    break;
                    case cap=='estados':
                        // infopuntoslayer();
                        var url = wmsSourceestados.getFeatureInfoUrl(
                            evt.coordinate,
                            viewResolution,
                            'EPSG:3857',
                            {'INFO_FORMAT': 'text/html', 'FEATURE_COUNT': 50}
                        );
                        document.getElementById('infolay').innerHTML = '<iframe seamless id="24pc" src="' + url + '"></iframe>';
                    break;
                    case cap=='anp':
                        // infopuntoslayer();
                        var url = wmsSourceANP.getFeatureInfoUrl(
                            evt.coordinate,
                            viewResolution,
                            'EPSG:3857',
                            {'INFO_FORMAT': 'text/html', 'FEATURE_COUNT': 50}
                        );
                        document.getElementById('infolay').innerHTML = '<iframe seamless id="24pc" src="' + url + '"></iframe>';
                    break;
                    case cap=='hum':
                        // infopuntoslayer();
                        var url = wmsSourcehumedales.getFeatureInfoUrl(
                            evt.coordinate,
                            viewResolution,
                            'EPSG:3857',
                            {'INFO_FORMAT': 'text/html', 'FEATURE_COUNT': 50}
                        );
                        document.getElementById('infolay').innerHTML = '<iframe seamless id="24pc" src="' + url + '"></iframe>';
                    break;
                    case cap=='nidos':
                        // infopuntoslayer();
                        var url = wmsSourcenidos.getFeatureInfoUrl(
                            evt.coordinate,
                            viewResolution,
                            'EPSG:3857',
                            {'INFO_FORMAT': 'text/html', 'FEATURE_COUNT': 50}
                        );
                        document.getElementById('infolay').innerHTML = '<iframe seamless id="24pc" src="' + url + '"></iframe>';
                    break;
                    case cap=='man':
                        // infopuntoslayer();
                        var url = wmsSourceman.getFeatureInfoUrl(
                            evt.coordinate,
                            viewResolution,
                            'EPSG:3857',
                            {'INFO_FORMAT': 'text/html', 'FEATURE_COUNT': 50}
                        );
                        document.getElementById('infolay').innerHTML = '<iframe seamless id="24pc" src="' + url + '"></iframe>';
                    break;
                    case cap=='insu':
                        // infopuntoslayer();
                        var url = wmsSourceinsu.getFeatureInfoUrl(
                            evt.coordinate,
                            viewResolution,
                            'EPSG:3857',
                            {'INFO_FORMAT': 'text/html', 'FEATURE_COUNT': 50}
                        );
                        document.getElementById('infolay').innerHTML = '<iframe seamless id="24pc" src="' + url + '"></iframe>';
                    break;
                    case cap=='sentineltc':
                        // infopuntoslayer();
                        var url = wmsSourceSentinel.getFeatureInfoUrl(
                            evt.coordinate,
                            viewResolution,
                            'EPSG:3857',
                            {'INFO_FORMAT': 'text/html', 'FEATURE_COUNT': 50}
                        );
                        document.getElementById('infolay').innerHTML = '<iframe seamless id="24pc" src="' + url + '"></iframe>';
                    break;
                    case cap=='sentinelfal':
                        // infopuntoslayer();
                        var url = wmsSourceSentinelfal.getFeatureInfoUrl(
                            evt.coordinate,
                            viewResolution,
                            'EPSG:3857',
                            {'INFO_FORMAT': 'text/html', 'FEATURE_COUNT': 50}
                        );
                        document.getElementById('infolay').innerHTML = '<iframe seamless id="24pc" src="' + url + '"></iframe>';
                    break;
                }
            });
            map.on('pointermove', function (evt) {
                if (evt.dragging) {
                    return;
                }
                var pixel = map.getEventPixel(evt.originalEvent);
                var hit = map.forEachLayerAtPixel(pixel, function () {
                    return true;
                });
                map.getTargetElement().style.cursor = hit ? 'pointer' : '';
            });
        }
        infopuntoslayer();
                
    });
};






// // const ipunt = document.querySelector("#infolay");
       
// if($(this).is(':checked')){
//     // console.log('#infolay');
//     var infopuntoslayer =  function(){
//         /*alert("Si funciona");*/
        
//         var view1 = new ol.View({
//             center: ol.proj.transform([-90, 20], 'EPSG:4326', 'EPSG:3857'),//Cambiamos proyección a WGS84
//             zoom: 4.5
//         });
//         map.on('singleclick', function (evt) {
//         document.getElementById('infolay').innerHTML = 'Espere un momento por favor';
//         var viewResolution = /** @type {number} **/ (view1.getResolution());
//         var url = wmsSourcenidos.getFeatureInfoUrl(
//             evt.coordinate,
//             viewResolution,
//             'EPSG:3857',
//             {'INFO_FORMAT': 'text/html', 'FEATURE_COUNT': 50}
//         );
//         // var urlin = wmsSourcenidos.getFeatureInfoUrl(
//         //     evt.coordinate,
//         //     viewResolution,
//         //     'EPSG:3857',
//         //     {'INFO_FORMAT': 'text/html', 'FEATURE_COUNT': 50}
//         // );
//         if ($('#nidos').is(':checked')) {
//             // $('infopuntos').remove('#conpc');
//             document.getElementById('infolay').innerHTML = '<iframe seamless id="24pc" src="' + url + '"></iframe>';
//         }
//         // } else{
//         //     $('infopuntos').remove('#24pc');
//         // }
//         // if ($('#pconsul').is(':checked')){
//         //     $('infopuntos').remove('#24pc');
//         //     document.getElementById('infopuntos').innerHTML = '<iframe seamless id="conpc" src="' + urlin + '"></iframe>';
//         // } else{
//         //     $('infopuntos').remove('#conpc');
//         // }
//         });
//         map.on('pointermove', function (evt) {
//             if (evt.dragging) {
//                 return;
//             }
//             var pixel = map.getEventPixel(evt.originalEvent);
//             var hit = map.forEachLayerAtPixel(pixel, function () {
//                 return true;
//             });
//             map.getTargetElement().style.cursor = hit ? 'pointer' : '';
//             });
//         }
//     infopuntoslayer();
//     // ipunt.style.display = "initial";
//     $("#fig1").css({"box-shadow": "0px 0px 15px #1689e3", "border-radius": "10px",  "border": "2px solid", "border-color": "#189907", "background": "white"});           
// } else {
//     document.getElementById('infolay').innerHTML = '';
//     map.on('pointermove', function (evt) {
//         if (evt.dragging) {
//             return;
//         }
//         var pixel = map.getEventPixel(evt.originalEvent);
//         var hit = map.forEachLayerAtPixel(pixel, function () {
//             return true;
//         });
//         map.getTargetElement().style.cursor = hit ? 'default' : '';
//         });
//     /**alert("Ahora se destruira funcion");*/
//     // ipunt.style.display = "none";
//     // document.getElementById('infolayer').innerHTML = '';
//     // document.getElementById('infopuntos1').innerHTML = '';
//     $("#fig1").css({"box-shadow": "none", "border": "none"});
// }


function moreinfo(){
    //Sargazo
    $('#moreinfos').click(function(){
        if($(this).is(':checked')){
            $('#mis').html('Detección de polígonos de sargazo mediante el sensor MSI / Sentinel-2.<br>'+
                'Resolución temporal: 5 días.<br>'+
                'Intervalo de datos: 2015 - actual.<br>'+
                'Resolución espacial: 20 metros.<br>'+
                'Fuente: LANOT')
        }else{
            $('#mis').html('');
        }
    })
    //Límites y estados
    $('#moreinfol').click(function(){
        if($(this).is(':checked')){
            $('#mil').html('Es un mapa que representa los límites de los Estados y el contorno<br>'+
            'de la República Mexicana, a escala 1:1000000.<br>'+
            'Fuente: Comisión Nacional para el Conocimiento y Uso de la <br>'+
            'Biodiversidad (2005).<br>')
        }else{
            $('#mil').html('');
        }
    })
    //Área de estudio
    // $('#moreinfoa').click(function(){
    //     if($(this).is(':checked')){
    //         $('#mia').html('Es un mapa que representa los límites de los Estados y el contorno<br>'+
    //             'de la República Mexicana, a escala 1:1000000.<br>'+
    //             'Fuente: Comisión Nacional para el Conocimiento y Uso de la <br>'+
    //             'Biodiversidad (2005).<br>')
    //     }else{
    //         $('#mil').html('');
    //     }
    // })
    //Zona de estudio
    $('#moreinfoe').click(function(){
        if($(this).is(':checked')){
            $('#mie').html('Zona de estudio que abarca los siguientes cuadrantes de la malla de<br>'+
                'barrido de Sentinel-2 de acuerdo a la nomenclatura utilizada:<br>'+
                'T16QDJ,T16QEJ,T16QDH,T16QEH,T16QDG,T16QEG,T16QDF,T16QEF.<br>'+
                'Fuente: Copernicus EU.<br>')
        }else{
            $('#mie').html('');
        }
    })

    //Tiles de sentinel-2
    $('#moreinfotiles').click(function(){
        if($(this).is(':checked')){
            $('#micuad').html('Zona de estudio que abarca los siguientes cuadrantes de la malla de<br>'+
                'barrido de Sentinel-2 de acuerdo a la nomenclatura utilizada:<br>'+
                'T16QDJ,T16QEJ,T16QDH,T16QEH,T16QDG,T16QEG,T16QDF,T16QEF.<br>'+
                'Fuente: Copernicus EU.<br>')
        }else{
            $('#micuad').html('');
        }
    })

    //Linea de costa
    $('#moreinfol').click(function(){
        if($(this).is(':checked')){
            $('#milinea').html('Línea de costa vectorizada a partir de imágenes 2021 de Sentinel-2.<br>'+
            'Resolución espacial: 1:20000<br>'+
            'Fuente: LANOT'
            )
        }else{
            $('#milinea').html('');
        }
    })

    //True color
    $('#moreinfotrue').click(function(){
        if($(this).is(':checked')){
            $('#mitrue').html('Compuesto RGB en color verdadero, proveniente del producto TCI <br>'+
                'generado por el software sen2cor de la ESA. Utiliza las bandas 2, 3 y 4.<br>'+
                'Resolución temporal: 5 días.<br>'+
                'Intervalo de datos: Ultimo.<br>'+
                'Resolución espacial: 10 metros.<br>'+
                'Fuente: Copernicus EU.')
        }else{
            $('#mitrue').html('');
        }
    })

    //Sargazo compuesto
    $('#moreinfosar').click(function(){
        if($(this).is(':checked')){
            $('#misar').html('Compuesto RGB que utiliza las bandas 8A, 5 y 4. El uso de las<br>'+
                'mismas en el infrarrojo cercano permite discriminar mejor el sargazo.<br>'+
                'Resolución temporal: 5 días.<br>'+
                'Intervalo de datos: Ultimo.<br>'+
                'Resolución espacial: 20 metros.<br>'+
                'Fuente: Copernicus EU.')
        }else{
            $('#misar').html('');
        }
    })
    //Goes
    $('#moreinfogoes').click(function(){
        if($(this).is(':checked')){
            $('#migoes').html('La serie GOES-R proporciona a los pronosticadores una temperatura<br>'+
                'de la superficie del mar (SST) para cada píxel libre de nubes sobre <br>'+
                'el agua identificado por el ABI. El algoritmo SST empleado en la <br>'+
                'serie GOES-R utiliza la recuperación de regresión física híbrida<br>'+
                'para producir un producto más preciso.<br>'+
                'Resolución temporal: 1 hora.<br>'+
                'Intervalo de datos: Ultimo.<br>'+
                'Resolución espacial: 2 kilómetros.<br>'+
                'Fuente: GeonetCast.')
        }else{
            $('#migoes').html('');
        }
    })
    //Hycom direccion
    $('#moreinfohycom').click(function(){
        if($(this).is(':checked')){
            $('#mihycom').html('El modelo oceánico de coordenadas híbridas (HYCOM) es un modelo oceánico de coordenadas isopícnal-sigma-presión (generalizado) híbrido asimilativo de datos. <br>'+
            'Resolución temporal: 3 hrs.<br>'+
            'Intervalo de datos: Ultimo<br>'+
            'Resolución espacial: 0.04°, 0.08°<br>'+
            'Fuente: HYCOM')
        }else{
            $('#mihycom').html('');
        }
    })

    //Hycom velocidad
    $('#moreinfohycomvel').click(function(){
        if($(this).is(':checked')){
            $('#mihycomvel').html('El modelo oceánico de coordenadas híbridas (HYCOM) es un modelo oceánico de coordenadas isopícnal-sigma-presión (generalizado) híbrido asimilativo de datos. <br>'+
            'Resolución temporal: 3 hrs.<br>'+
            'Intervalo de datos: Ultimo<br>'+
            'Resolución espacial: 0.04°, 0.08°<br>'+
            'Fuente: HYCOM')
        }else{
            $('#mihycomvel').html('');
        }
    })

}



////////////////////////////////////////////////////////////////POOPUP/////////////////////////////////

function popup(){
    
    $('#fch4').click(function(){
        if($(this).is(':checked')){
            // Select  interaction
            select = new ol.interaction.Select({
                hitTolerance: 5,
                multi: true,
                condition: ol.events.condition.singleClick
            });
            attribu = []
            map.addInteraction(select);

                        
            atts = ['NOMBRE','ID_ANP','CAT_DECRET', 'CAT_MANEJO', 'ESTADOS', 'MUNICIPIOS', 'PRIM_DEC','HECTAREA','DESCRIPCION','SUELO','VEGETACION','USO']
            popups = new ol.Overlay.PopupFeature({
                popupClass: 'default anim',
                select: select,
                canFix: true,
                template: {
                    title: 
                    function(f){
                        attribu = []
                        attp=f.getKeys()
                        // console.log(attp);
                        for(i in atts){
                            // console.log(atts[i]);
                            for(j in attp){
                                // console.log(attp[j]);
                                if(atts[i] == attp[j]){
                                    console.log(atts[i]+'='+attp[j]);
                                    attribu.push("'"+atts[i]+"':{title:"+"'"+attp[j]+"'}")
                                    
                                }
                            } 
                        } attribu = attribu.toString();
                        console.log( f.getProperties());
                        return f.get('NOMBRE');
                    },
                    attributes:+attribu
                    
                }
            });
            map.addOverlay(popups);

        }else{
            // $('.ol-popup').css('display','none')
            map.removeOverlay(popups);
            map.removeInteraction(select)
        }
        
    })
}



