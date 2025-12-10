"""
German Business Document Generator - Enhanced Version
Generates 10-15 different variations per document type for robust model training
"""

import random
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from sklearn.utils import resample

class GermanDocumentGenerator:
    def __init__(self):
        # German company names
        self.companies = [
            "Müller GmbH", "Schmidt AG", "Weber & Co. KG", "Fischer Handel",
            "Becker Logistik GmbH", "Hoffmann Industries", "Schulz Consulting",
            "Koch Engineering", "Bauer Manufacturing", "Richter Solutions AG",
            "Zimmermann Tech", "Krüger Services", "Lehmann Group", "Braun Digital"
        ]
        
        self.cities = [
            "München", "Hamburg", "Berlin", "Frankfurt am Main", "Köln",
            "Stuttgart", "Düsseldorf", "Dortmund", "Essen", "Leipzig",
            "Dresden", "Hannover", "Nürnberg", "Bremen", "Bonn"
        ]
        
        self.streets = [
            "Hauptstraße 15", "Bahnhofstraße 23", "Kirchweg 8", "Industriestraße 42",
            "Am Marktplatz 5", "Königsallee 88", "Gartenstraße 12", "Berliner Straße 99"
        ]
        
        self.products = [
            "Beratungsleistung", "Softwareentwicklung", "Wartungsvertrag",
            "Lieferung Büromaterial", "IT-Support", "Marketing-Kampagne", 
            "Schulungsmaßnahme", "Personalvermittlung", "Reinigungsservice",
            "Logistikdienstleistung", "Webdesign", "Cloud-Hosting", "SEO-Optimierung"
        ]
        
        self.names = [
            "Thomas Müller", "Anna Schmidt", "Michael Weber", "Sarah Fischer",
            "Martin Becker", "Julia Hoffmann", "Klaus Schulz", "Lisa Koch",
            "Peter Bauer", "Maria Richter", "Stefan Wagner", "Laura Klein"
        ]
    def random_date(self):
        """Generate a random date within the last 2 years"""
        days_ago = random.randint(1, 730)  # 730 days = ~2 years
        return (datetime.now() - timedelta(days=days_ago)).strftime('%d.%m.%Y')
    
    def generate_invoices(self, n=100):
        """Generate 15 different invoice template variations"""
        invoices = []
        
        templates = [
            self._invoice_template_formal,
            self._invoice_template_simple,
            self._invoice_template_detailed,
            self._invoice_template_multi_item,
            self._invoice_template_service,
            self._invoice_template_international,
            self._invoice_template_small_business,
            self._invoice_template_partial_payment,
            self._invoice_template_credit_note,
            self._invoice_template_advance,
            self._invoice_template_subscription,
            self._invoice_template_hourly,
            self._invoice_template_project,
            self._invoice_template_retail,
            self._invoice_template_freelancer
        ]
        
        for i in range(n):
            template = random.choice(templates)
            invoices.append({'text': template(i), 'label': 'Rechnung'})
        
        return invoices
    
    def _invoice_template_formal(self, i):
        """Formal corporate invoice"""
        invoice_num = f"RE-2024-{1000+i}"
        date = (datetime.now() - timedelta(days=random.randint(1, 180))).strftime('%d.%m.%Y')
        due_date = (datetime.now() + timedelta(days=random.randint(14, 30))).strftime('%d.%m.%Y')
        company = random.choice(self.companies)
        city = random.choice(self.cities)
        street = random.choice(self.streets)
        product = random.choice(self.products)
        amount = random.randint(1000, 25000)
        tax = round(amount * 0.19, 2)
        total = round(amount + tax, 2)
        
        return f"""
═══════════════════════════════════════════════════════════════
                         R E C H N U N G
═══════════════════════════════════════════════════════════════

{random.choice(self.companies)}
{random.choice(self.streets)}
{random.choice(self.cities)}
Steuernummer: {random.randint(100, 999)}/{random.randint(1000, 9999)}/{random.randint(1000, 9999)}

Rechnungsempfänger:
{company}
{street}
{city}

Rechnungsnummer:    {invoice_num}
Rechnungsdatum:     {date}
Leistungsdatum:     {date}
Kundennummer:       KD-{random.randint(10000, 99999)}

─────────────────────────────────────────────────────────────────
Position    Bezeichnung                  Menge    Preis      Gesamt
─────────────────────────────────────────────────────────────────
1           {product}                    1        {amount:.2f}€  {amount:.2f}€
─────────────────────────────────────────────────────────────────

                                        Nettobetrag:    {amount:.2f}€
                                        MwSt. 19%:      {tax:.2f}€
                                        ═════════════════════════
                                        Gesamtbetrag:   {total:.2f}€

Zahlbar bis: {due_date} ohne Abzug
Zahlungsziel: 14 Tage netto

Bankverbindung:
IBAN: DE{random.randint(10, 99)} {random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(10, 99)}
BIC: DEUTDEFF
Bank: Deutsche Bank

Vielen Dank für Ihren Auftrag!

Mit freundlichen Grüßen
Buchhaltungsabteilung
"""
    
    def _invoice_template_simple(self, i):
        """Simple minimal invoice"""
        return f"""Rechnung Nr. {1000+i}

Datum: {(datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%d.%m.%Y')}

An: {random.choice(self.companies)}

Leistung: {random.choice(self.products)}
Betrag: {random.randint(500, 5000)},00 EUR (inkl. MwSt.)

Bitte überweisen Sie den Betrag bis {(datetime.now() + timedelta(days=14)).strftime('%d.%m.%Y')}.

Vielen Dank!
"""
    
    def _invoice_template_detailed(self, i):
        """Detailed invoice with multiple line items"""
        amount1 = random.randint(500, 3000)
        amount2 = random.randint(300, 2000)
        amount3 = random.randint(200, 1500)
        subtotal = amount1 + amount2 + amount3
        tax = round(subtotal * 0.19, 2)
        total = subtotal + tax
        
        return f"""
RECHNUNG

Von: {random.choice(self.companies)}
     {random.choice(self.cities)}

An:  {random.choice(self.companies)}
     {random.choice(self.streets)}
     {random.choice(self.cities)}

Rechnungs-Nr: INV-{random.randint(10000, 99999)}
Datum: {datetime.now().strftime('%d.%m.%Y')}

Pos  Artikel/Dienstleistung              Menge  Einzelpreis  Gesamtpreis
───────────────────────────────────────────────────────────────────────
1    {random.choice(self.products)}      10     {amount1/10:.2f}€    {amount1:.2f}€
2    {random.choice(self.products)}      5      {amount2/5:.2f}€     {amount2:.2f}€
3    {random.choice(self.products)}      1      {amount3:.2f}€       {amount3:.2f}€

                                         Zwischensumme: {subtotal:.2f}€
                                         MwSt (19%):    {tax:.2f}€
                                         ─────────────────────────
                                         GESAMT:        {total:.2f}€

Zahlungsbedingungen: 30 Tage netto
Fällig am: {(datetime.now() + timedelta(days=30)).strftime('%d.%m.%Y')}
"""
    
    def _invoice_template_multi_item(self, i):
        """Invoice with 5-7 different items"""
        items = random.sample(self.products, k=min(6, len(self.products)))
        subtotal = 0
        item_lines = ""
        
        for idx, item in enumerate(items, 1):
            qty = random.randint(1, 10)
            price = random.randint(50, 500)
            total_item = qty * price
            subtotal += total_item
            item_lines += f"{idx:2d}  {item:30s}  {qty:3d}  {price:6.2f}€  {total_item:8.2f}€\n"
        
        tax = round(subtotal * 0.19, 2)
        total = subtotal + tax
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                    RECHNUNG / INVOICE                        ║
╚══════════════════════════════════════════════════════════════╝

Rechnungsnummer: R-{random.randint(2024000, 2024999)}
Datum: {datetime.now().strftime('%d.%m.%Y')}

Kunde: {random.choice(self.companies)}

Pos  Beschreibung                      Menge  Preis     Gesamt
──────────────────────────────────────────────────────────────
{item_lines}
──────────────────────────────────────────────────────────────
                                      Netto:          {subtotal:.2f}€
                                      + MwSt 19%:     {tax:.2f}€
                                      ══════════════════════════
                                      TOTAL:          {total:.2f}€

Bitte zahlen Sie bis: {(datetime.now() + timedelta(days=14)).strftime('%d.%m.%Y')}
"""
    
    def _invoice_template_service(self, i):
        """Service-based invoice with hours"""
        hours = random.randint(10, 80)
        rate = random.randint(80, 150)
        subtotal = hours * rate
        tax = round(subtotal * 0.19, 2)
        
        return f"""
DIENSTLEISTUNGSRECHNUNG

Rechnung: DL-{random.randint(5000, 9999)}
Datum: {datetime.now().strftime('%d.%m.%Y')}

