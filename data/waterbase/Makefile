YEAR=2015
all: DELFZL.txt DENHDR.txt HARLGN.txt HOEKVHLD.txt IJMDBTHVN.txt VLISSGN.txt
%.txt:
	wget -O $*-${YEAR}.txt 'http://live.waterbase.nl/wswaterbase/cgi-bin/wbGETDATA?ggt=id1&site=MIV&lang=nl&a=getData&gaverder=GaVerder&from=${YEAR}01010000&loc=$*&to=${YEAR}12312359&fmt=text'
