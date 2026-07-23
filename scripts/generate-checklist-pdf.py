#!/usr/bin/env python3
"""Génère la grille remplissable du suivi humidité sur 7 jours."""
from pathlib import Path
import sys

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
import fitz

OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('public/downloads/checklist-humidite-7-jours.pdf')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
PAGE_W, PAGE_H = A4
M = 14 * mm
CW = PAGE_W - 2 * M
NAVY = HexColor('#17324D')
BLUE = HexColor('#2B6F9C')
PALE_BLUE = HexColor('#EAF3F8')
PALE_RED = HexColor('#FCE8E6')
PALE_GREEN = HexColor('#EEF5F0')
TEXT = HexColor('#253746')
MUTED = HexColor('#5E6F7D')
BORDER = HexColor('#AABBC7')
LIGHT = HexColor('#D5E0E7')
URL = 'https://www.maisonmoinshumide.fr/checklists/humidite-maison/'


def wrapped_lines(text, font, size, width):
    lines, current = [], ''
    for word in text.split():
        candidate = f'{current} {word}'.strip()
        if stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(c, text, x, y, width, font='Helvetica', size: float = 8, leading: float = 10, color=TEXT):
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrapped_lines(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def header(c, page, subtitle):
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 29 * mm, PAGE_W, 29 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 19)
    c.drawString(M, PAGE_H - 13 * mm, 'Suivi humidité — 7 jours')
    c.setFont('Helvetica', 9)
    c.drawString(M, PAGE_H - 20 * mm, subtitle)
    c.setFont('Helvetica-Bold', 9)
    c.drawRightString(PAGE_W - M, PAGE_H - 13 * mm, f'FICHE {page}/2')
    c.setFont('Helvetica', 7.5)
    c.drawRightString(PAGE_W - M, PAGE_H - 20 * mm, 'maisonmoinshumide.fr')


def footer(c):
    c.setStrokeColor(LIGHT)
    c.line(M, 15 * mm, PAGE_W - M, 15 * mm)
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 6.8)
    c.drawString(M, 10.5 * mm, 'Relevé d’orientation, pas diagnostic : une fuite ou un mur mouillé reste prioritaire.')
    c.drawRightString(PAGE_W - M, 10.5 * mm, 'Version 2026-07')


def title(c, number, text, y):
    c.setFillColor(BLUE)
    c.roundRect(M, y - 3 * mm, 8 * mm, 8 * mm, 2 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(M + 4 * mm, y - .5 * mm, str(number))
    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 12.5)
    c.drawString(M + 12 * mm, y - .5 * mm, text)


def text_field(c, name, x, y, w, h, tooltip, font_size: float = 8, multiline=False):
    c.acroForm.textfield(
        name=name, tooltip=tooltip, x=x, y=y, width=w, height=h,
        borderWidth=0, fillColor=white, textColor=TEXT, forceBorder=False,
        fontName='Helvetica', fontSize=font_size,
        fieldFlags='multiline' if multiline else '',
    )


def checkbox(c, name, label, x, y, width=None):
    size = 4.2 * mm
    c.acroForm.checkbox(
        name=name, tooltip=label, x=x, y=y, size=size,
        buttonStyle='check', borderWidth=1, borderColor=BORDER,
        fillColor=white, checked=False, fieldFlags='', forceBorder=True,
    )
    if width:
        draw_wrapped(c, label, x + 6 * mm, y + 1.2 * mm, width, size=7.8, leading=9)
    else:
        c.setFillColor(TEXT)
        c.setFont('Helvetica', 7.8)
        c.drawString(x + 6 * mm, y + 1.2 * mm, label)


def radio(c, group, value, label, x, y, question):
    size = 4.1 * mm
    c.acroForm.radio(
        name=group, value=value, selected=False,
        tooltip=f'{question} — {label}', x=x, y=y, size=size,
        buttonStyle='circle', borderWidth=1, borderColor=BORDER,
        fillColor=white, textColor=BLUE,
        fieldFlags='noToggleToOff radio', forceBorder=True,
    )
    c.setFillColor(TEXT)
    c.setFont('Helvetica', 7)
    c.drawString(x + 5.7 * mm, y + 1.1 * mm, label)