Leistungsempfänger:
{random.choice(self.companies)}
{random.choice(self.cities)}

Leistungsbeschreibung:
{random.choice(self.products)} für Projekt XYZ

Zeitraum: {(datetime.now() - timedelta(days=30)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}

Stundenabrechnung:
{hours} Stunden à {rate}€/Std = {subtotal}€

Nettobetrag:              {subtotal}€
Umsatzsteuer 19%:         {tax:.2f}€
───────────────────────────────────
Rechnungsbetrag:          {subtotal + tax:.2f}€

Zahlbar innerhalb 14 Tagen.
"""
    
    def _invoice_template_international(self, i):
        """International style invoice (bilingual hints)"""
        amount = random.randint(2000, 15000)
        tax = round(amount * 0.19, 2)
        
        return f"""
INVOICE / RECHNUNG

Invoice No. / Rechnungsnr.: INT-{random.randint(10000, 99999)}
Date / Datum: {datetime.now().strftime('%d.%m.%Y')}

Billed to / Rechnungsempfänger:
{random.choice(self.companies)}
{random.choice(self.cities)}, Germany

Description / Beschreibung:
{random.choice(self.products)}

Amount / Betrag (net):           €{amount:.2f}
VAT 19% / MwSt. 19%:             €{tax:.2f}
─────────────────────────────────────────
Total / Gesamt:                  €{amount + tax:.2f}

Payment terms / Zahlungsbedingungen: 30 days net / 30 Tage netto
Due date / Fälligkeitsdatum: {(datetime.now() + timedelta(days=30)).strftime('%d.%m.%Y')}

Thank you for your business / Vielen Dank für Ihren Auftrag
"""
    
    def _invoice_template_small_business(self, i):
        """Small business invoice (§19 UStG - no VAT)"""
        amount = random.randint(300, 2000)
        
        return f"""
Kleinunternehmer-Rechnung

Rechnung Nr.: KU-{random.randint(1000, 9999)}
Ausstellungsdatum: {datetime.now().strftime('%d.%m.%Y')}

Rechnungssteller:
{random.choice(self.names)}
Freiberuflicher {random.choice(['Berater', 'Designer', 'Entwickler'])}
{random.choice(self.streets)}, {random.choice(self.cities)}

Auftraggeber:
{random.choice(self.companies)}

Leistung:
{random.choice(self.products)}

Rechnungsbetrag: {amount}€

Gemäß §19 UStG wird keine Umsatzsteuer berechnet.

Bitte überweisen Sie den Betrag innerhalb von 14 Tagen.

Herzlichen Dank!
{random.choice(self.names)}
"""
    
    def _invoice_template_partial_payment(self, i):
        """Partial payment / installment invoice"""
        total = random.randint(10000, 50000)
        partial = round(total * 0.3, 2)
        
        return f"""
ABSCHLAGSRECHNUNG / TEILRECHNUNG

Rechnung Nr.: AB-{random.randint(1000, 9999)}
Datum: {datetime.now().strftime('%d.%m.%Y')}

Projekt: {random.choice(self.products)}
Auftraggeber: {random.choice(self.companies)}

Gesamtauftragswert:              {total}€
Bereits bezahlt:                 {round(total * 0.1, 2)}€
Abschlagszahlung (30%):          {partial}€
───────────────────────────────────────────
Fälliger Betrag:                 {partial}€

Dies ist die 2. von 4 Teilrechnungen.

Zahlbar bis: {(datetime.now() + timedelta(days=7)).strftime('%d.%m.%Y')}
"""
    
    def _invoice_template_credit_note(self, i):
        """Credit note / Gutschrift"""
        amount = random.randint(500, 5000)
        tax = round(amount * 0.19, 2)
        
        return f"""
GUTSCHRIFT

Gutschrift-Nr.: GS-{random.randint(1000, 9999)}
Datum: {datetime.now().strftime('%d.%m.%Y')}
Bezug: Rechnung RE-{random.randint(1000, 9999)}

An: {random.choice(self.companies)}

Grund: Rücknahme / Retoure / Preisnachlass

Position: {random.choice(self.products)}

Gutschriftbetrag netto:     -{amount}€
MwSt. 19%:                  -{tax:.2f}€
─────────────────────────────────────
Gesamtgutschrift:           -{amount + tax:.2f}€

Der Betrag wird Ihrem Konto gutgeschrieben oder mit der nächsten Rechnung verrechnet.

Mit freundlichen Grüßen
"""
    
    def _invoice_template_advance(self, i):
        """Advance payment invoice"""
        total = random.randint(15000, 80000)
        advance = round(total * 0.5, 2)
        tax = round(advance * 0.19, 2)
        
        return f"""
ANZAHLUNGSRECHNUNG

Rechnung: ANZ-{random.randint(1000, 9999)}
Datum: {datetime.now().strftime('%d.%m.%Y')}

Kunde: {random.choice(self.companies)}
Projekt: {random.choice(self.products)}

Gesamtauftragswert:          {total}€
Anzahlung 50%:               {advance}€
MwSt. 19%:                   {tax:.2f}€
─────────────────────────────────────
Fälliger Betrag:             {advance + tax:.2f}€

Diese Rechnung ist eine Vorauszahlung. Die Endabrechnung erfolgt nach Projektabschluss.

Bitte überweisen Sie den Betrag bis {(datetime.now() + timedelta(days=7)).strftime('%d.%m.%Y')}.
"""
    
    def _invoice_template_subscription(self, i):
        """Monthly subscription invoice"""
        monthly = random.randint(99, 999)
        tax = round(monthly * 0.19, 2)
        
        return f"""
ABONNEMENT-RECHNUNG

Rechnung: ABO-{random.randint(10000, 99999)}
Abrechnungszeitraum: {datetime.now().strftime('%m/%Y')}

Kunde: {random.choice(self.companies)}
Kunden-ID: {random.randint(100000, 999999)}

Abonnement: {random.choice(['Professional Plan', 'Enterprise License', 'Premium Service'])}
Laufzeit: monatlich

Monatsbeitrag:           {monthly}€
MwSt. 19%:               {tax:.2f}€
─────────────────────────────────
Gesamt:                  {monthly + tax:.2f}€

Die Zahlung erfolgt automatisch per SEPA-Lastschrift am {random.randint(1, 5)}. des Monats.

Bei Fragen: support@{random.choice(self.companies).lower().replace(' ', '')}.de
"""
    
    def _invoice_template_hourly(self, i):
        """Detailed hourly rate invoice"""
        return f"""
STUNDENNACHWEIS & RECHNUNG

Rechnung: ST-{random.randint(1000, 9999)}
Zeitraum: {(datetime.now() - timedelta(days=30)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}

Auftraggeber: {random.choice(self.companies)}
Dienstleister: {random.choice(self.names)}

Datum       Tätigkeit                           Stunden  Rate    Betrag
─────────────────────────────────────────────────────────────────────
{(datetime.now() - timedelta(days=20)).strftime('%d.%m')}  {random.choice(['Entwicklung', 'Beratung', 'Design'])}  {random.randint(4, 8)}h     95€     {random.randint(380, 760)}€
{(datetime.now() - timedelta(days=15)).strftime('%d.%m')}  {random.choice(['Testing', 'Meeting', 'Planung'])}     {random.randint(2, 6)}h     95€     {random.randint(190, 570)}€
{(datetime.now() - timedelta(days=10)).strftime('%d.%m')}  {random.choice(['Implementation', 'Review'])}          {random.randint(5, 8)}h     95€     {random.randint(475, 760)}€
{(datetime.now() - timedelta(days=5)).strftime('%d.%m')}   {random.choice(['Dokumentation', 'Support'])}          {random.randint(3, 5)}h     95€     {random.randint(285, 475)}€

Gesamtstunden: {random.randint(25, 45)}h
Nettobetrag: {random.randint(2000, 4500)}€
MwSt. 19%: {random.randint(380, 855)}€
─────────────────────────────────────────────────────────────────────
GESAMT: {random.randint(2380, 5355)}€
"""
    
    def _invoice_template_project(self, i):
        """Project milestone invoice"""
        milestone = random.choice(['Konzeptphase', 'Design-Phase', 'Entwicklungsphase', 'Testing-Phase', 'Go-Live'])
        amount = random.randint(8000, 25000)
        
        return f"""
PROJEKT-RECHNUNG

Rechnung: PR-{random.randint(10000, 99999)}
Datum: {datetime.now().strftime('%d.%m.%Y')}

Projekt: "{random.choice(['Website Relaunch', 'App Entwicklung', 'System Integration', 'Cloud Migration'])}"
Kunde: {random.choice(self.companies)}
Projekt-Nr: P{random.randint(2024000, 2024999)}

Meilenstein: {milestone} (abgeschlossen)
Projektfortschritt: {random.randint(20, 80)}%

Rechnungsbetrag (netto):     {amount}€
Umsatzsteuer 19%:            {round(amount * 0.19, 2)}€
═══════════════════════════════════════
GESAMTBETRAG:                {amount + round(amount * 0.19, 2)}€

Nächster Meilenstein: {random.choice(['Q4 2024', 'Q1 2025', 'Ende November'])}

Zahlbar innerhalb 14 Tagen ab Rechnungsdatum.
"""
    
    def _invoice_template_retail(self, i):
        """Retail/Shop invoice"""
        return f"""
════════════════════════════════════════
    {random.choice(self.companies)}
    {random.choice(self.streets)}
    {random.choice(self.cities)}
════════════════════════════════════════

KASSENBON / RECHNUNG
Bon-Nr: {random.randint(100000, 999999)}
Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}
Kasse: {random.randint(1, 5)}

Artikel                      Anzahl  Preis
────────────────────────────────────────
{random.choice(['Laptop', 'Monitor', 'Tastatur'])}                     1    {random.randint(400, 1200)}€
{random.choice(['Maus', 'Headset', 'Webcam'])}                        2    {random.randint(30, 150)}€
{random.choice(['USB-Stick', 'Kabel', 'Adapter'])}                    3    {random.randint(10, 40)}€

                        SUMME: {random.randint(500, 1500)}€
                  davon MwSt.: {random.randint(95, 285)}€

Zahlungsart: {random.choice(['Kartenzahlung', 'Bar', 'Rechnung'])}

Vielen Dank für Ihren Einkauf!
Umtausch nur mit Kassenbon.
════════════════════════════════════════
"""
    
    def _invoice_template_freelancer(self, i):
        """Freelancer invoice"""
        amount = random.randint(1500, 6000)
        
        return f"""
HONORARRECHNUNG

Von:
{random.choice(self.names)}
Freiberufliche/r {random.choice(['Grafiker/in', 'Texter/in', 'Fotograf/in', 'Berater/in'])}
{random.choice(self.streets)}
{random.choice(self.cities)}
Steuernummer: {random.randint(100, 999)}/{random.randint(1000, 9999)}/{random.randint(1000, 9999)}

An:
{random.choice(self.companies)}

Rechnung Nr.: FL-{random.randint(2024, 2025)}-{random.randint(100, 999)}
Leistungsdatum: {(datetime.now() - timedelta(days=7)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}
Rechnungsdatum: {datetime.now().strftime('%d.%m.%Y')}

Leistungsbeschreibung:
{random.choice(self.products)} gemäß Vereinbarung vom {(datetime.now() - timedelta(days=30)).strftime('%d.%m.%Y')}

Honorar:                     {amount}€
Umsatzsteuer 19%:            {round(amount * 0.19, 2)}€
───────────────────────────────────────
Gesamtbetrag:                {amount + round(amount * 0.19, 2)}€

Zahlbar innerhalb von 14 Tagen netto.

Mit freundlichen Grüßen
{random.choice(self.names)}
"""

    def generate_contracts(self, n=100):
        """Generate 15 different contract variations"""
        contracts = []
        
        templates = [
            self._contract_template_service,
            self._contract_template_employment,
            self._contract_template_rental,
            self._contract_template_nda,
            self._contract_template_partnership,
            self._contract_template_license,
            self._contract_template_maintenance,
            self._contract_template_consulting,
            self._contract_template_supply,
            self._contract_template_framework,
            self._contract_template_subcontractor,
            self._contract_template_sales,
            self._contract_template_loan,
            self._contract_template_hosting,
            self._contract_template_training
        ]
        
        for i in range(n):
            template = random.choice(templates)
            contracts.append({'text': template(i), 'label': 'Vertrag'})
        
        return contracts
    
    def _contract_template_service(self, i):
        """Standard service contract"""
        contract_num = f"V-2024-{2000+i}"
        date = datetime.now().strftime('%d.%m.%Y')
        company1 = random.choice(self.companies)
        company2 = random.choice([c for c in self.companies if c != company1])
        duration = random.choice(['12', '24', '36'])
        service = random.choice(self.products)
        value = random.randint(10000, 100000)
        
        return f"""
DIENSTLEISTUNGSVERTRAG

Vertragsnummer: {contract_num}
Vertragsdatum: {date}

zwischen

{company1}
{random.choice(self.streets)}
{random.choice(self.cities)}
(nachfolgend "Auftraggeber" genannt)

und

{company2}
{random.choice(self.streets)}
{random.choice(self.cities)}
(nachfolgend "Auftragnehmer" genannt)

§ 1 Vertragsgegenstand
Der Auftragnehmer verpflichtet sich zur Erbringung folgender Leistungen:
{service}

§ 2 Vertragslaufzeit
Dieser Vertrag beginnt am {date} und läuft über eine Dauer von {duration} Monaten.
Eine ordentliche Kündigung ist mit einer Frist von 3 Monaten zum Monatsende möglich.

§ 3 Vergütung und Zahlung
Die Vergütung beträgt {value:,}€ netto pro Jahr.
Die Zahlung erfolgt in monatlichen Raten von {round(value/12, 2):,}€.
Rechnungsstellung jeweils zum Monatsende, Zahlung innerhalb von 14 Tagen.

§ 4 Leistungsumfang
Der Auftragnehmer erbringt die Leistungen nach bestem Wissen und Gewissen.
Änderungen des Leistungsumfangs bedürfen der Schriftform.

§ 5 Haftung
Die Haftung richtet sich nach den gesetzlichen Bestimmungen.

§ 6 Geheimhaltung
Beide Parteien verpflichten sich zur Vertraulichkeit über alle im Rahmen dieses
Vertrages bekannt gewordenen Informationen.

§ 7 Schlussbestimmungen
Es gilt das Recht der Bundesrepublik Deutschland.
Erfüllungsort und Gerichtsstand ist {random.choice(self.cities)}.

{random.choice(self.cities)}, {date}        {random.choice(self.cities)}, {date}

_______________________              _______________________
Auftraggeber                         Auftragnehmer
"""
    
    def _contract_template_employment(self, i):
        """Employment contract"""
        name = random.choice(self.names)
        company = random.choice(self.companies)
        salary = random.randint(45000, 85000)
        position = random.choice(['Software Engineer', 'Projektmanager', 'Vertriebsmitarbeiter', 'Controller'])
        
        return f"""
ARBEITSVERTRAG

zwischen

{company}
{random.choice(self.streets)}
{random.choice(self.cities)}
- nachfolgend "Arbeitgeber" -

und

{name}
{random.choice(self.streets)}
{random.choice(self.cities)}
- nachfolgend "Arbeitnehmer/in" -

§ 1 Beginn und Dauer des Arbeitsverhältnisses
Das Arbeitsverhältnis beginnt am {(datetime.now() + timedelta(days=30)).strftime('%d.%m.%Y')}.
Es wird auf unbestimmte Zeit geschlossen.
Die Probezeit beträgt 6 Monate.

§ 2 Tätigkeit
Der/Die Arbeitnehmer/in wird als {position} eingestellt.

§ 3 Arbeitszeit
Die regelmäßige wöchentliche Arbeitszeit beträgt 40 Stunden.

§ 4 Vergütung
Das Bruttomonatsgehalt beträgt {round(salary/12, 2):,}€.
Das Jahresbruttogehalt beträgt {salary:,}€.
Die Zahlung erfolgt monatlich nachträglich.

§ 5 Urlaub
Der/Die Arbeitnehmer/in hat Anspruch auf 30 Arbeitstage Erholungsurlaub pro Jahr.

§ 6 Kündigungsfristen
Während der Probezeit beträgt die Kündigungsfrist 2 Wochen.
Nach der Probezeit gelten die gesetzlichen Kündigungsfristen.

§ 7 Nebentätigkeiten
Nebentätigkeiten bedürfen der vorherigen schriftlichen Zustimmung des Arbeitgebers.

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Arbeitgeber                          Arbeitnehmer/in
"""
    
    def _contract_template_rental(self, i):
        """Rental/Lease contract"""
        rent = random.randint(800, 2500)
        deposit = rent * 3
        
        return f"""
MIETVERTRAG

zwischen

{random.choice(self.names)}
{random.choice(self.streets)}
{random.choice(self.cities)}
- nachfolgend "Vermieter" -

und

{random.choice(self.names)}
{random.choice(self.streets)}
{random.choice(self.cities)}
- nachfolgend "Mieter" -

§ 1 Mietobjekt
Vermietet wird die Wohnung im {random.choice(['EG', 'OG', '1. OG', '2. OG'])}
{random.choice(self.streets)}
{random.choice(self.cities)}
Wohnfläche: ca. {random.randint(45, 120)} qm, {random.randint(2, 4)} Zimmer

§ 2 Mietbeginn und Mietdauer
Das Mietverhältnis beginnt am {(datetime.now() + timedelta(days=60)).strftime('%d.%m.%Y')}.
Der Vertrag wird auf unbestimmte Zeit geschlossen.

§ 3 Miete und Nebenkosten
Die Kaltmiete beträgt monatlich {rent}€.
Die Vorauszahlung für Nebenkosten beträgt monatlich {random.randint(150, 350)}€.
Die Gesamtmiete beträgt somit {rent + random.randint(150, 350)}€.

§ 4 Kaution
Der Mieter zahlt eine Kaution in Höhe von {deposit}€.

§ 5 Kündigungsfrist
Die Kündigungsfrist beträgt 3 Monate zum Monatsende.

§ 6 Schönheitsreparaturen
Schönheitsreparaturen trägt der Mieter gemäß gesonderter Vereinbarung.

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Vermieter                            Mieter
"""
    
    def _contract_template_nda(self, i):
        """Non-Disclosure Agreement"""
        return f"""
GEHEIMHALTUNGSVEREINBARUNG
(Non-Disclosure Agreement - NDA)

zwischen

{random.choice(self.companies)}
{random.choice(self.cities)}
- "offenlegende Partei" -

und

{random.choice(self.companies)}
{random.choice(self.cities)}
- "empfangende Partei" -

Präambel
Die Parteien beabsichtigen eine Geschäftsbeziehung und werden dabei vertrauliche
Informationen austauschen.

§ 1 Gegenstand
Vertrauliche Informationen umfassen alle technischen und geschäftlichen Informationen,
die als "vertraulich" gekennzeichnet sind oder deren Vertraulichkeit sich aus den
Umständen ergibt.

§ 2 Verpflichtungen
Die empfangende Partei verpflichtet sich:
- Vertrauliche Informationen geheim zu halten
- Diese nur für den vereinbarten Zweck zu verwenden
- Zugang nur befugten Mitarbeitern zu gewähren

§ 3 Ausnahmen
Nicht unter diese Vereinbarung fallen öffentlich bekannte Informationen oder
Informationen, die rechtmäßig von Dritten erhalten wurden.

§ 4 Dauer
Diese Vereinbarung gilt ab {datetime.now().strftime('%d.%m.%Y')} für einen Zeitraum
von {random.choice(['3', '5'])} Jahren.

§ 5 Vertragsstrafe
Bei Verstößen kann eine Vertragsstrafe von bis zu {random.randint(10000, 50000)}€
geltend gemacht werden.

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Offenlegende Partei                  Empfangende Partei
"""
    
    def _contract_template_partnership(self, i):
        """Partnership agreement"""
        return f"""
KOOPERATIONSVERTRAG

zwischen

{random.choice(self.companies)} ("Partner A")
und
{random.choice(self.companies)} ("Partner B")

§ 1 Gegenstand der Kooperation
Die Partner vereinbaren eine strategische Zusammenarbeit im Bereich
{random.choice(self.products)}.

§ 2 Dauer
Die Kooperation beginnt am {datetime.now().strftime('%d.%m.%Y')} und läuft zunächst
für {random.choice(['2', '3', '5'])} Jahre.

§ 3 Leistungen der Partner
Partner A: {random.choice(['Bereitstellung von Technologie', 'Vertriebsunterstützung', 'Marketing'])}
Partner B: {random.choice(['Finanzierung', 'Markterschließung', 'Ressourcen'])}

§ 4 Umsatzbeteiligung
Die Umsätze aus der Kooperation werden im Verhältnis {random.choice(['50:50', '60:40', '70:30'])} aufgeteilt.

§ 5 Exklusivität
{random.choice(['Diese Kooperation ist exklusiv.', 'Diese Kooperation ist nicht exklusiv.'])}

§ 6 Kündigung
Ordentliche Kündigung mit {random.choice(['6', '12'])} Monaten Frist zum Jahresende.

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Partner A                            Partner B
"""
    
    def _contract_template_license(self, i):
        """Software license agreement"""
        return f"""
SOFTWARE-LIZENZVERTRAG

zwischen

{random.choice(self.companies)} ("Lizenzgeber")
und
{random.choice(self.companies)} ("Lizenznehmer")

§ 1 Lizenzgegenstand
Der Lizenzgeber räumt dem Lizenznehmer das nicht-ausschließliche Recht zur
Nutzung der Software "{random.choice(['ERP System Pro', 'CloudManager', 'DataAnalytics Suite'])}" ein.

§ 2 Lizenzumfang
- {random.choice(['Einzelplatzlizenz', 'Netzwerklizenz für bis zu 50 User', 'Enterprise-Lizenz'])}
- Installation auf {random.choice(['1', '5', 'unbegrenzt vielen'])} Systemen
- Nutzung für {random.choice(['internen Gebrauch', 'kommerzielle Zwecke'])}

§ 3 Lizenzgebühr
Einmalige Lizenzgebühr: {random.randint(5000, 50000)}€
Jährliche Wartungsgebühr: {random.randint(1000, 10000)}€

§ 4 Laufzeit
Die Lizenz wird auf {random.choice(['unbestimmte Zeit', '5 Jahre', '3 Jahre'])} erteilt.

§ 5 Einschränkungen
Der Lizenznehmer darf die Software nicht:
- Weitergeben oder vermieten
- Reverse Engineering betreiben
- Modifizieren oder abgeleitete Werke erstellen

§ 6 Gewährleistung
Der Lizenzgeber gewährleistet die Funktionsfähigkeit gemäß Spezifikation.
Gewährleistungsfrist: 12 Monate ab Lieferung.

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Lizenzgeber                          Lizenznehmer
"""
    
    def _contract_template_maintenance(self, i):
        """Maintenance contract"""
        return f"""
WARTUNGSVERTRAG

Vertrag zwischen

{random.choice(self.companies)} ("Auftraggeber")
und
{random.choice(self.companies)} ("Wartungsunternehmen")

§ 1 Wartungsgegenstand
Wartung und Instandhaltung von:
{random.choice(['IT-Systemen', 'Produktionsanlagen', 'Gebäudetechnik', 'Fahrzeugflotte'])}

§ 2 Leistungsumfang
- Regelmäßige Inspektion ({random.choice(['monatlich', 'quartalsweise', 'halbjährlich'])})
- Instandsetzung bei Störungen
- 24/7 Notfallhotline
- Ersatzteilversorgung
- Fernwartung

§ 3 Reaktionszeiten
- Kritische Störungen: innerhalb {random.choice(['2', '4'])} Stunden
- Normale Störungen: innerhalb {random.choice(['24', '48'])} Stunden
- Geplante Wartungen: nach Vereinbarung

§ 4 Vertragslaufzeit
Beginn: {datetime.now().strftime('%d.%m.%Y')}
Laufzeit: {random.choice(['12', '24', '36'])} Monate
Automatische Verlängerung um jeweils 12 Monate

§ 5 Vergütung
Monatliche Pauschale: {random.randint(500, 5000)}€
Zusätzliche Arbeiten nach Aufwand (Stundensatz: {random.randint(80, 150)}€)

§ 6 Kündigung
Kündigungsfrist: 3 Monate zum Vertragsende

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Auftraggeber                         Wartungsunternehmen
"""
    
    def _contract_template_consulting(self, i):
        """Consulting contract"""
        return f"""
BERATUNGSVERTRAG

zwischen

{random.choice(self.companies)} ("Mandant")
und
{random.choice(self.names)} ("Berater/in")

§ 1 Beratungsleistungen
Der/Die Berater/in erbringt Beratungsleistungen in folgendem Bereich:
{random.choice(['Unternehmensberatung', 'IT-Beratung', 'Strategieberatung', 'Prozessoptimierung'])}

Projekt: {random.choice(['Digitalisierung', 'Reorganisation', 'Markteintritt', 'Kostenoptimierung'])}

§ 2 Vertragsdauer
Projektbeginn: {datetime.now().strftime('%d.%m.%Y')}
Voraussichtliches Ende: {(datetime.now() + timedelta(days=180)).strftime('%d.%m.%Y')}
Geschätzter Aufwand: {random.randint(50, 300)} Beratertage

§ 3 Honorar
Tagessatz: {random.randint(800, 2000)}€
Abrechnung: monatlich nach tatsächlichem Aufwand
Reisekosten: nach Aufwand

§ 4 Berichte und Dokumentation
Der/Die Berater/in erstellt:
- {random.choice(['Wöchentliche', 'Monatliche'])} Statusberichte
- Zwischen- und Abschlussbericht
- Dokumentation der Ergebnisse

§ 5 Vertraulichkeit
Alle Projektinformationen unterliegen der Verschwiegenheit.

§ 6 Kündigung
Ordentliche Kündigung mit 4 Wochen Frist zum Monatsende möglich.

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Mandant                              Berater/in
"""
    
    def _contract_template_supply(self, i):
        """Supply agreement"""
        return f"""
LIEFERVERTRAG

zwischen

{random.choice(self.companies)} ("Käufer")
und
{random.choice(self.companies)} ("Lieferant")

§ 1 Vertragsgegenstand
Der Lieferant verpflichtet sich zur regelmäßigen Lieferung von:
{random.choice(['Büromaterial', 'IT-Hardware', 'Rohstoffe', 'Verbrauchsmaterial'])}

§ 2 Liefermenge und -termine
Monatliche Lieferung: {random.randint(100, 5000)} Einheiten
Liefertermin: jeweils am {random.choice(['5.', '10.', '15.', '20.'])} des Monats
Lieferort: {random.choice(self.streets)}, {random.choice(self.cities)}

§ 3 Preise
Stückpreis: {random.randint(10, 500)}€
Mindestabnahmemenge: {random.randint(50, 500)} Einheiten/Monat
Preisanpassungen: jährlich gemäß Verbraucherpreisindex

§ 4 Qualität
Die gelieferte Ware muss folgenden Standards entsprechen:
- DIN/ISO Norm {random.randint(9000, 14000)}
- CE-Kennzeichnung
- Herstellerzertifikate

§ 5 Gewährleistung
Gewährleistungsfrist: {random.choice(['12', '24'])} Monate ab Lieferung
Bei Mängeln: Nachbesserung oder Ersatzlieferung

§ 6 Vertragslaufzeit
Laufzeit: {random.choice(['2', '3', '5'])} Jahre ab {datetime.now().strftime('%d.%m.%Y')}
Kündigungsfrist: 6 Monate zum Jahresende

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Käufer                               Lieferant
"""
    
    def _contract_template_framework(self, i):
        """Framework agreement"""
        return f"""
RAHMENVERTRAG

zwischen

{random.choice(self.companies)} ("Auftraggeber")
und
{random.choice(self.companies)} ("Auftragnehmer")

Präambel
Die Parteien beabsichtigen eine langfristige Zusammenarbeit und schließen daher
einen Rahmenvertrag über die Erbringung von Dienstleistungen.

§ 1 Vertragsgegenstand
Dieser Rahmenvertrag regelt die grundsätzlichen Bedingungen für Einzelaufträge
im Bereich: {random.choice(self.products)}

§ 2 Einzelaufträge
Einzelaufträge werden durch schriftliche Bestellung ausgelöst.
Jeder Einzelauftrag enthält: Leistungsbeschreibung, Preis, Liefertermin.

§ 3 Preise und Konditionen
Stundensätze:
- Senior Consultant: {random.randint(120, 180)}€/h
- Consultant: {random.randint(90, 130)}€/h  
- Junior Consultant: {random.randint(60, 90)}€/h

Rabattstaffel bei Jahresumsatz:
- bis {random.randint(50000, 100000)}€: 0%
- bis {random.randint(150000, 250000)}€: 5%
- über {random.randint(250000, 500000)}€: 10%

§ 4 Vertragslaufzeit
Laufzeit: {random.choice(['3', '5'])} Jahre ab {datetime.now().strftime('%d.%m.%Y')}
Automatische Verlängerung um jeweils 1 Jahr bei Nicht-Kündigung

§ 5 Kündigung
Ordentliche Kündigung: 6 Monate zum Jahresende
Einzelaufträge bleiben von Kündigung unberührt

§ 6 Ansprechpartner
Auftraggeber: {random.choice(self.names)}
Auftragnehmer: {random.choice(self.names)}

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Auftraggeber                         Auftragnehmer
"""
    
    def _contract_template_subcontractor(self, i):
        """Subcontractor agreement"""
        return f"""
SUBUNTERNEHMERVERTRAG

zwischen

{random.choice(self.companies)} ("Hauptauftragnehmer")
und
{random.choice(self.companies)} ("Subunternehmer")

§ 1 Vertragsgegenstand
Der Subunternehmer übernimmt im Auftrag des Hauptauftragnehmers folgende Leistungen:
{random.choice(self.products)}

Hauptprojekt: {random.choice(['Großprojekt Alpha', 'Bauvorhaben Beta', 'IT-Projekt Gamma'])}
Auftraggeber (Endkunde): {random.choice(self.companies)}

§ 2 Leistungsumfang
Der Subunternehmer erbringt:
- {random.choice(['Installation', 'Montage', 'Programmierung', 'Lieferung'])}
- Einhaltung der Qualitätsstandards
- Dokumentation der Arbeiten
- Schulung bei Bedarf

§ 3 Vergütung
Pauschalbetrag: {random.randint(25000, 150000)}€
Zahlungsplan:
- 30% bei Auftragserteilung
- 40% bei Zwischenabnahme
- 30% bei Endabnahme

§ 4 Termine
Projektbeginn: {datetime.now().strftime('%d.%m.%Y')}
Zwischenabnahme: {(datetime.now() + timedelta(days=60)).strftime('%d.%m.%Y')}
Fertigstellung: {(datetime.now() + timedelta(days=120)).strftime('%d.%m.%Y')}

Vertragsstrafe bei Verzug: {random.randint(100, 500)}€ pro Tag (max. 10% der Auftragssumme)

§ 5 Gewährleistung
Gewährleistungsfrist: {random.choice(['24', '36'])} Monate ab Abnahme

§ 6 Haftung
Der Subunternehmer haftet für Schäden aus der Leistungserbringung.
Haftungshöchstgrenze: {random.randint(100000, 500000)}€

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Hauptauftragnehmer                   Subunternehmer
"""
    
    def _contract_template_sales(self, i):
        """Sales representative agreement"""
        return f"""
HANDELSVERTRETERVERTRAG

zwischen

{random.choice(self.companies)} ("Unternehmen")
und
{random.choice(self.names)} ("Handelsvertreter/in")

§ 1 Vertragsgegenstand
Der/Die Handelsvertreter/in übernimmt die Vermittlung von Geschäften für das
Unternehmen im Bereich: {random.choice(self.products)}

§ 2 Gebiet
Vertragsgebiet: {random.choice(['Süddeutschland', 'Norddeutschland', 'Westdeutschland', 'Ostdeutschland'])}
Umfasst die Bundesländer: {random.choice(['Bayern, Baden-Württemberg', 'NRW, Hessen', 'Hamburg, Schleswig-Holstein'])}

§ 3 Provision
Provisionssatz: {random.choice(['5', '8', '10', '12'])}% vom Nettoumsatz
Mindestprovision: {random.randint(1000, 3000)}€/Monat
Provisionsabrechnung: monatlich
Zahlungsziel: 15 Tage nach Rechnungsstellung

§ 4 Pflichten des Handelsvertreters
- Aktive Kundenakquise und -betreuung
- Regelmäßige Berichterstattung
- Teilnahme an Schulungen
- Einhaltung der Preisliste

§ 5 Ausschließlichkeit
{random.choice(['Der/Die Handelsvertreter/in arbeitet ausschließlich für das Unternehmen.',
                'Der/Die Handelsvertreter/in kann auch für andere Unternehmen tätig sein.'])}

§ 6 Vertragsdauer
Beginn: {datetime.now().strftime('%d.%m.%Y')}
Laufzeit: unbefristet
Kündigungsfrist: {random.choice(['3', '6'])} Monate zum Quartalsende

§ 7 Ausgleichsanspruch
Bei Vertragsbeendigung besteht Anspruch auf Ausgleich gemäß §89b HGB.

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Unternehmen                          Handelsvertreter/in
"""
    
    def _contract_template_loan(self, i):
        """Loan agreement"""
        amount = random.randint(50000, 500000)
        rate = random.uniform(2.5, 5.5)
        
        return f"""
DARLEHENSVERTRAG

zwischen

{random.choice(self.companies)} ("Darlehensgeber")
und
{random.choice(self.companies)} ("Darlehensnehmer")

§ 1 Darlehensbetrag
Der Darlehensgeber gewährt dem Darlehensnehmer ein Darlehen in Höhe von:
{amount:,}€ (in Worten: {random.choice(['fünfzigtausend', 'hunderttausend', 'zweihunderttausend'])} Euro)

§ 2 Auszahlung
Die Auszahlung erfolgt am {(datetime.now() + timedelta(days=7)).strftime('%d.%m.%Y')} auf folgendes Konto:
IBAN: DE{random.randint(10, 99)} {random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(10, 99)}

§ 3 Zinsen
Zinssatz: {rate:.2f}% p.a. (fest für die gesamte Laufzeit)
Zinsberechnung: 30/360 Methode
Zinszahlung: jährlich nachträglich

§ 4 Rückzahlung
Laufzeit: {random.choice(['5', '7', '10'])} Jahre
Tilgung: {random.choice(['endfällig', 'in monatlichen Raten', 'in vierteljährlichen Raten'])}
Monatliche Rate: {round(amount / (int(random.choice(['5', '7', '10'])) * 12), 2):,}€

§ 5 Sicherheiten
Als Sicherheit dienen:
- {random.choice(['Grundschuld', 'Bürgschaft', 'Verpfändung von Geschäftsanteilen', 'Sicherungsübereignung'])}

§ 6 Vorzeitige Rückzahlung
Vorzeitige Rückzahlung möglich mit {random.choice(['1%', '2%', '3%'])} Vorfälligkeitsentschädigung.

§ 7 Kündigung
Ordentliche Kündigung nur zum Laufzeitende möglich.
Außerordentliche Kündigung bei Zahlungsverzug über 2 Monate.

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Darlehensgeber                       Darlehensnehmer
"""
    
    def _contract_template_hosting(self, i):
        """Web hosting contract"""
        return f"""
HOSTING-VERTRAG

zwischen

{random.choice(self.companies)} ("Provider")
und
{random.choice(self.companies)} ("Kunde")

§ 1 Vertragsgegenstand
Der Provider stellt dem Kunden folgende Hosting-Leistungen zur Verfügung:

Paket: {random.choice(['Basic', 'Professional', 'Enterprise', 'Premium'])}
- Webspace: {random.choice(['10', '50', '100', 'unbegrenzt'])} GB
- Traffic: {random.choice(['100', '500', '1000', 'unbegrenzt'])} GB/Monat
- Domains: {random.choice(['1', '5', '10', 'unbegrenzt'])} inklusive
- E-Mail-Postfächer: {random.choice(['10', '50', '100', 'unbegrenzt'])}
- Datenbanken: {random.choice(['5', '10', '25', 'unbegrenzt'])}
- SSL-Zertifikat: {random.choice(['inklusive', 'optional', 'kostenlos'])}

§ 2 Verfügbarkeit
Garantierte Verfügbarkeit: {random.choice(['99,5%', '99,9%', '99,95%'])} pro Jahr
Wartungsfenster: Sonntags 02:00-06:00 Uhr

§ 3 Vergütung
Monatliche Grundgebühr: {random.randint(10, 200)}€
Setup-Gebühr (einmalig): {random.randint(0, 100)}€
Abrechnungszeitraum: {random.choice(['monatlich', 'vierteljährlich', 'jährlich'])}

§ 4 Vertragslaufzeit
Mindestlaufzeit: {random.choice(['1', '12', '24'])} Monate ab {datetime.now().strftime('%d.%m.%Y')}
Kündigungsfrist: {random.choice(['1 Monat', '3 Monate'])} zum Monatsende

§ 5 Backups
- Tägliche Backups (7 Tage Aufbewahrung)
- Wöchentliche Backups (4 Wochen Aufbewahrung)
- Wiederherstellung: kostenlos

§ 6 Support
Support-Zeiten: {random.choice(['Mo-Fr 9-17 Uhr', '24/7', 'Mo-Fr 8-20 Uhr'])}
Reaktionszeit: {random.choice(['2', '4', '8'])} Stunden
Kanäle: Telefon, E-Mail, Ticket-System

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Provider                             Kunde
"""
    
    def _contract_template_training(self, i):
        """Training/Education contract"""
        return f"""
SCHULUNGSVERTRAG

zwischen

{random.choice(self.companies)} ("Auftraggeber")
und
{random.choice(self.companies)} ("Schulungsanbieter")

§ 1 Schulungsgegenstand
Schulung: "{random.choice(['Microsoft Office Komplett', 'SAP Grundlagen', 'Python Programmierung',
                           'Projektmanagement', 'Datenschutz DSGVO', 'Führungskräfte-Training'])}"

