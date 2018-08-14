Bespreekpunten:
- get_data is een ipynb bevat nu i/o routines en definieert het regressiemodel.
Kwestie: schrijven we een aparte module met functionaliteit om data en modellen in te lezen? En zo ja, waar zetten we die module dan neer?

- surge_data: hoe maken we deze data beschikbaar voor de gebruiker?

- wind_data: wij bepalen de kwadraten van de windcomponenten main en perp op maandelijkse basis (uit de maandelijks gemiddelde u en v componenten) en vertalen later de maandgemiddelde kwadratische componenten naar jaargemiddelde waarden.
Mogelijk kan de eerste stap worden verbeterd als we de windcomponenten main en perp op dagbasis bepalen.