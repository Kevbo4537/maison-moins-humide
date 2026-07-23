import test from 'node:test';
import assert from 'node:assert/strict';
import { analyzeHumidityWeek } from '../src/lib/humidity-report.mjs';

function week(values, temps = Array(14).fill(19)) {
  return values.map((rh, index) => ({
    day: Math.floor(index / 2) + 1,
    period: index % 2 === 0 ? 'morning' : 'evening',
    temp: temps[index],
    rh,
  }));
}

function input(overrides = {}) {
  return {
    roomType: 'chambre',
    readings: week(Array(14).fill(52)),
    contexts: Array.from({ length: 7 }, (_, index) => ({ day: index + 1, event: 'none' })),
    signs: {
      condensation: false,
      odor: false,
      mold: false,
      wetWall: false,
      blistering: false,
      salts: false,
    },
    rainWorse: 'no',
    ventilation: 'yes',
    scope: 'none',
    ...overrides,
  };
}

test('refuse de produire un compte rendu avec moins de 14 relevés complets', () => {
  const result = analyzeHumidityWeek(input({ readings: week(Array(13).fill(52)) }));
  assert.equal(result.status, 'incomplete');
  assert.equal(result.missingReadings, 1);
});

test('refuse les températures vides au lieu de les convertir en zéro', () => {
  const result = analyzeHumidityWeek(input({ readings: week(Array(14).fill(52), Array(14).fill(null)) }));
  assert.equal(result.status, 'incomplete');
  assert.equal(result.missingReadings, 14);
});

test('exige exactement un relevé matin et soir pour chacun des sept jours', () => {
  const duplicated = week(Array(14).fill(52)).map((reading) => ({ ...reading }));
  duplicated[13] = { ...duplicated[12] };
  const result = analyzeHumidityWeek(input({ readings: duplicated }));
  assert.equal(result.status, 'incomplete');
  assert.match(result.message, /jour 7.*soir|créneau/i);
});

test('refuse un bilan post-J7 laissé sans réponse', () => {
  const result = analyzeHumidityWeek(input({ rainWorse: '', ventilation: '', scope: '' }));
  assert.equal(result.status, 'incomplete-context');
  assert.match(result.message, /questions.*jour 7|répond/i);
});

test('refuse la contradiction entre signes cochés et portée aucun signe', () => {
  const signs = { ...input().signs, mold: true };
  const result = analyzeHumidityWeek(input({ signs, scope: 'none' }));
  assert.equal(result.status, 'incomplete-context');
  assert.match(result.message, /contradic/i);
});

test('priorise une moisissure visible déclarée sur plusieurs zones', () => {
  const signs = { ...input().signs, mold: true };
  const result = analyzeHumidityWeek(input({ signs, scope: 'multiple' }));
  assert.equal(result.status, 'complete');
  assert.equal(result.primary.code, 'mold-widespread');
  assert.equal(result.alert.level, 'urgent');
});

test('priorise une moisissure déclarée comme récidivante', () => {
  const signs = { ...input().signs, mold: true, moldRecurring: true };
  const result = analyzeHumidityWeek(input({ signs, scope: 'local' }));
  assert.equal(result.status, 'complete');
  assert.equal(result.primary.code, 'mold-widespread');
  assert.equal(result.alert.level, 'urgent');
});

test('résume réellement les 14 relevés', () => {
  const values = [50, 55, 61, 65, 70, 71, 48, 52, 63, 58, 57, 60, 62, 59];
  const result = analyzeHumidityWeek(input({ readings: week(values) }));
  assert.equal(result.status, 'complete');
  assert.equal(result.summary.countAbove60, 6);
  assert.equal(result.summary.countAtLeast70, 2);
  assert.equal(result.summary.minRh, 48);
  assert.equal(result.summary.maxRh, 71);
  assert.equal(result.summary.averageRh, 59.4);
});

test('reconnaît un suivi rassurant sans proposer d’achat', () => {
  const result = analyzeHumidityWeek(input());
  assert.equal(result.primary.code, 'reassuring');
  assert.match(result.actions.join(' '), /aucun achat/i);
});

test('ne présente pas quatorze relevés à 59 % comme zéro partout', () => {
  const result = analyzeHumidityWeek(input({ readings: week(Array(14).fill(59)) }));
  assert.equal(result.status, 'complete');
  assert.equal(result.summary.countHighComfort, 14);
  assert.equal(result.summary.countAbove60, 0);
  assert.equal(result.primary.code, 'high-comfort-zone');
  assert.match(result.primary.title, /zone haute|surveiller/i);
  assert.match(result.evidence.join(' '), /14 relevés sur 14.*55.*60/i);
  assert.match(result.actions.join(' '), /surveill|ventilation|aération/i);
});