Zielgruppe: {random.choice(['Mitarbeiter IT-Abteilung', 'Alle Mitarbeiter', 'Führungskräfte', 'Auszubildende'])}
Teilnehmerzahl: {random.choice(['5-10', '10-15', '8-12'])} Personen

§ 2 Schulungstermine
Zeitraum: {datetime.now().strftime('%d.%m.%Y')} bis {(datetime.now() + timedelta(days=90)).strftime('%d.%m.%Y')}
Umfang: {random.choice(['2', '3', '5'])} Tage à {random.choice(['6', '7', '8'])} Schulungsstunden

Termine:
- Tag 1: {(datetime.now() + timedelta(days=14)).strftime('%d.%m.%Y')}, 09:00-17:00 Uhr
- Tag 2: {(datetime.now() + timedelta(days=21)).strftime('%d.%m.%Y')}, 09:00-17:00 Uhr
{f"- Tag 3: {(datetime.now() + timedelta(days=28)).strftime('%d.%m.%Y')}, 09:00-17:00 Uhr" if random.choice([True, False]) else ""}

§ 3 Schulungsort
{random.choice(['Beim Auftraggeber', 'Beim Schulungsanbieter', 'Online (Webinar)', 'Hotel/Tagungsraum'])}
Adresse: {random.choice(self.streets)}, {random.choice(self.cities)}

