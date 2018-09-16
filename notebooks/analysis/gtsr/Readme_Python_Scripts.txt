Bespreekpunten:
- advies aan Fedor: werk in de zeespiegelmonitor verder met het model met storm surge
overwegingen hierbij zijn:
> het model presteert op de data vanaf 1979 iets beter dan het model met wind 
> het voordeel is dat de fysische vertaalslag van wind naar opzet in mm is gemaakt, de correlatie tussen storm surge en zeespiegel is hoog (0,9)  
> het nadeel van het model met storm surge is dat de storm surges pas vanaf 1979 beschikbaar zijn, de wind is beschikbaar vanaf 1948 -> het model met wind presteert over de periode 1890-2016 beter dan het model met storm surge (tot respectievelijk 1948 en 1979 worden dan gemiddelde waarden gebruikt)
> Overweging: het model met storm surge is mogelijk gevoeliger voor trendbreuken in de parameters vanwege de beschikbaarheid van storm surge gegevens vanaf 1979 

- get_data is een ipynb bevat nu i/o routines en definieert het regressiemodel.
Kwestie: schrijven we een aparte module met functionaliteit om data en modellen in te lezen? En zo ja, waar zetten we die module dan neer?

- surge_data: hoe maken we deze data beschikbaar voor de gebruiker?

- wind_data: wij bepalen de kwadraten van de windcomponenten main en perp op maandelijkse basis (uit de maandelijks gemiddelde u en v componenten) en vertalen later de maandgemiddelde kwadratische componenten naar jaargemiddelde waarden.
Mogelijk kan de eerste stap worden verbeterd als we de windcomponenten main en perp op dagbasis bepalen.