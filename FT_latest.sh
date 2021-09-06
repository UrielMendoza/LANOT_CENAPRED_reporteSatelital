#! /bin/bash

source /home/lanotadm/.bashrc

data=`ls -t /data2/output/polar/jpss1/viirs/level2/vistas/fire/*noaa20_viirs_FT* | head -1`

cp $data /data/tmp/latest/

data1=`ls -t /data/tmp/latest/*noaa20_viirs_FT* | head -1`

mv $data1 /data/tmp/latest/viirs_FT_latest.tif

echo $data
echo $data1

data2=`ls -t /data/goes16/abi/vistas/fire/conus/goes16.abi* | head -1`

cp $data2 /data/tmp/latest/

data3=`ls -t /data/tmp/latest/goes16.abi* | head -1`

mv $data3 /data/tmp/latest/abi_FT_latest.tif

echo $data2
echo $data3

data4=`ls -t /data/goes16/abi/vistas/fire/mexico_caribe/goes16.abi* | head -1`
cp $data4 /data/tmp/latest/
data5=`ls -t /data/tmp/latest/goes16.abi* | head -1`
mv $data5 /data/tmp/latest/abi_FD_FT_fires_latest.tif
echo $data4
echo $data5