§ 4 Vergütung
Schulungsgebühr gesamt: {random.randint(2000, 15000)}€
Pro Teilnehmer: {random.randint(200, 1500)}€
Inklusive: Schulungsunterlagen, Zertifikat, Verpflegung

§ 5 Leistungen des Schulungsanbieters
- Erfahrene Trainer mit Zertifizierung
- Umfangreiche Schulungsunterlagen
- Praktische Übungen
- Teilnahmezertifikat
- 4 Wochen kostenloser Support nach Schulung

§ 6 Stornierungsbedingungen
- Bis 4 Wochen vorher: kostenfrei
- Bis 2 Wochen vorher: 50% der Gebühr
- Danach: 100% der Gebühr

{random.choice(self.cities)}, {datetime.now().strftime('%d.%m.%Y')}

_______________________              _______________________
Auftraggeber                         Schulungsanbieter
"""

    def generate_purchase_orders(self, n=100):
        """Generate 15 different purchase order variations"""
        orders = []
        
        templates = [
            self._po_template_standard,
            self._po_template_bulk,
            self._po_template_urgent,
            self._po_template_international,
            self._po_template_services            
            # self._po_template_recurring,
            # self._po_template_construction,
            # self._po_template_it_equipment,
            # self._po_template_office_supplies,
            # self._po_template_raw_materials,
            # self._po_template_consulting_services,
            # self._po_template_maintenance_parts,
            # self._po_template_marketing_materials,
            # self._po_template_software_licenses,
            # self._po_template_logisticsplate_logistics


        ]
        
        for i in range(n):
            template = random.choice(templates)
            orders.append({'text': template(i), 'label': 'Bestellung'})
        
        return orders
    
    def _po_template_standard(self, i):
        """Standard purchase order"""
        order_num = f"PO-2024-{3000+i}"
        date = datetime.now().strftime('%d.%m.%Y')
        delivery_date = (datetime.now() + timedelta(days=random.randint(14, 30))).strftime('%d.%m.%Y')
        company = random.choice(self.companies)
        product = random.choice(self.products)
        quantity = random.randint(10, 100)
        price = random.randint(50, 500)
        total = quantity * price
        
        return f"""
