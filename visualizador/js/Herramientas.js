$(document).ready(searchsargazo);
$(document).ready(boxselection);
$(document).ready(medir);
$(document).ready(changecolor);
$(document).ready(displaycircle);
$(document).ready(tableatt);
$(document).ready(histograma);
$(document).ready(catalogotc);
$(document).ready(catalogosargazo);

//--------------------------------------------------------------------------------------------------------------
//función para busqueda de sargazo
function searchsargazo(){
    //Función para buscar fecha y mostrar en mapa
    $('.botton-Buscar').click(function(){
                            
        fecha_1 = $("#date3").val();
        fecha_2 = $("#date4").val();
        
        switch (true){
            case fecha_1 == '' && fecha_2 == '':
            swal('Por favor selecciona una fecha de inicio y de termino para realizar tu consulta');
            break;

            case fecha_1 == '':
            swal('Faltó ingresar la fecha inicial de su consulta.');
            break;

            case fecha_2 == '':
            swal('Faltó ingresar la fecha de termino de su consulta.');
            break;

            case fecha_2 < fecha_1:
            swal('Su fecha de termino es menor que la de inicio.');
            break;

            default:
            swal('Tu consulta comprende de: '+fecha_1+' a '+fecha_2);
            
                            
            cql_filter = "fechadia between '"+fecha_1+"' and '"+fecha_2+"'";
            
            wmsLayersargazo.getSource().updateParams({'LAYERS': 'sargazo:sargazo', 'CQL_FILTER': cql_filter});
            $('#fecha-sargazo').html(fecha_1+" al "+fecha_2);
            
            conta =1;
            

        //Función de descarga botton-Json    
        $('.botton-Json').click(function(){
        if (fecha_1 == '' && fecha_2 == ''){
            swal('Por favor selecciona una fecha de inicio y de termino para realizar tu descarga.');
        } else if(fecha_1 == '' || fecha_2 == ''){
            swal('Revisa por favor las fechas de tu consulta, para realizar la descarga.')    
        } else{
            url=('http://132.247.103.145:8080/geoserver/fires/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=fires:puntos_d&viewparams=f:'+fecha_1+ ';f1:'+fecha_2+ '&outputFormat=application/json')
            swal("Usted descargará el archivo en formato GeoJson.");
            return  window.location = url
        }
        });

        //Función de descarga CSV    
        $('.botton-CSV').click(function(){
        if (fecha_1 == '' && fecha_2 == ''){
            swal('Por favor selecciona una fecha de inicio y de termino para realizar tu descarga.');
        } else if(fecha_1 == '' || fecha_2 == ''){
            swal('Revisa por favor las fechas de tu consulta, para realizar la descarga.')    
        } else{
            url=('http://132.247.103.145:8080/geoserver/fires/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=fires:puntos_d&viewparams=f:'+fecha_1+ ';f1:'+fecha_2+ '&outputFormat=CSV')
            swal("Usted descargará el archivo en formato Archivo delimitado por comas (CSV).");
            return  window.location = url
        }
        });

        //Función de descarga SHP    
        $('.botton-Shape').click(function(){
        if (fecha_1 == '' && fecha_2 == ''){
            swal('Por favor selecciona una fecha de inicio y de termino para realizar tu descarga.');
        } else if(fecha_1 == '' || fecha_2 == ''){
            swal('Revisa por favor las fechas de tu consulta, para realizar la descarga.')    
        } else{
            url=('http://132.247.103.145:8080/geoserver/fires/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=fires:puntos_d&viewparams=f:'+fecha_1+ ';f1:'+fecha_2+ '&outputFormat=shape-zip')
            swal("Usted descargará el archivo en formato Shapefile comprimido en .ZIP .");
            return  window.location = url
        }
        });                     

        }
        
        
        return ;
        
    });


    //Función busqueda por área
    $('#ejecutar').click(function(){
        signo = $('#mayormenor').val();
        area = $('#area').val();
        cql_filter = "fecha between '"+fecha_1+"' and '"+fecha_2+"' and area_km2"+signo+""+area;
        swal('Su consulta corresponde a las fechas: '+fecha_1+' y '+fecha_2+'. Área'+signo+''+area+' kilómetros cuadrados.');       
        wmsLayersargazo.getSource().updateParams({'LAYERS': 'sargazo:sargazo', 'CQL_FILTER': cql_filter});
        $.ajax({
            type: "GET",
            url: 'http://132.247.103.145/lanot/sargazo/visualizador/',
            data: {
                "fecha_1": fecha_1,
                "fecha_2": fecha_2, 
            },
            dataType: "json",
            success: function (data) {       
                console.log(data.areaT);
                console.log(data.areaF);
                //alert('AREA:'+data.areaT);  
                document.getElementById("areaS").innerHTML = data.areaT + " km2";
                document.getElementById("areaF").innerHTML = data.areaF + " km2";
                document.getElementById("areaF_f").innerHTML =  fecha_1+'/'+fecha_2;                                           
            },
            error: function (error) {
                console.log(error);
            }
        });
    })


            
}



    //----------------------------------------Box Selection------------------------------------------------------------------

    function boxselection(){
        //Función de rectángulo
        
        $('#fch3').click(function(){
            if($(this).is(':checked')){
                $('.areaSelect').animate({right: '5em'});
                //Creamos el layer del recuadro
                vectorec = new ol.layer.Vector({
                    name: 'Vecteur',
                    source: new ol.source.Vector(),
                    style: new ol.style.Style({
                        fill: new ol.style.Fill({
                        color: 'rgba(255, 255, 255, 0.2)',
                        }),
                        stroke: new ol.style.Stroke({
                        color: '#ffcc33',
                        width: 2,
                        zIndex: 2.0
                        }),
                        
                    }),
                });

                //Agregamos el recuadro
                map.addLayer(vectorec);

                //Creamos interacción del boxcontrol
                intera = new ol.interaction.DrawRegular({
                    source: vectorec.getSource(),
                    sides:10
                })

                //Agregamos la interacción del boxcontrol
                map.addInteraction(intera);

                //Borramos el anterior boxcontrol
                intera.on('drawing', function(event){
                    vectorec.getSource().clear();
                })

                //Crea el nuevo layer y manda las coordenadas mediante ajax
                intera.on('drawend', function (event) {
                    //Creamos el objeto a con coordenadas 4326
                    var a = event.feature.getGeometry().transform('EPSG:3857','EPSG:4326').getCoordinates();
                    //Creamos el objeto b con coordenadas 3857 para que se muestre el box
                    var b = event.feature.getGeometry().transform('EPSG:4326','EPSG:3857').getCoordinates();
                    //Condicional si se realizó ya una consulta por fechas 
                    if(conta==1){
                        cql_filter = "fechadia between '"+fecha_1+"' and '"+fecha_2+"'";
                        wmsLayersargazo.getSource().updateParams({'LAYERS': 'sargazo:sargazo',  'CQL_FILTER': cql_filter});
                        // Prueba de envio a django

                        //Cambiar el URL antes de hacer el commit 'http://132.247.103.145/LANOT_pagina/sargazo/visualizador_sargazo/'
                        $.ajax({
                            type: "GET",
                            url: 'http://132.247.103.145/lanot/sargazo/visualizador/', 
                            data: {
                                "result": a,
                                "fecha_1": fecha_1,
                                "fecha_2": fecha_2, 
                            },
                            dataType: "json",
                            success: function (data) {       
                                dat = JSON.parse(data.infotab)
                                console.log(dat)
                                // km2  
                                document.getElementById("areaS").innerHTML = data.areaT + " km2";
                                document.getElementById("areaF").innerHTML = data.areaF + " km2";
                                // hectareas
                                document.getElementById("areaS_h").innerHTML = data.areaT_h + " ha";
                                document.getElementById("areaF_h").innerHTML = data.areaF_h + " ha";
                                document.getElementById("areaF_f").innerHTML =  fecha_1+'/'+fecha_2; 
                                $("tbody").html('');
                                for (i = 0; i < dat.length; i++){
 
                                    $("tbody").append('<tr>' + 
                                        '<td align="center" style="dislay: none;">' + dat[i].id + '</td>'+
                                        '<td align="center" style="dislay: none;">' + dat[i].idpoligono + '</td>'+
                                        '<td align="center" style="dislay: none;">' + dat[i].tile + '</td>'+
                                        '<td align="center" style="dislay: none;">' + dat[i].fecha + '</td>'+
                                        '<td align="center" style="dislay: none;">' + dat[i].fechadia + '</td>'+
                                        '<td align="center" style="dislay: none;">' + dat[i].area_km2 + '</td>'+
                                        '<td align="center" style="dislay: none;">' + dat[i].distcost_km + '</td>'+'</tr>');
                                }
                                                                            
                            },
                            error: function (error) {
                                console.log(error);
                            }
                        });
                        
                    }else{ //Si no se realizó consulta se muestra la última fecha
                        
                        conta=0;
                        
                        // Prueba de envio a django
                        $.ajax({
                            type: "GET",
                            url: 'http://132.247.103.145/lanot/sargazo/visualizador/',
                            data: {
                                "result": a,
                                "fecha_1": fecha_1,
                                "fecha_2": fecha_2, 
                            },
                            dataType: "json",
                            success: function (data) {       
                                // console.log(data.areaT);
                                // console.log(data.areaF);
                               
                                dat = JSON.parse(data.infotab)
                                dats = JSON.parse(data.infotabcom)
                                // console.log(dat)
                                console.log(dats)
                                
                                // km2  
                                document.getElementById("areaS").innerHTML = data.areaT + " km2";
                                document.getElementById("areaF").innerHTML = data.areaF + " km2";
                                // hectareas
                                document.getElementById("areaS_h").innerHTML = data.areaT_h + " ha";
                                document.getElementById("areaF_h").innerHTML = data.areaF_h + " ha";                                
                                document.getElementById("areaF_f").innerHTML = cql_date.substr(-10);
                                $("tbody").html('');
                                for (i = 0; i < dat.length; i++){
 
                                    $("tbody").append('<tr>' + 
                                        '<td align="center" style="dislay: none;">' + dat[i].id + '</td>'+
                                        '<td align="center" style="dislay: none;">' + dat[i].idpoligono + '</td>'+
                                        '<td align="center" style="dislay: none;">' + dat[i].tile + '</td>'+
                                        '<td align="center" style="dislay: none;">' + dat[i].fecha + '</td>'+
                                        '<td align="center" style="dislay: none;">' + dat[i].fechadia + '</td>'+
                                        '<td align="center" style="dislay: none;">' + dat[i].area_km2 + '</td>'+
                                        '<td align="center" style="dislay: none;">' + dat[i].distcost_km + '</td>'+'</tr>');
                                }
                                          
                            },
                            error: function (error) {
                                console.log(error);
                            }
                        });
                    }
                    
            
                    
                });//cierre drawend
                $('#fch7').prop('checked', true)
                $('#infolayer').css('display','block');
            }else{//Se da click para ocultar función
                $('.areaSelect').animate({right: '-100%'});
                $('#fch7').prop('checked', false)
                $('#infolayer').css('display','none');
                map.removeInteraction(intera);
                map.removeLayer(vectorec);
                $("tbody").html(function(){
                    for (i = 0; i < dats.length; i++){
 
                        $("tbody").append('<tr>' + 
                            '<td align="center" style="dislay: none;">' + dats[i].id + '</td>'+
                            '<td align="center" style="dislay: none;">' + dats[i].idpoligono + '</td>'+
                            '<td align="center" style="dislay: none;">' + dats[i].tile + '</td>'+
                            '<td align="center" style="dislay: none;">' + dats[i].fecha + '</td>'+
                            '<td align="center" style="dislay: none;">' + dats[i].fechadia + '</td>'+
                            '<td align="center" style="dislay: none;">' + dats[i].area_km2 + '</td>'+
                            '<td align="center" style="dislay: none;">' + dats[i].distcost_km + '</td>'+'</tr>');
                    }
                });
                
            }
        })//cierre click fig
    }//cierre función general


