all: dsea.12mgrid_512.nc dsea.12mgrid_512-center-0.tiff

dsea.12mgrid_512.nc:
	wget -c -nd http://www.atmosp.physics.utoronto.ca/~peltier/datasets/Ice6G_C_VM5a_O512/dsea.12mgrid_512.nc

dsea.12mgrid_512-center-0.tiff: dsea.12mgrid_512.nc
	gdal_translate -a_srs EPSG:4326 dsea.12mgrid_512.nc dsea.12mgrid_512.tiff
	gdalwarp -t_srs WGS84 dsea.12mgrid_512.tiff dsea.12mgrid_512-center-0.tiff  -wo SOURCE_EXTRA=1000 --config CENTER_LONG 0
