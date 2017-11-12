all: napinfo.json
napinfo.json:
	ogr2ogr -f geojson napinfo.json 'WFS:https://geodata.nationaalgeoregister.nl/napinfo/wfs'
