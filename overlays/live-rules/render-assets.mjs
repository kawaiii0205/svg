import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const projectDir = dirname(fileURLToPath(import.meta.url));
const htmlUrl = pathToFileURL(join(projectDir, 'latest-standard.html')).href;
const browser = await chromium.launch({
  headless: true,
  executablePath: '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
});
const errors = [];
await mkdir(projectDir, { recursive: true });

const page = await browser.newPage({ viewport: { width: 384, height: 540 } });
page.on('pageerror', (error) => errors.push(error.message));
await page.goto(`${htmlUrl}?static=1`, { waitUntil: 'load' });
await page.screenshot({
  path: join(projectDir, '最新标准-左侧五分之一-384x540.png'),
  omitBackground: true,
});
await page.close();

const preview = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
preview.on('pageerror', (error) => errors.push(error.message));
await preview.goto(`${htmlUrl}?preview=1`, { waitUntil: 'load' });
await preview.screenshot({
  path: join(projectDir, '最新标准-直播画面预览-1920x1080.png'),
});
await preview.close();
await browser.close();

if (errors.length) throw new Error(errors.join('\n'));
console.log('Exported latest standard overlay assets.');
