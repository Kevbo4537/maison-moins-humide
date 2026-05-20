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
walk(dist);
let errors = 0;
for (const file of htmlFiles) {
  const html = fs.readFileSync(file, 'utf8');
  const rel = path.relative(dist, file);
  const title = html.match(/<title>(.*?)<\/title>/i)?.[1]?.trim();
  const desc = html.match(/<meta name="description" content="([^"]+)"/i)?.[1]?.trim();
  const h1s = [...html.matchAll(/<h1[\s>]/gi)].length;
  const canonical = /<link rel="canonical" href="[^"]+"/i.test(html);
  const bad = [];
  if (!title) bad.push('missing title');
  if (!desc) bad.push('missing meta description');
  if (h1s !== 1) bad.push(`h1 count ${h1s}`);
  if (!canonical) bad.push('missing canonical');
  if (bad.length) { errors++; console.log(`${rel}: ${bad.join(', ')}`); }
}
console.log(`SEO check: ${htmlFiles.length} HTML pages checked, ${errors} page(s) with issues.`);
if (errors) process.exit(1);
