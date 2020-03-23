all: ddl-stations.json

ddl-stations.json: OphalenCatalogus.json
	cp OphalenCatalogus.json ddl-stations.json

OphalenCatalogus.json:
	http --json --download POST 'https://waterwebservices.rijkswaterstaat.nl/METADATASERVICES_DBO/OphalenCatalogus/' < request.json

get_stations:
	ddlpy locations --station HOEK --station VLIS --station HOEKVHLBSD --station HOEKVHLD --station IJMDN --station DENHDR --station DELFZL --station HARLGN --station VLISSGN --station DLFZ --station DENH --station HARL --station tHOEK -g WATHTE -h NAP locations.csv

get_measurements:
	ddlpy measurements --locations locations.csv --start-date 2016-01-01 --end-date 2019-12-31

clean_stations:
	rm locations.csv

clean:
	rm OphalenCatalogus.json ddl-stations.json
