EPL Project

Detta är projekt som visar Engelska Premier League tabellen med live data from football-data.org API.

Fullständig tabell med färgkodade placeringar för kvalificering till Champions League och Europa League samt för nedflyttning till andra ligan.
Man kan även söka efter ett specifikt lag i premier league för att få fram deras 5 senaste resultat. 
Sedan kan man även se lagens matchform i form av W/L/D (Win = grön, Lose = röd, Draw = grå).

Installation:

1. Clona repository med länk:
git clone https://github.com/filipsw1/epl_project.git
cd epl_project

2. Skapa och aktivera virtuell miljö:
python -m venv venv
venv\Scripts\activate

3. Installera dependencies:
pip install -r requirements.txt

## Hur man kör programmet

python src/main.py

## Notering

API-nyckeln är inkluderad i projektet för att underlätta testning. I vanliga fall hade den gömts.