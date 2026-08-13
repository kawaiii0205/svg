#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { chromium } from "playwright";

const root = path.resolve(import.meta.dirname, "..");
const targets = [
  ["templates/order-notice/roem-order-notice-escort.svg", "output/roem-order-notice-escort"],
  ["templates/order-notice/roem-order-notice-escort-quick.svg", "output/roem-order-notice-escort-quick"],
  ["output/roem-price-experience.svg", "output/roem-price-experience"],
  ["output/roem-price-fun.svg", "output/roem-price-fun"],
  ["output/roem-price-escort.svg", "output/roem-price-escort"],
  ["output/roem-price-companion.svg", "output/roem-price-companion"],
];
const browser = await chromium.launch({ headless: true });

try {
  await fs.mkdir(path.join(root, "output"), { recursive: true });
  for (const [sourcePath, destination] of targets) {
    const svgPath = path.join(root, sourcePath);
    const svgText = await fs.readFile(svgPath, "utf8");
    const sizeMatch = svgText.match(/<svg[^>]*\bwidth="(\d+)"[^>]*\bheight="(\d+)"/);
    if (!sizeMatch) throw new Error(`No SVG dimensions in ${sourcePath}`);
    const width = Number(sizeMatch[1]);
    const height = Number(sizeMatch[2]);

    for (const { scale, suffix } of [
      { scale: 1, suffix: ".png" },
      { scale: 2, suffix: "@2x.png" },
    ]) {
      const context = await browser.newContext({
        viewport: { width, height: 900 },
        deviceScaleFactor: scale,
      });
      const page = await context.newPage();
      const pageErrors = [];
      page.on("pageerror", (error) => pageErrors.push(error.message));
      await page.goto(pathToFileURL(svgPath).href, { waitUntil: "load" });
      const report = await page.locator("svg").evaluate((svg) => {
        const viewBox = svg.viewBox.baseVal;
        const out = [...svg.querySelectorAll("text")].map((el) => {
          const box = el.getBBox();
          return {
            text: el.textContent,
            x: box.x,
            y: box.y,
            right: box.x + box.width,
            bottom: box.y + box.height,
          };
        }).filter((b) =>
          b.x < -0.5 || b.y < -0.5 || b.right > viewBox.width + 0.5 || b.bottom > viewBox.height + 0.5
        );
        return { out };
      });
      const outputPath = path.join(root, `${destination}${suffix}`);
      await page.locator("svg").screenshot({ path: outputPath });
      console.log(`${path.basename(outputPath)}  ${width * scale} x ${height * scale}`);
      for (const item of report.out) {
        console.log(`  OUT-OF-BOUNDS: ${item.text}`);
      }
      if (pageErrors.length) console.log(`  PAGE ERRORS: ${pageErrors.join("; ")}`);
      await context.close();
    }
  }
} finally {
  await browser.close();
}
