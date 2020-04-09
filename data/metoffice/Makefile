all: EN.4.2.1.analyses.g10.download-list.txt

EN.4.2.1.analyses.g10.download-list.txt:
	wget https://www.metoffice.gov.uk/hadobs/en4/EN.4.2.1.analyses.g10.download-list.txt


# The next steps include something like
# 24142  mv ~/Downloads/density_teos10_EN421f_analysis_g10 .
# 24143  gdal_translate density_teos10_EN421f_analysis_g10/density_teos10_en4_1900.nc density_teos10_en4_1900.tiff
# 24144  workon main
# 24145  earthengine
# 24146  earthengine   upload  --help
# 24147  earthengine   upload  image
# 24148  earthengine   upload  image --help
# 24149  gdalinfo density_teos10_en4_1900.tiff
# 24150  gdal_translate --help density_teos10_EN421f_analysis_g10/density_teos10_en4_1900.nc density_teos10_en4_1900.tiff
# 24151  gdal_translate density_teos10_EN421f_analysis_g10/density_teos10_en4_1900.nc  -a_srs  EPSG:4326  density_teos10_en4_1900.tiff
# 24152  gsutil
# 24153  gcloud projects
# 24154  gcloud projects list
# 24155  gsutil ls sea-level-rise-11202746-010
# 24156  gsutil ls gs://slr
# 24157  gsutil ls gs://slr/metoffice
# 24158  gsutil mkdir gs://slr/metoffice
# 24159  gsutil --help
# 24160  gsutil cp -r   density_teos10_EN421f_analysis_g10/ gs://slr/metoffice/density_teos10_EN421f
# 24161  gsutil cp -r   density_teos10_EN421f_analysis_g10/ gs://slr/metoffice/density_teos10_en4
# 24162  cd density_teos10_EN421f_analysis_g10/
# 24163  for f in *.nc; do gdal_translate -a_srs EPSG:4326 $f $f.tiff;  done
# 24164  e .
# 24165  gsutil -m cp -r   *.tiff gs://slr/metoffice/density_teos10_en4/
