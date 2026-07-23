#!/usr/bin/env python3
"""Génère la checklist PDF remplissable « Humidité — 7 jours ».

Dépendances (hors projet Astro) : reportlab.
Exemple :
  /opt/data/.venvs/mmh-pdf/bin/python scripts/generate-checklist-pdf.py
"""
from pathlib import Path
import sys

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.pdfdoc import PDFString
from reportlab.pdfgen import canvas

OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "public/downloads/checklist-humidite-7-jours.pdf"
)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = A4
MARGIN = 14 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

NAVY = HexColor("#17324D")
BLUE = HexColor("#2B6F9C")
PALE_BLUE = HexColor("#EAF3F8")
SAGE = HexColor("#DDEBE3")
PALE_YELLOW = HexColor("#FFF4D6")
PALE_RED = HexColor("#FCE8E6")
TEXT = HexColor("#253746")
MUTED = HexColor("#5E6F7D")
BORDER = HexColor("#AABBC7")
LIGHT_BORDER = HexColor("#D5E0E7")


def wrap(text: str, font: str, size: float, width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if stringWidth(candidate, font, size) <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(c, text, x, y, width, font="Helvetica", size=8.5, leading=10.5, color=TEXT, max_lines=None):
    lines = wrap(text, font, size, width)
    if max_lines:
        lines = lines[:max_lines]
    c.setFont(font, size)
    c.setFillColor(color)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def section_title(c, number, title, y):
    c.setFillColor(BLUE)
    c.roundRect(MARGIN, y - 4 * mm, 9 * mm, 9 * mm, 2 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(MARGIN + 4.5 * mm, y - 1.1 * mm, str(number))
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN + 13 * mm, y - 1.5 * mm, title)


def header(c, page_number, subtitle):
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 31 * mm, PAGE_W, 31 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 19)
    c.drawString(MARGIN, PAGE_H - 14 * mm, "Suivi humidité — 7 jours")
    c.setFont("Helvetica", 9.5)
    c.drawString(MARGIN, PAGE_H - 21 * mm, subtitle)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 14 * mm, f"FICHE {page_number}/3")
    c.setFont("Helvetica", 7.5)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 21 * mm, "maisonmoinshumide.fr")


def footer(c):
    c.setStrokeColor(LIGHT_BORDER)
    c.line(MARGIN, 15 * mm, PAGE_W - MARGIN, 15 * mm)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.8)
    c.drawString(MARGIN, 10.5 * mm, "Repère pratique, pas diagnostic : cette fiche ne permet pas d’identifier seule la cause.")
    c.drawRightString(PAGE_W - MARGIN, 10.5 * mm, "Version 2026-07")


def text_field(c, name, x, y, w, h, font_size: float = 9, multiline=False, fill=white, tooltip=None):
    flags = "multiline" if multiline else ""
    c.acroForm.textfield(
        name=name,
        tooltip=tooltip or name.replace("_", " "),
        x=x,
        y=y,
        width=w,
        height=h,
        borderWidth=0,
        fillColor=fill,
        textColor=TEXT,
        forceBorder=False,
        fontName="Helvetica",
        fontSize=font_size,
        fieldFlags=flags,
    )


def checkbox(c, name, x, y, label, size=4.2 * mm, font_size=8.2, label_width=None):
    c.acroForm.checkbox(
        name=name,
        tooltip=label,
        x=x,
        y=y,
        size=size,
        buttonStyle="check",
        borderWidth=1,
        borderColor=BORDER,
        fillColor=white,
        checked=False,
        forceBorder=True,
    )
    label_x = x + size + 2 * mm
    if label_width:
        draw_wrapped(c, label, label_x, y + size - 2.4 * mm, label_width, size=font_size, leading=9)
    else:
        c.setFillColor(TEXT)
        c.setFont("Helvetica", font_size)
        c.drawString(label_x, y + size - 2.4 * mm, label)


def labelled_field(c, label, name, x, y, w, h=8 * mm):
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 7.2)
    c.drawString(x, y + h + 1.5 * mm, label.upper())
    c.setStrokeColor(BORDER)
    c.setFillColor(white)
    c.roundRect(x, y, w, h, 1.5 * mm, fill=1, stroke=1)
    text_field(c, name, x + 1.5 * mm, y + 1 * mm, w - 3 * mm, h - 2 * mm, tooltip=label)


