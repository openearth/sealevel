# AVISO data is not maintained anymore
merged.nc:
	wget -c -nd --recursive --accept '*.nc*' ftp://ftp.aviso.altimetry.fr/global/delayed-time/grids/climatology/monthly_mean/
	gunzip *.nc.gz
	for f in $(find . -name 'dt_upd_*.nc' -exec basename {} \;); do ncecat -v Grid_0001 $f record_$f; done


# The new approach is to use the data from nasa
# But this is too much work
# merged_nasa.nc:
# 	wget -c -nd --recursive --accept 'cdr_grid*'  --accept '*.nc*' ftp://podaac-ftp.jpl.nasa.gov/SeaSurfaceTopography/merged_alt/L4/cdr_grid/
# 	wget -c -nd --recursive --accept 'cdr_grid*'  --accept '*.nc*' ftp://podaac-ftp.jpl.nasa.gov/SeaSurfaceTopography/merged_alt/L4/cdr_grid_interim/
