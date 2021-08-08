# Homeautomation

Een verzameling tools om zaken binnenshuis te kunnen automatiseren.

## Algemeen gebruik

### Randvoorwaarden
* Python > 3.6 geinstalleerd
* Influxdb > 1.8.9 geinstalleerd
* P1 naar USB kabel
* P1 protocol versie 5

### Aanpassen van de secrets.ini
In src/main/resources staat een voorbeeld (secrets.example). 
Hernoem deze naar secrets.ini en vul de juiste waardes in.

Voor beide databronnen kun je een andere database kiezen via de configuratie.

#### P1 gegevens
Behalve de database naam kun je alleen nog de port aangeven waarop de data binnen komt.

#### Weer gegevens
Voor gebruik van weerlive (knmi) gegevens:
Haal een API key op via: https://weerlive.nl/delen.php
Daar vind je ook de juiste benaming voor de locatie.

Om een of andere reden kan je op deze manier niet heerslag gevevens ophalen. 
Voor gebruik van weerhuisje.nl kun je een weerstation naam ophalen via:
https://www.mijneigenweer.nl/participants.php?langchoice=nl

Vul deze naam in bij locatie_1

# Scripts
Tot nu toe zijn er twee scripts die data ophalen en in de influxdb plaatsen, namelijk energiemeter.py en weerdata.py

## Algemene Software Architectuur
Het main script (controller) roept een sensor gateway aan, die op zijn beurt afhankelijk is van een device waar de echte meting plaatsvindt. 
De sensor gateway heeft als doel om de specifiek gemeten waardes om te zetten naar een algemene 'meetwaarde' entiteit.
De controller ontvangt deze meetwaardes en sluist die door naar de database gateway (persistence), 
die als doel heeft om de meetdata in influxdb te zetten.

Per script wordt er een database aangemaakt, en als measurement wordt uitgegaan van de eenheid van de meting.
Door middel van tags (geleverd dus door de sensor gateway, want die is bekend met de meting) 
is daarmee dan nog een specifieke selectie te maken zodat b.v. Grafana dit eenvoudig in een grafiek kan zetten.


## Energiemeter
Deze leest gegevens uit de slimme meter via de P1 poort aangesloten via een kabeltje die de data levert aan de USB poort.
Er is op dit moment alleen ondersteuning van versie 5 van het protocol 
(https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf)

Uitgaande van de root van dit project als werkdirectory kan deze als volgt worden aangeroepen:
> python src/main/python/energiemeter.py

Om te testen kun je deze ook aanroepen met optie --dryrun, dan wordt de data niet opgeslagen in de database.

De makkelijkste manier om dit geautomatiseerd aan te roepen elke minuut is via een cronjob:
``` 
* * * * * cd /home/pi/homeautomation;/home/pi/.pyenv/shims/python src/main/python/energiemeter.py >> /home/pi/cron_p1.log 2>&1
```


Op deze manier log je gelijk in de home directory.

## Weerdata
Deze leest weer gegevens uit twee (API) bronnen (omdat 1 onvoldoende informatie teruggaf) 

Uitgaande van de root van dit project als werkdirectory kan deze als volgt worden aangeroepen:
> python src/main/python/weerdata.py

Om te testen kun je deze ook aanroepen met optie --dryrun, dan wordt de data niet opgeslagen in de database.

Volgens de gebruiksvoorwaarden mag de weerdata maximaal 300 keer per dag worden opgehaald, 
vandaar dat elke 10 minuten beter is dan elke minuut (= 144 keer per dag). 
Veel vaker ophalen heeft overigens toch niet veel zin, omdat het weer nu ook weer niet zo vaak wijzigt.

Ook dit kan weer met een cronjob worden uitgevoerd als volgt:

```
*/10 * * * * cd /home/pi/homeautomation;/home/pi/.pyenv/shims/python src/main/python/weerdata.py >> /home/pi/cron_weer.log 2>&1
```


# To Do
* 1 main maken zodat voor energie meter en weerdata, omdat er veel dubbele code in zit (configuratie file, database aanroep)

* Philips Hue data ophalen en opslaan.