BESTELLUNG

Bestellnummer: {order_num}
Bestelldatum: {date}
Besteller: {random.choice(self.companies)}

Lieferant:
{company}
{random.choice(self.streets)}
{random.choice(self.cities)}

Pos  Artikelbeschreibung                  Menge    Einzelpreis  Gesamtpreis
───────────────────────────────────────────────────────────────────────────
1    {product}                            {quantity}       {price}€         {total}€

Lieferadresse:
{random.choice(self.companies)}
{random.choice(self.streets)}
{random.choice(self.cities)}

Gewünschter Liefertermin: {delivery_date}
Zahlungsbedingungen: 30 Tage netto nach Lieferung

Bitte bestätigen Sie den Eingang dieser Bestellung und den Liefertermin.

Mit freundlichen Grüßen
Einkaufsabteilung

_______________________
Unterschrift Einkäufer
"""

    def _po_template_bulk(self, i):
        """Bulk order template"""
        return f"""
GROSSBESTELLUNG

Bestellnummer: GB-{random.randint(10000, 99999)}
Datum: {datetime.now().strftime('%d.%m.%Y')}

Lieferant: {random.choice(self.companies)}

Artikel                     Menge   Einheit   Preis/Einheit   Gesamt
────────────────────────────────────────────────────────────────────
{random.choice(['Stahlträger', 'Betonplatten'])}     {random.randint(100, 1000)}   Stk.      {random.randint(50, 200)}€        {random.randint(5000, 200000)}€
{random.choice(['Schrauben', 'Nieten'])}           {random.randint(1000, 5000)}   Stk.      {random.randint(1, 5)}€         {random.randint(1000, 25000)}€
{random.choice(['Farbe', 'Lack'])}                {random.randint(100, 500)}     Liter     {random.randint(10, 50)}€       {random.randint(1000, 25000)}€

