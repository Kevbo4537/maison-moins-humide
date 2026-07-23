from pathlib import Path
import fitz

PDF = Path('public/downloads/checklist-humidite-7-jours.pdf')
doc = fitz.open(PDF)
text = '\n'.join(page.get_text() for page in doc)

assert len(doc) == 2, f'expected 2 pages, got {len(doc)}'
for phrase in [
    'AVANT LE PREMIER RELEVÉ',
    'DU JOUR 1 AU JOUR 7',
    'APRÈS LE DERNIER RELEVÉ DU JOUR 7',
    'Générez votre compte rendu personnalisé',
    'maisonmoinshumide.fr/checklists/humidite-maison/',
]:
    assert phrase in text, phrase
assert '24 à 48' not in text
assert 'Testez une seule action' not in text

page_widgets = [(page, widget) for page in doc for widget in (page.widgets() or [])]
widgets = [widget for _, widget in page_widgets]
assert len(widgets) == 61, len(widgets)
assert len({widget.field_name for widget in widgets}) == 53
assert all(widget.field_label for widget in widgets)
assert 'signe_aucun' not in {widget.field_name for widget in widgets}
assert all('?' in widget.field_label for widget in widgets if widget.field_type_string == 'RadioButton')
lang_type, lang_value = doc.xref_get_key(doc.pdf_catalog(), 'Lang')
assert lang_value == 'fr-FR', (lang_type, lang_value)
for page, widget in page_widgets:
    assert widget.rect.x0 >= 0 and widget.rect.y0 >= 0
    assert widget.rect.x1 <= page.rect.width and widget.rect.y1 <= page.rect.height

names = {widget.field_name for widget in widgets}
for day in range(1, 8):
    for suffix in ('matin_temp', 'matin_hr', 'soir_temp', 'soir_hr', 'fait'):
        assert f'jour_{day}_{suffix}' in names

filled = Path('/tmp/mmh-checklist-filled-test.pdf')
for widget in widgets:
    if widget.field_name == 'jour_1_matin_temp':
        widget.field_value = '19,5'
        widget.update()
    elif widget.field_name == 'jour_1_matin_hr':
        widget.field_value = '62'
        widget.update()
doc.save(filled)
doc.close()

reopened = fitz.open(filled)
values = {widget.field_name: widget.field_value for page in reopened for widget in (page.widgets() or [])}
assert values['jour_1_matin_temp'] == '19,5'
assert values['jour_1_matin_hr'] == '62'
reopened.close()
print('PDF_FLOW_OK 2 pages, 61 widgets, save/reopen OK')
