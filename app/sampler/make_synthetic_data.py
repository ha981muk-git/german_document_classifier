from pathlib import Path
from typing import Optional, Sequence
from faker import Faker
import random


class SyntheticDocumentGenerator:
    """Generate German business documents and persist them as .txt files."""

    def __init__(
        self,
        per_category: int = 200,
        output_dir: str = "app/data/synthetic",
        locales: Optional[Sequence[str]] = None,
        seed: Optional[int] = None,
    ) -> None:
        self.fake = Faker(locales or ["de_DE", "de_AT", "de_CH"])
        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)
        self.per_category = per_category
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generators = {
            "invoices": self.make_invoice,
            "contracts": self.make_contract,
            "orders": self.make_order,
            "paymentreminders": self.make_reminder,
            "complaints": self.make_complaint,
        }

    def random_date(self) -> str:
        return self.fake.date_between(start_date="-2y", end_date="today").strftime(
            "%d.%m.%Y"
        )

    # ------------------ INVOICE (Rechnung) ------------------
    def make_invoice(self):
        templates = [
            f"""Rechnung Nr. {self.fake.random_int(1000,9999)}
Datum: {self.random_date()}
Kunde: {self.fake.name()}
{self.fake.company()}, {self.fake.address()}

Pos. | Beschreibung             | Betrag (EUR)
1    | {self.fake.word().capitalize()}                | {random.randint(100,800)}
2    | {self.fake.word().capitalize()}                | {random.randint(50,600)}

Zwischensumme: {random.randint(400,1500)} EUR
MwSt (19%): {round(random.uniform(10,300),2)} EUR
Gesamtbetrag: {random.randint(500,5000)} EUR
Bitte überweisen Sie den Betrag bis {self.fake.date_this_month()}.

Mit freundlichen Grüßen,
{self.fake.company()}
""",
            f"""Rechnung
Rechnungsnummer: {self.fake.random_int(1000,9999)}
Rechnungsdatum: {self.random_date()}

Leistungszeitraum: {self.fake.date_this_year()} - {self.fake.date_this_year()}
Empfänger: {self.fake.name()}, {self.fake.company()}
Summe: {random.randint(200,3000)} EUR
Zahlungsziel: 14 Tage ab Rechnungsdatum.
""",
            f"""*** RECHNUNG ***
Von: {self.fake.company()}
An: {self.fake.name()}
Rechnungsdatum: {self.random_date()}
Betrag: {random.randint(100,5000)} EUR

Bitte zahlen Sie auf Konto IBAN DE{self.fake.random_int(10000000000000000000,99999999999999999999)}.
""",
            f"""RECHNUNG - {self.fake.company()}
Kunde: {self.fake.name()}
Adresse: {self.fake.address()}
Rechnungsdatum: {self.random_date()}
Zahlungsbedingungen: 30 Tage netto
Gesamt: {random.randint(500,7000)} EUR
""",
            f"""Rechnung {self.fake.random_int(1000,9999)}
Firma: {self.fake.company()}
Empfänger: {self.fake.name()}
Leistung: {self.fake.catch_phrase()}
Preis: {random.randint(300,5000)} EUR (inkl. MwSt)
""",
            f"""Rechnungsbeleg
Firma: {self.fake.company()}
Adresse: {self.fake.address()}
Rechnung Nr.: {self.fake.random_int(1000,9999)} | Datum: {self.random_date()}
Gesamtbetrag: {random.randint(100,4000)} EUR
Fällig am: {self.fake.date_this_month()}
""",
        ]
        return random.choice(templates)

    # ------------------ CONTRACT (Vertrag) ------------------
    def make_contract(self):
        templates = [
            f"""Dienstleistungsvertrag
Zwischen {self.fake.company()} (Auftragnehmer)
und {self.fake.company()} (Auftraggeber)

Vertragsbeginn: {self.random_date()}
Laufzeit: {random.randint(6,36)} Monate
Leistungsumfang: {self.fake.catch_phrase()}
Kündigungsfrist: 3 Monate zum Vertragsende.
""",
            f"""Kaufvertrag
Verkäufer: {self.fake.company()}
Käufer: {self.fake.company()}
Ware: {self.fake.word().capitalize()}
Preis: {random.randint(500,8000)} EUR
Lieferdatum: {self.fake.date_this_month()}
""",
            f"""Vertrag über Zusammenarbeit
Dieser Vertrag wird zwischen {self.fake.company()} und {self.fake.company()} geschlossen.
Beginn: {self.random_date()}
Ziel: Förderung gemeinsamer Projekte im Bereich {self.fake.word()}.
""",
            f"""Mietvertrag
Vermieter: {self.fake.company()}
Mieter: {self.fake.name()}
Objekt: {self.fake.address()}
Monatsmiete: {random.randint(800,2500)} EUR
Vertragsbeginn: {self.random_date()}
""",
            f"""Arbeitsvertrag
Arbeitgeber: {self.fake.company()}
Arbeitnehmer: {self.fake.name()}
Beginn: {self.random_date()}
Tätigkeit: {self.fake.job()}
Vergütung: {random.randint(2500,6000)} EUR monatlich.
""",
            f"""Kooperationsvertrag
Zwischen {self.fake.company()} und {self.fake.company()}.
Vertragsdauer: {random.randint(12,48)} Monate
Kündigung: schriftlich, Frist 4 Wochen.
Ort, Datum: {self.fake.city()}, {self.random_date()}
""",
        ]
        return random.choice(templates)

    # ------------------ PURCHASE ORDER (Bestellung) ------------------
    def make_order(self):
        templates = [
            f"""Bestellung Nr. {self.fake.random_int(1000,9999)}
Datum: {self.random_date()}
Wir bestellen folgende Artikel:
- {self.fake.word()} ({random.randint(1,50)} Stück)
- {self.fake.word()} ({random.randint(1,20)} Stück)
Liefertermin: {self.fake.date_this_month()}
""",
            f"""Auftragsbestätigung / Bestellung
Kunde: {self.fake.company()}
Artikelübersicht:
{self.fake.word()} – Menge: {random.randint(10,200)} – Preis: {random.randint(100,3000)} EUR
Versand: DHL | Lieferadresse: {self.fake.address()}
""",
            f"""Bestellformular
Firma: {self.fake.company()}
An: {self.fake.company()}
Datum: {self.random_date()}
Bestellung: {self.fake.word()} – {random.randint(5,100)} Stück
Zahlungsart: Rechnung
""",
            f"""Einkaufsbestellung
Abteilung: Einkauf
Lieferant: {self.fake.company()}
Artikel: {self.fake.word().capitalize()}, Preis: {random.randint(100,1000)} EUR
Lieferung bis: {self.fake.date_this_month()}
""",
            f"""Online-Bestellung
Kundennummer: {self.fake.random_int(10000,99999)}
Produkt: {self.fake.word()} ({random.randint(1,10)}x)
Gesamtbetrag: {random.randint(100,2500)} EUR
Bezahlmethode: PayPal
""",
            f"""Bestellung
Sehr geehrte Damen und Herren,
bitte liefern Sie uns folgende Produkte bis {self.fake.date_this_month()}:
- {self.fake.word()} ({random.randint(2,15)} Stück)
- {self.fake.word()} ({random.randint(1,5)} Stück)
Mit freundlichen Grüßen,
{self.fake.name()}
""",
        ]
        return random.choice(templates)

    # ------------------ PAYMENT REMINDER (Zahlungserinnerung) ------------------
    def make_reminder(self):
        templates = [
            f"""Zahlungserinnerung
Sehr geehrte Damen und Herren,
unsere Rechnung Nr. {self.fake.random_int(1000,9999)} vom {self.random_date()} ist noch offen.
Bitte begleichen Sie den Betrag von {random.randint(100,2000)} EUR innerhalb von 7 Tagen.
""",
            f"""Mahnung
Kundennummer: {self.fake.random_int(10000,99999)}
Offene Rechnung Nr. {self.fake.random_int(1000,9999)}.
Wir fordern Sie auf, den Betrag von {random.randint(100,5000)} EUR umgehend zu zahlen.
""",
            f"""Letzte Mahnung
Sehr geehrte Damen und Herren,
trotz mehrfacher Erinnerung ist Ihre Zahlung noch nicht eingegangen.
Gesamtforderung: {random.randint(500,3000)} EUR
Bitte überweisen Sie sofort.
""",
            f"""Erste Zahlungserinnerung
Rechnung {self.fake.random_int(1000,9999)} vom {self.random_date()}.
Offener Betrag: {random.randint(50,800)} EUR.
Zahlungsziel: {self.fake.date_this_month()}
""",
            f"""Freundliche Zahlungserinnerung
Dies ist eine Erinnerung an Ihre unbezahlte Rechnung Nr. {self.fake.random_int(1000,9999)}.
Gesamtbetrag: {random.randint(300,2000)} EUR
Zahlung bis spätestens {self.fake.date_this_month()} erbeten.
""",
            f"""Mahnung 2. Stufe
Offene Forderung: {random.randint(200,1000)} EUR.
Falls bereits gezahlt, betrachten Sie dieses Schreiben als gegenstandslos.
""",
        ]
        return random.choice(templates)

    # ------------------ COMPLAINT (Beschwerde) ------------------
    def make_complaint(self):
        templates = [
            f"""Beschwerde über Lieferung
Am {self.random_date()} haben wir beschädigte Ware erhalten ({self.fake.word()}).
Wir bitten um Ersatz oder Gutschrift.
Mit freundlichen Grüßen,
{self.fake.name()}, {self.fake.company()}
""",
            f"""Reklamation – Falsche Lieferung
Unsere Bestellung Nr. {self.fake.random_int(1000,9999)} war unvollständig.
Bitte prüfen Sie den Vorgang und liefern Sie nach.
""",
            f"""Kundenbeschwerde
Sehr geehrtes Serviceteam,
wir sind mit der Bearbeitung unseres Auftrags Nr. {self.fake.random_int(1000,9999)} unzufrieden.
Wir bitten um Stellungnahme innerhalb von 5 Werktagen.
""",
            f"""Mangelanzeige
Bei der Lieferung vom {self.random_date()} wurde ein defektes Produkt festgestellt.
Artikel: {self.fake.word().capitalize()}
Bitte senden Sie uns Ersatz.
""",
            f"""Reklamation
Sehr geehrte Damen und Herren,
die gelieferte Ware entspricht nicht der Bestellung.
Wir erwarten eine Korrektur oder Rückerstattung.
""",
            f"""Beschwerde über Kundenservice
Ich bin unzufrieden mit der Kommunikation Ihres Kundendienstes.
Ticketnummer: {self.fake.random_int(10000,99999)}
Bitte kontaktieren Sie mich zur Klärung.
""",
        ]
        return random.choice(templates)

    def generate_documents(
        self, per_category: Optional[int] = None, overwrite: bool = False
    ) -> int:
        """Create .txt files for every configured category."""
        per_category = per_category or self.per_category
        files_written = 0

        for category, generator in self.generators.items():
            category_dir = self.output_dir / category
            category_dir.mkdir(exist_ok=True)
            for i in range(per_category):
                filename = category_dir / f"{category.rstrip('s')}_v0_{i+1}.txt"
                if filename.exists() and not overwrite:
                    continue
                filename.write_text(generator(), encoding="utf-8")
                files_written += 1

        return files_written