Gesamtsumme: {random.randint(15000, 250000)}€

Lieferung in 3 Teilen:
- 1. Teil: {(datetime.now() + timedelta(days=14)).strftime('%d.%m.%Y')}
- 2. Teil: {(datetime.now() + timedelta(days=28)).strftime('%d.%m.%Y')}
- 3. Teil: {(datetime.now() + timedelta(days=42)).strftime('%d.%m.%Y')}

Qualitätsanforderungen: DIN ISO 9001
Verpackung: Palette
Zahlung: 50% Anzahlung, 50% nach Endlieferung
"""

    def _po_template_urgent(self, i):
        """Urgent purchase order"""
        return f"""
DRINGENDE BESTELLUNG - EILT!

Bestellnummer: EIL-{random.randint(1000, 9999)}
Bestelldatum: {datetime.now().strftime('%d.%m.%Y %H:%M')}

Lieferant: {random.choice(self.companies)}
Ansprechpartner: {random.choice(self.names)}
Telefon: +49 {random.randint(100, 999)} {random.randint(1000000, 9999999)}

Artikel: {random.choice(['Notfall-Ersatzteil', 'Dringendes Verbrauchsmaterial'])}
Menge: {random.randint(1, 10)}
Dringende Lieferung erforderlich bis: {(datetime.now() + timedelta(hours=48)).strftime('%d.%m.%Y %H:%M')}

