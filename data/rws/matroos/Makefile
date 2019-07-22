all:


%_observed.nc: %
	
	wget -O $@ 'http://noos.matroos.rws.nl/direct/get_series.php?loc=$location&source=observed&unit=waterlevel&tstart=201701010000&tstop=201901010100&format=netcdf'	
%_surge.nc:
	wget -O $@ 'http://noos.matroos.rws.nl/direct/get_series.php?loc=hoekvanholland&source=RWS_prediction&unit=waterlevel_surge&tstart=201701010000&tstop=201901010100&format=netcdf'
	wget -O hoekvanholland.nc 'http://noos.matroos.rws.nl/direct/get_series.php?loc=hoekvanholland&source=RWS_prediction&unit=waterlevel&tstart=201701010000&tstop=201901010100&format=netcdf'
