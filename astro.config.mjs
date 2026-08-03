import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// 独自ドメイン確定までは GitHub Pages のプロジェクトURLで配信（Task 8 で独自ドメインへ）。
// site=オリジン / base=サブパス。内部リンク・資産は base 前提で解決される。
// 内部リンクは import.meta.env.BASE_URL を使用しているため、独自ドメインのルート配信へ移す際は
// この base 行を消すだけで BASE_URL='/' になり、コード無変更で両対応できる（手戻りゼロ）。
export default defineConfig({
  site: 'https://aech22.github.io',
  base: '/gadget-affiliate-blog/',
  integrations: [sitemap({ changefreq: 'weekly', priority: 0.7 })],
  vite: {
    plugins: [tailwindcss()],
  },
});
