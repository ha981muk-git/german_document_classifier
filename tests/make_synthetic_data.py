# make_synthetic_data.py
from faker import Faker
import os
import random

fake = Faker(['de_DE', 'de_AT', 'de_CH'])  # adds regional diversity
os.makedirs("../data/data_synthetic", exist_ok=True)

def random_date():
    return fake.date_between(start_date='-2y', end_date='today').strftime('%d.%m.%Y')

# ------------------ INVOICE (Rechnung) ------------------
def make_invoice():
    templates = [
        f"""Rechnung Nr. {fake.random_int(1000,9999)}
Datum: {random_date()}
Kunde: {fake.name()}
{fake.company()}, {fake.address()}

Pos. | Beschreibung             | Betrag (EUR)
1    | {fake.word().capitalize()}                | {random.randint(100,800)}
2    | {fake.word().capitalize()}                | {random.randint(50,600)}

Zwischensumme: {random.randint(400,1500)} EUR
MwSt (19%): {round(random.uniform(10,300),2)} EUR
Gesamtbetrag: {random.randint(500,5000)} EUR
Bitte überweisen Sie den Betrag bis {fake.date_this_month()}.

Mit freundlichen Grüßen,
{fake.company()}
""",
        f"""Rechnung
Rechnungsnummer: {fake.random_int(1000,9999)}
Rechnungsdatum: {random_date()}

Leistungszeitraum: {fake.date_this_year()} - {fake.date_this_year()}
Empfänger: {fake.name()}, {fake.company()}
Summe: {random.randint(200,3000)} EUR
Zahlungsziel: 14 Tage ab Rechnungsdatum.
""",
        f"""*** RECHNUNG ***
Von: {fake.company()}
An: {fake.name()}
Rechnungsdatum: {random_date()}
Betrag: {random.randint(100,5000)} EUR

Bitte zahlen Sie auf Konto IBAN DE{fake.random_int(10000000000000000000,99999999999999999999)}.
""",
        f"""RECHNUNG - {fake.company()}
Kunde: {fake.name()}
Adresse: {fake.address()}
Rechnungsdatum: {random_date()}
Zahlungsbedingungen: 30 Tage netto
Gesamt: {random.randint(500,7000)} EUR
""",
        f"""Rechnung {fake.random_int(1000,9999)}
Firma: {fake.company()}
Empfänger: {fake.name()}
Leistung: {fake.catch_phrase()}
Preis: {random.randint(300,5000)} EUR (inkl. MwSt)
""",
        f"""Rechnungsbeleg
Firma: {fake.company()}
Adresse: {fake.address()}
Rechnung Nr.: {fake.random_int(1000,9999)} | Datum: {random_date()}
Gesamtbetrag: {random.randint(100,4000)} EUR
Fällig am: {fake.date_this_month()}
"""
    ]
    return random.choice(templates)

# ------------------ CONTRACT (Vertrag) ------------------
def make_contract():
    templates = [
        f"""Dienstleistungsvertrag
Zwischen {fake.company()} (Auftragnehmer)
und {fake.company()} (Auftraggeber)

Vertragsbeginn: {random_date()}
Laufzeit: {random.randint(6,36)} Monate
Leistungsumfang: {fake.catch_phrase()}
Kündigungsfrist: 3 Monate zum Vertragsende.
""",
        f"""Kaufvertrag
Verkäufer: {fake.company()}
Käufer: {fake.company()}
Ware: {fake.word().capitalize()}
Preis: {random.randint(500,8000)} EUR
Lieferdatum: {fake.date_this_month()}
""",
        f"""Vertrag über Zusammenarbeit
Dieser Vertrag wird zwischen {fake.company()} und {fake.company()} geschlossen.
Beginn: {random_date()}
Ziel: Förderung gemeinsamer Projekte im Bereich {fake.word()}.
""",
        f"""Mietvertrag
Vermieter: {fake.company()}
Mieter: {fake.name()}
Objekt: {fake.address()}
Monatsmiete: {random.randint(800,2500)} EUR
Vertragsbeginn: {random_date()}
""",
        f"""Arbeitsvertrag
Arbeitgeber: {fake.company()}
Arbeitnehmer: {fake.name()}
Beginn: {random_date()}
Tätigkeit: {fake.job()}
Vergütung: {random.randint(2500,6000)} EUR monatlich.
""",
        f"""Kooperationsvertrag
Zwischen {fake.company()} und {fake.company()}.
Vertragsdauer: {random.randint(12,48)} Monate
Kündigung: schriftlich, Frist 4 Wochen.
Ort, Datum: {fake.city()}, {random_date()}
"""
    ]
    return random.choice(templates)

