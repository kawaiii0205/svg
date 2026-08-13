# ROEM SVG Poster Generator

ROEM 海报与直播考核贴片的独立 SVG 生成仓库。

## 内容

- `scripts/render-posters.py`：从价格表生成价格、玩法和考核 SVG。
- `scripts/export-png.mjs`：将 SVG 导出为 PNG 和 `@2x` PNG，并检查文本边界。
- `data/price-list.xlsx`：生成价格表时使用的数据源。
- `templates/order-notice/`：点单须知 SVG 模板。
- `overlays/live-rules/`：直播考核标准 HTML 贴片及截图脚本。

## 环境

- Python 3.10+
- Node.js 20+
- Chromium 或 Playwright Chromium

## 使用

```bash
npm install
npm run build
```

只生成 SVG：

```bash
npm run generate
```

只导出 PNG：

```bash
npm run export
```

产物写入 `output/`，默认不提交到 Git。

## 当前业务覆盖

- 体验单、陪玩/技术服务、护航单、趣味单价格与规则。
- 赤岩技术猛攻双陪 `178`。
- 八险一金 `388`、倒反天罡 `336`。
- 明星圣尊考核为三取三。
- 点单须知补偿方案使用明确的 `1/2/3` 序号。

本仓库包含业务价格和公开规则。
