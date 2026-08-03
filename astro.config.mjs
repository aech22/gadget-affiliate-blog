import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// 独自ドメイン確定までは GitHub Pages のプロジェクトURLで配信（Task 8 で独自ドメインへ）。SEO・sitemap・OGP・canonical で使用
export default defineConfig({
  site: 'https://aech22.github.io/gadget-affiliate-blog',
  integrations: [sitemap({ changefreq: 'weekly', priority: 0.7 })],
  vite: {
    plugins: [tailwindcss()],
  },
});
