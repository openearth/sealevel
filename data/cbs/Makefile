all: CBSvierkant100m_2017_v1_wgs84.zip
CBSvierkant100m_2017_v1_wgs84.zip:
	wget -c http://download.cbs.nl/regionale-kaarten/2017-CBSvierkant100m_2017v1.zip
	unzip 2017-CBSvierkant100m_2017v1.zip
	ogr2ogr -s_srs EPSG:28992  -t_srs EPSG:4326  CBSvierkant100m_2017_v1_wgs84.shp  CBSvierkant100m_2017_v1.shp
	zip CBSvierkant100m_2017_v1_wgs84.zip CBSvierkant100m_2017_v1_wgs84.*
clean:
	rm -f Statistische*.pdf
	rm -f CBS*