test('distingue des pics liés aux activités d’une humidité persistante', () => {
  const readings = week([51, 52, 50, 66, 52, 53, 50, 68, 51, 52, 49, 65, 50, 51]);
  const contexts = [
    { day: 1, event: 'none' },
    { day: 2, event: 'activity' },
    { day: 3, event: 'none' },
    { day: 4, event: 'activity' },
    { day: 5, event: 'none' },
    { day: 6, event: 'activity' },
    { day: 7, event: 'none' },
  ];
  const result = analyzeHumidityWeek(input({ readings, contexts }));
  assert.equal(result.primary.code, 'activity-peaks');
  assert.ok(result.evidence.some((item) => item.includes('3 relevés')));
});

test('oriente vers air et vapeur quand les dépassements persistent hors activité et que la ventilation est négative', () => {
  const readings = week([65, 66, 64, 67, 68, 69, 65, 66, 64, 67, 71, 70, 66, 68]);
  const result = analyzeHumidityWeek(input({ readings, ventilation: 'no' }));
  assert.equal(result.primary.code, 'air-vapor');
  assert.ok(result.actions.some((item) => /ventilation|extraction|entrée d’air/i.test(item)));
});

test('fait primer un mur mouillé sur les pourcentages rassurants', () => {
  const signs = { ...input().signs, wetWall: true };
  const result = analyzeHumidityWeek(input({ signs, scope: 'local' }));
  assert.equal(result.primary.code, 'water-building');
  assert.equal(result.alert.level, 'urgent');
});

test('signale une humidité locale cachée même avec un air ambiant peu élevé', () => {
  const signs = { ...input().signs, odor: true, mold: true };
  const result = analyzeHumidityWeek(input({ signs, scope: 'local' }));
  assert.equal(result.primary.code, 'hidden-local');
});

test('utilise la température et avertit si elle rend les pourcentages difficiles à comparer', () => {
  const temps = [16, 22, 16, 22, 16, 22, 16, 22, 16, 22, 16, 22, 16, 22];
  const result = analyzeHumidityWeek(input({ readings: week(Array(14).fill(58), temps) }));
  assert.equal(result.summary.temperatureRange, 6);
  assert.match(result.temperatureNote, /6[,.]0 °C|6 °C/);
  assert.match(result.temperatureNote, /prudence|comparer/i);
});

test('une aggravation après pluie produit une piste bâtiment sans inventer une cause certaine', () => {
  const signs = { ...input().signs, blistering: true };
  const result = analyzeHumidityWeek(input({ signs, rainWorse: 'yes', scope: 'local' }));
  assert.equal(result.primary.code, 'water-building');
  assert.match(result.primary.title, /à vérifier/i);
  assert.doesNotMatch(result.primary.title, /cause certaine|diagnostic confirmé/i);
});

test('des pics limités aux jours de pluie ont une utilité dans le compte rendu', () => {
  const readings = week([52, 53, 51, 64, 52, 53, 50, 65, 51, 52, 49, 53, 50, 51]);
  const result = analyzeHumidityWeek(input({
    readings,
    contexts: [1, 2, 3, 4, 5, 6, 7].map((day) => ({ day, event: [2, 4].includes(day) ? 'rain' : 'none' })),
  }));
  assert.equal(result.primary.code, 'weather');
  assert.match(result.evidence.join(' '), /pluie/i);
  assert.match(result.actions.join(' '), /jours? sans pluie|temps sec/i);
});

test('la pièce suivie adapte le contrôle de ventilation proposé', () => {
  const humid = week([64, 65, 66, 67, 65, 66, 64, 65, 66, 67, 65, 66, 64, 65]);
  const bathroom = analyzeHumidityWeek(input({ roomType: 'salle-bain', readings: humid, ventilation: 'no' }));
  const bedroom = analyzeHumidityWeek(input({ roomType: 'chambre', readings: humid, ventilation: 'no' }));
  assert.match(bathroom.actions[0], /extraction/i);
  assert.match(bedroom.actions[0], /entrées? d’air/i);
});

test('conserve à la fois activité et pluie lorsqu’elles surviennent le même jour', () => {
  const readings = week([50, 51, 50, 66, 50, 51, 50, 67, 50, 51, 50, 51, 50, 51]);
  const contexts = [
    { day: 2, events: ['activity', 'rain'] },
    { day: 4, events: ['activity', 'rain'] },
  ];
  const result = analyzeHumidityWeek(input({ readings, contexts }));
  assert.equal(result.status, 'complete');
  assert.ok(result.evidence.some((item) => /activité/i.test(item)));
  assert.ok(result.evidence.some((item) => /pluie/i.test(item)));
});