//---------------------------------------------------------------------Medir distancia y área-------------------------------------------

    //función para distancia y área

    function medir(){
        
        $('#fch2').click(function(){
            if($(this).is(':checked')){
                // alert("se encendió");
                $('.medir').animate({right: '5em'});

                const source = new ol.source.Vector();

                vector = new ol.layer.Vector({
                    source: source,
                    style: new ol.style.Style({
                        fill: new ol.style.Fill({
                        color: 'rgba(255, 255, 255, 0.2)',
                        }),
                        stroke: new ol.style.Stroke({
                        color: '#ffcc33',
                        width: 2,
                        zIndex: 2.0
                        }),
                        
                    }),
                });

                /**
                 * Currently drawn feature.
                 * @type {import("../src/ol/Feature.js").default}
                 */
                var sketch;

                /**
                 * The help tooltip element.
                 * @type {HTMLElement}
                */
                let helpTooltipElement;

                /**
                 * Overlay to show the help messages.
                 * @type {Overlay}
                 */
                let helpTooltip;

                /**
                 * The measure tooltip element.
                 * @type {HTMLElement}
                 */
                let measureTooltipElement;

                /**
                 * Overlay to show the measurement.
                 * @type {Overlay}
                 */
                let measureTooltip;

                /**
                 * Message to show when the user is drawing a polygon.
                 * @type {string}
                 */
                const continuePolygonMsg = 'Click para continuar al polygono';

                /**
                 * Message to show when the user is drawing a line.
                 * @type {string}
                 */
                const continueLineMsg = 'Click para continuar la línea';

                /**
                 * Handle pointer move.
                 * @param {import("../src/ol/MapBrowserEvent").default} evt The event.
                 */
                const pointerMoveHandler = function (evt) {
                if (evt.dragging) {
                    return;
                }
                /** @type {string} */
                helpMsg = 'Click para comenzar';

                if (sketch) {
                    const geom = sketch.getGeometry();
                    if (geom instanceof ol.geom.Polygon) {
                    helpMsg = continuePolygonMsg;
                    } else if (geom instanceof ol.geom.LineString) {
                    helpMsg = continueLineMsg;
                    }
                }

                helpTooltipElement.innerHTML = helpMsg;
                helpTooltip.setPosition(evt.coordinate);

                helpTooltipElement.classList.remove('hidden');
                };

                
                map.on('pointermove', pointerMoveHandler);

                map.getViewport().addEventListener('mouseout', function () {
                helpTooltipElement.classList.add('hidden');
                });

                const typeSelect = document.getElementById('type');

                

                /**
                 * Format length output.
                 * @param {LineString} line The line.
                 * @return {string} The formatted length.
                **/
                const formatLength = function (line) {
                const length = ol.sphere.getLength(line);
                let output;
                if (length > 100) {
                    output = Math.round((length / 1000) * 100) / 100 + ' ' + 'km';
                } else {
                    output = Math.round(length * 100) / 100 + ' ' + 'm';
                }
                return output;
                };

                /**
                 * Format area output.
                 * @param {Polygon} polygon The polygon.
                 * @return {string} Formatted area.
                 */
                const formatArea = function (polygon) {
                const area = ol.sphere.getArea(polygon);
                let output;
                if (area > 10000) {
                    output = Math.round((area / 1000000) * 100) / 100 + ' ' + 'km<sup>2</sup>';
                } else {
                    output = Math.round(area * 100) / 100 + ' ' + 'm<sup>2</sup>';
                }
                return output;
                };

                //let dibujo; // global so we can remove it later
                function addInteractions() {
                    const type = typeSelect.value == 'area' ? 'Polygon' : 'LineString';
                    dibujo = new ol.interaction.Draw({
                        source: source,
                        type: type,
                        style: new ol.style.Style({
                        fill: new ol.style.Fill({
                            color: 'rgba(255, 255, 255, 0.2)',
                        }),
                        stroke: new ol.style.Stroke({
                            color: 'rgba(0, 0, 0, 0.5)',
                            lineDash: [10, 10],
                            width: 2,
                        }),
                        image: new ol.style.Circle({
                            radius: 5,
                            stroke: new ol.style.Stroke({
                            color: 'rgba(0, 0, 0, 0.7)',
                            }),
                            fill: new ol.style.Fill({
                            color: 'rgba(255, 255, 255, 0.2)',
                            }),
                        }),
                        }),
                    });

                    
                    

                    createMeasureTooltip();
                    createHelpTooltip();

                    let listener;
                    dibujo.on('drawstart', function (evt) {
                        // set sketch
                        sketch = evt.feature;

                        /** @type {import("../src/ol/coordinate.js").Coordinate|undefined} */
                        let tooltipCoord = evt.coordinate;

                        listener = sketch.getGeometry().on('change', function (evt) {
                        const geom = evt.target;
                        let output;
                        if (geom instanceof ol.geom.Polygon) {
                            output = formatArea(geom);
                            tooltipCoord = geom.getInteriorPoint().getCoordinates();
                        } else if (geom instanceof ol.geom.LineString) {
                            output = formatLength(geom);
                            tooltipCoord = geom.getLastCoordinate();
                        }
                        measureTooltipElement.innerHTML = output;
                        measureTooltip.setPosition(tooltipCoord);
                        });
                    });

                    dibujo.on('drawend', function () {
                        measureTooltipElement.className = 'ol-tooltip ol-tooltip-/static';
                        measureTooltip.setOffset([0, -7]);
                        // unset sketch
                        sketch = null;
                        // unset tooltip so that a new one can be created
                        measureTooltipElement = null;
                        createMeasureTooltip();
                        ol.Observable.unByKey(listener);
                    });

                    map.addInteraction(dibujo);

                    return dibujo;
                }

                /**
                 * Creates a new help tooltip
                 */
                function createHelpTooltip() {
                    if (helpTooltipElement) {
                        helpTooltipElement.parentNode.removeChild(helpTooltipElement);
                    }
                        helpTooltipElement = document.createElement('div');
                        helpTooltipElement.className = 'ol-tooltip hidden';
                        helpTooltip = new ol.Overlay({
                            element: helpTooltipElement,
                            offset: [15, 0],
                            positioning: 'center-left',
                    });
                    map.addOverlay(helpTooltip);
                }

                /**
                * Creates a new measure tooltip
                */
                function createMeasureTooltip() {
                if (measureTooltipElement) {
                    measureTooltipElement.parentNode.removeChild(measureTooltipElement);
                }
                measureTooltipElement = document.createElement('div');
                measureTooltipElement.className = 'ol-tooltip ol-tooltip-measure';
                measureTooltip = new ol.Overlay({
                    element: measureTooltipElement,
                    offset: [0, -15],
                    positioning: 'bottom-center',
                    stopEvent: false,
                    insertFirst: false,
                });
                map.addOverlay(measureTooltip);
                
                }
                
                /**
                * Let user change the geometry type.
                */
                typeSelect.onchange = function () {
                    map.removeInteraction(dibujo);
                                                           
                    // //Agregamos la función para el nuevo tipo de selección
                    addInteractions();
                                        
                }
                
                addInteractions();
                map.addLayer(vector);
                
            } else {
                //Ocultamos el div
                $('.medir').animate({right: '-100%'});
                //Removemos vector y hiddentooltip
                map.removeInteraction(dibujo);
                map.removeLayer(vector);
                $('.ol-tooltip').html('');
                $('.ol-overlay-container').html('');
                    
               
            }

            

        })
    }
 /******************************************Función de cambio de color en circulo ******************************************************/