def page_one(c):
    header(c, 1, 'Page 1 : ce que vous faites avant puis pendant les 7 jours')
    y = PAGE_H - 39 * mm
    title(c, 1, 'AVANT LE PREMIER RELEVÉ', y)
    y -= 13 * mm
    c.setFillColor(PALE_BLUE)
    c.setStrokeColor(LIGHT)
    c.roundRect(M, y - 25 * mm, CW, 25 * mm, 2.5 * mm, fill=1, stroke=1)
    draw_wrapped(c, 'Choisissez une seule pièce. Posez l’hygromètre toujours au même endroit, loin d’un radiateur, d’une fenêtre ouverte et d’une bouche d’air.', M + 4 * mm, y - 5 * mm, CW - 8 * mm, size=8.2, leading=10)
    c.setFont('Helvetica-Bold', 7.2)
    c.setFillColor(MUTED)
    c.drawString(M + 4 * mm, y - 16.5 * mm, 'PIÈCE SUIVIE')
    c.setFillColor(white)
    c.roundRect(M + 32 * mm, y - 21 * mm, CW - 36 * mm, 8 * mm, 1.5 * mm, fill=1, stroke=1)
    text_field(c, 'piece', M + 34 * mm, y - 20 * mm, CW - 40 * mm, 6 * mm, 'Pièce suivie')

    y -= 35 * mm
    title(c, 2, 'DU JOUR 1 AU JOUR 7', y)
    draw_wrapped(c, 'Chaque matin et chaque soir, avant d’aérer : notez température et humidité. Notez tous les faits utiles de la journée ; activité, pluie et autre changement peuvent se cumuler.', M + 12 * mm, y - 8 * mm, CW - 12 * mm, size=8.1, leading=9.5)

    top = y - 20 * mm
    hh, rh = 10 * mm, 16 * mm
    widths = [15 * mm, 22 * mm, 18 * mm, 18 * mm, 18 * mm, 18 * mm, CW - 109 * mm]
    labels = ['JOUR', 'DATE', 'MATIN °C', 'MATIN %', 'SOIR °C', 'SOIR %', 'FAITS : heure, activité, pluie, autre…']
    x = M
    c.setFillColor(NAVY)
    c.roundRect(M, top - hh, CW, hh, 2 * mm, fill=1, stroke=0)
    for index, (width, label) in enumerate(zip(widths, labels)):
        if index:
            c.setStrokeColor(HexColor('#587087'))
            c.line(x, top - hh, x, top)
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 6.6)
        for line_index, line in enumerate(wrapped_lines(label, 'Helvetica-Bold', 6.6, width - 2 * mm)[:2]):
            c.drawCentredString(x + width / 2, top - 4 * mm - line_index * 3 * mm, line)
        x += width

    for day in range(1, 8):
        row_y = top - hh - day * rh
        c.setFillColor(white if day % 2 else HexColor('#F7FAFC'))
        c.setStrokeColor(BORDER)
        c.rect(M, row_y, CW, rh, fill=1, stroke=1)
        x = M
        for width in widths[:-1]:
            x += width
            c.line(x, row_y, x, row_y + rh)
        c.setFillColor(NAVY)
        c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(M + widths[0] / 2, row_y + 6.2 * mm, f'J{day}')
        x = M + widths[0]
        names = [f'jour_{day}_date', f'jour_{day}_matin_temp', f'jour_{day}_matin_hr', f'jour_{day}_soir_temp', f'jour_{day}_soir_hr', f'jour_{day}_fait']
        tips = [f'Jour {day} date', f'Jour {day} matin température', f'Jour {day} matin humidité', f'Jour {day} soir température', f'Jour {day} soir humidité', f'Jour {day} fait notable']
        for width, name, tip in zip(widths[1:], names, tips):
            text_field(c, name, x + 1 * mm, row_y + 2 * mm, width - 2 * mm, rh - 4 * mm, tip, font_size=7.2, multiline=name.endswith('fait'))
            x += width

    alert_y = 22 * mm
    c.setFillColor(PALE_RED)
    c.setStrokeColor(HexColor('#D9A7A2'))
    c.roundRect(M, alert_y, CW, 15 * mm, 2 * mm, fill=1, stroke=1)
    c.setFont('Helvetica-Bold', 7.6)
    c.setFillColor(TEXT)
    c.drawString(M + 4 * mm, alert_y + 9.5 * mm, 'N’ATTENDEZ PAS LE JOUR 7 : fuite active, mur mouillé ou moisissures étendues / récidivantes.')
    c.setFont('Helvetica', 7.2)
    c.drawString(M + 4 * mm, alert_y + 4.3 * mm, 'Faites vérifier sans attendre ; le relevé ne doit jamais retarder une intervention utile.')
    footer(c)


def answer_row(c, group, question, y, values, offsets=None):
    draw_wrapped(c, question, M + 4 * mm, y + 4.5 * mm, 86 * mm, size=7.8, leading=9)
    start = M + 96 * mm
    positions = offsets or [index * 21 for index in range(len(values))]
    for index, (value, label) in enumerate(values):
        radio(c, group, value, label, start + positions[index] * mm, y, question)


