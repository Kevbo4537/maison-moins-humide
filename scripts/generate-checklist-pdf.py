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
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 14 * mm, f"FICHE {page_number}/2")
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


def page_one(c):
    header(c, 1, "Mesurez matin et soir, avant d’aérer. Une seule pièce par fiche.")

    section_title(c, 1, "Préparer le suivi", PAGE_H - 40 * mm)
    box_y = PAGE_H - 77 * mm
    c.setFillColor(PALE_BLUE)
    c.setStrokeColor(LIGHT_BORDER)
    c.roundRect(MARGIN, box_y, CONTENT_W, 29 * mm, 3 * mm, fill=1, stroke=1)
    gap = 5 * mm
    col1 = 58 * mm
    col2 = 42 * mm
    col3 = CONTENT_W - col1 - col2 - 2 * gap - 8 * mm
    x = MARGIN + 4 * mm
    labelled_field(c, "Pièce suivie", "piece", x, box_y + 8 * mm, col1)
    x += col1 + gap
    labelled_field(c, "Du", "date_debut", x, box_y + 8 * mm, col2)
    x += col2 + gap
    labelled_field(c, "Au", "date_fin", x, box_y + 8 * mm, col3)

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
    header(c, 2, "Bilan après 14 mesures, puis test complémentaire. Cette fiche repère des indices, pas une cause.")

    section_title(c, 4, "Compter et comparer", PAGE_H - 40 * mm)
    trend_y = PAGE_H - 93 * mm
    c.setFillColor(PALE_BLUE)
    c.setStrokeColor(LIGHT_BORDER)
    c.roundRect(MARGIN, trend_y, CONTENT_W, 44 * mm, 3 * mm, fill=1, stroke=1)
    labelled_field(c, "Mesures > 60 % (sur 14)", "compte_sup_60", MARGIN + 4 * mm, trend_y + 29 * mm, 38 * mm, 7 * mm)
    labelled_field(c, "Mesures ≥ 70 % (sur 14)", "compte_70", MARGIN + 48 * mm, trend_y + 29 * mm, 38 * mm, 7 * mm)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.2)
    c.drawString(MARGIN + 94 * mm, trend_y + 32 * mm, "40–60 % est un repère, pas un seuil diagnostique absolu.")
    trends = [
        ("tendance_activite", "Pics après douche, cuisson ou linge"),
        ("tendance_hors_activite", "Valeurs élevées hors activité"),
        ("tendance_matin", "Taux surtout élevé le matin"),
        ("tendance_pluie", "Traces augmentent après la pluie"),
        ("tendance_locale", "Une seule pièce (fiches comparées)"),
        ("tendance_generale", "Plusieurs pièces (fiches comparées)"),
    ]
    col_w = (CONTENT_W - 10 * mm) / 2
    for idx, (key, label) in enumerate(trends):
        col = idx % 2
        row = idx // 2
        checkbox(c, key, MARGIN + 4 * mm + col * col_w, trend_y + 18 * mm - row * 7.2 * mm, label, label_width=col_w - 9 * mm)

    section_title(c, 5, "Vérifications simples", PAGE_H - 102 * mm)
    check_y = PAGE_H - 146 * mm
    c.setFillColor(white)
    c.setStrokeColor(LIGHT_BORDER)
    c.roundRect(MARGIN, check_y, CONTENT_W, 35 * mm, 3 * mm, fill=1, stroke=1)
    checks = [
        ("verif_entrees", "Entrées d’air dégagées"),
        ("verif_bouche", "Bouche d’extraction propre"),
        ("verif_papier", "Aspiration apparente (pas le débit)"),
        ("verif_porte", "Dégagement sous les portes présent"),
        ("verif_fuite", "Tuyaux et raccords inspectés"),
        ("verif_pluie", "Traces comparées avant / après pluie"),
        ("verif_meuble", "Meuble écarté du mur de 5 à 10 cm"),
        ("verif_aeration", "Aération 5 à 10 min testée"),
    ]
    for idx, (key, label) in enumerate(checks):
        col = idx % 2
        row = idx // 2
        checkbox(c, key, MARGIN + 4 * mm + col * col_w, check_y + 25 * mm - row * 7.2 * mm, label, font_size=7.8, label_width=col_w - 9 * mm)

    section_title(c, 6, "Test complémentaire : 24 à 48 h", PAGE_H - 154 * mm)
    action_y = PAGE_H - 197 * mm
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

    section_title(c, 7, "Comprendre sans diagnostiquer", PAGE_H - 204 * mm)
    decision_top = PAGE_H - 213 * mm
    card_gap = 2.5 * mm
    card_h = 12 * mm
    decisions = [
        (PALE_BLUE, "REPÈRE, PAS SEUIL", "40 à 60 % est un repère. Regardez surtout les répétitions, le contexte et l’évolution des signes."),
        (SAGE, "PISTE À VÉRIFIER", "Valeurs répétées hors activité : vérifiez ventilation et vapeur. Une baisse après aération n’exclut pas une autre cause."),
        (PALE_YELLOW, "AIDE TEMPORAIRE", "Apport temporaire identifié, sans signe d’eau : un déshumidificateur peut aider, mais ne traite pas la cause."),
        (PALE_RED, "NE PAS ATTENDRE", "Fuite active, mur mouillé ou moisissures importantes : bâtiment / assurance. Symptômes ou personne fragile : avis médical."),
    ]
    y = decision_top - card_h
    for color, title, text in decisions:
        c.setFillColor(color)
        c.setStrokeColor(LIGHT_BORDER)
        c.roundRect(MARGIN, y, CONTENT_W, card_h, 2 * mm, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 7.6)
        c.drawString(MARGIN + 4 * mm, y + 8.2 * mm, title)
        draw_wrapped(c, text, MARGIN + 43 * mm, y + 8.7 * mm, CONTENT_W - 47 * mm, size=7.1, leading=7.8, max_lines=2)
        y -= card_h + card_gap

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 7.8)
    c.drawString(MARGIN, 20 * mm, "À garder : photos datées des traces + photo de l’hygromètre et de son emplacement.")
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
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
