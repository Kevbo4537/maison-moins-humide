import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const source = readFileSync(new URL('../src/pages/checklists/humidite-maison/index.astro', import.meta.url), 'utf8');

test('les 14 couples température humidité utilisent la validation native', () => {
  assert.doesNotMatch(source, /<form[^>]*novalidate/);
  const requiredNumbers = source.match(/<input[^>]+type="number"[^>]+required/g) || [];
  assert.equal(requiredNumbers.length, 4, 'les quatre modèles Astro doivent porter required');
});

test('les trois réponses post-J7 ne sont jamais présélectionnées', () => {
  for (const name of ['rainWorse', 'ventilation', 'scope']) {
    assert.match(source, new RegExp(`<select name="${name}" required><option value="">Choisir`));
  }
});

test('une panne localStorage ne bloque pas le bilan', () => {
  assert.match(source, /function saveForm[\s\S]*?try \{[\s\S]*?localStorage\.setItem/);
  assert.match(source, /catch[\s\S]*?Enregistrement local indisponible/);
});

test('le submit focalise le premier champ invalide', () => {
  assert.match(source, /form\.checkValidity\(\)/);
  assert.match(source, /querySelector\(':invalid'\)/);
  assert.match(source, /aria-invalid/);
});
