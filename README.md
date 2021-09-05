# Homeautomation

Een verzameling tools om zaken binnenshuis te kunnen automatiseren.

## Algemeen gebruik

### Randvoorwaarden
* Python > 3.6 geinstalleerd
* Influxdb > 1.8.9 geinstalleerd

#### Voor energiemeter
* P1 naar USB kabel
* P1 protocol versie 5

### Extra Python Modules

#### Voor energiemeter
* influxdb

#### Voor weerdata
* influxdb
* requests

#### Voor deurbel
* Pidfile
* rpi.GPIO (op de Raspberry pi, voor lokaal ontwikkelen niet nodig)

#### Voor Woning
* requests

### Aanpassen van de secrets.ini
In src/main/resources staat een voorbeeld (secrets.example). 
Hernoem deze naar secrets.ini en vul de juiste waardes in.

Voor de databronnen kun je een andere databasenaam kiezen via de configuratie.

#### P1 gegevens
Behalve de database naam kun je alleen nog de port aangeven waarop de P1 data binnen komt.

#### Weer gegevens
Voor gebruik van weerlive (knmi) gegevens:
Haal een API key op via: https://weerlive.nl/delen.php
Daar vind je ook de juiste benaming voor de locatie.

Om een of andere reden kan je op deze manier niet heerslag gegevens ophalen, daarom weerhuisje. 
Voor gebruik van weerhuisje.nl kun je een weerstation naam ophalen via:
https://www.mijneigenweer.nl/participants.php?langchoice=nl

Vul deze naam in bij locatie_1

#### deurbel
De juiste pin nummer op de raspberrypi (Board nummering) voor de belknop en voor de bel gong.
Optioneel de duur van de bel per keer. Standaard is dat 1 seconde. Korter kan ook, b.v. 0.6 seconde.

#### telegram
Deze wordt gebruikt voor het versturen van een telegram bericht. Hiervoor is dus een token nodig om in te kunnen loggen, en een channel_id
De token kan je ophalen via de fatherbot (je moet dus een nieuwe bot maken).
Daarnaast moet je een channel maken waarnaar gepost gaat worden. Je moet de bot toevoegen als admin, en het ID kun je vervolgens weer ophalen via b.v. browser (URL).
Googlen, want het wijzigt nogal eens...

# Scripts
Er zijn 4 hoofdscripts die het beste via cron gestart kunnen worden (details onder).


## Algemene Software Architectuur
Het main script (controller) roept een device gateway aan, die op zijn beurt afhankelijk is van een device waar de echte meting plaatsvindt. 
De device gateway heeft als doel om de specifiek gemeten waardes om te zetten naar een algemene 'meetwaarde' entiteit.
De controller ontvangt deze meetwaardes en sluist die door naar de database gateway (persistence), 
die als doel heeft om de meetdata in influxdb te zetten.

Per script wordt er een database aangemaakt, en als measurement wordt uitgegaan van de eenheid van de meting.
Door middel van tags (geleverd dus door de device gateway, want die is bekend met de meting) 
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
* * * * * cd /home/pi/homeautomation;/home/pi/.pyenv/shims/python -u src/main/python/energiemeter.py >> /home/pi/cron_p1.log 2>&1
```

Op deze manier log je gelijk in de home directory of het proces nog loopt.

## Weerdata
Deze leest weer gegevens uit twee (API) bronnen (omdat 1 onvoldoende informatie teruggaf) 

Uitgaande van de root van dit project als werkdirectory kan deze als volgt worden aangeroepen:
> python src/main/python/weerdata.py

Om te testen kun je deze ook aanroepen met optie --dryrun, dan wordt de data niet opgeslagen in de database.

Volgens de gebruiksvoorwaarden mag de weerdata maximaal 300 keer per dag worden opgehaald, 
vandaar dat elke 10 minuten (= 144 keer per dag) beter is dan elke minuut. 
Veel vaker ophalen heeft overigens toch niet veel zin, omdat het weer nu ook weer niet zo vaak wijzigt.

Ook dit kan weer met een cronjob worden uitgevoerd als volgt:

```
*/10 * * * * cd /home/pi/homeautomation;/home/pi/.pyenv/shims/python src/main/python/weerdata.py >> /home/pi/cron_weer.log 2>&1
```

## Deurbel
Het main script is een controller die altijd blijft draaien (tenzij gecrashed, maar ook dat wordt zoveel mogelijk voorkomen.)
Ook dit script is het beste te starten via een cron job, want er zit een beveiliging in dat het script maar 1 keer mag zijn opgestart.

De -u parameter is om te zorgen dat de prints niet worden gebuffered. 
Gebleken is dat de combinatie met pidfile (voor de beveiliging dat er maar 1 proces tegelijkertijd kan draaien) er anders 
voor zorgt dat er niet meteen gelogd wordt.
``` 
* * * * * cd /home/pi/homeautomation;/home/pi/.pyenv/shims/python -u src/main/python/deurbel.py >> /home/pi/cron_deurbel.log 2>&1
```

De main loop vraagt aan de deurbel gateway of er iemand bij de deur staat, oftewel iemand op de knop heeft gedrukt.
De gateway regelt dat er dan ook altijd de gong afgaat (voor een vaste duur). 
Dit loopt in een aparte thread waardoor de control loop meteen weet of er iemand op de knop heeft gedrukt (asynchroon dus), 
en zonodig ook nog wat anders tegelijk kan doen, zoals het sturen van een bericht.
De gateway zorgt er ook voor dat er altijd maar 1 keer binnen de periode van de ring, door komt dat er op de knop gedrukt is.

### Messenger
Als messenger om te notificeren als er iemand voor de deur staat wordt gebruikt gemaakt van Telegram.
Via de BotFather moet een bot gemaakt worden. Dit is een account dat gebruikt wordt voor het script. 
De Botfather levert uiteindelijk een token op. De token moet worden ingevuld in de ini file. 
Daarnaast moet er een channel aangemaakt worden, en de bot moet admin van die channel worden.
Het channel ID kan achterhaald worden door eerst als de bot een melding in het channel te maken, en vervolgens via
https://api.telegram.org/bot{BOT_TOKEN}/getUpdates kan dan het channel ID achterhaald worden.

## Woning
De woning is op dit moment alleen het ophalen van de status van de lichten via een Hue Bridge.
Als er een andere bridge gebruikt wordt, moet je een andere bridge device schrijven, en die via de controller aan de gateway hangen.
Er wordt alleen gekeken of een lamp aan of uit staat, en dat wordt in de database opgeslagen met als tags de naam en ID van lamp.



# To Do
* 1 main maken voor energie meter en weerdata, en dan aanroepen via een parameter, omdat er veel dubbele code in zit (configuratie file, database aanroep)
