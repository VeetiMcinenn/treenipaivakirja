# Treenipäiväkirja

Sovelluksessa käyttäjät pystyvät pitämään kirjaa tekemistään treeneistä ja selaamaan myös muiden käyttäjien lisäämiä treenimerkintöjä. Treenimerkintään voi tallentaa esimerkiksi treenin nimen, kuvauksen, päivämäärän ja keston.

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään treenimerkintöjä sekä muokkaamaan ja poistamaan niitä.
- Käyttäjä näkee sovellukseen lisätyt treenimerkinnät.
- Käyttäjä pystyy etsimään treenimerkintöjä hakusanalla tai luokittelun perusteella.
- Käyttäjäsivu näyttää, montako treenimerkintää käyttäjä on lisännyt, sekä listan käyttäjän lisäämistä treeneistä.
- Käyttäjä pystyy valitsemaan treenimerkinnälle yhden tai useamman luokittelun (esim. salitreeni, juoksu, kiipeily, liikkuvuus).
- Käyttäjä pystyy lisäämään kommentteja omiin ja muiden käyttäjien treenimerkintöihin liittyen.

Tässä pääasiallinen tietokohde on treenimerkintä ja toissijainen tietokohde on kommentti.


# Treenipäiväkirja

Tämä on Helsingin yliopiston Tietokannat ja web-ohjelmointi -kurssin harjoitustyö (Välipalautus 2).
Sovellus on treenipäiväkirja, jonka avulla käyttäjä voi pitää kirjaa omista urheilusuorituksistaan.

Vaatimusten mukaisesti sovelluksessa on tällä hetkellä seuraavat toiminnot:
- **Käyttäjähallinta:** Käyttäjä voi luoda itselleen tunnuksen ja kirjautua sisään. Salasanat on suojattu asianmukaisesti.
- **Tietokohteiden käsittely:** Kirjautunut käyttäjä pystyy lisäämään uusia treenejä (päivämäärä, laji, kesto ja muistiinpanot). Käyttäjä pystyy myös muokkaamaan ja poistamaan **vain omia** treenejään.
- **Tietojen katselu:** Etusivulla näkyy lista kaikista sovellukseen lisätyistä treeneistä uusimmasta vanhimpaan.
- **Hakutoiminto:** Käyttäjä pystyy etsimään treenejä vapaalla sanahaulla. Haku kohdistuu treenin lajiin ja muistiinpanoihin.

## Asennus- ja testausohjeet

Näillä ohjeilla saat alustettua tietokannan ja käynnistettyä sovelluksen paikallisesti.

### 1. Lataa projekti ja siirry kansioon
Kloonaa tämä repositorio omalle koneellesi ja siirry projektin juurikansioon:
```bash
git clone [https://github.com/OMA-TUNNUKSESI/treenipaivakirja.git](https://github.com/OMA-TUNNUKSESI/treenipaivakirja.git)
cd treenipaivakirja
```

### 2. Luo virtuaaliympäristö ja asenna riippuvuudet
Luo ja aktivoi Pythonin virtuaaliympäristö:
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# Windows: venv\Scripts\activate
```

Asenna tarvittavat kirjastot:
```bash
pip install Flask Flask-SQLAlchemy werkzeug
```

### 3. Tietokannan alustaminen
Tietokantatiedostoa (`database.db`) ei ole repositoriossa. Sovellus käyttää uusinta Flask-SQLAlchemyä, joka olettaa tietokannan sijaitsevan `instance`-kansiossa. 

Luo kansio ja alusta tietokanta `schema.sql` -tiedoston pohjalta suorittamalla nämä komennot projektin juuressa:
```bash
mkdir instance
sqlite3 instance/database.db < schema.sql
```

### 4. Käynnistä sovellus
Käynnistä paikallinen kehityspalvelin:
```bash
flask run
```
Sovellus on nyt käytettävissä selaimessa osoitteessa http://127.0.0.1:5000. 
Voit testata toiminnallisuuksia luomalla uuden tunnuksen etusivun kautta.