Lieferadresse:
{random.choice(self.companies)}
{random.choice(self.streets)}
{random.choice(self.cities)}
Lager/Eingang: Tor {random.randint(1, 5)}

Express-Lieferung! Kostenübernahme für Expressversand zugesagt.

Bitte umgehende Bestätigung der Lieferfähigkeit!
"""

    def _po_template_international(self, i):
        """International purchase order"""
        return f"""
INTERNATIONAL PURCHASE ORDER / BESTELLSCHEIN

PO Number: INT-{random.randint(10000, 99999)}
Date: {datetime.now().strftime('%d.%m.%Y')}

Supplier: {random.choice(self.companies)}
Country: {random.choice(['USA', 'China', 'Japan', 'South Korea'])}

Item Description              Qty   Unit Price   Total Price
────────────────────────────────────────────────────────────
{random.choice(['Electronic Components', 'Mechanical Parts'])}   {random.randint(100, 500)}   ${random.randint(10, 100)}       ${random.randint(1000, 50000)}

Delivery Terms: {random.choice(['FOB Shanghai', 'CIF Hamburg', 'EXW Shenzhen'])}
Payment Terms: {random.choice(['LC 30 days', 'TT in advance', '30 days net'])}
Currency: {random.choice(['USD', 'EUR', 'CNY'])}

Shipping Method: {random.choice(['Air Freight', 'Sea Freight', 'Express'])}
Delivery Date: {(datetime.now() + timedelta(days=random.randint(21, 60))).strftime('%d.%m.%Y')}

Special Instructions:
- Certificate of Origin required
- Quality inspection upon arrival
- Packing list in duplicate
"""

    def _po_template_services(self, i):
        """Services purchase order"""
        return f"""
DIENSTLEISTUNGSBESTELLUNG

Bestellnummer: DL-{random.randint(10000, 99999)}
Datum: {datetime.now().strftime('%d.%m.%Y')}

Auftragnehmer: {random.choice(self.companies)}

Leistungsbeschreibung:
{random.choice(self.products)}

Zeitraum: {(datetime.now() + timedelta(days=7)).strftime('%d.%m.%Y')} - {(datetime.now() + timedelta(days=90)).strftime('%d.%m.%Y')}

Vergütung:
Stundensatz: {random.randint(80, 150)}€/h
Geschätzter Aufwand: {random.randint(100, 500)} Stunden
Maximalbudget: {random.randint(8000, 75000)}€

Leistungsnachweise:
- Wöchentliche Statusberichte
- Stundennachweise
- Abschlussbericht

Ansprechpartner:
{random.choice(self.names)}
Tel: +49 {random.randint(100, 999)} {random.randint(1000000, 9999999)}
Email: {random.choice(self.names).lower().replace(' ', '.')}@company.de

Zahlungsbedingungen: Netto 30 Tage nach Rechnungserhalt
"""

    def generate_reminders(self, n=100):
        """Generate 15 different reminder variations"""
        reminders = []
        
        templates = [
            self._reminder_template_friendly,
            self._reminder_template_first,
            self._reminder_template_second,
            self._reminder_template_final,
            self._reminder_template_legal
            # self._reminder_template_phone,
            # self._reminder_template_email_style,
            # self._reminder_template_payment_plan,
            # self._reminder_template_partial_payment,
            # self._reminder_template_service_reminder,
            # self._reminder_template_subscription,
            # self._reminder_template_urgent,
            # self._reminder_template_last_chance,
            # self._reminder_template_collection,
            # self._reminder_template_pre_legal
        ]
        
        for i in range(n):
            template = random.choice(templates)
            reminders.append({'text': template(i), 'label': 'Mahnung'})
        
        return reminders

    def _reminder_template_friendly(self, i):
        """Friendly first reminder"""
        return f"""
FREUNDLICHE ERINNERUNG

Sehr geehrte Damen und Herren,

leider haben wir den fälligen Betrag in Höhe von {random.randint(500, 5000)}€ 
für unsere Rechnung Nr. RE-{random.randint(1000, 9999)} vom {(datetime.now() - timedelta(days=45)).strftime('%d.%m.%Y')} 
bisher nicht erhalten.

Eventuell ist die Überweisung unterwegs zu uns oder es ist ein Versehen passiert.
Bitte überprüfen Sie den Zahlungseingang auf Ihrer Seite.

Falls Sie bereits gezahlt haben, betrachten Sie dieses Schreiben als gegenstandslos.

Ansonsten bitten wir um umgehende Überweisung.

Mit freundlichen Grüßen
{random.choice(self.companies)}
"""

    def _reminder_template_first(self, i):
        """First formal reminder"""
        return f"""
ERSTE MAHNUNG

Mahnung zur Rechnung Nr. RE-{random.randint(1000, 9999)}
Rechnungsdatum: {(datetime.now() - timedelta(days=40)).strftime('%d.%m.%Y')}
Fälligkeitsdatum: {(datetime.now() - timedelta(days=26)).strftime('%d.%m.%Y')}
Offener Betrag: {random.randint(1000, 8000)}€

Sehr geehrte Damen und Herren,

trotz Fälligkeit am {(datetime.now() - timedelta(days=26)).strftime('%d.%m.%Y')} 
ist der Rechnungsbetrag bisher nicht auf unserem Konto eingegangen.

Bitte begleichen Sie den offenen Betrag umgehend, spätestens bis zum 
{(datetime.now() + timedelta(days=7)).strftime('%d.%m.%Y')}.

Sollten Sie bereits gezahlt haben, teilen Sie uns dies bitte mit.

Hochachtungsvoll
{random.choice(self.companies)}
"""

    def _reminder_template_second(self, i):
        """Second reminder with warning"""
        return f"""
ZWEITE MAHNUNG

Betrifft: Rechnung Nr. RE-{random.randint(1000, 9999)} vom {(datetime.now() - timedelta(days=60)).strftime('%d.%m.%Y')}
Offener Betrag: {random.randint(1500, 10000)}€

Sehr geehrte Damen und Herren,

wir müssen feststellen, dass unser Schreiben vom {(datetime.now() - timedelta(days=15)).strftime('%d.%m.%Y')} 
ohne Reaktion geblieben ist.

Der Betrag von {random.randint(1500, 10000)}€ ist nun seit {random.randint(45, 75)} Tagen überfällig.

Wir fordern Sie auf, den ausstehenden Betrag innerhalb von 7 Tagen 
auf unser Konto zu überweisen.

Andernfalls werden wir weitere Maßnahmen ergreifen müssen.

Mit freundlichen Grüßen
{random.choice(self.companies)}
"""

    def _reminder_template_final(self, i):
        """Final reminder before legal action"""
        return f"""
LETZTE MAHNUNG VOR AUSSENSTELLUNG

Rechnung: RE-{random.randint(1000, 9999)}
Rechnungsdatum: {(datetime.now() - timedelta(days=90)).strftime('%d.%m.%Y')}
Offener Betrag: {random.randint(2000, 12000)}€
Überfällig seit: {random.randint(60, 85)} Tagen

Sehr geehrte Damen und Herren,

trotz zweier Mahnungen ist der fällige Betrag weiterhin nicht beglichen.

Dies ist unsere letzte Aufforderung zur Zahlung.

Wir fordern Sie auf, den vollständigen Betrag inklusive Verzugszinsen 
in Höhe von {random.randint(10, 100)}€ bis zum {(datetime.now() + timedelta(days=3)).strftime('%d.%m.%Y')} zu begleichen.

Bei Nichtzahlung werden wir den Betrag ohne weitere Ankündigung 
einer Inkassostelle übergeben.

