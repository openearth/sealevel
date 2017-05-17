# Note that AVISO data is not maintained anymore, possibly the delayed monthly grids
# download all files
# unzip
# convert time to record dimension
# concatenate record dimensions
# convert to netCDF4 for compression
# cleanup converted files
# cleanup year files
dt_global_allsat_msla_h_merged_nc4.nc:
	wget -c -N -nd --recursive --accept '*.nc*' ftp://ftp.aviso.altimetry.fr/global/delayed-time/grids/climatology/monthly_mean/
	gunzip -f -k *.nc.gz
	for f in `find . -name 'dt_global_*.nc' -exec basename {} \;`; do \
		ncks --mk_rec_dmn time $$f unlimited_$$f; \
	done
	ncrcat unlimited_*.nc dt_global_merged_msla_h_merged.nc
	nc3tonc4 dt_global_merged_msla_h_merged.nc  dt_global_merged_msla_h_merged_nc4.nc
	rm unlimited_*.nc
	rm dt_global_allsat_msla_h_y*
	rm dt_global_merged_msla_h_merged.nc


# The new approach is to use the data from nasa
# But this is too much work
# merged_nasa.nc:
# 	wget -c -nd --recursive --accept 'cdr_grid*'  --accept '*.nc*' ftp://podaac-ftp.jpl.nasa.gov/SeaSurfaceTopography/merged_alt/L4/cdr_grid/
# 	wget -c -nd --recursive --accept 'cdr_grid*'  --accept '*.nc*' ftp://podaac-ftp.jpl.nasa.gov/SeaSurfaceTopography/merged_alt/L4/cdr_grid_interim/
