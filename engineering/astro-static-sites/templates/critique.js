#!/usr/bin/env node
/**
 * Visual critique capture script for Astro sites.
 *
 * Captures each page at desktop (1440×900) and mobile (390×844) —
 * both above-the-fold and full-page — after triggering all
 * IntersectionObserver animations via scroll simulation.
 *
 * Outputs a JSON manifest at screenshots/critique/manifest.json.
 *
 * Usage:
 *   node scripts/critique.js              — build + capture
 *   node scripts/critique.js --no-build   — skip build, use existing dist/
 *   node scripts/critique.js --open       — open output dir after capture
 */

import { chromium }                      from 'playwright';
import { execSync, spawn }               from 'child_process';
import { mkdirSync, writeFileSync }      from 'fs';
import { resolve, dirname }              from 'path';
import { fileURLToPath }                 from 'url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const OUT  = resolve(ROOT, 'screenshots', 'critique');
const PORT = 4201;

const PAGES = [
  { path: '/',              name: 'home' },
  { path: '/services/',     name: 'services' },
  { path: '/about/',        name: 'about' },
  { path: '/testimonials/', name: 'testimonials' },
  { path: '/contact/',      name: 'contact' },
];

const VIEWPORTS = [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'mobile',  width: 390,  height: 844 },
];

const args  = process.argv.slice(2);
const build = !args.includes('--no-build');
const open  = args.includes('--open');

mkdirSync(OUT, { recursive: true });

if (build) {
  console.log('Building...');
  execSync('npx astro build --silent', { cwd: ROOT, stdio: 'inherit' });
}

console.log(`Starting preview on :${PORT}...`);
const server = spawn('npx', ['astro', 'preview', '--port', String(PORT)], {
  cwd: ROOT, stdio: 'pipe',
});

await new Promise(r => setTimeout(r, 2500));

const browser  = await chromium.launch();
const manifest = { captured_at: new Date().toISOString(), screenshots: [] };
const captured = [];

for (const vp of VIEWPORTS) {
  const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
  const page    = await context.newPage();

  for (const pg of PAGES) {
    const url = `http://localhost:${PORT}${pg.path}`;
    await page.goto(url, { waitUntil: 'networkidle' });

    // Trigger IntersectionObserver animations by scrolling the full page,
    // then return to top so fold capture is correct.
    await page.evaluate(async () => {
      const delay = (ms) => new Promise(r => setTimeout(r, ms));
      const h    = document.body.scrollHeight;
      const step = Math.ceil(h / 10);
      for (let y = 0; y <= h; y += step) { window.scrollTo(0, y); await delay(80); }
      window.scrollTo(0, 0);
      await delay(200);
    });

    const foldFile = resolve(OUT, `${pg.name}--${vp.name}--fold.png`);
    await page.screenshot({ path: foldFile, fullPage: false });

    const fullFile = resolve(OUT, `${pg.name}--${vp.name}--full.png`);
    await page.screenshot({ path: fullFile, fullPage: true });

    manifest.screenshots.push(
      { page: pg.name, viewport: vp.name, type: 'fold', path: foldFile },
      { page: pg.name, viewport: vp.name, type: 'full', path: fullFile },
    );
    captured.push(foldFile, fullFile);
    console.log(`  ✓ ${pg.name.padEnd(14)} ${vp.name.padEnd(8)} fold + full`);
  }

  await context.close();
}

await browser.close();
server.kill();

writeFileSync(resolve(OUT, 'manifest.json'), JSON.stringify(manifest, null, 2));
console.log(`\nDone. ${captured.length} screenshots → screenshots/critique/`);
console.log(`Manifest: screenshots/critique/manifest.json`);
if (open) execSync(`open ${OUT}`, { cwd: ROOT });