# ------------------ PURCHASE ORDER (Bestellung) ------------------
def make_order():
    templates = [
        f"""Bestellung Nr. {fake.random_int(1000,9999)}
Datum: {random_date()}
Wir bestellen folgende Artikel:
- {fake.word()} ({random.randint(1,50)} Stück)
- {fake.word()} ({random.randint(1,20)} Stück)
Liefertermin: {fake.date_this_month()}
""",
        f"""Auftragsbestätigung / Bestellung
Kunde: {fake.company()}
Artikelübersicht:
{fake.word()} – Menge: {random.randint(10,200)} – Preis: {random.randint(100,3000)} EUR
Versand: DHL | Lieferadresse: {fake.address()}
""",
        f"""Bestellformular
Firma: {fake.company()}
An: {fake.company()}
Datum: {random_date()}
Bestellung: {fake.word()} – {random.randint(5,100)} Stück
Zahlungsart: Rechnung
""",
        f"""Einkaufsbestellung
Abteilung: Einkauf
Lieferant: {fake.company()}
Artikel: {fake.word().capitalize()}, Preis: {random.randint(100,1000)} EUR
Lieferung bis: {fake.date_this_month()}
""",
        f"""Online-Bestellung
Kundennummer: {fake.random_int(10000,99999)}
Produkt: {fake.word()} ({random.randint(1,10)}x)
Gesamtbetrag: {random.randint(100,2500)} EUR
Bezahlmethode: PayPal
""",
        f"""Bestellung
Sehr geehrte Damen und Herren,
bitte liefern Sie uns folgende Produkte bis {fake.date_this_month()}:
- {fake.word()} ({random.randint(2,15)} Stück)
- {fake.word()} ({random.randint(1,5)} Stück)
Mit freundlichen Grüßen,
{fake.name()}
"""
    ]
    return random.choice(templates)

# ------------------ PAYMENT REMINDER (Zahlungserinnerung) ------------------
def make_reminder():
    templates = [
        f"""Zahlungserinnerung
Sehr geehrte Damen und Herren,
unsere Rechnung Nr. {fake.random_int(1000,9999)} vom {random_date()} ist noch offen.
Bitte begleichen Sie den Betrag von {random.randint(100,2000)} EUR innerhalb von 7 Tagen.
""",
        f"""Mahnung
Kundennummer: {fake.random_int(10000,99999)}
Offene Rechnung Nr. {fake.random_int(1000,9999)}.
Wir fordern Sie auf, den Betrag von {random.randint(100,5000)} EUR umgehend zu zahlen.
""",
        f"""Letzte Mahnung
Sehr geehrte Damen und Herren,
trotz mehrfacher Erinnerung ist Ihre Zahlung noch nicht eingegangen.
Gesamtforderung: {random.randint(500,3000)} EUR
Bitte überweisen Sie sofort.
""",
        f"""Erste Zahlungserinnerung
Rechnung {fake.random_int(1000,9999)} vom {random_date()}.
Offener Betrag: {random.randint(50,800)} EUR.
Zahlungsziel: {fake.date_this_month()}
""",
        f"""Freundliche Zahlungserinnerung
Dies ist eine Erinnerung an Ihre unbezahlte Rechnung Nr. {fake.random_int(1000,9999)}.
Gesamtbetrag: {random.randint(300,2000)} EUR
Zahlung bis spätestens {fake.date_this_month()} erbeten.
""",
        f"""Mahnung 2. Stufe
Offene Forderung: {random.randint(200,1000)} EUR.
Falls bereits gezahlt, betrachten Sie dieses Schreiben als gegenstandslos.
"""
    ]
    return random.choice(templates)

# ------------------ COMPLAINT (Beschwerde) ------------------
def make_complaint():
    templates = [
        f"""Beschwerde über Lieferung
Am {random_date()} haben wir beschädigte Ware erhalten ({fake.word()}).
Wir bitten um Ersatz oder Gutschrift.
Mit freundlichen Grüßen,
{fake.name()}, {fake.company()}
""",
        f"""Reklamation – Falsche Lieferung
Unsere Bestellung Nr. {fake.random_int(1000,9999)} war unvollständig.
Bitte prüfen Sie den Vorgang und liefern Sie nach.
""",
        f"""Kundenbeschwerde
Sehr geehrtes Serviceteam,
wir sind mit der Bearbeitung unseres Auftrags Nr. {fake.random_int(1000,9999)} unzufrieden.
Wir bitten um Stellungnahme innerhalb von 5 Werktagen.
""",
        f"""Mangelanzeige
Bei der Lieferung vom {random_date()} wurde ein defektes Produkt festgestellt.
Artikel: {fake.word().capitalize()}
Bitte senden Sie uns Ersatz.
""",
        f"""Reklamation
Sehr geehrte Damen und Herren,
die gelieferte Ware entspricht nicht der Bestellung.
Wir erwarten eine Korrektur oder Rückerstattung.
""",
        f"""Beschwerde über Kundenservice
Ich bin unzufrieden mit der Kommunikation Ihres Kundendienstes.
Ticketnummer: {fake.random_int(10000,99999)}
Bitte kontaktieren Sie mich zur Klärung.
"""
    ]
    return random.choice(templates)

# ------------------ GENERATE FILES ------------------
generators = {
    "invoice": make_invoice,
    "contract": make_contract,
    "order": make_order,
    "reminder": make_reminder,
    "complaint": make_complaint
}

# generate 100 per category
for category, func in generators.items():
    for i in range(100):
        with open(f"data_raw/{category}_{i+1}.txt", "w", encoding="utf-8") as f:
            f.write(func())

print("✅ Generated 500+ diverse German business documents in data_raw/")
