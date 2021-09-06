#! /bin/bash

input='/data/tmp/latest/*'
output='/home/urielm/webApp_ReporteSatelital/latest'

ssh urielm@132.247.103.145 "rm "$output"/fechas/GOES16/*"
ssh urielm@132.247.103.145 "rm "$output"/fechas/NOAA20/*"
#KAWAK
#rm $output/fechas/GOES16/*
#rm $output/fechas/NOAA20/*

input='/data/tmp/latest/*'
output='/home/urielm/webApp_ReporteSatelital/latest'

inputG16='/data/goes16/abi/vistas/rgb/conus/'
inputNOAA20='/data2/output/polar/jpss1/viirs/level2/vistas/cviirs/'

ultimoG16=`ls -t $inputG16* | head -1`
ultimoNOAA20=`ls -t $inputNOAA20* | head -1`

echo $ultimoG16
echo $ultimoNOAA20

scp $ultimoG16 urielm@132.247.103.145:$output/fechas/GOES16
scp $ultimoNOAA20 urielm@132.247.103.145:$output/fechas/NOAA20
scp $input urielm@132.247.103.145:$output
#KAWAK
#cp $ultimoG16 $output/fechas/GOES16
#cp $ultimoNOAA20 $output/fechas/NOAA20
#cp $input $output


echo $input
echo $output
echo 'Archivos copiados latest FT y TC de abi y viirs'