{random.choice(self.companies)}
"""

    def _reminder_template_legal(self, i):
        """Legal warning reminder"""
        return f"""
RECHTSANWALTLICHE MAHUNG

Im Auftrag von: {random.choice(self.companies)}
Mandanten-Nr: M-{random.randint(10000, 99999)}

An: {random.choice(self.companies)}

Betreff: Zahlungserinnerung für Rechnung RE-{random.randint(1000, 9999)}

Forderungshöhe: {random.randint(2500, 15000)}€
Verzugszinsen: {random.randint(25, 150)}€
Mahntgebühr: {random.randint(5, 15)}€
Gesamtforderung: {random.randint(2530, 15165)}€

Sie haben es trotz mehrfacher Mahnungen unterlassen, 
die fällige Forderung zu begleichen.

Wir fordern Sie auf, den Gesamtbetrag innerhalb von 7 Tagen 
auf das unten genannte Konto zu überweisen.

Sollten Sie dieser Aufforderung nicht nachkommen, werden wir 
gerichtliche Schritte einleiten.

Rechtsanwaltskanzlei Müller & Partner
"""

    def generate_complaints(self, n=100):
        """Generate 15 different complaint variations"""
        complaints = []
        
        templates = [
            self._complaint_template_delivery,
            self._complaint_template_quality
            # self._complaint_template_wrong_item,
            # self._complaint_template_damaged,
            # self._complaint_template_service,
            # self._complaint_template_delay,
            # self._complaint_template_invoice,
            # self._complaint_template_warranty,
            # self._complaint_template_urgent,
            # self._complaint_template_formal,
            # self._complaint_template_simple,
            # self._complaint_template_technical,
            # self._complaint_template_quantity,
            # self._complaint_template_packaging,
            # self._complaint_template_follow_up
        ]
        
        for i in range(n):
            template = random.choice(templates)
            complaints.append({'text': template(i), 'label': 'Reklamation'})
        
        return complaints

    def _complaint_template_delivery(self, i):
        """Delivery complaint"""
        return f"""
REKLAMATION - LIEFERUNG

Rechnung Nr: RE-{random.randint(1000, 9999)}
Lieferdatum: {(datetime.now() - timedelta(days=7)).strftime('%d.%m.%Y')}
Bestellnummer: PO-{random.randint(1000, 9999)}

Sehr geehrte Damen und Herren,

mit Bezug auf unsere Bestellung vom {(datetime.now() - timedelta(days=14)).strftime('%d.%m.%Y')} 
müssen wir leider folgende Mängel reklamieren:

- {random.choice(['Teillieferung', 'Falsche Artikel', 'Nicht gelieferte Positionen'])}

Fehlende/fehlerhafte Artikel:
{random.choice(['Artikel XYZ, Menge 10 Stück', 'Modell ABC, Farbe silber statt schwarz'])}

Bitte liefern Sie die fehlenden/korrekten Artikel umgehend nach 
oder teilen Sie uns mit, wie Sie das Problem lösen werden.

Wir erwarten Ihre umgehende Stellungnahme.

Mit freundlichen Grüßen
{random.choice(self.companies)}
"""

    def _complaint_template_quality(self, i):
        """Quality complaint"""
        return f"""
QUALITÄTSREKLAMATION

Lieferung vom: {(datetime.now() - timedelta(days=5)).strftime('%d.%m.%Y')}
Artikel: {random.choice(['Elektrogerät', 'Maschinenteil', 'Software'])}
Seriennummer: SN-{random.randint(100000, 999999)}

Sehr geehrte Damen und Herren,

der gelieferte Artikel weist folgende Qualitätsmängel auf:

- {random.choice(['Funktionsstörung', 'Beschädigung', 'Nicht konform mit Spezifikation'])}
- {random.choice(['Oberflächenfehler', 'Montagefehler', 'Falsche Dimensionen'])}

Konkrete Probleme:
{random.choice(['Gerät startet nicht', 'Display zeigt Fehlermeldung', 'Lautstärke zu hoch'])}

Wir fordern:
{random.choice(['Austausch', 'Reparatur', 'Preisminderung'])}

Bitte teilen Sie uns innerhalb von 3 Werktagen mit, 
wie Sie vorgehen werden.

Hochachtungsvoll
{random.choice(self.companies)}
"""

    def balance_dataset(self, df, target_count_per_class=None):
        """
        Balance the dataset to have equal number of samples per class
        """
        if target_count_per_class is None:
            # Use the minority class count
            target_count_per_class = df['label'].value_counts().min()
        
        balanced_dfs = []
        
        for label in df['label'].unique():
            label_df = df[df['label'] == label]
            
            if len(label_df) >= target_count_per_class:
                # Downsample
                balanced_label_df = label_df.sample(target_count_per_class, random_state=42)
            else:
                # Upsample with replacement
                balanced_label_df = resample(label_df, 
                                           replace=True, 
                                           n_samples=target_count_per_class, 
                                           random_state=42)
            balanced_dfs.append(balanced_label_df)
        
        balanced_df = pd.concat(balanced_dfs, ignore_index=True)
        balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        return balanced_df

    def save_dataset_csv(self, df, output_dir):
        """Save dataset as CSV only"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Save main CSV file
        csv_path = output_dir / "german_business_documents.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        # Also save individual CSV files for each document type
        for label in df['label'].unique():
            label_df = df[df['label'] == label]
            label_path = output_dir / f"{label.lower()}_documents.csv"
            label_df.to_csv(label_path, index=False, encoding='utf-8')
        
        return {
            'main_csv': csv_path,
            'label_csvs': [f"{label.lower()}_documents.csv" for label in df['label'].unique()]
        }
    def save_as_text_files(self, documents_list, output_dir, category_name):
        """
        Save each document as a separate .txt file
        
        Args:
            documents_list: List of dicts with 'text' and 'label' keys
            output_dir: Directory to save files
            category_name: Category name for filename prefix (e.g., 'invoice', 'contract')
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        files_written = 0
        for i, doc in enumerate(documents_list, start=1):
            filename = output_dir / f"{category_name}_{i}.txt"
            
            # Write the text content to file
            text_content = doc['text'] if isinstance(doc, dict) else str(doc)
            filename.write_text(text_content, encoding='utf-8')
            files_written += 1
        
        return files_written

def save_all_synthetic_as_text_files(per_category=200, output_dir="app/data/synthetic", overwrite=False):
    """
    Generate all document types and save each one as a separate .txt file
    
    Args:
        per_category: Number of documents to generate per category
        output_dir: Directory to save all .txt files
        overwrite: Whether to overwrite existing files
    
    Returns:
        Dictionary with statistics about generated files
    """
    generator = GermanDocumentGenerator()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    stats = {}
    total_files = 0
    
    # Document types to generate
    document_types = {
        'invoices': generator.generate_invoices,
        'contracts': generator.generate_contracts,
        'orders': generator.generate_purchase_orders,
        'paymentreminders': generator.generate_reminders,
        'complaints': generator.generate_complaints
    }
    
    print(f"Generating {per_category} documents per category...")
    print(f"Output directory: {output_path.absolute()}\n")
    
    for category, generate_func in document_types.items():
        print(f"📝 Generating {category} documents...")
        
        # Generate documents for this category
        documents = generate_func(per_category)
        
        category_dir = output_path / category
        category_dir.mkdir(exist_ok=True)
        
        # Save each document as a separate .txt file
        files_written = 0
        for i, doc in enumerate(documents, start=1):
            filename = category_dir / f"{category.rstrip('s')}_v1_{i}.txt"
            
            # Skip if file exists and overwrite is False
            if filename.exists() and not overwrite:
                continue
            
            # Extract text content
            text_content = doc['text'] if isinstance(doc, dict) else str(doc)
            
            # Write to file
            filename.write_text(text_content, encoding='utf-8')
            files_written += 1
        
        stats[category] = files_written
        total_files += files_written
        print(f"   ✅ Saved {files_written} {category} files")
    
    print(f"\n{'='*60}")
    print(f"✅ Total files generated: {total_files}")
    print(f"📁 Location: {output_path.absolute()}")
    print(f"{'='*60}\n")
    
    # Print file breakdown
    print("File breakdown by category:")
    for category, count in stats.items():
        print(f"  - {category:12s}: {count:4d} files")
    
    return {
        'total_files': total_files,
        'output_dir': str(output_path.absolute()),
        'stats': stats
    }


def save_synthetic_texts(per_category=200, out_dir="app/data/synthetic", overwrite=False):
    """
    Alternative function name for compatibility
    Generates documents using the make_* helpers and saves each document as a UTF-8 .txt file.
    
    Args:
        per_category: How many documents to generate per category
        out_dir: Directory to write files into (will be created if missing)
        overwrite: If False, existing files will be preserved
    
    Returns:
        Number of files written
    """
    result = save_all_synthetic_as_text_files(per_category, out_dir, overwrite)
    return result['total_files']