def radio(c, group, value, x, y, label, selected=False):
    c.acroForm.radio(
        name=group,
        value=value,
        selected=selected,
        tooltip="Le signe s’est-il amélioré ? Une seule réponse.",
        x=x,
        y=y,
        size=4.2 * mm,
        buttonStyle="circle",
        borderWidth=1,
        borderColor=BORDER,
        fillColor=white,
        textColor=BLUE,
        forceBorder=True,
    )
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 8)
    c.drawString(x + 6 * mm, y + 1.1 * mm, label)


def tri_state_row(c, group, label, y):
    """Une réponse exploitable : Oui / Non / Non vérifié, jamais une case ambiguë."""
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 7.8)
    c.drawString(MARGIN + 4 * mm, y + 1.1 * mm, label)
    for value, x, short_label in [
        ("oui", MARGIN + 134 * mm, "Oui"),
        ("non", MARGIN + 150 * mm, "Non"),
        ("non_verifie", MARGIN + 166 * mm, "N/V"),
    ]:
        c.acroForm.radio(
            name=group,
            value=value,
            selected=False,
            tooltip=f"{label} — Oui, Non ou Non vérifié. Une seule réponse.",
            x=x,
            y=y,
            size=3.8 * mm,
            buttonStyle="circle",
            borderWidth=1,
            borderColor=BORDER,
            fillColor=white,
            textColor=BLUE,
            forceBorder=True,
        )
        c.setFont("Helvetica", 6.8)
        c.drawString(x + 4.7 * mm, y + .9 * mm, short_label)


def page_one(c):
    header(c, 1, "Mesurez matin et soir, avant d’aérer. Une seule pièce par fiche.")

    section_title(c, 1, "Préparer le suivi", PAGE_H - 40 * mm)
    box_y = PAGE_H - 77 * mm
    c.setFillColor(PALE_BLUE)
    c.setStrokeColor(LIGHT_BORDER)
    c.roundRect(MARGIN, box_y, CONTENT_W, 29 * mm, 3 * mm, fill=1, stroke=1)
    labelled_field(c, "Pièce suivie — une fiche distincte par pièce", "piece", MARGIN + 4 * mm, box_y + 8 * mm, CONTENT_W - 8 * mm)

    alert_y = 194 * mm
    c.setFillColor(PALE_RED)
    c.setStrokeColor(HexColor("#D9A7A2"))
    c.roundRect(MARGIN, alert_y, CONTENT_W, 19 * mm, 2 * mm, fill=1, stroke=1)
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 7.8)
    c.drawString(MARGIN + 4 * mm, alert_y + 13.2 * mm, "N’attendez pas 7 jours : fuite active, mur mouillé ou moisissures étendues / récidivantes.")
    c.setFont("Helvetica", 7.4)
    c.drawString(MARGIN + 4 * mm, alert_y + 8.5 * mm, "Bâtiment / assurance selon la situation. Symptômes respiratoires ou occupant fragile : demandez un avis médical.")
    c.drawString(MARGIN + 4 * mm, alert_y + 3.8 * mm, "Sinon, mesurez au même endroit avant d’aérer et notez seulement les faits utiles : douche, linge, cuisson ou pluie.")

    section_title(c, 2, "Noter les mesures", PAGE_H - 112 * mm)
    table_x = MARGIN
    table_top = PAGE_H - 121 * mm
    header_h = 11 * mm
    row_h = 13 * mm
    widths = [22 * mm, 19 * mm, 19 * mm, 19 * mm, 19 * mm, CONTENT_W - 98 * mm]
    headers = ["JOUR / DATE", "MATIN\n°C", "MATIN\n%", "SOIR\n°C", "SOIR\n%", "FAIT NOTABLE / OBSERVATION"]

    c.setFillColor(NAVY)
    c.roundRect(table_x, table_top - header_h, CONTENT_W, header_h, 2 * mm, fill=1, stroke=0)
    x = table_x
    for i, (w, label) in enumerate(zip(widths, headers)):
        if i:
            c.setStrokeColor(HexColor("#587087"))
            c.line(x, table_top - header_h, x, table_top)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 7.4)
        parts = label.split("\n")
        for j, part in enumerate(parts):
            c.drawCentredString(x + w / 2, table_top - 4.5 * mm - j * 3.2 * mm, part)
        x += w

    for day in range(1, 8):
        y = table_top - header_h - day * row_h
        fill = white if day % 2 else HexColor("#F7FAFC")
        c.setFillColor(fill)
        c.setStrokeColor(BORDER)
        c.rect(table_x, y, CONTENT_W, row_h, fill=1, stroke=1)
        x = table_x
        for w in widths[:-1]:
            x += w
            c.line(x, y, x, y + row_h)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(table_x + 2.5 * mm, y + row_h - 4.2 * mm, f"J{day}")
        text_field(c, f"jour_{day}_date", table_x + 2 * mm, y + 1 * mm, widths[0] - 4 * mm, 6 * mm, 7.5, fill=fill, tooltip=f"Jour {day} — date")
        x = table_x + widths[0]
        measures = [
            ("matin_temp", "température du matin en degrés Celsius"),
            ("matin_hr", "humidité du matin en pourcentage"),
            ("soir_temp", "température du soir en degrés Celsius"),
            ("soir_hr", "humidité du soir en pourcentage"),
        ]
        for (key, label), w in zip(measures, widths[1:5]):
            text_field(c, f"jour_{day}_{key}", x + 1.2 * mm, y + 1.5 * mm, w - 2.4 * mm, row_h - 3 * mm, 9, fill=fill, tooltip=f"Jour {day} — {label}")
            x += w
        text_field(c, f"jour_{day}_note", x + 2 * mm, y + 1.5 * mm, widths[5] - 4 * mm, row_h - 3 * mm, 7.5, True, fill, tooltip=f"Jour {day} — fait notable ou observation")

    block_top = table_top - header_h - 7 * row_h - 8 * mm
    section_title(c, 3, "Localiser ce que vous voyez", block_top)
    note_y = 31 * mm
    c.setFillColor(SAGE)
    c.setStrokeColor(HexColor("#A8C7B2"))
    c.roundRect(MARGIN, note_y, CONTENT_W, 28 * mm, 3 * mm, fill=1, stroke=1)
    labels = [
        ("condensation", "Vitre / miroir embué"),
        ("odeur", "Odeur de moisi"),
        ("moisissure", "Points noirs / moisissure"),
        ("mur_humide", "Mur humide au toucher"),
        ("peinture", "Peinture qui cloque"),
        ("salpetre", "Dépôt blanc / salpêtre"),
    ]
    cols = 3
    col_w = (CONTENT_W - 8 * mm) / cols
    for idx, (key, label) in enumerate(labels):
        col = idx % cols
        row = idx // cols
        checkbox(c, f"symptome_{key}", MARGIN + 4 * mm + col * col_w, note_y + 17 * mm - row * 10 * mm, label, label_width=col_w - 10 * mm)

    labelled_field(c, "Emplacement précis (ex. angle nord, bas de mur, derrière une armoire)", "emplacement_precis", MARGIN, 18 * mm, CONTENT_W, 9 * mm)
    footer(c)


