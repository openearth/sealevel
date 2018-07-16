#!/bin/bash
# convert to vrt file
gdal_translate -of VRT NETCDF:"$1":SLA $1-outline.vrt
# add global control points (swap lat,lon)
gdal_translate -of VRT -gcp 0 0 360 -80 -gcp 960 0 360 80 -gcp 0 2160 0 -80 -gcp 960 2160 0 80 $1-outline.vrt $1-rotated.vrt
# convert using the control points
gdalwarp -r bilinear -t_srs EPSG:4326 $1-rotated.vrt $1-warped.tiff
# regrid
gdal_translate -of VRT -a_ullr 0 80 360 -80 $1-warped.tiff $1-warped.vrt
# convert to WGS84
gdalwarp -co compress=lzw -co predictor=2 -t_srs WGS84 $1-warped.vrt $1-final.tiff -wo SOURCE_EXTRA=1000 --config CENTER_LONG 0
