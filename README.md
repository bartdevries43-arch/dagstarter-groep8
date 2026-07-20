# Dagstarter groep 8

Een dagstarterboekje voor groep 8 om elke schooldag mee te beginnen. Elke dag
is één printbare A4-pagina met een gevarieerde mix, oplopend in moeilijkheid
over het schooljaar (±200 dagen).

## Wat zit erin per dag
- **Automatiseren** — keer- en deelsommen
- **Hoofdrekenen** — optellen en aftrekken
- **Redactiesommen** — verhaaltjessommen
- **Wisselblok** — klokrekenen, geld, meten, meetkunde of procenten
- **Spelling** — ei/ij, au/ou, werkwoorden, voorzetsels
- **Technisch lezen** — woordenrij in de kolom links
- **Kleurplaat** — elke dag een unieke tekening om in te kleuren

## Bestanden
- `index.html` — startpagina met links naar het boekje en het antwoordenboek
- `boekje.html` — het leerlingenboekje (print-klaar op A4)
- `antwoorden.html` — antwoordenboek voor de leerkracht
- `generate.py` — generator; pas `AANTAL_DAGEN` aan en draai `python3 generate.py`
- `download_plaatjes.py` — downloadt de kleurplaten opnieuw
- `kleurplaten_data.py` — de ingebakken kleurplaten

## Zelf opnieuw genereren
```bash
python3 generate.py
```

## Printen
Open `boekje.html`, druk op Ctrl/Cmd + P, kies A4, marges "geen"/"standaard"
en vink "achtergrondafbeeldingen" aan voor de kleuren.

## Credits
Kleurplaten: [OpenMoji](https://openmoji.org) (CC BY-SA 4.0).