def page_two(c):
    header(c, 2, "Transformez les 14 relevés en indices, puis vérifiez chaque piste sans supposer la cause.")

    section_title(c, 4, "Compter et comparer", PAGE_H - 40 * mm)
    trend_y = PAGE_H - 93 * mm
    c.setFillColor(PALE_BLUE)
    c.setStrokeColor(LIGHT_BORDER)
    c.roundRect(MARGIN, trend_y, CONTENT_W, 44 * mm, 3 * mm, fill=1, stroke=1)
    labelled_field(c, "Relevés > 60 % (sur 14)", "compte_sup_60", MARGIN + 4 * mm, trend_y + 29 * mm, 38 * mm, 7 * mm)
    labelled_field(c, "Relevés ≥ 70 % (sur 14)", "compte_70", MARGIN + 48 * mm, trend_y + 29 * mm, 38 * mm, 7 * mm)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.2)
    c.drawString(MARGIN + 94 * mm, trend_y + 32 * mm, "40–60 % : repère pratique, jamais diagnostic à lui seul.")
    trends = [
        ("tendance_activite", "Pics après douche, cuisson ou linge"),
        ("tendance_hors_activite", "Valeurs élevées hors activité"),
        ("tendance_matin", "Taux surtout élevé le matin"),
        ("tendance_retour", "Retour vers 40–60 % entre deux pics"),
        ("tendance_locale", "Une seule pièce (fiches comparées)"),
        ("tendance_generale", "Plusieurs pièces (fiches comparées)"),
    ]
    col_w = (CONTENT_W - 10 * mm) / 2
    for idx, (key, label) in enumerate(trends):
        col = idx % 2
        row = idx // 2
        checkbox(c, key, MARGIN + 4 * mm + col * col_w, trend_y + 18 * mm - row * 7.2 * mm, label, label_width=col_w - 9 * mm)

    section_title(c, 5, "Noter le résultat des vérifications", PAGE_H - 102 * mm)
    check_y = 110 * mm
    c.setFillColor(white)
    c.setStrokeColor(LIGHT_BORDER)
    c.roundRect(MARGIN, check_y, CONTENT_W, 75 * mm, 3 * mm, fill=1, stroke=1)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 6.8)
    c.drawRightString(MARGIN + 178 * mm, check_y + 68 * mm, "OUI      NON      N/V")
    checks = [
        ("verif_entrees", "Entrées d’air présentes et libres ?"),
        ("verif_bouche", "Bouche d’extraction présente et propre ?"),
        ("verif_papier", "Aspiration apparente au papier ? (pas une mesure de débit)"),
        ("verif_porte", "Passage d’air sous la porte présent ?"),
        ("verif_fuite", "Fuite ou trace d’eau repérée près des tuyaux / raccords ?"),
        ("verif_pluie", "Trace ou mur plus humide après la pluie ?"),
        ("verif_meuble", "Signe concentré derrière un meuble collé au mur ?"),
        ("verif_aeration", "Taux en baisse 10 min après une aération franche ?"),
    ]
    for idx, (group, label) in enumerate(checks):
        y = check_y + 58 * mm - idx * 7.1 * mm
        if idx:
            c.setStrokeColor(HexColor("#EDF1F4"))
            c.line(MARGIN + 4 * mm, y + 5.2 * mm, PAGE_W - MARGIN - 4 * mm, y + 5.2 * mm)
        tri_state_row(c, group, label, y)

    section_title(c, 6, "Tester une seule action : 24 à 48 h", 100 * mm)
    action_y = 55 * mm
    c.setFillColor(SAGE)
    c.setStrokeColor(HexColor("#A8C7B2"))
    c.roundRect(MARGIN, action_y, CONTENT_W, 34 * mm, 3 * mm, fill=1, stroke=1)
    labelled_field(c, "Action testée — même heure, même endroit et conditions proches", "action_testee", MARGIN + 4 * mm, action_y + 19 * mm, CONTENT_W - 8 * mm, 7 * mm)
    x = MARGIN + 4 * mm
    for label, name, width in [
        ("Avant °C", "action_avant_temp", 20 * mm),
        ("Avant %", "action_avant_hr", 20 * mm),
        ("Après °C", "action_apres_temp", 20 * mm),
        ("Après %", "action_apres_hr", 20 * mm),
    ]:
        labelled_field(c, label, name, x, action_y + 4 * mm, width, 7 * mm)
        x += width + 4 * mm
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x + 1 * mm, action_y + 13 * mm, "LE SIGNE S’EST-IL AMÉLIORÉ ?")
    radio(c, "effet", "oui", x + 1 * mm, action_y + 4 * mm, "Oui")
    radio(c, "effet", "non", x + 24 * mm, action_y + 4 * mm, "Non")
    radio(c, "effet", "incertain", x + 47 * mm, action_y + 4 * mm, "Incertain")

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 7.6)
    c.drawString(MARGIN, 43 * mm, "Passez à la page 3 : aucune donnée ci-dessus n’est interprétée isolément.")
    footer(c)


