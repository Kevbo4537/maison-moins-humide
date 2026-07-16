import fs from 'node:fs';
import path from 'node:path';

const dist = path.resolve('dist');
const htmlFiles = [];

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(p);
    else if (entry.name.endsWith('.html')) htmlFiles.push(p);
  }
}

function htmlExistsForHref(href) {
  const clean = href.split('#')[0].split('?')[0];
  if (!clean || clean === '/') return fs.existsSync(path.join(dist, 'index.html'));
  const relative = clean.replace(/^\//, '');
  if (/\.[a-z0-9]+$/i.test(relative)) return fs.existsSync(path.join(dist, relative));
  return fs.existsSync(path.join(dist, relative, 'index.html')) || fs.existsSync(path.join(dist, `${relative}.html`));
}

walk(dist);
let errors = 0;
let warnings = 0;
const knownBrokenLinks = new Set();

for (const file of htmlFiles) {
  const html = fs.readFileSync(file, 'utf8');
  const rel = path.relative(dist, file);
  const title = html.match(/<title>(.*?)<\/title>/i)?.[1]?.trim();
  const desc = html.match(/<meta name="description" content="([^"]+)"/i)?.[1]?.trim();
  const robots = html.match(/<meta name="robots" content="([^"]+)"/i)?.[1]?.trim();
  const canonical = html.match(/<link rel="canonical" href="([^"]+)"/i)?.[1]?.trim();
  const h1s = [...html.matchAll(/<h1[\s>]/gi)].length;
  const bad = [];

  if (!title) bad.push('missing title');
  if (!desc) bad.push('missing meta description');
  if (!robots) bad.push('missing robots meta');
  if (h1s !== 1) bad.push(`h1 count ${h1s}`);
  if (!canonical) bad.push('missing canonical');
  else if (!canonical.startsWith('https://www.maisonmoinshumide.fr/')) bad.push(`non-canonical domain: ${canonical}`);

  for (const match of html.matchAll(/<script type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi)) {
    try {
      JSON.parse(match[1]);
    } catch (error) {
      bad.push(`invalid JSON-LD: ${error.message}`);
    }
  }

  for (const match of html.matchAll(/<a\b[^>]*href="([^"]+)"/gi)) {
    const href = match[1];
    if (!href.startsWith('/') || href.startsWith('//')) continue;
    if (!htmlExistsForHref(href)) knownBrokenLinks.add(`${rel} -> ${href}`);
  }

  if (bad.length) {
    errors++;
    console.log(`${rel}: ${bad.join(', ')}`);
  }

  if (title && title.length > 68) {
    warnings++;
    console.log(`WARN ${rel}: title length ${title.length}`);
  }
  if (desc && (desc.length < 90 || desc.length > 165)) {
    warnings++;
    console.log(`WARN ${rel}: description length ${desc.length}`);
  }
}

for (const broken of [...knownBrokenLinks].sort()) {
  errors++;
  console.log(`BROKEN ${broken}`);
}

console.log(`SEO check: ${htmlFiles.length} HTML pages checked, ${errors} error(s), ${warnings} warning(s).`);
if (errors) process.exit(1);
