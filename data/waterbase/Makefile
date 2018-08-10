YEAR=2018

all: latest_nc latest_txt
latest_nc: id1-IJMDNDSS.nc id1-DELFZL.nc id1-VLISSGN.nc id1-HOEKVHLD.nc id1-HARLGN.nc id1-DENHDR.nc id1-IJMDBTHVN.nc



# get the latest text files from waterbase, in case the netCDF files are not updated
latest_txt: DELFZL.txt DENHDR.txt HARLGN.txt HOEKVHLD.txt IJMDBTHVN.txt VLISSGN.txt
%.txt:
	wget -O $*-${YEAR}.txt 'http://live.waterbase.nl/wswaterbase/cgi-bin/wbGETDATA?ggt=id1&site=MIV&lang=nl&a=getData&gaverder=GaVerder&from=${YEAR}01010000&loc=$*&to=${YEAR}12312359&fmt=text'
%.nc:
	wget -c http://opendap.deltares.nl/thredds/fileServer/opendap/rijkswaterstaat/waterbase/27_Waterhoogte_in_cm_t.o.v._normaal_amsterdams_peil_in_oppervlaktewater/nc/$@
