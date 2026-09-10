#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dagstarter / automatiseren-boekje voor groep 8.

Genereert per schooldag een gevarieerde dagstarter (rekenen + spelling +
technisch lezen), oplopend in moeilijkheid over het hele schooljaar.
Levert twee bestanden op:
  - boekje.html        (het leerlingenboekje, print-klaar op A4)
  - antwoorden.html    (antwoordenboek voor de leerkracht)

Alles is deterministisch: dezelfde dag levert altijd dezelfde opgaven en
antwoorden. Pas AANTAL_DAGEN aan om het boekje korter/langer te maken.
"""

import random
import html

from kleurplaten_data import PLAATJES

# Vaste, gehusselde vololgorde zodat elke dag een uniek plaatje krijgt
# (geen enkel plaatje komt twee keer terug zolang AANTAL_DAGEN <= aantal plaatjes).
_plaatjes_volgorde = list(range(len(PLAATJES)))
random.Random(2024).shuffle(_plaatjes_volgorde)

# ---------------------------------------------------------------------------
# Instellingen
# ---------------------------------------------------------------------------
AANTAL_DAGEN = 200          # ~40 schoolweken x 5 dagen
DAGEN_PER_WEEK = 5
DAGNAMEN = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag"]

# Vriendelijke themawoordjes bovenaan de dag (roteren, puur decoratief)
THEMAS = [
    "Goedemorgen!", "Fris van start", "Kop op, aan de slag",
    "Even opwarmen", "Reken je warm", "Denk mee", "Scherp beginnen",
    "Hersenkrakers", "Eerst dit, dan de dag", "Knappe koppen",
]


# ===========================================================================
# Hulpfuncties
# ===========================================================================
def euro(cents):
    """Formatteer een bedrag in centen als Nederlands euro-bedrag."""
    teken = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{teken}€ {cents // 100},{cents % 100:02d}"


def getal(n):
    """Nederlandse duizendtal-notatie met een punt (12.500)."""
    return f"{n:,}".replace(",", ".")


# ===========================================================================
# Rekenblokken
# ===========================================================================
def gen_automatiseren(rnd, t):
    """Keer- en deelsommen die met de dagen moeilijker worden (zonder dubbele)."""
    items = []
    seen = set()
    pog = 0
    while len(items) < 8 and pog < 500:
        pog += 1
        if t < 0.20:
            a, b = rnd.randint(2, 10), rnd.randint(2, 10)
        elif t < 0.45:
            a, b = rnd.randint(3, 12), rnd.randint(3, 12)
        elif t < 0.70:
            if rnd.random() < 0.5:
                a, b = rnd.randint(11, 20), rnd.randint(3, 9)
            else:
                a, b = rnd.choice([25, 50, 15, 40]), rnd.randint(3, 9)
        else:
            if rnd.random() < 0.5:
                a, b = rnd.randint(12, 40), rnd.randint(3, 9)
            else:
                a, b = rnd.randint(11, 25), rnd.randint(11, 20)
        v = f"{a} × {b} ="
        if v in seen:
            continue
        seen.add(v)
        items.append({"vraag": v, "antwoord": str(a * b)})
    pog = 0
    while len(items) < 14 and pog < 500:
        pog += 1
        if t < 0.20:
            deler, quot = rnd.randint(2, 10), rnd.randint(2, 10)
            rest = 0
        elif t < 0.45:
            deler, quot = rnd.randint(3, 12), rnd.randint(3, 12)
            rest = 0
        elif t < 0.70:
            deler, quot = rnd.randint(3, 12), rnd.randint(6, 15)
            rest = rnd.choice([0, 0, rnd.randint(1, deler - 1)])
        else:
            deler, quot = rnd.randint(4, 12), rnd.randint(8, 25)
            rest = rnd.choice([0, rnd.randint(1, deler - 1)])
        deeltal = deler * quot + rest
        v = f"{deeltal} : {deler} ="
        if v in seen:
            continue
        seen.add(v)
        antw = f"{quot} rest {rest}" if rest else str(quot)
        items.append({"vraag": v, "antwoord": antw})
    return {"titel": "Automatiseren", "kolommen": 2, "items": items}


def gen_hoofdrekenen(rnd, t):
    """Optellen en aftrekken, oplopend; zonder dubbele sommen."""
    items = []
    seen = set()
    pog = 0
    while len(items) < 6 and pog < 500:
        pog += 1
        if t < 0.20:
            a, b = rnd.randint(11, 99), rnd.randint(11, 99)
        elif t < 0.45:
            a, b = rnd.randint(120, 899), rnd.randint(110, 499)
        elif t < 0.70:
            a, b = rnd.randint(1000, 8999), rnd.randint(500, 4999)
        else:
            a, b = rnd.randint(10000, 89999), rnd.randint(2000, 39999)
        if rnd.random() < 0.5:
            v = f"{getal(a)} + {getal(b)} ="
            antw = getal(a + b)
        else:
            if b > a:
                a, b = b, a
            v = f"{getal(a)} − {getal(b)} ="
            antw = getal(a - b)
        if v in seen:
            continue
        seen.add(v)
        items.append({"vraag": v, "antwoord": antw})
    return {"titel": "Hoofdrekenen", "kolommen": 2, "items": items}


# ---------------------------------------------------------------------------
# Redactiesommen (verhaaltjessommen)
# ---------------------------------------------------------------------------
NAMEN = ["Sara", "Tim", "Noor", "Lars", "Fatima", "Daan", "Sofie", "Youssef",
         "Emma", "Bram", "Lisa", "Mees", "Julia", "James", "Mohammed", "Chen",
         "Amara", "Yusuf", "Aisha", "Sem", "Nora", "Finn", "Ravi", "Yara"]


def _redactie_makkelijk(rnd):
    naam = rnd.choice(NAMEN)
    keuze = rnd.randint(0, 3)
    if keuze == 0:
        per, dozen = rnd.randint(6, 12), rnd.randint(4, 9)
        return (f"In elke doos zitten {per} knikkers. {naam} heeft {dozen} "
                f"dozen. Hoeveel knikkers heeft {naam} in totaal?",
                f"{per * dozen} knikkers")
    if keuze == 1:
        prijs, aantal = rnd.randint(2, 8) * 100 + 50, rnd.randint(3, 6)
        return (f"Een schrift kost {euro(prijs)}. {naam} koopt er {aantal}. "
                f"Hoeveel betaalt {naam}?", euro(prijs * aantal))
    if keuze == 2:
        totaal, af = rnd.randint(60, 120), rnd.randint(15, 45)
        return (f"Een reis is {totaal} km. Ze hebben al {af} km gereden. "
                f"Hoeveel km moeten ze nog?", f"{totaal - af} km")
    snoep, kind = rnd.randint(5, 9) * rnd.randint(4, 8), rnd.randint(4, 8)
    rest = snoep % kind
    return (f"{snoep} snoepjes worden eerlijk verdeeld over {kind} kinderen. "
            f"Hoeveel krijgt ieder kind en hoeveel blijft over?",
            f"{snoep // kind} per kind, {rest} over")


def _redactie_middel(rnd):
    naam = rnd.choice(NAMEN)
    keuze = rnd.randint(0, 3)
    if keuze == 0:
        stuk, aantal = rnd.randint(8, 20) * 100, rnd.randint(6, 15)
        return (f"Een kaartje voor het pretpark kost {euro(stuk)}. Een klas "
                f"van {aantal} kinderen gaat erheen. Wat kost dat samen?",
                euro(stuk * aantal))
    if keuze == 1:
        totaal = rnd.randint(20, 40) * 100
        betaald = rnd.randint(4, 12) * 100 + rnd.choice([0, 25, 50, 75])
        return (f"{naam} heeft {euro(totaal)} gespaard en geeft er "
                f"{euro(betaald)} van uit. Hoeveel houdt {naam} over?",
                euro(totaal - betaald))
    if keuze == 2:
        flessen, per_uur = rnd.randint(1200, 3600), rnd.choice([300, 400, 600])
        return (f"Een machine maakt {getal(per_uur)} flessen per uur. Er zijn "
                f"{getal(flessen)} flessen nodig. Hoeveel uur is de machine "
                f"bezig (afgerond naar boven)?",
                f"{-(-flessen // per_uur)} uur")
    mensen = rnd.randint(3, 6)
    per_glas = rnd.choice([150, 200, 250, 300])
    ml = mensen * per_glas
    return (f"{ml} ml limonade wordt eerlijk verdeeld over {mensen} glazen. "
            f"Hoeveel ml komt er in elk glas?", f"{per_glas} ml")


def _redactie_moeilijk(rnd):
    naam = rnd.choice(NAMEN)
    keuze = rnd.randint(0, 3)
    if keuze == 0:
        prijs = rnd.randint(4, 20) * 1000  # hele euro's in centen
        pct = rnd.choice([10, 20, 25, 50])
        korting = prijs * pct // 100
        return (f"Een jas kost {euro(prijs)}. Er is {pct}% korting. Hoeveel "
                f"korting krijgt {naam} en wat is de nieuwe prijs?",
                f"korting {euro(korting)}, nieuwe prijs {euro(prijs - korting)}")
    if keuze == 1:
        kaartjes = rnd.randint(20, 45)
        prijs = rnd.randint(15, 30) * 100
        totaal = kaartjes * prijs
        return (f"Juf betaalt {euro(totaal)} voor het schoolreisje. Een "
                f"kaartje kost {euro(prijs)}. Hoeveel kinderen gaan er mee?",
                f"{kaartjes} kinderen")
    if keuze == 2:
        uur = rnd.choice([2, 3, 4])
        per_uur = rnd.randint(60, 120)
        km = uur * per_uur
        return (f"Een trein rijdt {km} km in {uur} uur. Hoeveel km rijdt de "
                f"trein gemiddeld per uur?", f"{per_uur} km per uur")
    while True:
        a, b, c = rnd.randint(4, 10), rnd.randint(4, 10), rnd.randint(4, 10)
        if (a + b + c) % 3 == 0:
            break
    return (f"{naam} haalt de rapportcijfers {a}, {b} en {c}. "
            f"Wat is het gemiddelde?", str((a + b + c) // 3))


def gen_redactie(rnd, t):
    if t < 0.33:
        makers = [_redactie_makkelijk, _redactie_makkelijk, _redactie_middel]
    elif t < 0.66:
        makers = [_redactie_makkelijk, _redactie_middel, _redactie_moeilijk]
    else:
        makers = [_redactie_middel, _redactie_moeilijk, _redactie_moeilijk]
    rnd.shuffle(makers)
    items = []
    for mk in makers[:2]:
        vraag, antw = mk(rnd)
        items.append({"vraag": vraag, "antwoord": antw})
    return {"titel": "Redactiesommen", "kolommen": 1, "items": items}


# ---------------------------------------------------------------------------
# Wisselblok: tijd / geld / meten / meetkunde / procenten (roteert per dag)
# ---------------------------------------------------------------------------
def _wissel_tijd(rnd, t):
    items = []
    for _ in range(4):
        u, m = rnd.randint(0, 23), rnd.choice([0, 5, 10, 15, 20, 30, 40, 45])
        plus_u, plus_m = rnd.randint(1, 4), rnd.choice([5, 10, 15, 25, 35, 45])
        totaal = (u * 60 + m + plus_u * 60 + plus_m) % (24 * 60)
        items.append({
            "vraag": f"{u:02d}:{m:02d}  →  {plus_u} uur en {plus_m} "
                     f"minuten later is het",
            "antwoord": f"{totaal // 60:02d}:{totaal % 60:02d}"})
    return "Klokrekenen", items


def _wissel_geld(rnd, t):
    items = []
    for _ in range(4):
        if rnd.random() < 0.5:
            betaald = rnd.choice([2000, 5000, 10000])
            prijs = rnd.randint(3, betaald // 100 - 1) * 100 + rnd.choice([5, 25, 45, 65, 95])
            items.append({"vraag": f"Je betaalt {euro(betaald)} voor iets van "
                                   f"{euro(prijs)}. Hoeveel krijg je terug?",
                          "antwoord": euro(betaald - prijs)})
        else:
            a = rnd.randint(3, 25) * 100 + rnd.choice([0, 25, 50, 75])
            b = rnd.randint(3, 25) * 100 + rnd.choice([0, 25, 50, 75])
            items.append({"vraag": f"{euro(a)} + {euro(b)} =",
                          "antwoord": euro(a + b)})
    return "Rekenen met geld", items


def _wissel_meten(rnd, t):
    paren = [
        ("m", "cm", 100), ("cm", "mm", 10), ("km", "m", 1000),
        ("kg", "g", 1000), ("l", "ml", 1000), ("dm", "cm", 10),
    ]
    items = []
    for _ in range(4):
        groot, klein, factor = rnd.choice(paren)
        waarde = rnd.randint(2, 45)
        if rnd.random() < 0.5:
            items.append({"vraag": f"{waarde} {groot} = ______ {klein}",
                          "antwoord": f"{getal(waarde * factor)} {klein}"})
        else:
            veelvoud = waarde * factor
            items.append({"vraag": f"{getal(veelvoud)} {klein} = ______ {groot}",
                          "antwoord": f"{waarde} {groot}"})
    return "Meten en omrekenen", items


def _wissel_meetkunde(rnd, t):
    items = []
    seen = set()
    while len(items) < 4:
        l, b = rnd.randint(4, 25), rnd.randint(3, 18)
        if (l, b) in seen:
            continue
        seen.add((l, b))
        items.append({"vraag": f"Rechthoek {l} cm bij {b} cm → omtrek = ______ cm",
                      "antwoord": f"{2 * (l + b)} cm"})
        items.append({"vraag": f"Rechthoek {l} cm bij {b} cm → oppervlakte = ______ cm²",
                      "antwoord": f"{l * b} cm²"})
    return "Meetkunde: omtrek en oppervlakte", items[:4]


def _wissel_procenten(rnd, t):
    items = []
    for _ in range(4):
        pct = rnd.choice([10, 20, 25, 50, 75])
        geheel = rnd.randint(4, 40) * 100
        deel = geheel * pct // 100
        items.append({"vraag": f"{pct}% van {euro(geheel)} =",
                      "antwoord": euro(deel)})
    return "Procenten", items


def gen_wissel(rnd, t, dagnummer):
    vroeg = [_wissel_tijd, _wissel_geld, _wissel_meten, _wissel_meetkunde]
    laat = [_wissel_tijd, _wissel_geld, _wissel_meten, _wissel_meetkunde,
            _wissel_procenten]
    pool = vroeg if t < 0.4 else laat
    maker = pool[dagnummer % len(pool)]
    titel, items = maker(rnd, t)
    gezien = set()
    uniek = []
    for it in items:
        if it["vraag"] not in gezien:
            gezien.add(it["vraag"])
            uniek.append(it)
    return {"titel": titel, "kolommen": 1, "items": uniek}


# ===========================================================================
# Spelling (roteert per dag over categorieën)
# ===========================================================================
EI_WOORDEN = ["klein", "trein", "plein", "reis", "keizer", "weide", "dweil",
              "eigen", "meisje", "geit", "feit", "leiden", "dreigen",
              "verleiden", "eiland", "breien", "reizen", "azijn_no",
              "einde", "bereiken", "zeil", "sleutel_no", "peil", "vlei"]
EI_WOORDEN = [w for w in EI_WOORDEN if not w.endswith("_no")]

IJ_WOORDEN = ["tijd", "wijn", "kijken", "blij", "vrij", "prijs", "ijs",
              "rijst", "wijzer", "zijde", "blijven", "schrijven", "mijden",
              "vermijden", "kwijt", "lijst", "twijfel", "vijver", "pijn",
              "wijk", "strijd", "vrijheid", "verrijken", "bewijs"]

AU_WOORDEN = ["paus", "saus", "gauw", "nauw", "dauw", "blauw", "rauw",
              "kauwen", "pauze", "applaus", "kabouter", "augurk",
              "restaurant", "astronaut", "auto", "sauna", "cadeau_no"]
AU_WOORDEN = [w for w in AU_WOORDEN if not w.endswith("_no")]

OU_WOORDEN = ["koud", "goud", "zout", "fout", "hout", "bout", "mouw",
              "vrouw", "touw", "schouder", "houden", "vouwen", "verkouden",
              "stout", "oud", "flauw_no", "benauwd", "schoudertas",
              "bourgondisch_no", "koud"]
OU_WOORDEN = [w for w in OU_WOORDEN if not w.endswith("_no")]

# Werkwoorden tegenwoordige tijd: (infinitief, onderwerp, juiste vorm)
WW_TT = [
    ("worden", "hij", "wordt"), ("vinden", "zij", "vindt"),
    ("antwoorden", "de meester", "antwoordt"), ("rijden", "hij", "rijdt"),
    ("bieden", "zij", "biedt"), ("houden", "hij", "houdt"),
    ("verwachten", "hij", "verwacht"), ("branden", "het vuur", "brandt"),
    ("wandelen", "zij", "wandelt"), ("gebeuren", "er", "gebeurt"),
    ("verhuizen", "hij", "verhuist"), ("bedanken", "zij", "bedankt"),
    ("beloven", "hij", "belooft"), ("schudden", "hij", "schudt"),
]

# Werkwoorden verleden tijd ('t kofschip): (infinitief, onderwerp, juiste vorm)
WW_VT = [
    ("werken", "hij", "werkte"), ("leven", "zij", "leefde"),
    ("fietsen", "hij", "fietste"), ("verhuizen", "zij", "verhuisde"),
    ("hopen", "hij", "hoopte"), ("antwoorden", "hij", "antwoordde"),
    ("branden", "het vuur", "brandde"), ("redden", "zij", "redde"),
    ("gebeuren", "er", "gebeurde"), ("racen", "hij", "racete"),
    ("landen", "het vliegtuig", "landde"), ("bakken", "zij", "bakte"),
    ("praten", "hij", "praatte"), ("wandelen", "zij", "wandelde"),
]

# Vaste voorzetsels: (zin met ___, juiste voorzetsel)
VOORZETSELS = [
    ("Ik ben trots ___ mijn werk.", "op"),
    ("Hij is bang ___ spinnen.", "voor"),
    ("Zij houdt ___ muziek.", "van"),
    ("We wachten ___ de bus.", "op"),
    ("Denk je nog ___ mij?", "aan"),
    ("Deze foto lijkt ___ die van gisteren.", "op"),
    ("Iedereen mag deelnemen ___ de wedstrijd.", "aan"),
    ("Ze is verliefd ___ hem.", "op"),
    ("Hij twijfelt ___ zijn keuze.", "over"),
    ("Pas ___ voor het verkeer.", "op"),
    ("Ik ben benieuwd ___ de uitslag.", "naar"),
    ("Zij zorgt goed ___ haar hond.", "voor"),
]


def _gap_woord(woord, digraaf):
    """Vervang de eerste ei/ij/au/ou in het woord door een streepje."""
    idx = woord.find(digraaf)
    return woord[:idx] + "__" + woord[idx + 2:]


def gen_spelling(rnd, t, dagnummer):
    categorie = dagnummer % 6
    items = []
    if categorie == 0:  # ei / ij
        titel = "Spelling: vul in ei of ij"
        keuze = [(w, "ei") for w in EI_WOORDEN] + [(w, "ij") for w in IJ_WOORDEN]
        rnd.shuffle(keuze)
        for woord, dg in keuze[:8]:
            items.append({"vraag": _gap_woord(woord, dg), "antwoord": dg})
    elif categorie == 1:  # au / ou
        titel = "Spelling: vul in au of ou"
        keuze = [(w, "au") for w in AU_WOORDEN] + [(w, "ou") for w in OU_WOORDEN]
        rnd.shuffle(keuze)
        for woord, dg in keuze[:8]:
            items.append({"vraag": _gap_woord(woord, dg), "antwoord": dg})
    elif categorie == 2:  # werkwoord tegenwoordige tijd
        titel = "Werkwoorden: tegenwoordige tijd"
        keuze = WW_TT[:]
        rnd.shuffle(keuze)
        for inf, ond, vorm in keuze[:6]:
            items.append({"vraag": f"{ond.capitalize()} ___ ({inf}).",
                          "antwoord": vorm})
    elif categorie == 3:  # werkwoord verleden tijd
        titel = "Werkwoorden: verleden tijd"
        keuze = WW_VT[:]
        rnd.shuffle(keuze)
        for inf, ond, vorm in keuze[:6]:
            items.append({"vraag": f"{ond.capitalize()} ___ ({inf}).",
                          "antwoord": vorm})
    elif categorie == 4:  # vaste voorzetsels
        titel = "Spelling: vul het juiste voorzetsel in"
        keuze = VOORZETSELS[:]
        rnd.shuffle(keuze)
        for zin, antw in keuze[:6]:
            items.append({"vraag": zin, "antwoord": antw})
    else:  # gemengd woorddictee-achtig: ei/ij + au/ou door elkaar
        titel = "Spelling: vul de juiste letters in"
        keuze = ([(w, "ei") for w in EI_WOORDEN] +
                 [(w, "ij") for w in IJ_WOORDEN] +
                 [(w, "au") for w in AU_WOORDEN] +
                 [(w, "ou") for w in OU_WOORDEN])
        rnd.shuffle(keuze)
        for woord, dg in keuze[:8]:
            items.append({"vraag": _gap_woord(woord, dg), "antwoord": dg})
    gezien = set()
    items = [it for it in items if not (it["vraag"] in gezien or gezien.add(it["vraag"]))]
    return {"titel": titel, "kolommen": 2, "items": items}


# ===========================================================================
# Technisch lezen (woordenrij, oplopend moeilijker)
# ===========================================================================
LEESWOORDEN = [
    # eenvoudiger (kort, bekend)
    "vakantie", "computer", "familie", "muziek", "station", "elektrisch",
    "gitaar", "kalender", "vandaag", "morgen", "schilder", "voetbal",
    "tijdschrift", "onmiddellijk", "spannend", "grappig", "misschien",
    "eigenlijk", "natuurlijk", "verschillende", "belangrijk", "gemakkelijk",
    "ingewikkeld", "opnieuw", "gehoorzaam", "aardbeving", "krantenbezorger",
    "reddingsboot", "tentoonstelling", "kampeerboerderij", "wereldoorlog",
    "vergadering", "ochtendgymnastiek", "reclamefilmpje", "wereldbevolking",
    "hartoperatie", "boormachine", "paradijsvogel", "spaarrekening",
    "reddingsvest", "voorstelling", "gebeurtenis", "handtekening",
    "temperatuur", "gereedschap", "verkeersbord", "milieuvriendelijk",
    "verantwoordelijk", "onafhankelijk", "nieuwsgierig", "geheimzinnig",
    "aantrekkelijk", "professioneel", "internationaal", "kilometerteller",
    "voetbalstadion", "ziekenhuisopname", "computerprogramma",
    "wetenschapper", "elektriciteit", "burgemeester", "gereedschapskist",
    "verjaardagsfeest", "achtereenvolgens", "onafscheidelijk",
    "tegenovergestelde", "verantwoordelijkheid", "gebruiksaanwijzing",
    "vanzelfsprekend", "buitengewoon", "onvoorstelbaar", "grootmoedig",
    "waarschijnlijk", "geleidelijk", "oorspronkelijk", "middeleeuwen",
    "beschaving", "uitzonderlijk", "samenwerking", "geschiedenis",
    "aardrijkskunde", "vermenigvuldigen", "wiskundeproefwerk",
    "kampioenschap", "trainingskamp", "atletiekvereniging",
    "zwembadtemperatuur", "voorjaarsvakantie", "herfstvakantie",
    "sinterklaasfeest", "kerstvakantie", "koningsspelen", "avondvierdaagse",
]


def gen_lezen(rnd, t):
    """Kies een woordenrij die past bij de moeilijkheidsgraad."""
    n = len(LEESWOORDEN)
    # window schuift op met t, zodat latere dagen bij de moeilijker woorden zitten
    centrum = int(t * (n - 1))
    laag = max(0, centrum - 14)
    hoog = min(n, centrum + 14)
    venster = LEESWOORDEN[laag:hoog]
    gekozen = rnd.sample(venster, min(20, len(venster)))
    return {"titel": "Technisch lezen", "woorden": gekozen}


# ===========================================================================
# Kleurplaat-figuren (line-art om in te kleuren, vullen de onderruimte)
# De tekeningen komen uit kleurplaten_data.py (OpenMoji, CC BY-SA 4.0).
# ===========================================================================
KLEUR_TITELS = [
    "Klaar met je werk? Kleur de tekening mooi in!",
    "Extra tijd over? Maak deze tekening kleurrijk!",
    "Even ontspannen: kleur de tekening in.",
    "Wie kleurt het netst? Aan de slag!",
    "Kleur mij in met je mooiste kleuren!",
]


def gen_kleurplaat(dagnummer):
    # Uniek plaatje per dag via de gehusselde volgorde; geen herhaling
    # zolang AANTAL_DAGEN <= aantal beschikbare plaatjes.
    idx = _plaatjes_volgorde[(dagnummer - 1) % len(_plaatjes_volgorde)]
    titel = KLEUR_TITELS[dagnummer % len(KLEUR_TITELS)]
    return {"svg": PLAATJES[idx], "titel": titel}


# ===========================================================================
# Dag samenstellen
# ===========================================================================
def maak_dag(dagnummer):
    rnd = random.Random(4000 + dagnummer)
    t = (dagnummer - 1) / max(1, AANTAL_DAGEN - 1)
    week = (dagnummer - 1) // DAGEN_PER_WEEK + 1
    dagnaam = DAGNAMEN[(dagnummer - 1) % DAGEN_PER_WEEK]
    sterren = 1 + min(4, int(t * 5))   # moeilijkheidsmeter 1..5
    return {
        "nummer": dagnummer,
        "week": week,
        "dagnaam": dagnaam,
        "thema": THEMAS[dagnummer % len(THEMAS)],
        "sterren": sterren,
        "automatiseren": gen_automatiseren(rnd, t),
        "hoofdrekenen": gen_hoofdrekenen(rnd, t),
        "redactie": gen_redactie(rnd, t),
        "wissel": gen_wissel(rnd, t, dagnummer),
        "spelling": gen_spelling(rnd, t, dagnummer),
        "lezen": gen_lezen(rnd, t),
        "kleurplaat": gen_kleurplaat(dagnummer),
    }


# ===========================================================================
# HTML-rendering
# ===========================================================================
def esc(s):
    return html.escape(str(s))


def render_sommenblok(blok, met_antwoord):
    kol = blok.get("kolommen", 2)
    rijen = []
    for it in blok["items"]:
        if met_antwoord:
            regel = (f'<span class="v">{esc(it["vraag"])}</span>'
                     f'<span class="a">{esc(it["antwoord"])}</span>')
        else:
            regel = (f'<span class="v">{esc(it["vraag"])}</span>'
                     f'<span class="lijn"></span>')
        rijen.append(f'<li>{regel}</li>')
    return (f'<div class="blok">'
            f'<h3>{esc(blok["titel"])}</h3>'
            f'<ul class="items kol{kol}">{"".join(rijen)}</ul></div>')


def render_lezen(blok):
    woorden = "".join(f"<li>{esc(w)}</li>" for w in blok["woorden"])
    return (f'<aside class="lezen">'
            f'<h3>{esc(blok["titel"])}</h3>'
            f'<ol>{woorden}</ol></aside>')


def render_kleurhoek(dag):
    kp = dag["kleurplaat"]
    return (f'<div class="kleurhoek">'
            f'<span class="kleurtitel">{esc(kp["titel"])}</span>'
            f'<div class="kleurfig">{kp["svg"]}</div></div>')


def render_dag(dag, met_antwoord=False):
    sterren = "★" * dag["sterren"] + "☆" * (5 - dag["sterren"])
    blokken = [
        render_sommenblok(dag["automatiseren"], met_antwoord),
        render_sommenblok(dag["hoofdrekenen"], met_antwoord),
        render_sommenblok(dag["redactie"], met_antwoord),
        render_sommenblok(dag["wissel"], met_antwoord),
        render_sommenblok(dag["spelling"], met_antwoord),
    ]
    if not met_antwoord:
        blokken.append(render_kleurhoek(dag))
    hoofd = "".join(blokken)
    return f'''
<section class="dag">
  <header class="dagkop">
    <div class="dagkop-links">
      <span class="dagnr">Dag {dag["nummer"]}</span>
    </div>
    <div class="dagkop-midden">{esc(dag["thema"])}</div>
    <div class="dagkop-rechts"><span class="niveau">{sterren}</span></div>
  </header>
  <div class="dagbody">
    {render_lezen(dag["lezen"])}
    <div class="hoofd">{hoofd}</div>
  </div>
  <div class="naamregel">Naam: <span class="naamlijn"></span></div>
</section>'''


CSS = """
:root{
  --auto:#d9ecdd;   --auto-l:#eef7f0;
  --hoofd:#fde5d6;  --hoofd-l:#fdf1ea;
  --redac:#dbeafe;  --redac-l:#eef4fe;
  --wissel:#e9e0f7; --wissel-l:#f3eefb;
  --spel:#fdeecf;   --spel-l:#fdf6e8;
  --lezen:#d5eef0;  --lezen-l:#e9f6f7;
  --ink:#2f3a36; --grijs:#7c8a84; --lijn:#c4cec9;
}
*{box-sizing:border-box;}
body{
  font-family:"Trebuchet MS","Segoe UI",Verdana,sans-serif;
  color:var(--ink); margin:0; background:#f4f6f5;
  font-size:11px; line-height:1.3;
}
.dag{
  width:210mm; min-height:297mm; padding:12mm 11mm 10mm;
  margin:0 auto 8mm; background:#fff; position:relative;
  page-break-after:always; display:flex; flex-direction:column;
}
.dag:last-child{page-break-after:auto;}

