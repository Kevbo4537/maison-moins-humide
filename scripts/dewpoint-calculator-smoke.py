#!/usr/bin/env python3
import math
from itertools import product

ROOMS = ['chambre','salle de bain','cuisine','cave','buanderie','placard','salon','autre']
SYMPTOMS = ['condensation','mur froid','odeur','moisissure','linge','salpetre','pluie','aucun']
FREQUENCIES = ['ponctuel','matin','souvent','permanent','pluie']


def saturation_vapor_pressure(temp_c):
    return 6.1094 * math.exp((17.625 * temp_c) / (243.04 + temp_c))


def dew_point(temp_c, rh):
    gamma = math.log(rh / 100) + (17.625 * temp_c) / (243.04 + temp_c)
    return (243.04 * gamma) / (17.625 - gamma)


def absolute_humidity(temp_c, rh):
    return 216.7 * saturation_vapor_pressure(temp_c) * (rh / 100) / (temp_c + 273.15)


def surface_relative_humidity(air_temp, rh, surface_temp):
    return 100 * saturation_vapor_pressure(air_temp) * (rh / 100) / saturation_vapor_pressure(surface_temp)


def classify(air_temp, rh, surface_temp, room, symptom, frequency, alerts=()):
    dp = dew_point(air_temp, rh)
    ah = absolute_humidity(air_temp, rh)
    has_surface = surface_temp is not None
    delta = surface_temp - dp if has_surface else None
    srh = surface_relative_humidity(air_temp, rh, surface_temp) if has_surface else None

    recurrent = frequency in ('matin','souvent','permanent')
    visible_condensation_likely = symptom == 'condensation' and recurrent
    visible_mold_or_musty = symptom == 'moisissure' or (symptom in ('odeur','mur froid') and recurrent)
    slow_drying_likely = symptom == 'linge' and rh >= 60
    technical_alert = symptom in ('salpetre','pluie') or frequency == 'pluie' or bool(alerts)

    if technical_alert:
        level = 'technical'
    elif (has_surface and (delta <= 2 or srh >= 95)) or visible_condensation_likely:
        level = 'condensation'
    elif (has_surface and srh >= 80) or visible_mold_or_musty:
        level = 'mold'
    elif rh >= 70 or (rh >= 60 and frequency != 'ponctuel') or slow_drying_likely:
        level = 'humid'
    else:
        level = 'ok'
    return dict(level=level, dew_point=dp, absolute_humidity=ah, delta=delta, surface_rh=srh)

# Golden cases: expected from scientific/UX logic, not just code paths.
golden = [
    ('air sec normal', dict(air_temp=22, rh=45, surface_temp=16, room='salon', symptom='aucun', frequency='ponctuel'), 'ok'),
    ('chambre condensation calculée', dict(air_temp=19, rh=70, surface_temp=13, room='chambre', symptom='condensation', frequency='matin'), 'condensation'),
    ('surface humide sans gouttes', dict(air_temp=20, rh=60, surface_temp=15, room='salon', symptom='aucun', frequency='ponctuel'), 'mold'),
    ('cave fraîche humide', dict(air_temp=10, rh=80, surface_temp=8, room='cave', symptom='odeur', frequency='souvent'), 'condensation'),
    ('RH haute sans surface', dict(air_temp=19, rh=72, surface_temp=None, room='chambre', symptom='aucun', frequency='souvent'), 'humid'),
    ('vitre embuée sans surface', dict(air_temp=20, rh=55, surface_temp=None, room='chambre', symptom='condensation', frequency='matin'), 'condensation'),
    ('moisissure visible valeurs basses', dict(air_temp=21, rh=45, surface_temp=None, room='chambre', symptom='moisissure', frequency='souvent'), 'mold'),
    ('odeur persistante valeurs basses', dict(air_temp=20, rh=50, surface_temp=None, room='placard', symptom='odeur', frequency='permanent'), 'mold'),
    ('linge sèche mal à 65%', dict(air_temp=19, rh=65, surface_temp=None, room='buanderie', symptom='linge', frequency='ponctuel'), 'humid'),
    ('salpêtre prioritaire', dict(air_temp=20, rh=45, surface_temp=18, room='cave', symptom='salpetre', frequency='ponctuel'), 'technical'),
]

failures=[]
for name, kwargs, expected in golden:
    got=classify(**kwargs)['level']
    if got != expected:
        failures.append(f'Golden {name}: expected {expected}, got {got}')

# Exhaustive sanity checks over realistic grid.
temps = [8, 10, 16, 19, 22, 26]
rhs = [35, 45, 55, 60, 65, 70, 80, 90]
surfaces = [None, 5, 8, 10, 13, 15, 18, 21]
levels_count = {k:0 for k in ['ok','humid','mold','condensation','technical']}
checked=0
for air_temp, rh, surface_temp, room, symptom, frequency in product(temps, rhs, surfaces, ROOMS, SYMPTOMS, FREQUENCIES):
    # skip impossible-ish: surface massively hotter than hot air is allowed but not useful; keep to stress logic.
    res=classify(air_temp, rh, surface_temp, room, symptom, frequency)
    level=res['level']; levels_count[level]+=1; checked+=1
    if symptom in ('salpetre','pluie') and level != 'technical':
        failures.append(f'technical symptom not prioritized: {air_temp},{rh},{surface_temp},{symptom},{frequency}->{level}')
    if frequency == 'pluie' and level != 'technical':
        failures.append(f'pluie frequency not prioritized: {air_temp},{rh},{surface_temp},{symptom}->{level}')
    if symptom == 'moisissure' and level == 'ok':
        failures.append(f'moisissure visible classified ok: {air_temp},{rh},{surface_temp},{frequency}')
    if symptom == 'condensation' and frequency in ('matin','souvent','permanent') and level == 'ok':
        failures.append(f'recurrent condensation classified ok: {air_temp},{rh},{surface_temp},{frequency}')
    if surface_temp is not None and res['surface_rh'] >= 100 and level not in ('condensation','technical'):
        failures.append(f'surface RH>=100 not condensation/technical: {air_temp},{rh},{surface_temp},{symptom},{frequency}->{level}')
    if rh >= 80 and level == 'ok':
        failures.append(f'RH>=80 classified ok: {air_temp},{rh},{surface_temp},{symptom},{frequency}')
    if len(failures) > 20:
        break

print('Golden cases:', len(golden), 'OK')
print('Grid cases checked:', checked)
print('Level distribution:', levels_count)
if failures:
    print('FAIL')
    for f in failures[:30]: print('-', f)
    raise SystemExit(1)
print('All coherence checks passed')
