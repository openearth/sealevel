#!/bin/bash
# One of these attempts worked...
# 21456  earthengine
# 21457  earthengine upload --help
# 21458  earthengine upload image --help
# 21459  earthengine upload image gs://slr/osu/h_k2_tpxo9_atlas_30.tiff
# 21460  earthengine upload image --assert_id  osu/h_k2_tpxo9_atlas_30 gs://slr/osu/h_k2_tpxo9_atlas_30.tiff
# 21461  earthengine upload image --asset_id  osu/h_k2_tpxo9_atlas_30 gs://slr/osu/h_k2_tpxo9_atlas_30.tiff
# 21462  earthengine upload image --asset_id  osu/h-k2-tpxo9-atlas-30 gs://slr/osu/h_k2_tpxo9_atlas_30.tiff
# 21463  earthengine upload image --asset_id  osu/hk2tpxo9atlas30 gs://slr/osu/h_k2_tpxo9_atlas_30.tiff
# 21464  earthengine upload image --help
# 21465  earthengine upload image --asset_id  users/fbaart/osu/h_k2_tpxo9_atlas_30 gs://slr/osu/h_k2_tpxo9_atlas_30.tiff
# 21466  gdalinfo ~/Downloads/osu_h_k2_tpxo9_atlas_30.tiff
# 21467  gdalinfo ~/Downloads/osu_h_k2_tpxo9_atlas_30\ \(1\).tiff
# 21468  gdalinfo ~/Downloads/osu_u_k2_tpxo9_atlas_30_v.tiff
# 21469  ipython
# 21470  earthengine upload image --asset_id  users/fbaart/osu/h_k2_tpxo9_atlas_30 gs://slr/osu/h_k2_tpxo9_atlas_30.tiff
# 21471  earthengine upload image --asset_id  users/fbaart/osu/u_k2_tpxo9_atlas_30_u gs://slr/osu/u_k2_tpxo9_atlas_30_u.tiff
# 21472  earthengine upload image --asset_id  users/fbaart/osu/u_k2_tpxo9_atlas_30_v gs://slr/osu/u_k2_tpxo9_atlas_30_v.tiff
# 21489  gdalinfo ~/Downloads/osu_u_k2_tpxo9_atlas_30_u.tiff
# 21490  ncks -O -H --msa -v lon -d lon,0.,180. -d lon,-180.,-1.0 in.nc
# 21491  ncks -O -H --msa -v lon -d lon,0.,180. -d lon,-180.,-1.0 ./h_m2_tpxo9_atlas_30.nc
# 21492  ncdump -h h_m2_tpxo9_atlas_30.nc
# 21493  ncks -O -H --msa -v lon_z -d lon,0.,180. -d lon,-180.,-1.0 ./h_m2_tpxo9_atlas_30.nc
# 21494  ncks -O -H --msa -v lon_z -d nx,0.,180. -d nx,-180.,-1.0 ./h_m2_tpxo9_atlas_30.nc
# 21495  ncrename --overwrite -v lon_z,lon -v lat_z,lat -d ny,lat -d nx,lon ./h_m2_tpxo9_atlas_30.nc ./h_m2_tpxo9_atlas_30_lonlat.nc
# 21496  ncks -O -H --msa -v lon -d lon,0.,180. -d lon,-180.,-1.0 ./h_m2_tpxo9_atlas_30_lonlat.nc
# 21497  ncks -O -H --msa -v lon -d lon,180.,360. -d lon,0.,-.0.001 ./h_m2_tpxo9_atlas_30_lonlat.nc
# 21498  ncks -O -H --msa -v lon -d lon,180.,360. -d lon,0.,-0.001 ./h_m2_tpxo9_atlas_30_lonlat.nc
# 21499  ncks -O -H --msa -v lon -d lon,180.,360. -d lon,0.,-0.001 ./h_m2_tpxo9_atlas_30_lonlat.nc  ./h_m2_tpxo9_atlas_30_lonlat_180.n
# 21500  ncdump -h ./h_m2_tpxo9_atlas_30_lonlat_180.nc
# 21501  ncks -O -H --msa -v lon -d lon,180.,360. -d lon,0.,-0.001 ./h_m2_tpxo9_atlas_30_lonlat.nc  ./h_m2_tpxo9_atlas_30_lonlat_180.nc
# 21502  ncks -O -H --msa  -d lon,180.,360. -d lon,0.,-0.001 ./h_m2_tpxo9_atlas_30_lonlat.nc  ./h_m2_tpxo9_atlas_30_lonlat_180.nc
# 21503  ncdump -h ./h_m2_tpxo9_atlas_30_lonlat_180.nc
# 21504  ncdump -v lon ./h_m2_tpxo9_atlas_30_lonlat_180.nc  | less
# 21505  ncdump -v lon ./h_m2_tpxo9_atlas_30_lonlat.nc  | less
# 21506  ncks -O -H --msa  -d lon,180.,360. -d lon,0.,180  ./h_m2_tpxo9_atlas_30_lonlat.nc  ./h_m2_tpxo9_atlas_30_lonlat_180.nc
# 21507  ncks -O -H --msa  -d lon,180.,360. -d lon,0.,180.0  ./h_m2_tpxo9_atlas_30_lonlat.nc  ./h_m2_tpxo9_atlas_30_lonlat_180.nc
# 21508  ncdump -v lon ./h_m2_tpxo9_atlas_30_lonlat.nc  | less
# 21509  ncdump -v lon ./h_m2_tpxo9_atlas_30_lonlat_180.nc  | less/Users/baart_f/Library/Containers/com.apple.mail/Data/Library/Mail Downloads/2C845AEE-9C3E-450C-A4D6-F636C7230755/wrapper.py
# 21510  ncks -O -H --msa -v lon  -d lon,180.,360. -d lon,0.,180.0  ./h_m2_tpxo9_atlas_30_lonlat.nc  ./h_m2_tpxo9_atlas_30_lonlat_180.nc
# 21511  ncdump -v lon ./h_m2_tpxo9_atlas_30_lonlat_180.nc  | less
# 21512  ncdump -v lon ./h_m2_tpxo9_atlas_30_lonlat.nc  | less
# 21513  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.,360. -d lon,0.,180.0  ./h_m2_tpxo9_atlas_30_lonlat.nc  ./h_m2_tpxo9_atlas_30_lonlat_180.nc
# 21514  ncdump -v lon ./h_m2_tpxo9_atlas_30_lonlat.nc  | less
# 21515  ncdump -v lon ./h_m2_tpxo9_atlas_30_lonlat_180.nc  | less
# 21516  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.0,360.0 -d lon,0.0,180.0  ./h_m2_tpxo9_atlas_30_lonlat.nc  ./h_m2_tpxo9_atlas_30_lonlat_180.nc
# 21517  ncdump -v lon ./h_m2_tpxo9_atlas_30_lonlat_180.nc  | less
# 21518  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,359.75 -d lon,0.0,180.0  ./h_m2_tpxo9_atlas_30_lonlat.nc  ./h_m2_tpxo9_atlas_30_lonlat_180.nc
# 21519  ncdump -v lon ./h_m2_tpxo9_atlas_30_lonlat_180.nc  | less
# 21520  ncks -O -H --msa_usr_rdr -d lon,180.25,359.75 -d lon,0.0,180.0  ./h_m2_tpxo9_atlas_30_lonlat.nc  ./h_m2_tpxo9_atlas_30_lonlat_180.nc
# 21521  ncdump -v lon ./h_m2_tpxo9_atlas_30_lonlat_180.nc  | less
# 21522  ncdump -v lon ./h_m2_tpxo9_atlas_30_lonlat.nc  | less
# 21523  ncks -O -H --msa_usr_rdr -d lon,180.25,359.75   ./h_m2_tpxo9_atlas_30_lonlat.nc
# 21524  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,359.75   ./h_m2_tpxo9_atlas_30_lonlat.nc
# 21525  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,359.75   ./h_m2_tpxo9_atlas_30_lonlat.nc   | less
# 21526  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,359.75  -d lon,0.0,180.0 ./h_m2_tpxo9_atlas_30_lonlat.nc   | less
# 21527  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,359.75  -d lon,0.0,180.0 ./h_m2_tpxo9_atlas_30_lonlat.nc   test.nc
# 21528  ncdump test.nc | less
# 21529  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,359.75  -d lon,0.0,180.0 ./h_m2_tpxo9_atlas_30_lonlat.nc  test.nc
# 21530  ncdump test.nc
# 21531  sudo port selfupdate
# 21532  sudo port upgrade nco
# 21533  earthengine upload image --asset_id  users/fbaart/osu/u_k2_tpxo9_atlas_30_v gs://slr/osu/h_k2_tpxo9_atlas_30.tiff
# 21534  fg
# 21535  earthengine upload image --asset_id  users/fbaart/osu/u_k2_tpxo9_atlas_30_v gs://slr/osu/h_k2_tpxo9_atlas_30.tiff
# 21536  earthengine upload image --asset_id  users/fbaart/osu/u_k2_tpxo9_atlas_30_v gs://slr/osu/h_s2_tpxo9_atlas_30.tiff
# 21537  earthengine upload image --asset_id  users/fbaart/osu/h_s2_tpxo9_atlas_30_v gs://slr/osu/h_s2_tpxo9_atlas_30.tiff
# 21538  earthengine upload image --asset_id  users/fbaart/osu/h_k2_tpxo9_atlas_30 gs://slr/osu/h_k2_tpxo9_atlas_30.tiff
# 21539  earthengine upload image --asset_id  users/fbaart/osu/h_s2_tpxo9_atlas_30 gs://slr/osu/h_s2_tpxo9_atlas_30.tiff
# 21540  earthengine upload image --asset_id  users/fbaart/osu/h_mn4_tpxo9_atlas_30 gs://slr/osu/h_mn4_tpxo9_atlas_30.tiff
# 21542  earthengine upload image --asset_id  users/fbaart/osu/u_k2_tpxo9_atlas_30_v gs://slr/osu/u_k2_tpxo9_atlas_30_v.tiff
# 21543  ncdump -h -v lat h_m2_tpxo9_atlas_30.nc
# 21544  ncdump -h -v lat_z h_m2_tpxo9_atlas_30.nc
# 21545  ncdump -v lat_z h_m2_tpxo9_atlas_30.nc
# 21546  ncdump -v lat_z h_m2_tpxo9_atlas_30.nc  | less
# 21547  ncdump -v hRe h_m2_tpxo9_atlas_30.nc  | less
# 21548  earthengine upload image --asset_id  users/fbaart/osu/h_o1_tpxo9_atlas_30 gs://slr/osu/h_o1_tpxo9_atlas_30.tiff
# 21549  earthengine upload image --asset_id  users/fbaart/osu/h_k1_tpxo9_atlas_30 gs://slr/osu/h_k1_tpxo9_atlas_30.tiff
# 21550  earthengine upload image --asset_id  users/fbaart/osu/h_m2_tpxo9_atlas_30 gs://slr/osu/h_m2_tpxo9_atlas_30.tiff
# 21551  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,359.75  -d lon,0.0,180.0 ./h_m2_tpxo9_atlas_30_lonlat.nc  test.nc
# 21552  ncdump test.nc
# 21553  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,359.75  -d lon,0.0,180.0 ./h_m2_tpxo9_atlas_30_lonlat.nc  test.nc
# 21554  rm test.nc
# 21555  ncdump test.nc
# 21556  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,359.75  -d lon,0.0,180.0 ./h_m2_tpxo9_atlas_30_lonlat.nc  test.nc
# 21557  ncdump test.nc
# 21558  rm test.nc
# 21559  ncks -O -H --msa -v lon  -d lon,180.25,359.75  -d lon,0.0,180.0 ./h_m2_tpxo9_atlas_30_lonlat.nc  test.nc
# 21560  ncdump test.nc
# 21561  ncks -O -H --msa_usr_rdr -v lon   -d lon,0.0,180.0 ./h_m2_tpxo9_atlas_30_lonlat.nc  test.nc
# 21562  ncdump test.nc
# 21563  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,359.75  -d lon,0.0,180.0 ./h_m2_tpxo9_atlas_30_lonlat.nc
# 21564  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,1  -d lon,0.0,180.0 ./h_m2_tpxo9_atlas_30_lonlat.nc
# 21565  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,190.0 ./h_m2_tpxo9_atlas_30_lonlat.nc
# 21566  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,190.0 ./h_m2_tpxo9_atlas_30_lonlat.nc  a.nc
# 21567  ncdump a.nc
# 21568  ncdump a.nc
# 21569  ncks -O -H --msa_usr_rdr -v lon  -d lon,180.25,190.0 ./h_m2_tpxo9_atlas_30_lonlat.nc  a.nc
# 21570  ncdump a.nc
# 21571  wget --no-directories -c ftp://ftp.oce.orst.edu/dist/tides/TPXO9_atlas_nc/h_m2_tpxo9_atlas_30.nc
# 21572  ncrename --overwrite -v lon_z,lon -v lat_z,lat -d ny,lat -d nx,lon ./h_m2_tpxo9_atlas_30.nc ./h_m2_tpxo9_atlas_30_lonlat.nc
# 21573  ncdump -v out.nc
# 21574  ncdump -v lon out.nc
# 21575  nco --version
# 21576  ncks --version
# 21577  emacsd
# 21578  ec sync-gcs-ee.sh
# 21579  earthengine
# 21580  earthengine upload_manifest
# 21581  earthengine upload_manifest --help
# 21582  cv src/ddlpy/
# 21583  git remote -v
# 21584  gsutil ls
# 21585  less ddlpy/ddlpy.py
# 21586  e ddlpy/ddlpy.py
# 21587  earthengine upload image --asset_id  users/fbaart/osu/h_tpxo9_atlas_30/m2 gs://slr/osu/h_m2_tpxo9_atlas_30.tiff


# ncks -O  --msa_usr_rdr -v lon  -d lon,180.0,360.0 -d lon,0.0,180.0 ./h_m2_tpxo9_atlas_30_lonlat.nc  out.nc