/* Kop */
.dagkop{
  display:flex; align-items:center; justify-content:space-between;
  border-bottom:3px solid var(--auto); padding-bottom:6px; margin-bottom:8px;
}
.dagkop-links{display:flex; align-items:baseline; gap:10px;}
.dagnr{font-size:24px; font-weight:bold; letter-spacing:.5px;}
.dagnaam{font-size:12px; color:var(--grijs);}
.dagkop-midden{font-size:13px; font-style:italic; color:var(--grijs);}
.niveau{font-size:15px; color:#e8a13c; letter-spacing:2px;}

/* Body: leeskolom links + hoofd rechts */
.dagbody{display:flex; gap:8px; flex:1;}
.lezen{
  width:34mm; flex:0 0 34mm; background:var(--lezen-l);
  border:1.5px solid var(--lezen); border-radius:8px; padding:6px 4px;
}
.lezen h3{
  margin:0 0 5px; font-size:11px; text-align:center; color:var(--ink);
  background:var(--lezen); border-radius:5px; padding:3px 2px;
}
.lezen ol{margin:0; padding-left:20px;}
.lezen ol li{margin-bottom:2.5px; font-size:10.5px;}

.hoofd{flex:1; display:flex; flex-direction:column; gap:7px;}

/* Blokken */
.blok{border-radius:8px; padding:6px 8px 7px;}
.blok h3{margin:0 0 5px; font-size:11.5px;}
.blok:nth-child(1){background:var(--auto-l); border:1.5px solid var(--auto);}
.blok:nth-child(1) h3{color:#2f7d4f;}
.blok:nth-child(2){background:var(--hoofd-l); border:1.5px solid var(--hoofd);}
.blok:nth-child(2) h3{color:#c76a3a;}
.blok:nth-child(3){background:var(--redac-l); border:1.5px solid var(--redac);}
.blok:nth-child(3) h3{color:#3a6bb0;}
.blok:nth-child(4){background:var(--wissel-l); border:1.5px solid var(--wissel);}
.blok:nth-child(4) h3{color:#6a4bab;}
.blok:nth-child(5){background:var(--spel-l); border:1.5px solid var(--spel);}
.blok:nth-child(5) h3{color:#c79228;}

/* Items */
ul.items{list-style:none; margin:0; padding:0; display:grid; gap:2px 14px;}
ul.items.kol2{grid-template-columns:1fr 1fr;}
ul.items.kol1{grid-template-columns:1fr;}
ul.items li{display:flex; align-items:baseline; gap:6px; padding:1px 0;}
ul.items .v{white-space:normal;}
ul.items.kol2 .v{min-width:78px;}
.lijn{flex:1; border-bottom:1.5px dotted var(--lijn); min-width:26px;
  align-self:flex-end; height:0; margin-bottom:2px;}
.a{color:#b03636; font-weight:bold;}

/* Kleurhoek onderaan: vult de resterende ruimte met een tekening */
.kleurhoek{flex:1; min-height:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center; text-align:center;
  border:2px dashed var(--lijn); border-radius:12px; padding:6px; margin-top:1px;
  background:repeating-linear-gradient(45deg,#fff,#fff 12px,#fbfcfb 12px,#fbfcfb 24px);}
.kleurtitel{font-size:11px; color:var(--grijs); font-style:italic; margin-bottom:4px;}
.kleurfig{flex:1; min-height:0; width:100%; position:relative; overflow:hidden;}
.kleurfig svg{position:absolute; inset:0; width:100%; height:100%;}
.kleurfig svg *{stroke-width:1.7 !important;}

/* Redactie en wissel: iets meer ruimte per item */
.blok:nth-child(3) ul.items li,.blok:nth-child(4) ul.items li{padding:2px 0;}

/* Naamregel */
.naamregel{margin-top:8px; padding-top:6px; border-top:1px dashed var(--lijn);
  font-size:11px; color:var(--grijs); display:flex; align-items:baseline; gap:8px;}
.naamlijn{flex:0 0 60mm; border-bottom:1.2px solid var(--lijn); height:0;}

/* Voorblad */
.voorblad{
  width:210mm; min-height:297mm; margin:0 auto 8mm; background:#fff;
  page-break-after:always; display:flex; flex-direction:column;
  align-items:center; justify-content:center; text-align:center; padding:30mm;
  position:relative; overflow:hidden;
}
.voorblad .bubbels span{position:absolute; border-radius:50%; opacity:.55;}
.voorblad h1{font-size:44px; margin:0 0 6px; z-index:2;}
.voorblad h2{font-size:22px; color:var(--grijs); font-weight:normal; margin:0 0 30px; z-index:2;}
.voorblad .groep{font-size:70px; font-weight:bold; color:#2f7d4f; z-index:2; line-height:1;}
.voorblad .naamkader{margin-top:40px; z-index:2; font-size:18px;}
.voorblad .naamkader .lijnlang{display:inline-block; width:70mm;
  border-bottom:2px solid var(--lijn); margin-left:10px;}
.voorblad .uitleg{position:absolute; bottom:20mm; font-size:12px; color:var(--grijs);
  max-width:150mm; z-index:2;}
.voorblad .credit{position:absolute; bottom:10mm; font-size:9px; color:#aab2ae; z-index:2;}

/* Scherm-hulp (niet printen) */
.schermbalk{max-width:210mm; margin:10px auto; font-family:sans-serif;
  font-size:13px; color:#555; text-align:center;}

@media print{
  body{background:#fff; font-size:10.5px;}
  .schermbalk{display:none;}
  .dag,.voorblad{margin:0; box-shadow:none;}
  @page{size:A4; margin:0;}
}
@media screen{
  .dag,.voorblad{box-shadow:0 2px 12px rgba(0,0,0,.12);}
}
"""


def render_voorblad(titel, ondertitel, uitleg):
    bubbels = ""
    kleuren = ["#d9ecdd", "#fde5d6", "#dbeafe", "#e9e0f7", "#fdeecf", "#d5eef0"]
    rnd = random.Random(7)
    for i in range(14):
        d = rnd.randint(40, 150)
        top = rnd.randint(-20, 260)
        left = rnd.randint(-20, 190)
        kl = kleuren[i % len(kleuren)]
        bubbels += (f'<span style="width:{d}px;height:{d}px;background:{kl};'
                    f'top:{top}mm;left:{left}mm;"></span>')
    return f'''
<section class="voorblad">
  <div class="bubbels">{bubbels}</div>
  <h1>{esc(titel)}</h1>
  <h2>{esc(ondertitel)}</h2>
  <div class="groep">Groep 8</div>
  <div class="naamkader">Naam:<span class="lijnlang"></span></div>
  <div class="uitleg">{esc(uitleg)}</div>
  <div class="credit">Kleurplaten: OpenMoji (CC BY-SA 4.0)</div>
</section>'''


def bouw_document(dagen, met_antwoord, titel, ondertitel):
    if met_antwoord:
        voorblad = render_voorblad(
            titel, ondertitel,
            "Antwoordenboek voor de leerkracht. De antwoorden staan in het "
            "rood achter elke opgave.")
    else:
        voorblad = render_voorblad(
            titel, ondertitel,
            "Elke dag begin je met een korte dagstarter: eerst automatiseren, "
            "dan hoofdrekenen, redactiesommen, een wisselopdracht en spelling. "
            "In de kolom links oefen je technisch lezen. De sterren bovenaan "
            "laten zien hoe pittig de dag is: het wordt steeds een beetje "
            "moeilijker.")
    secties = "".join(render_dag(d, met_antwoord) for d in dagen)
    return f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titel)}{" - antwoorden" if met_antwoord else ""}</title>
<style>{CSS}</style>
</head>
<body>
<div class="schermbalk">Tip: druk op Ctrl/Cmd + P om te printen. Kies A4 en
zet marges op "geen" of "standaard", en vink "achtergrondafbeeldingen" aan
voor de kleuren.</div>
{voorblad}
{secties}
</body>
</html>'''


# ===========================================================================
# Main
# ===========================================================================
def main():
    dagen = [maak_dag(n) for n in range(1, AANTAL_DAGEN + 1)]
    titel = "Dagstarter"
    ondertitel = "Automatiseren & taal - elke dag scherp beginnen"

    with open("boekje.html", "w", encoding="utf-8") as f:
        f.write(bouw_document(dagen, False, titel, ondertitel))
    with open("antwoorden.html", "w", encoding="utf-8") as f:
        f.write(bouw_document(dagen, True, titel, ondertitel))

    print(f"Klaar: {len(dagen)} dagen gegenereerd.")
    print("  - boekje.html")
    print("  - antwoorden.html")


if __name__ == "__main__":
    main()
