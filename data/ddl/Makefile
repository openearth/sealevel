all: ddl-stations.json

ddl-stations.json: OphalenCatalogus.json
	cp OphalenCatalogus.json ddl-stations.json

OphalenCatalogus.json:
	http --json --download POST 'https://waterwebservices.rijkswaterstaat.nl/METADATASERVICES_DBO/OphalenCatalogus/' < request.json

clean:
	rm OphalenCatalogus.json ddl-stations.json
