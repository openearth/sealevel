Bespreekpunten:
- Keuze voor Fedor:
> Welk model gaan we mee verder. Op zich is het model met storm surge minstens net zo goed als het model met windopzet, maar de databeschikbaarheid vanaf 1979 reduceert de prestaties iets.
Overweging: model met storm surge is misschien niet zo handig om te gebruiken bij het zoeken naar trendbreuken vanwege de beschikbaarheid van storm surge gegevens vanaf 1979 
	

- get_data is een ipynb bevat nu i/o routines en definieert het regressiemodel.
Kwestie: schrijven we een aparte module met functionaliteit om data en modellen in te lezen? En zo ja, waar zetten we die module dan neer?

- surge_data: hoe maken we deze data beschikbaar voor de gebruiker?

- wind_data: wij bepalen de kwadraten van de windcomponenten main en perp op maandelijkse basis (uit de maandelijks gemiddelde u en v componenten) en vertalen later de maandgemiddelde kwadratische componenten naar jaargemiddelde waarden.
Mogelijk kan de eerste stap worden verbeterd als we de windcomponenten main en perp op dagbasis bepalen.