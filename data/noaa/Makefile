all: uwnd.10m.mon.mean.nc vwnd.10m.mon.mean.nc amo.txt nao.json sst.mnmean.nc

uwnd.10m.mon.mean.nc:
	wget -c https://www.esrl.noaa.gov/psd/thredds/fileServer/Datasets/ncep.reanalysis.derived/surface_gauss/uwnd.10m.mon.mean.nc
vwnd.10m.mon.mean.nc:
	wget -c https://www.esrl.noaa.gov/psd/thredds/fileServer/Datasets/ncep.reanalysis.derived/surface_gauss/vwnd.10m.mon.mean.nc

sst.mnmean.nc:
	wget -c ftp://ftp.cdc.noaa.gov/Datasets/noaa.ersst.v5/sst.mnmean.nc


nao.json:
	wget -c https://www.ncdc.noaa.gov/teleconnections/nao/data.json
	mv data.json nao.json

amo.txt:
	wget -c https://www.esrl.noaa.gov/psd/data/correlation/amon.us.long.data
	mv amon.us.long.data amo.txt
