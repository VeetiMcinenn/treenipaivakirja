# Treenipäiväkirja (Flask-sovellus)

Tämä on Flaskilla ja SQLitellä toteutettu treenipäiväkirjasovellus, joka on tehty osana tietokantasovellusten kurssia. Sovelluksessa käyttäjät voivat seurata treenejään, luokitella niitä ja olla vuorovaikutuksessa muiden käyttäjien kanssa.

## Ominaisuudet (Välipalautus 3)

* **Käyttäjähallinta:** Rekisteröityminen ja kirjautuminen (salasanat suojattu hashilla).
* **Treenit:** Käyttäjä voi lisätä omia treenejä (laji, päivämäärä, kesto, muistiinpanot).
* **Haku:** Etusivulla on haku, jolla voi suodattaa treenejä lajin tai muistiinpanojen perusteella.
* **Oma sivu (Profiili):** Näyttää käyttäjän omat treenit ja laskee SQL-kyselyillä tilastoja (treenien määrä, kokonaisaika ja suosikkilaji).
* **Luokittelut:** Treeneihin voi valita useita luokkia (esim. Voimaharjoittelu, Ulkoilu) Many-to-Many-tietokantarakenteen avulla.
* **Sosiaalisuus:** Käyttäjät voivat katsoa muiden treenejä ja jättää niihin kommentteja/lisätietoja.
* **Suojaus:** Vain kirjautunut käyttäjä voi lisätä tai muokata omia tietojaan.

## Tietokantarakenne

Sovellus käyttää SQLite-tietokantaa (`database.db`). Tärkeimmät taulut ovat:
* `users`: Käyttäjätiedot.
* `workouts`: Treenien perustiedot.
* `categories`: Mahdolliset luokitukset.
* `workout_categories`: Liitostaulu treenien ja luokkien välille.
* `comments`: Treenikohtaiset kommentit.

## Asennus ja testaus

1.  **Lataa projekti ja varmista, että Python on asennettuna.**
2.  **Luo virtuaaliympäristö ja aktivoi se:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    source venv/bin/activate # Mac/Linux
    ```
3.  **Asenna tarvittavat kirjastot:**
    ```bash
    pip install flask
    ```
4.  **Alusta tietokanta:**
    Luo `database.db` ja suorita tarvittavat `CREATE TABLE` -lauseet 
5.  **Käynnistä sovellus:**
    ```bash
    flask run --debug
    ```
6.  **Testaus selaimessa:**
    Avaa osoite `http://127.0.0.1:5000`.
    * Luo uusi tunnus ("Luo tunnus").
    * Kirjaudu sisään.
    * Lisää uusi treeni ja valitse sille luokkia.
    * Mene "Oma sivu" -osioon tarkastelemaan tilastoja.
    * Kokeile etusivun hakutoimintoa.
    * Klikkaa treenin "Katso lisätiedot" -linkkiä ja jätä kommentti.