function changecolor(){
    if (fechasarg == fechapaso){
        $('circle').css('fill','red')
        // $('#infosemaforo').title('Se detectó sargazo.')

    }else{
        $('circle').css('fill','#00FF4D')
        // $('#infosemaforo').title('No se detectó sargazo.')
    }
}

/**********************************************************Función display color del circulo *******************************************************/

function displaycircle(){
    $('#fch5').click(function(){
        if($(this).is(':checked')){
            $('#ultimopaso').css('display','block');
        }else{
            $('#ultimopaso').css('display','none');
        }
    });
}

/********************************************************Función para ocultar tabla de atributos  *********************************/

function tableatt(){
    $('#fch7').click(function(){
        if($(this).is(':checked')){
            $('#infolayer').css('display','block');
        }else{
            $('#infolayer').css('display','none');
        }
    });
}

/**********************************************************Función para estadísticas ****************************************/


function histograma(){
    $('#fch6').click(function(){
        if($(this).is(':checked')){
            $('.estadistica').css('display','block');
            $('#body-grapper').css('display','block');
        }else{
            $('.estadistica').css('display','none');
            $('#body-grapper').css('display','none');
        }
    });
}

/******************************************************Función buscar catalogo TC ***************************************/

function catalogotc(){
     
    cql_datetc= $("#date5").val();
    
    $('.botton-Buscartc').click(function(){
        wmsLayersargazocatalogoTC.getSource().updateParams({'LAYERS': 'sargazo:catalogo_TC', 'time': $("#date5").val()});
        alert("Su consulta corresponde a la fecha: "+$("#date5").val());
    });
}

/******************************************************Función buscar catalogo TC ***************************************/

function catalogosargazo(){
     
    cql_datetc= $("#date6").val();
    
    $('.botton-Buscarcatsargazo').click(function(){
        wmsLayersargazocatalogoSargazo.getSource().updateParams({'LAYERS': 'sargazo:catalogo_sargazo', 'time': $("#date6").val()});
        alert("Su consulta corresponde a la fecha: "+$("#date6").val());
    });
}