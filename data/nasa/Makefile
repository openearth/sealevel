all: ocean_mass.json mei.data gmsl.txt OCN_steric_height_changes_Llovel2014.csv ocean_land_temperature.csv

ocean_land_temperature.csv:
	curl https://data.giss.nasa.gov/gistemp/graphs/graph_data/Temperature_Anomalies_over_Land_and_over_Ocean/graph.csv > ocean_land_temperature.csv
gmsl.txt:
	wget -c -r -nd ftp://podaac.jpl.nasa.gov/allData/merged_alt/L2/TP_J1_OSTM/global_mean_sea_level/
	cp GMSL_TPJAOS_4.2_199209_201803.txt gmsl.txt

ocean_mass.json:
	wget -c -r -nd ftp://podaac-ftp.jpl.nasa.gov/allData/tellus/L3/mascon/RL05/JPL/CRI/mass_variability_time_series/
	./series2json
OCN_steric_height_changes_Llovel2014.csv:
	wget -c -r -nd https://sealevel-nexus.jpl.nasa.gov/data/OCN_steric_height_changes_Llovel2014.csv

mei.data:
	wget -c https://www.esrl.noaa.gov/psd/data/correlation/mei.data
clean:
	rm *.txt
	rm *.json
	rm mei.data