def decision_card(c, y, color, key, title, indices, action):
    card_h = 22.5 * mm
    c.setFillColor(color)
    c.setStrokeColor(LIGHT_BORDER)
    c.roundRect(MARGIN, y, CONTENT_W, card_h, 2 * mm, fill=1, stroke=1)
    checkbox(c, f"orientation_{key}", MARGIN + 4 * mm, y + 12.3 * mm, title, font_size=7.2, label_width=31 * mm)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 6.6)
    c.drawString(MARGIN + 41 * mm, y + 17 * mm, "INDICES À RELIER")
    c.drawString(MARGIN + 111 * mm, y + 17 * mm, "SUITE LOGIQUE")
    draw_wrapped(c, indices, MARGIN + 41 * mm, y + 13 * mm, 65 * mm, size=6.6, leading=7.1)
    draw_wrapped(c, action, MARGIN + 111 * mm, y + 13 * mm, 65 * mm, size=6.6, leading=7.1)


def page_three(c):
    header(c, 3, "Reliez plusieurs indices. Une valeur, une case ou un test isolé ne suffit pas à conclure.")

    section_title(c, 7, "Avant d’interpréter", PAGE_H - 40 * mm)
    note_y = 220 * mm
    c.setFillColor(PALE_YELLOW)
    c.setStrokeColor(HexColor("#DFC66D"))
    c.roundRect(MARGIN, note_y, CONTENT_W, 28 * mm, 3 * mm, fill=1, stroke=1)
    draw_wrapped(c, "Température : l’humidité relative varie avec elle. Comparez surtout des relevés pris à température proche ; si l’écart avant / après dépasse environ 2 °C, n’attribuez pas la variation du % à l’action seule.", MARGIN + 4 * mm, note_y + 20 * mm, CONTENT_W - 8 * mm, font="Helvetica-Bold", size=7.4, leading=9)
    draw_wrapped(c, "Dates + faits notables : ils servent à relier les variations à la pluie, à une activité ou à une récidive. L’emplacement précis distingue un signe local d’un problème plus général. Conservez la fiche et des photos datées.", MARGIN + 4 * mm, note_y + 9 * mm, CONTENT_W - 8 * mm, size=7.2, leading=8.5)

    section_title(c, 8, "Orienter la suite", 211 * mm)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.1)
    c.drawString(MARGIN, 197 * mm, "Cochez les orientations appuyées par plusieurs indices. Elles peuvent se cumuler ; « Eau / bâti » prime sur les autres.")

    cards = [
        (PALE_RED, "eau", "EAU / BÂTI", "Fuite = Oui ou mur mouillé ; ou cloque / dépôt blanc en bas de mur, ou aggravation après pluie = Oui.", "Fuite active ou mur mouillé : n’attendez pas. Sinon, faites chercher infiltration / remontée ; un déshumidificateur ne répare pas l’entrée d’eau."),
        (SAGE, "ventilation", "AIR / VAPEUR", "Nombreux relevés > 60 % ou relevés ≥ 70 %, avec pics d’activité ou valeurs élevées hors activité, et au moins un contrôle d’air = Non.", "Dégagez / nettoyez, réduisez les apports, remesurez. Si cela persiste : contrôle de la ventilation par un professionnel."),
        (PALE_BLUE, "condensation", "CONDENSATION LOCALE", "Buée, taux surtout élevé le matin, signe derrière meuble = Oui, zone froide ; amélioration après aération / écartement.", "Améliorez circulation d’air et ventilation. Utilisez le calculateur ; si récidive locale, recherchez pont thermique / défaut du bâti."),
        (PALE_YELLOW, "cachee", "HUMIDITÉ LOCALE CACHÉE", "Odeur, moisissure, cloque ou mur humide très localisé dans une seule pièce, alors que les relevés restent souvent dans le repère.", "Un taux ambiant rassurant n’exclut pas un support humide. Cherchez la source ; professionnel si humide, étendu ou récidivant."),
        (HexColor("#F3F5F7"), "ponctuel", "APPORT PONCTUEL", "Pics liés à une activité, retour vers 40–60 % entre les pics, aucun signe d’eau, et amélioration au test.", "Corrigez d’abord l’activité / l’aération. Déshumidificateur seulement en aide temporaire si besoin, jamais comme réparation."),
        (HexColor("#EAF3EC"), "rassurant", "SUIVI RASSURANT", "Relevés surtout entre 40 et 60 %, aucun ≥ 70 %, aucun signe visible ; contrôles applicables = Oui, fuite et aggravation après pluie = Non.", "Conservez les habitudes. Aucun achat n’est justifié par cette fiche ; recommencez si saison, usage ou signes changent."),
        (white, "incertain", "INDÉTERMINÉ / GÉNÉRAL", "Résultats contradictoires, aucune tendance nette, plusieurs pièces touchées ou action sans effet clair.", "Vérifiez placement / appareil, répétez ou comparez une autre pièce. Si signes ou persistance : diagnostic professionnel."),
    ]
    y = 168 * mm
    for color, key, title, indices, action in cards:
        decision_card(c, y, color, key, title, indices, action)
        y -= 24.5 * mm

    footer(c)


def build_pdf():
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    getattr(c, "_doc").Catalog.Lang = PDFString("fr-FR")
    c.setTitle("Suivi humidité — 7 jours")
    c.setAuthor("Maison Moins Humide")
    c.setSubject("Fiche A4 remplissable pour suivre l’humidité d’une pièce pendant 7 jours")
    c.setKeywords("humidité, hygromètre, relevé, condensation, logement")
    page_one(c)
    c.showPage()
    page_two(c)
    c.showPage()
    page_three(c)
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
