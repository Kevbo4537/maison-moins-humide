import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://www.maisonmoinshumide.fr',
  integrations: [sitemap()],
  output: 'static',
});
