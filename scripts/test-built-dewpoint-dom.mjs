import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import vm from 'node:vm';

const astroDir = 'dist/_astro';
const jsFile = readdirSync(astroDir).find((file) => file.startsWith('hoisted.') && file.endsWith('.js') && readFileSync(join(astroDir, file), 'utf8').includes('dewpoint-form'));
if (!jsFile) throw new Error('Built calculator JS not found. Run npm run build first.');
let code = readFileSync(join(astroDir, jsFile), 'utf8').replace(/^import[^;]+;/, '');

function createHarness(initial = {}) {
  const listeners = new Map();
  const elements = {
    'dewpoint-form': {
      addEventListener(type, fn) { listeners.set(type, fn); },
      dispatchEvent(event) { const fn = listeners.get(event.type); if (fn) fn(event); return true; },
    },
    'dewpoint-result': { className: 'result-card', innerHTML: '' },
    'air-temp': { value: String(initial.airTemp ?? 19) },
    'relative-humidity': { value: String(initial.rh ?? 70) },
    'surface-temp': { value: initial.surfaceTemp === null || initial.surfaceTemp === undefined ? '' : String(initial.surfaceTemp) },
    room: { value: initial.room ?? 'chambre' },
    symptom: { value: initial.symptom ?? 'condensation' },
    frequency: { value: initial.frequency ?? 'matin' },
  };
  const checkedAlerts = initial.alerts ?? [];
  const document = {
    getElementById(id) { return elements[id] ?? null; },
    querySelectorAll(selector) {
      if (selector === 'input[name="alert"]:checked') return checkedAlerts.map((value) => ({ value }));
      return [];
    },
  };
  class Event {
    constructor(type, opts = {}) { this.type = type; this.cancelable = !!opts.cancelable; }
    preventDefault() { this.defaultPrevented = true; }
  }
  const context = { document, Event, Math, Number, console };
  vm.createContext(context);
  vm.runInContext(code, context);
  return elements['dewpoint-result'];
}

function getLabel(html) {
  const match = html.match(/<h2>(.*?)<\/h2>/);
  return match ? match[1] : '';
}

const cases = [
  ['air sec normal', { airTemp: 22, rh: 45, surfaceTemp: 16, room: 'salon', symptom: 'aucun', frequency: 'ponctuel' }, 'Risque faible'],
  ['chambre condensation calculée', { airTemp: 19, rh: 70, surfaceTemp: 13, room: 'chambre', symptom: 'condensation', frequency: 'matin' }, 'Risque élevé de condensation'],
  ['surface humide sans gouttes', { airTemp: 20, rh: 60, surfaceTemp: 15, room: 'salon', symptom: 'aucun', frequency: 'ponctuel' }, 'Conditions favorables aux moisissures'],
  ['cave fraîche humide', { airTemp: 10, rh: 80, surfaceTemp: 8, room: 'cave', symptom: 'odeur', frequency: 'souvent' }, 'Risque élevé de condensation'],
  ['RH haute sans surface', { airTemp: 19, rh: 72, surfaceTemp: null, room: 'chambre', symptom: 'aucun', frequency: 'souvent' }, 'Humidité intérieure élevée'],
  ['vitre embuée sans surface', { airTemp: 20, rh: 55, surfaceTemp: null, room: 'chambre', symptom: 'condensation', frequency: 'matin' }, 'Risque élevé de condensation'],
  ['moisissure visible valeurs basses', { airTemp: 21, rh: 45, surfaceTemp: null, room: 'chambre', symptom: 'moisissure', frequency: 'souvent' }, 'Conditions favorables aux moisissures'],
  ['odeur persistante valeurs basses', { airTemp: 20, rh: 50, surfaceTemp: null, room: 'placard', symptom: 'odeur', frequency: 'permanent' }, 'Conditions favorables aux moisissures'],
  ['linge sèche mal à 65%', { airTemp: 19, rh: 65, surfaceTemp: null, room: 'buanderie', symptom: 'linge', frequency: 'ponctuel' }, 'Humidité intérieure élevée'],
  ['salpêtre prioritaire', { airTemp: 20, rh: 45, surfaceTemp: 18, room: 'cave', symptom: 'salpetre', frequency: 'ponctuel' }, 'Signal d’alerte technique'],
  ['alerte checkbox prioritaire', { airTemp: 22, rh: 40, surfaceTemp: 20, room: 'salon', symptom: 'aucun', frequency: 'ponctuel', alerts: ['fuite'] }, 'Signal d’alerte technique'],
];

let failures = 0;
for (const [name, input, expected] of cases) {
  const result = createHarness(input);
  const label = getLabel(result.innerHTML);
  const ok = label.includes(expected);
  console.log(`${ok ? 'OK' : 'FAIL'} ${name}: ${label}`);
  if (!ok) failures += 1;
  if (!result.innerHTML.includes('Point de rosée') || !result.innerHTML.includes('Actions prioritaires')) {
    console.log(`FAIL ${name}: missing metrics/actions block`);
    failures += 1;
  }
}
if (failures) process.exit(1);
console.log(`Built DOM calculator tests passed: ${cases.length} cases on ${jsFile}`);