def page_two(c):
    header(c, 2, 'Page 2 : à remplir une seule fois, après le dernier relevé du jour 7')
    y = PAGE_H - 39 * mm
    title(c, 3, 'APRÈS LE DERNIER RELEVÉ DU JOUR 7', y)
    draw_wrapped(c, 'Répondez maintenant selon ce qui s’est produit à un moment quelconque pendant la semaine. Ces réponses ne sont pas à remplir au début.', M + 12 * mm, y - 8 * mm, CW - 12 * mm, size=8.2, leading=10)

    box_top = y - 23 * mm
    c.setFillColor(PALE_BLUE)
    c.setStrokeColor(LIGHT)
    c.roundRect(M, box_top - 46 * mm, CW, 46 * mm, 2.5 * mm, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(M + 4 * mm, box_top - 7 * mm, 'Signes apparus au moins une fois pendant les 7 jours')
    items = [
        ('signe_condensation', 'Buée ou eau sur vitre / paroi'), ('signe_odeur', 'Odeur de moisi'),
        ('signe_moisissure', 'Moisissure visible'), ('signe_moisissure_recidive', 'Moisissure réapparue après nettoyage'),
        ('signe_mur_mouille', 'Mur mouillé au toucher'),
        ('signe_cloque', 'Peinture ou enduit qui cloque'), ('signe_depot', 'Dépôt blanc / salpêtre possible'),
    ]
    for index, (name, label) in enumerate(items):
        col = index % 2
        row = index // 2
        checkbox(c, name, label, M + 5 * mm + col * 88 * mm, box_top - 16 * mm - row * 7 * mm, 73 * mm)
    draw_wrapped(c, 'Si aucun signe n’est apparu, ne cochez rien ici puis choisissez « Aucun » à la question sur leur emplacement.', M + 5 * mm, box_top - 43 * mm, CW - 10 * mm, size=7.2, leading=8.5)

    y = box_top - 53 * mm
    c.setFillColor(white)
    c.setStrokeColor(BORDER)
    c.roundRect(M, y - 57 * mm, CW, 57 * mm, 2.5 * mm, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 8.8)
    c.drawString(M + 4 * mm, y - 7 * mm, 'Trois réponses de fin de suivi')
    common = [('oui', 'Oui'), ('non', 'Non'), ('inconnu', 'Inconnu'), ('na', 'N/A')]
    answer_row(c, 'pluie', 'Une trace s’est-elle aggravée après la pluie ?', y - 20 * mm, common)
    c.setStrokeColor(LIGHT); c.line(M + 4 * mm, y - 26 * mm, PAGE_W - M - 4 * mm, y - 26 * mm)
    answer_row(c, 'ventilation', 'Les entrées d’air ou l’extraction attendues sont-elles présentes, ouvertes et propres ?', y - 38 * mm, common)
    c.setStrokeColor(LIGHT); c.line(M + 4 * mm, y - 44 * mm, PAGE_W - M - 4 * mm, y - 44 * mm)
    answer_row(c, 'portee', 'Où les signes sont-ils apparus ?', y - 54 * mm, [('aucun', 'Aucun'), ('local', 'Zone précise'), ('multiple', 'Plusieurs zones')], offsets=[0, 22, 56])

    y -= 70 * mm
    title(c, 4, 'Générez votre compte rendu personnalisé', y)
    c.setFillColor(PALE_GREEN)
    c.setStrokeColor(HexColor('#B8D1C1'))
    c.roundRect(M, y - 61 * mm, CW, 52 * mm, 3 * mm, fill=1, stroke=1)
    draw_wrapped(c, 'À ce stade seulement, reportez les 14 mesures et les réponses ci-dessus dans l’outil du site. Il calcule automatiquement :', M + 5 * mm, y - 18 * mm, CW - 10 * mm, font='Helvetica-Bold', size=8.4, leading=10)
    bullets = [
        'le nombre de relevés au-dessus de 60 % et à 70 % ou plus ;',
        'la moyenne, le minimum, le maximum et la persistance ;',
        'les liens avec les activités ou la pluie et l’effet des variations de température ;',
        'une piste principale, les faits qui la justifient et trois actions concrètes.',
    ]
    bullet_y = y - 31 * mm
    for item in bullets:
        c.setFillColor(BLUE); c.circle(M + 7 * mm, bullet_y + 1 * mm, 1 * mm, fill=1, stroke=0)
        draw_wrapped(c, item, M + 11 * mm, bullet_y, CW - 17 * mm, size=8, leading=9)
        bullet_y -= 8 * mm

    url_y = 26 * mm
    c.setFillColor(NAVY)
    c.roundRect(M, url_y, CW, 20 * mm, 3 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(PAGE_W / 2, url_y + 12 * mm, 'Saisir les données et obtenir le bilan :')
    c.setFont('Helvetica', 8.2)
    c.drawCentredString(PAGE_W / 2, url_y + 6 * mm, 'maisonmoinshumide.fr/checklists/humidite-maison/')
    c.linkURL(URL, (M, url_y, PAGE_W - M, url_y + 20 * mm), relative=0)
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 7.2)
    c.drawCentredString(PAGE_W / 2, 19.5 * mm, 'Le site ne transmet pas vos données : elles restent dans votre navigateur.')
    footer(c)


def build():
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    c.setTitle('Suivi humidité 7 jours — grille et compte rendu')
    c.setAuthor('Maison Moins Humide')
    c.setSubject('14 relevés puis compte rendu personnalisé en ligne')
    page_one(c); c.showPage()
    page_two(c); c.showPage()
    c.save()
    doc = fitz.open(OUTPUT)
    doc.xref_set_key(doc.pdf_catalog(), 'Lang', '(fr-FR)')
    doc.saveIncr()
    doc.close()


if __name__ == '__main__':
    build()
    print(f'Generated {OUTPUT}')
