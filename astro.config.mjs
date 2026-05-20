import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const isGitHubPages = process.env.GITHUB_PAGES === 'true';

export default defineConfig({
  site: isGitHubPages ? 'https://kevbo4537.github.io' : 'https://www.maisonmoinshumide.fr',
  base: isGitHubPages ? '/maison-moins-humide/' : '/',
  integrations: [sitemap()],
  output: 'static',
});
