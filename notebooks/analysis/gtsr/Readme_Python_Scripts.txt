Bespreekpunten:
- advies aan Fedor: werk in de zeespiegelmonitor verder met het model met wind, maar laat het model met storm surge schaduw draaien
Overwegingen hierbij zijn:
> het model presteert op de data vanaf 1979 iets beter dan het model met wind 
> het voordeel is dat de fysische vertaalslag van wind naar opzet in mm is gemaakt, de correlatie tussen storm surge en zeespiegel is hoog (0,9)  
> het nadeel van het model met storm surge is dat de storm surges pas vanaf 1979 beschikbaar zijn, de wind is beschikbaar vanaf 1948 -> het model met wind presteert over de periode 1890-2016 beter dan het model met storm surge (tot respectievelijk 1948 en 1979 worden dan gemiddelde waarden gebruikt)
> Overweging: het model met storm surge is mogelijk gevoeliger voor trendbreuken in de parameters vanwege de beschikbaarheid van storm surge gegevens vanaf 1979 

- get_data is een ipynb bevat nu i/o routines en definieert het regressiemodel.
Kwestie: schrijven we een aparte module met functionaliteit om data en modellen in te lezen? En zo ja, waar zetten we die module dan neer?

- surge_data: hoe maken we deze data beschikbaar voor de gebruiker?

- wind_data: wij bepalen de kwadraten van de windcomponenten op maandbasis (uit de maandelijks gemiddelde u en v componenten) en vertalen later de maandgemiddelde kwadratische componenten naar jaargemiddelde waarden.
Mogelijk kan de eerste stap worden verbeterd als we de windcomponenten op dagbasis bepalen.

Trendbreuk:
- Bayesiaanse modelschatting (MCMC) wijst een trendbreuk uit aan het eind van de 20e eeuw. Mediaan vs. highest Posterior density.
- ...

Modeldiagnostiek
In zeespiegelmonitor alleen de eindversie of ook de modeldiagnostiek? Momenteel is de modeldiagnostiek beperkt en wordt of met of zonder AR(1) term gewerkt. De AR(1) term is niet zichtbaar in de resultaten.

- Autocorrelatie: in de zeespiegelmonitor wordt dit via GLSAR met onzichtbare AR(1) term meegenomen. Python kent in tegenstelling tot R niet een aparte, veel gebruikte en geciteerde ARMAX module. 
Alternatief is OLS met robuuste standaardfouten (HAC, corrigeert ook voor aanwezige heteroskedasticiteit). 

- Heteroskedasticiteit: in de zeespiegelmonitor worden de standaardfouten niet robuust geschat. Voorstel: covtype = 'HC0', maar GLSAR staat dit niet toe.

Voorstellen: 
- AR(1) term tonen.
- modellen met heteroscedasticiteit robuuste standaard fouten schatten (HC0 als AR term is opgenomen, HAC anders)

Vergelijking satellietdata
- we gebruiken nog geen wind

