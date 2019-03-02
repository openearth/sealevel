all: SLR_database.json

SLR_database.xlsx:
	wget -c https://github.com/AndraJGarner/SLRDatabase/raw/master/SLR_database.xlsx
SLR_database.json: SLR_database.xlsx
	./xl2json
