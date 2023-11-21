all: uwnd.10m.mon.mean.nc vwnd.10m.mon.mean.nc 20cr.uwnd.10m.mon.mean.nc 20cr.vwnd.10m.mon.mean.nc amo.txt norm.nao.monthly.b5001.current.ascii sst.mnmean.nc

uwnd.10m.mon.mean.nc:
	# wget -c https://www.esrl.noaa.gov/psd/thredds/fileServer/Datasets/ncep.reanalysis.derived/surface_gauss/uwnd.10m.mon.mean.nc'
	wget -c https://psl.noaa.gov/thredds/fileServer/Datasets/ncep.reanalysis.derived/surface_gauss/uwnd.10m.mon.mean.nc
vwnd.10m.mon.mean.nc:
	# wget -c https://www.esrl.noaa.gov/psd/thredds/fileServer/Datasets/ncep.reanalysis.derived/surface_gauss/vwnd.10m.mon.mean.nc
	wget -c https://psl.noaa.gov/thredds/fileServer/Datasets/ncep.reanalysis.derived/surface_gauss/vwnd.10m.mon.mean.nc

20cr.uwnd.10m.mon.mean.nc:
	# wget -c -O 20cr.uwnd.10m.mon.mean.nc https://downloads.psl.noaa.gov/Datasets/20thC_ReanV3/Monthlies/10mSI-MO/uwnd.10m.mon.mean.nc
	wget -c -O 20cr.uwnd.10m.mon.mean.nc https://psl.noaa.gov/thredds/fileServer/Datasets/20thC_ReanV3/Monthlies/10mSI-MO/uwnd.10m.mon.mean.nc

20cr.vwnd.10m.mon.mean.nc:
	# wget -c -O 20cr.vwnd.10m.mon.mean.nc https://downloads.psl.noaa.gov/Datasets/20thC_ReanV3/Monthlies/10mSI-MO/vwnd.10m.mon.mean.nc
	wget -c -O 20cr.vwnd.10m.mon.mean.nc https://psl.noaa.gov/thredds/fileServer/Datasets/20thC_ReanV3/Monthlies/10mSI-MO/vwnd.10m.mon.mean.nc

sst.mnmean.nc:
	# wget -c ftp://ftp.cdc.noaa.gov/Datasets/noaa.ersst.v5/sst.mnmean.nc
	wget -c https://psl.noaa.gov/thredds/fileServer/Datasets/noaa.ersst.v5/sst.mnmean.nc


norm.nao.monthly.b5001.current.ascii:
	wget -c 'https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii'

amo.txt:
	wget -c https://www.esrl.noaa.gov/psd/data/correlation/amon.us.long.data
	mv amon.us.long.data amo.txt
