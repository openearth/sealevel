all: ocean_mass.json
ocean_mass.json:
	wget -c -r -nd ftp://podaac-ftp.jpl.nasa.gov/allData/tellus/L3/mascon/RL05/JPL/CRI/mass_variability_time_series/
	./series2json
clean:
	rm *.txt
	rm *.json
