#!/usr/bin/env python3
from html import escape
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"
PRICE_BOOK = ROOT / "data" / "price-list.xlsx"
FONT = "'PingFang SC','Hiragino Sans GB','STHeiti','Microsoft YaHei',sans-serif"
SERIF = "'Songti SC','STSong','SimSun',serif"

THEMES = {
    "light-cute": {
        "club": "#f087a7",
        "title": "#ffb742",
        "subtitle": "#ff8b3d",
        "title_stroke": "#ffffff",
        "pill": "#ff8840",
        "pill_text": "#ffffff",
        "accent": "#ff8840",
        "table_border": "#62c4dc",
        "table_fill": "#ffffff",
        "table_fill_opacity": 0.42,
        "text": "#202124",
        "muted": "#333333",
        "badge_outer": "#ffe5c9",
        "badge_inner": "#ffffff",
        "badge_mark": "#78cde4",
        "footer_border": "#ffb16a",
        "shadow_color": "#e8792d",
        "gradients": {
            "base": ["#fff0cc", "#fffaf0", "#fff7ed", "#dff6ff"],
            "warm": ("0.05", "0.05", "0.8", "#ffb35f", "0.35"),
            "blue": ("1", "0.1", "0.7", "#93dfff", "0.55"),
            "pink": ("0", "1", "0.75", "#ff8fb4", "0.4"),
        },
    },
    "light-roem": {
        "club": "#df716e",
        "title": "#ff9f31",
        "subtitle": "#e95635",
        "title_stroke": "#ffffff",
        "pill": "#f06b32",
        "pill_text": "#ffffff",
        "accent": "#f06b32",
        "table_border": "#f4a166",
        "table_fill": "#fffaf3",
        "table_fill_opacity": 0.58,
        "text": "#241b18",
        "muted": "#3a2b26",
        "badge_outer": "#ffe0c2",
        "badge_inner": "#fff9f1",
        "badge_mark": "#ff9b42",
        "footer_border": "#f06b32",
        "shadow_color": "#d4542f",
        "gradients": {
            "base": ["#fff2dd", "#fff8ed", "#fff1e8", "#ffe0d0"],
            "warm": ("0.08", "0.06", "0.78", "#ff9445", "0.34"),
            "blue": ("1", "0.14", "0.68", "#ffd2a3", "0.36"),
            "pink": ("0", "1", "0.75", "#ff775c", "0.22"),
        },
    },
    "dark-esport": {
        "club": "#ff9a68",
        "title": "#ff7a35",
        "subtitle": "#ffd19a",
        "title_stroke": "#32120b",
        "pill": "#ff6a2f",
        "pill_text": "#fff8ef",
        "accent": "#ff8a3d",
        "table_border": "#ff8a3d",
        "table_fill": "#160d0b",
        "table_fill_opacity": 0.68,
        "text": "#fff1df",
        "muted": "#f5d5c0",
        "badge_outer": "#35140d",
        "badge_inner": "#1b0d0a",
        "badge_mark": "#ffb15c",
        "footer_border": "#ff8a3d",
        "shadow_color": "#ff4d1f",
        "gradients": {
            "base": ["#160705", "#21100b", "#120806", "#050405"],
            "warm": ("0.08", "0.05", "0.8", "#ff5b2e", "0.4"),
            "blue": ("1", "0.1", "0.7", "#ffb15c", "0.13"),
            "pink": ("0", "1", "0.8", "#9c1c15", "0.32"),
        },
    },
}


def e(value):
    return escape(str(value), quote=True)


class Svg:
    def __init__(self, width, height, theme):
        self.width = width
        self.height = height
        self.theme = theme
        self.items = []

    def add(self, raw):
        self.items.append(raw)

    def rect(
        self,
        x,
        y,
        w,
        h,
        rx=0,
        fill="none",
        stroke="none",
        sw=1,
        dash=None,
        opacity=None,
        fill_opacity=None,
        stroke_opacity=None,
    ):
        attrs = [
            f'x="{x}"',
            f'y="{y}"',
            f'width="{w}"',
            f'height="{h}"',
            f'rx="{rx}"',
            f'fill="{fill}"',
            f'stroke="{stroke}"',
            f'stroke-width="{sw}"',
        ]
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if fill_opacity is not None:
            attrs.append(f'fill-opacity="{fill_opacity}"')
        if stroke_opacity is not None:
            attrs.append(f'stroke-opacity="{stroke_opacity}"')
        self.add(f"<rect {' '.join(attrs)} />")

    def line(self, x1, y1, x2, y2, stroke="#000", sw=1, dash=None, opacity=None):
        attrs = [
            f'x1="{x1}"',
            f'y1="{y1}"',
            f'x2="{x2}"',
            f'y2="{y2}"',
            f'stroke="{stroke}"',
            f'stroke-width="{sw}"',
        ]
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f"<line {' '.join(attrs)} />")

    def circle(self, cx, cy, r, fill, opacity=None, stroke=None, sw=1):
        attrs = [f'cx="{cx}"', f'cy="{cy}"', f'r="{r}"', f'fill="{fill}"']
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if stroke:
            attrs.append(f'stroke="{stroke}"')
            attrs.append(f'stroke-width="{sw}"')
        self.add(f"<circle {' '.join(attrs)} />")

    def text(
        self,
        x,
        y,
        text,
        size=32,
        fill=None,
        weight=400,
        anchor="start",
        family=FONT,
        stroke=None,
        sw=0,
        italic=False,
        opacity=None,
    ):
        fill = fill or self.theme["text"]
        style = f"font-family:{family};font-size:{size}px;font-weight:{weight};"
        if italic:
            style += "font-style:italic;"
        attrs = [
            f'x="{x}"',
            f'y="{y}"',
            f'fill="{fill}"',
            f'text-anchor="{anchor}"',
            f'style="{style}"',
        ]
        if stroke:
            attrs.append(f'stroke="{stroke}"')
            attrs.append(f'stroke-width="{sw}"')
            attrs.append('paint-order="stroke fill"')
            attrs.append('stroke-linejoin="round"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f"<text {' '.join(attrs)}>{e(text)}</text>")

    def pill(self, x, y, label, width=None, height=58, fill=None, color=None, size=34):
        fill = fill or self.theme["pill"]
        color = color or self.theme["pill_text"]
        text_width = len(label) * size * 0.9
        w = width or int(text_width + 54)
        self.rect(x, y, w, height, rx=height // 2, fill=fill, stroke="none")
        self.text(x + w / 2, y + height - 17, label, size=size, fill=color, weight=900, anchor="middle")
        arrow_x = x + w + 18
        for i in range(5):
            self.text(arrow_x + i * 30, y + height - 16, "›", size=58, fill=self.theme["accent"], weight=900)
        return w + 185

    def table(self, x, y, col_widths, rows, row_h=64, header=True, font_size=31):
        w = sum(col_widths)
        h = row_h * len(rows)
        border = self.theme["table_border"]
        self.rect(
            x,
            y,
            w,
            h,
            rx=0,
            fill=self.theme["table_fill"],
            stroke=border,
            sw=2,
            dash="2 4",
            fill_opacity=self.theme["table_fill_opacity"],
        )
        current = x
        for width in col_widths[:-1]:
            current += width
            self.line(current, y, current, y + h, stroke=border, sw=2, dash="2 4")
        for index in range(1, len(rows)):
            yy = y + row_h * index
            self.line(x, yy, x + w, yy, stroke=border, sw=2, dash="2 4")
        for r, row in enumerate(rows):
            current_x = x
            for c, cell in enumerate(row):
                cx = current_x + col_widths[c] / 2
                cy = y + row_h * r + row_h / 2 + font_size / 2 - 7
                is_head = header and r == 0
                self.text(
                    cx,
                    cy,
                    cell,
                    size=font_size,
                    fill=self.theme["text"],
                    weight=900 if is_head or c == 0 else 500,
                    anchor="middle",
                    family=SERIF if not is_head else FONT,
                )
                current_x += col_widths[c]
        return y + h


def add_background(svg, width, height):
    theme = svg.theme
    base = theme["gradients"]["base"]
    warm = theme["gradients"]["warm"]
    blue = theme["gradients"]["blue"]
    pink = theme["gradients"]["pink"]

    svg.add(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{base[0]}"/>
    <stop offset="42%" stop-color="{base[1]}"/>
    <stop offset="72%" stop-color="{base[2]}"/>
    <stop offset="100%" stop-color="{base[3]}"/>
  </linearGradient>
  <radialGradient id="warm" cx="{warm[0]}" cy="{warm[1]}" r="{warm[2]}">
    <stop offset="0%" stop-color="{warm[3]}" stop-opacity="{warm[4]}"/>
    <stop offset="100%" stop-color="{warm[3]}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="blue" cx="{blue[0]}" cy="{blue[1]}" r="{blue[2]}">
    <stop offset="0%" stop-color="{blue[3]}" stop-opacity="{blue[4]}"/>
    <stop offset="100%" stop-color="{blue[3]}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="pink" cx="{pink[0]}" cy="{pink[1]}" r="{pink[2]}">
    <stop offset="0%" stop-color="{pink[3]}" stop-opacity="{pink[4]}"/>
    <stop offset="100%" stop-color="{pink[3]}" stop-opacity="0"/>
  </radialGradient>
  <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="{theme["shadow_color"]}" flood-opacity="0.18"/>
  </filter>
</defs>''')
    svg.rect(0, 0, width, height, fill="url(#bg)")
    svg.rect(0, 0, width, height, fill="url(#warm)")
    svg.rect(0, 0, width, height, fill="url(#blue)")
    svg.rect(0, 0, width, height, fill="url(#pink)")

    particle = "#ffffff" if theme["title_stroke"] == "#ffffff" else theme["accent"]
    particle_opacity = 0.28 if theme["title_stroke"] == "#ffffff" else 0.18
    for i in range(70):
        cx = (i * 157) % width
        cy = (i * 293) % height
        svg.circle(cx, cy, 1.2 + (i % 3), particle, opacity=particle_opacity)


def render_price_total(theme_key):
    theme = THEMES[theme_key]
    width = 1080
    height = 5000
    svg = Svg(width, height, theme)

    add_background(svg, width, height)

    svg.text(
        540,
        86,
        "RYMO Gaming Club",
        size=56,
        fill=theme["club"],
        weight=400,
        anchor="middle",
        family="'Snell Roundhand','Apple Chancery',cursive",
        italic=True,
    )
    svg.text(88, 205, "RYMO岩灼电竞", size=88, fill=theme["title"], weight=900, stroke=theme["title_stroke"], sw=12)
    svg.text(232, 322, "三角洲价目表", size=72, fill=theme["subtitle"], weight=900, stroke=theme["title_stroke"], sw=10)

    svg.add('<g filter="url(#softShadow)">')
    svg.circle(878, 198, 132, theme["badge_outer"])
    svg.circle(878, 198, 102, theme["badge_inner"], opacity=0.72, stroke=theme["footer_border"], sw=2)
    svg.text(878, 176, "RYMO", size=38, fill=theme["accent"], weight=900, anchor="middle")
    svg.text(878, 230, "△", size=76, fill=theme["badge_mark"], weight=900, anchor="middle")
    svg.add("</g>")

    x = 72
    y = 430

    svg.pill(x, y, "超值体验", width=190)
    y += 92
    y = svg.table(
        x,
        y,
        [330, 230, 330],
        [
            ["服务", "价格", "内容"],
            ["128元保688W", "128钻石", "2名陪玩"],
            ["258元保1288W", "258钻石", "2名陪玩"],
        ],
        row_h=68,
        font_size=32,
    ) + 60

    svg.pill(x, y, "娱乐陪玩", width=190)
    y += 92
    y = svg.table(
        x,
        y,
        [250, 320, 320],
        [
            ["分类", "1p1", "1p2"],
            ["女陪", "60钻石/小时", "70钻石/小时"],
            ["男陪", "50钻石/小时", "60钻石/小时"],
            ["娱乐Pro", "80钻石/小时", "90钻石/小时"],
        ],
        row_h=68,
        font_size=31,
    ) + 42
    svg.text(x + 8, y, "✦", size=45, fill=theme["accent"], weight=900)
    svg.text(x + 62, y - 6, "甜蜜陪模式、指定地图等后续以具体服务规格展示", size=30, fill=theme["muted"], weight=500)
    y += 70

    svg.pill(x, y, "陪跑任务", width=190)
    y += 92
    y = svg.table(
        x,
        y,
        [300, 295, 295],
        [
            ["地图", "1p1", "1p2"],
            ["常规图", "20钻石/小时", "30钻石/小时"],
            ["机密图", "30钻石/小时", "40钻石/小时"],
            ["绝密图", "60钻石/小时", "70钻石/小时"],
            ["9格培培", "60钻石/小时", "-"],
        ],
        row_h=66,
        font_size=30,
    ) + 42
    svg.text(x + 8, y, "✦", size=45, fill=theme["accent"], weight=900)
    svg.text(x + 62, y - 6, "推进任务为主，无需全装，不接受人头或撤离率投诉", size=30, fill=theme["muted"], weight=500)
    y += 78

    svg.pill(x, y, "技术教学", width=190)
    y += 86
    svg.text(x + 28, y, "✦", size=45, fill=theme["accent"], weight=900)
    svg.text(x + 90, y - 5, "1v1教学1p1", size=36, fill=theme["text"], weight=900, family=SERIF)
    svg.text(x + 350, y - 5, "80钻石/小时", size=36, fill=theme["accent"], weight=900)
    svg.text(x + 28, y + 58, "✦", size=45, fill=theme["accent"], weight=900)
    svg.text(x + 90, y + 53, "1v1教学1p2", size=36, fill=theme["text"], weight=900, family=SERIF)
    svg.text(x + 350, y + 53, "90钻石/小时", size=36, fill=theme["accent"], weight=900)
    svg.text(x + 28, y + 116, "✦", size=45, fill=theme["accent"], weight=900)
    svg.text(x + 90, y + 111, "60分钟，赤岩及以上选手指导，不接受撤离率投诉", size=30, fill=theme["muted"], weight=500)
    y += 186

    svg.pill(x, y, "技术猛攻", width=190)
    y += 92
    y = svg.table(
        x,
        y,
        [285, 200, 200, 205],
        [
            ["服务", "赤岩", "灼曜", "圣尊"],
            ["单陪1p1", "88", "118", "148"],
            ["单陪1p2", "98", "128", "158"],
            ["双陪2p1", "168", "228", "288"],
        ],
        row_h=66,
        font_size=30,
    ) + 60

    svg.pill(x, y, "物资护航", width=190)
    y += 92
    y = svg.table(
        x,
        y,
        [285, 200, 200, 205],
        [
            ["服务", "赤岩", "灼曜", "圣尊"],
            ["单陪1p1", "118", "138", "168"],
            ["单陪1p2", "128", "148", "178"],
            ["双陪2p1", "228", "278", "338"],
        ],
        row_h=66,
        font_size=30,
    ) + 60

    svg.pill(x, y, "保底清图", width=190)
    y += 92
    y = svg.table(
        x,
        y,
        [185, 205, 250, 250],
        [
            ["分类", "档位", "价格", "保底"],
            ["绝密", "168档", "168", "688W"],
            ["绝密", "288档", "288", "1288W"],
            ["绝密", "688档", "688", "3088W"],
            ["绝密", "1088档", "1088", "5088W"],
            ["机密", "88档", "88", "388W"],
            ["机密", "168档", "168", "888W"],
            ["机密", "268档", "268", "1388W"],
        ],
        row_h=62,
        font_size=28,
    ) + 42
    svg.text(x + 8, y, "✦", size=45, fill=theme["accent"], weight=900)
    svg.text(x + 62, y - 6, "红修、装备、红弹不算红；百万级=大红，两百万级=超大红", size=28, fill=theme["muted"], weight=500)
    y += 78

    svg.pill(x, y, "极速清图", width=190)
    y += 92
    y = svg.table(
        x,
        y,
        [210, 210, 230, 240],
        [
            ["服务", "价格", "保底", "说明"],
            ["15分钟", "338", "1188W", "可丢包撤"],
            ["10分钟", "788", "2688W", "可丢包撤"],
            ["7分钟", "1588", "4888W", "禁止撤离"],
        ],
        row_h=66,
        font_size=29,
    ) + 60

    svg.pill(x, y, "爆款趣味", width=190)
    y += 92
    y = svg.table(
        x,
        y,
        [300, 190, 400],
        [
            ["玩法", "价格", "说明"],
            ["小小巨人", "128起", "血量制，2名陪玩"],
            ["小巨人无上限", "888起", "血量无上限"],
            ["三宗罪自选", "588", "保底2388W"],
            ["七宗罪全通", "1188", "保底4288W"],
        ],
        row_h=66,
        font_size=29,
    ) + 72

    svg.rect(
        72,
        y,
        936,
        112,
        rx=30,
        fill=theme["table_fill"],
        fill_opacity=0.52,
        stroke=theme["footer_border"],
        sw=2,
    )
    svg.text(104, y + 45, "说明", size=31, fill=theme["accent"], weight=900)
    svg.text(200, y + 45, "1p1=1名陪玩服务1名老板｜1p2=1名陪玩服务2名老板", size=27, fill=theme["muted"], weight=500)
    svg.text(200, y + 86, "2p1=2名陪玩服务1名老板｜价格以小程序下单页为准", size=27, fill=theme["muted"], weight=500)

    svg.text(88, height - 82, "未成年禁止消费", size=26, fill=theme["muted"], weight=700)
    svg.text(width / 2, height - 82, "微信搜一搜 RYMO岩灼电竞", size=26, fill=theme["muted"], weight=700, anchor="middle")
    svg.text(width - 88, height - 82, "东东电竞搜 RYMO岩灼电竞", size=26, fill=theme["muted"], weight=700, anchor="end")

    svg.add("</svg>")
    return "\n".join(svg.items)


def render_tech_loot_polished():
    width = 1080
    height = 4200
    items = []

    def add(raw):
        items.append(raw)

    def rect(x, y, w, h, rx=0, fill="none", stroke="none", sw=1, fill_opacity=None, opacity=None, dash=None, filter_id=None):
        attrs = [
            f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"', f'rx="{rx}"',
            f'fill="{fill}"', f'stroke="{stroke}"', f'stroke-width="{sw}"'
        ]
        if fill_opacity is not None:
            attrs.append(f'fill-opacity="{fill_opacity}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if filter_id:
            attrs.append(f'filter="url(#{filter_id})"')
        add(f"<rect {' '.join(attrs)} />")

    def line(x1, y1, x2, y2, stroke="#ff8a3d", sw=2, opacity=None, dash=None):
        attrs = [f'x1="{x1}"', f'y1="{y1}"', f'x2="{x2}"', f'y2="{y2}"', f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        add(f"<line {' '.join(attrs)} />")

    def circle(cx, cy, r, fill, opacity=None):
        attrs = [f'cx="{cx}"', f'cy="{cy}"', f'r="{r}"', f'fill="{fill}"']
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        add(f"<circle {' '.join(attrs)} />")

    def path(d, stroke="#ff8a3d", sw=2, opacity=None):
        attrs = [f'd="{d}"', 'fill="none"', f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        add(f"<path {' '.join(attrs)} />")

    def text(x, y, value, size=32, fill="#fff1df", weight=400, anchor="start", family=FONT, stroke=None, sw=0):
        attrs = [
            f'x="{x}"', f'y="{y}"', f'fill="{fill}"', f'text-anchor="{anchor}"',
            f'style="font-family:{family};font-size:{size}px;font-weight:{weight};"'
        ]
        if stroke:
            attrs += [f'stroke="{stroke}"', f'stroke-width="{sw}"', 'paint-order="stroke fill"', 'stroke-linejoin="round"']
        add(f"<text {' '.join(attrs)}>{e(value)}</text>")

    def chip(x, y, label, w=None):
        w = w or max(124, len(label) * 27 + 42)
        rect(x, y, w, 48, 24, fill="#1d0f0b", stroke="#ff8a3d", sw=1.5, fill_opacity=0.82)
        text(x + w / 2, y + 33, label, 24, "#ffd19a", 800, "middle")
        return w

    def section_title(x, y, title, sub=None):
        rect(x, y, 920, 74, 28, fill="#1b0c08", stroke="url(#strokeGold)", sw=2, fill_opacity=0.86, filter_id="cardShadow")
        rect(x + 16, y + 14, 9, 46, 5, fill="url(#accentGrad)", stroke="none")
        text(x + 42, y + 49, title, 34, "#ffd19a", 900)
        if sub:
            text(x + 892, y + 47, sub, 23, "#d9ad8e", 700, "end")

    def table(x, y, col_widths, rows, row_height=74):
        total_width = sum(col_widths)
        total_height = row_height * len(rows)
        rect(x, y, total_width, total_height, 24, fill="#120806", stroke="url(#strokeGold)", sw=2, fill_opacity=0.76, filter_id="cardShadow")
        rect(x, y, total_width, row_height, 24, fill="#251008", stroke="none", fill_opacity=0.9)
        rect(x, y + row_height - 24, total_width, 24, 0, fill="#251008", stroke="none", fill_opacity=0.9)
        current_x = x
        for col_width in col_widths[:-1]:
            current_x += col_width
            line(current_x, y, current_x, y + total_height, "#ff8a3d", 1.6, 0.72, "5 7")
        for row_index in range(1, len(rows)):
            line(x, y + row_index * row_height, x + total_width, y + row_index * row_height, "#ff8a3d", 1.6, 0.72, "5 7")
        for row_index, row in enumerate(rows):
            current_x = x
            for col_index, cell in enumerate(row):
                is_header = row_index == 0
                is_price = row_index > 0 and col_index > 0
                fill = "#ffd19a" if is_header or is_price else "#fff1df"
                weight = 900 if is_header or col_index == 0 else 750
                size = 29 if len(cell) <= 8 else 26
                family = SERIF if row_index > 0 else FONT
                text(current_x + col_widths[col_index] / 2, y + row_index * row_height + 46, cell, size, fill, weight, "middle", family)
                current_x += col_widths[col_index]
        return y + total_height

    def rule_card(x, y, title, lines, tag):
        card_height = 116 + 44 * len(lines)
        rect(x, y, 920, card_height, 30, fill="#120806", stroke="url(#strokeGold)", sw=2, fill_opacity=0.78, filter_id="cardShadow")
        rect(x, y, 920, 78, 30, fill="#24100a", stroke="none", fill_opacity=0.94)
        rect(x, y + 52, 920, 26, 0, fill="#24100a", stroke="none", fill_opacity=0.94)
        chip(x + 28, y + 17, tag, 108)
        text(x + 154, y + 51, title, 32, "#ffd19a", 900)
        yy = y + 112
        for line_text in lines:
            circle(x + 42, yy - 10, 6, "#ff8a3d")
            text(x + 66, yy, line_text, 28, "#fff1df", 650)
            yy += 44
        return y + card_height

    add(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#130504"/>
    <stop offset="38%" stop-color="#21100a"/>
    <stop offset="72%" stop-color="#100806"/>
    <stop offset="100%" stop-color="#050304"/>
  </linearGradient>
  <radialGradient id="heroGlow" cx="0.18" cy="0.03" r="0.72">
    <stop offset="0%" stop-color="#ff6733" stop-opacity="0.52"/>
    <stop offset="100%" stop-color="#ff6733" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="sideGlow" cx="1" cy="0.22" r="0.78">
    <stop offset="0%" stop-color="#ffb15c" stop-opacity="0.22"/>
    <stop offset="100%" stop-color="#ffb15c" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="bottomGlow" cx="0" cy="1" r="0.9">
    <stop offset="0%" stop-color="#8f1c13" stop-opacity="0.42"/>
    <stop offset="100%" stop-color="#8f1c13" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ff5b2e"/>
    <stop offset="100%" stop-color="#ffbc69"/>
  </linearGradient>
  <linearGradient id="strokeGold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ff6a2f"/>
    <stop offset="55%" stop-color="#ffb15c"/>
    <stop offset="100%" stop-color="#7a2b1c"/>
  </linearGradient>
  <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="130%">
    <feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#000000" flood-opacity="0.32"/>
    <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#ff5b2e" flood-opacity="0.08"/>
  </filter>
</defs>''')

    rect(0, 0, width, height, fill="url(#bg)")
    rect(0, 0, width, height, fill="url(#heroGlow)")
    rect(0, 0, width, height, fill="url(#sideGlow)")
    rect(0, 0, width, height, fill="url(#bottomGlow)")
    for index in range(18):
        line(70 + index * 62, 360, 70 + index * 62 - 250, 4000, "#ff8a3d", 1, 0.035)
    for index in range(80):
        circle((index * 151 + 29) % width, (index * 277 + 61) % height, 1.2 + (index % 3), "#ffb15c", 0.13)
    path("M-80 520 C240 420 350 620 620 500 C820 410 940 360 1160 430", "#ff8a3d", 3, 0.11)
    path("M-80 3580 C220 3440 420 3660 720 3500 C900 3405 1010 3370 1160 3430", "#ff8a3d", 3, 0.09)

    text(82, 154, "RYMO岩灼电竞", 76, "#8d6640", 900, family=SERIF)
    text(80, 150, "RYMO岩灼电竞", 76, "#ffcf8c", 900, family=SERIF)
    text(80, 250, "技术猛攻 / 物资护航", 62, "#ffd19a", 900, stroke="#2a0d08", sw=8)
    text(84, 315, "赤岩｜灼曜｜圣尊 三档实力分层", 30, "#f5d5c0", 750)
    chip(84, 346, "价格单位：钻石/小时", 260)
    chip(366, 346, "下单页价格为准", 210)

    x = 80
    y = 455
    section_title(x, y, "技术猛攻价目表", "ATTACK SERVICE")
    y += 98
    y = table(x, y, [330, 185, 185, 220], [
        ["服务规格", "赤岩", "灼曜", "圣尊"],
        ["猛攻单陪1p1", "88", "118", "148"],
        ["猛攻单陪1p2", "98", "128", "158"],
        ["猛攻双陪2p1", "168", "228", "288"],
    ], 76) + 70

    section_title(x, y, "物资护航价目表", "LOOT ESCORT")
    y += 98
    y = table(x, y, [330, 185, 185, 220], [
        ["服务规格", "赤岩", "灼曜", "圣尊"],
        ["物资单陪1p1", "118", "138", "168"],
        ["物资单陪1p2", "128", "148", "178"],
        ["物资双陪2p1", "228", "278", "338"],
    ], 76) + 78

    rules = [
        ("单陪猛攻达标规则", "猛攻", ["灼曜猛攻：每小时击败数 ≥ 8人", "圣尊猛攻：每小时击败数 ≥ 10人", "只计算全队3人及以上击败", "无撤离率要求", "跨地图或跨段位按较低标准执行", "猛攻单不提供战备损失补偿"]),
        ("双陪猛攻达标规则", "双陪", ["赤岩双陪：每小时击败数 ≥ 11人", "灼曜双陪：每小时击败数 ≥ 13人", "圣尊双陪：每小时击败数 ≥ 16人", "赤岩按全队3人及以上击败计算", "灼曜、圣尊按全队4人及以上击败计算", "未达标时，该局击败不计入"]),
        ("单陪物资达标规则", "物资", ["灼曜物资：每小时撤离金额 ≥ 600W", "圣尊物资：每小时撤离金额 ≥ 800W", "物资单陪包6张物资卡", "地图红卡必须带齐，其他金卡补齐至6张"]),
        ("双陪物资达标规则", "双陪", ["赤岩双陪物资：每小时撤离金额 ≥ 900W", "灼曜双陪物资：每小时撤离金额 ≥ 1200W", "圣尊双陪物资：每小时撤离金额 ≥ 1400W", "物资双陪包全部物资卡", "撤离失败补偿：航天中心+60W，巴克什+60W，监狱+80W"]),
        ("通用说明", "说明", ["1p1 = 1名陪玩服务1名老板", "1p2 = 1名陪玩服务2名老板", "2p1 = 2名陪玩服务1名老板", "1p2场景下，老板产出合计计算", "1p2技术击败要求每小时减2人", "让头可计入护航击败", "老板需听从打手指挥", "恶意影响服务，平台有权结单"]),
    ]
    for title, tag, lines in rules:
        y = rule_card(x, y, title, lines, tag) + 50

    rect(80, height - 272, 920, 142, 30, fill="#120806", stroke="url(#strokeGold)", sw=2, fill_opacity=0.82, filter_id="cardShadow")
    text(118, height - 218, "具体服务标准以下单页与客服确认为准", 30, "#ffd19a", 900)
    text(118, height - 172, "东东电竞搜 RYMO岩灼电竞｜未成年禁止消费", 27, "#f5d5c0", 700)
    add("</svg>")
    return "\n".join(items)


def render_little_giant_polished():
    width = 1080
    height = 4000
    items = []

    def add(raw):
        items.append(raw)

    def rect(x, y, w, h, rx=0, fill="none", stroke="none", sw=1, fill_opacity=None, opacity=None, dash=None, filter_id=None):
        attrs = [
            f'x="{x}"',
            f'y="{y}"',
            f'width="{w}"',
            f'height="{h}"',
            f'rx="{rx}"',
            f'fill="{fill}"',
            f'stroke="{stroke}"',
            f'stroke-width="{sw}"',
        ]
        if fill_opacity is not None:
            attrs.append(f'fill-opacity="{fill_opacity}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if filter_id:
            attrs.append(f'filter="url(#{filter_id})"')
        add(f"<rect {' '.join(attrs)} />")

    def line(x1, y1, x2, y2, stroke="#ff8a3d", sw=2, opacity=None, dash=None):
        attrs = [
            f'x1="{x1}"',
            f'y1="{y1}"',
            f'x2="{x2}"',
            f'y2="{y2}"',
            f'stroke="{stroke}"',
            f'stroke-width="{sw}"',
        ]
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        add(f"<line {' '.join(attrs)} />")

    def circle(cx, cy, r, fill, opacity=None):
        attrs = [f'cx="{cx}"', f'cy="{cy}"', f'r="{r}"', f'fill="{fill}"']
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        add(f"<circle {' '.join(attrs)} />")

    def path(d, stroke="#ff8a3d", sw=2, opacity=None):
        attrs = [f'd="{d}"', 'fill="none"', f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        add(f"<path {' '.join(attrs)} />")

    def text(x, y, value, size=32, fill="#fff1df", weight=400, anchor="start", family=FONT, stroke=None, sw=0):
        attrs = [
            f'x="{x}"',
            f'y="{y}"',
            f'fill="{fill}"',
            f'text-anchor="{anchor}"',
            f'style="font-family:{family};font-size:{size}px;font-weight:{weight};"',
        ]
        if stroke:
            attrs += [f'stroke="{stroke}"', f'stroke-width="{sw}"', 'paint-order="stroke fill"', 'stroke-linejoin="round"']
        add(f"<text {' '.join(attrs)}>{e(value)}</text>")

    def chip(x, y, label, w=None):
        w = w or max(124, len(label) * 27 + 42)
        rect(x, y, w, 48, 24, fill="#1d0f0b", stroke="#ff8a3d", sw=1.5, fill_opacity=0.82)
        text(x + w / 2, y + 33, label, 24, "#ffd19a", 800, "middle")
        return w

    def section_title(x, y, title, sub=None):
        rect(x, y, 920, 74, 28, fill="#1b0c08", stroke="url(#strokeGold)", sw=2, fill_opacity=0.86, filter_id="cardShadow")
        rect(x + 16, y + 14, 9, 46, 5, fill="url(#accentGrad)", stroke="none")
        text(x + 42, y + 49, title, 34, "#ffd19a", 900)
        if sub:
            text(x + 892, y + 47, sub, 23, "#d9ad8e", 700, "end")

    def table(x, y, col_widths, rows, row_height=74, font_size=29):
        total_width = sum(col_widths)
        total_height = row_height * len(rows)
        rect(x, y, total_width, total_height, 24, fill="#120806", stroke="url(#strokeGold)", sw=2, fill_opacity=0.76, filter_id="cardShadow")
        rect(x, y, total_width, row_height, 24, fill="#251008", stroke="none", fill_opacity=0.9)
        rect(x, y + row_height - 24, total_width, 24, 0, fill="#251008", stroke="none", fill_opacity=0.9)
        current_x = x
        for col_width in col_widths[:-1]:
            current_x += col_width
            line(current_x, y, current_x, y + total_height, "#ff8a3d", 1.6, 0.72, "5 7")
        for row_index in range(1, len(rows)):
            line(x, y + row_index * row_height, x + total_width, y + row_index * row_height, "#ff8a3d", 1.6, 0.72, "5 7")
        for row_index, row in enumerate(rows):
            current_x = x
            for col_index, cell in enumerate(row):
                is_header = row_index == 0
                is_label = row_index > 0 and col_index == 0
                fill = "#ffd19a" if is_header or is_label else "#fff1df"
                weight = 900 if is_header or col_index == 0 else 750
                size = font_size if len(cell) <= 10 else font_size - 2
                family = SERIF if row_index > 0 else FONT
                text(current_x + col_widths[col_index] / 2, y + row_index * row_height + 46, cell, size, fill, weight, "middle", family)
                current_x += col_widths[col_index]
        return y + total_height

    def rule_card(x, y, title, lines, tag):
        card_height = 116 + 44 * len(lines)
        rect(x, y, 920, card_height, 30, fill="#120806", stroke="url(#strokeGold)", sw=2, fill_opacity=0.78, filter_id="cardShadow")
        rect(x, y, 920, 78, 30, fill="#24100a", stroke="none", fill_opacity=0.94)
        rect(x, y + 52, 920, 26, 0, fill="#24100a", stroke="none", fill_opacity=0.94)
        chip(x + 28, y + 17, tag, 108)
        text(x + 154, y + 51, title, 32, "#ffd19a", 900)
        yy = y + 112
        for line_text in lines:
            circle(x + 42, yy - 10, 6, "#ff8a3d")
            text(x + 66, yy, line_text, 28, "#fff1df", 650)
            yy += 44
        return y + card_height

    add(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#140504"/>
    <stop offset="38%" stop-color="#20100a"/>
    <stop offset="72%" stop-color="#0f0806"/>
    <stop offset="100%" stop-color="#050304"/>
  </linearGradient>
  <radialGradient id="heroGlow" cx="0.18" cy="0.03" r="0.72">
    <stop offset="0%" stop-color="#ff6c5f" stop-opacity="0.50"/>
    <stop offset="100%" stop-color="#ff6c5f" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="sideGlow" cx="1" cy="0.15" r="0.75">
    <stop offset="0%" stop-color="#ffb15c" stop-opacity="0.22"/>
    <stop offset="100%" stop-color="#ffb15c" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="bottomGlow" cx="0" cy="1" r="0.88">
    <stop offset="0%" stop-color="#8f1c13" stop-opacity="0.38"/>
    <stop offset="100%" stop-color="#8f1c13" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ff5b2e"/>
    <stop offset="100%" stop-color="#ffbc69"/>
  </linearGradient>
  <linearGradient id="strokeGold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ff6a2f"/>
    <stop offset="55%" stop-color="#ffb15c"/>
    <stop offset="100%" stop-color="#7a2b1c"/>
  </linearGradient>
  <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="130%">
    <feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#000000" flood-opacity="0.32"/>
    <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#ff5b2e" flood-opacity="0.08"/>
  </filter>
</defs>''')

    rect(0, 0, width, height, fill="url(#bg)")
    rect(0, 0, width, height, fill="url(#heroGlow)")
    rect(0, 0, width, height, fill="url(#sideGlow)")
    rect(0, 0, width, height, fill="url(#bottomGlow)")
    for index in range(18):
        line(70 + index * 62, 360, 70 + index * 62 - 250, 3800, "#ff8a3d", 1, 0.035)
    for index in range(78):
        circle((index * 151 + 29) % width, (index * 277 + 61) % height, 1.2 + (index % 3), "#ffb15c", 0.13)
    path("M-80 500 C200 400 360 600 620 490 C820 405 950 350 1160 420", "#ff8a3d", 3, 0.11)
    path("M-80 3360 C220 3220 420 3440 720 3280 C900 3190 1010 3150 1160 3220", "#ff8a3d", 3, 0.09)

    text(80, 150, "RYMO岩灼电竞", 76, "#ff7a35", 900, stroke="#2a0d08", sw=10)
    text(80, 250, "爆款趣味 / 小小巨人", 62, "#ffd19a", 900, stroke="#2a0d08", sw=8)
    text(84, 315, "血量制挑战｜2名陪玩全程服务", 30, "#f5d5c0", 750)
    chip(84, 346, "Q版 + 无上限", 228)
    chip(336, 346, "价格单位：钻石", 204)

    x = 80
    y = 455
    section_title(x, y, "小小巨人Q版价格表", "Q版")
    y += 98
    y = table(x, y, [280, 220, 420], [
        ["版本", "价格", "初始血量"],
        ["基础款", "128", "10滴"],
        ["进阶版", "238", "15滴"],
        ["畅玩版", "338", "20滴"],
        ["高端定制", "788", "25滴"],
    ], 74, 29) + 62

    section_title(x, y, "小小巨人Q版扣血规则", "Q版 RULE")
    y += 98
    y = table(x, y, [168, 160, 390, 202], [
        ["版本", "不扣血", "扣血规则", "失败加血"],
        ["基础款", "<500W", "500-900扣5｜>900扣10", "失败+2｜上限20"],
        ["进阶版", "<688W", "688-1000扣5｜>1000扣10", "失败+2｜上限30"],
        ["畅玩版", "<788W", "788-1000扣5｜>1000扣10", "失败+3｜上限40"],
        ["高端定制", "<999W", "999-1200扣10｜>1200扣15", "失败+3｜上限50"],
    ], 78, 22) + 62

    section_title(x, y, "小巨人硬核版（无上限）", "HARDCORE")
    y += 98
    y = table(x, y, [280, 200, 220, 220], [
        ["版本", "价格", "初始血量", "说明"],
        ["简单版", "888", "15滴", "血量无上限"],
        ["进阶版", "1288", "20滴", "血量无上限"],
        ["困难版", "1888", "30滴", "血量无上限"],
    ], 76, 28) + 60

    rule_card(x, y, "硬核版规则", [
        "撤离800W+扣5滴",
        "撤离988W+扣6滴",
        "撤离1188W+扣7滴",
        "撤离1300W+扣8滴",
        "撤离1588W+扣10滴",
        "撤离失败+2滴",
    ], "规则")
    y += 438

    rule_card(x, y, "通用说明", [
        "血量为0即结单",
        "老板丢包撤离按撤离失败处理",
        "老板需听从指挥，恶意影响服务可直接结单",
        "2名陪玩全程服务",
    ], "说明")

    rect(80, height - 272, 920, 142, 30, fill="#120806", stroke="url(#strokeGold)", sw=2, fill_opacity=0.82, filter_id="cardShadow")
    text(118, height - 218, "具体服务标准以下单页与客服确认为准", 30, "#ffd19a", 900)
    text(118, height - 172, "东东电竞搜 RYMO岩灼电竞｜未成年禁止消费", 27, "#f5d5c0", 700)
    add("</svg>")
    return "\n".join(items)


def render_seven_polished():
    width = 1080
    height = 3900
    items = []

    def add(raw):
        items.append(raw)

    def rect(x, y, w, h, rx=0, fill="none", stroke="none", sw=1, fill_opacity=None, opacity=None, dash=None, filter_id=None):
        attrs = [
            f'x="{x}"',
            f'y="{y}"',
            f'width="{w}"',
            f'height="{h}"',
            f'rx="{rx}"',
            f'fill="{fill}"',
            f'stroke="{stroke}"',
            f'stroke-width="{sw}"',
        ]
        if fill_opacity is not None:
            attrs.append(f'fill-opacity="{fill_opacity}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if filter_id:
            attrs.append(f'filter="url(#{filter_id})"')
        add(f"<rect {' '.join(attrs)} />")

    def line(x1, y1, x2, y2, stroke="#ff8a3d", sw=2, opacity=None, dash=None):
        attrs = [
            f'x1="{x1}"',
            f'y1="{y1}"',
            f'x2="{x2}"',
            f'y2="{y2}"',
            f'stroke="{stroke}"',
            f'stroke-width="{sw}"',
        ]
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        add(f"<line {' '.join(attrs)} />")

    def circle(cx, cy, r, fill, opacity=None):
        attrs = [f'cx="{cx}"', f'cy="{cy}"', f'r="{r}"', f'fill="{fill}"']
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        add(f"<circle {' '.join(attrs)} />")

    def path(d, stroke="#ff8a3d", sw=2, opacity=None):
        attrs = [f'd="{d}"', 'fill="none"', f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        add(f"<path {' '.join(attrs)} />")

    def text(x, y, value, size=32, fill="#fff1df", weight=400, anchor="start", family=FONT, stroke=None, sw=0):
        attrs = [
            f'x="{x}"',
            f'y="{y}"',
            f'fill="{fill}"',
            f'text-anchor="{anchor}"',
            f'style="font-family:{family};font-size:{size}px;font-weight:{weight};"',
        ]
        if stroke:
            attrs += [f'stroke="{stroke}"', f'stroke-width="{sw}"', 'paint-order="stroke fill"', 'stroke-linejoin="round"']
        add(f"<text {' '.join(attrs)}>{e(value)}</text>")

    def chip(x, y, label, w=None):
        w = w or max(124, len(label) * 27 + 42)
        rect(x, y, w, 48, 24, fill="#1d0f0b", stroke="#ff8a3d", sw=1.5, fill_opacity=0.82)
        text(x + w / 2, y + 33, label, 24, "#ffd19a", 800, "middle")
        return w

    def section_title(x, y, title, sub=None):
        rect(x, y, 920, 74, 28, fill="#1b0c08", stroke="url(#strokeGold)", sw=2, fill_opacity=0.86, filter_id="cardShadow")
        rect(x + 16, y + 14, 9, 46, 5, fill="url(#accentGrad)", stroke="none")
        text(x + 42, y + 49, title, 34, "#ffd19a", 900)
        if sub:
            text(x + 892, y + 47, sub, 23, "#d9ad8e", 700, "end")

    def table(x, y, col_widths, rows, row_height=74, font_size=29):
        total_width = sum(col_widths)
        total_height = row_height * len(rows)
        rect(x, y, total_width, total_height, 24, fill="#120806", stroke="url(#strokeGold)", sw=2, fill_opacity=0.76, filter_id="cardShadow")
        rect(x, y, total_width, row_height, 24, fill="#251008", stroke="none", fill_opacity=0.9)
        rect(x, y + row_height - 24, total_width, 24, 0, fill="#251008", stroke="none", fill_opacity=0.9)
        current_x = x
        for col_width in col_widths[:-1]:
            current_x += col_width
            line(current_x, y, current_x, y + total_height, "#ff8a3d", 1.6, 0.72, "5 7")
        for row_index in range(1, len(rows)):
            line(x, y + row_index * row_height, x + total_width, y + row_index * row_height, "#ff8a3d", 1.6, 0.72, "5 7")
        for row_index, row in enumerate(rows):
            current_x = x
            for col_index, cell in enumerate(row):
                is_header = row_index == 0
                is_label = row_index > 0 and col_index == 0
                fill = "#ffd19a" if is_header or is_label else "#fff1df"
                weight = 900 if is_header or col_index == 0 else 750
                size = font_size if len(cell) <= 14 else font_size - 3
                family = SERIF if row_index > 0 else FONT
                text(current_x + col_widths[col_index] / 2, y + row_index * row_height + 46, cell, size, fill, weight, "middle", family)
                current_x += col_widths[col_index]
        return y + total_height

    def rule_card(x, y, title, lines, tag):
        card_height = 116 + 44 * len(lines)
        rect(x, y, 920, card_height, 30, fill="#120806", stroke="url(#strokeGold)", sw=2, fill_opacity=0.78, filter_id="cardShadow")
        rect(x, y, 920, 78, 30, fill="#24100a", stroke="none", fill_opacity=0.94)
        rect(x, y + 52, 920, 26, 0, fill="#24100a", stroke="none", fill_opacity=0.94)
        chip(x + 28, y + 17, tag, 108)
        text(x + 154, y + 51, title, 32, "#ffd19a", 900)
        yy = y + 112
        for line_text in lines:
            circle(x + 42, yy - 10, 6, "#ff8a3d")
            text(x + 66, yy, line_text, 28, "#fff1df", 650)
            yy += 44
        return y + card_height

    add(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#120504"/>
    <stop offset="38%" stop-color="#21100a"/>
    <stop offset="72%" stop-color="#0f0806"/>
    <stop offset="100%" stop-color="#050304"/>
  </linearGradient>
  <radialGradient id="heroGlow" cx="0.18" cy="0.03" r="0.72">
    <stop offset="0%" stop-color="#ff5b2e" stop-opacity="0.50"/>
    <stop offset="100%" stop-color="#ff5b2e" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="sideGlow" cx="1" cy="0.18" r="0.76">
    <stop offset="0%" stop-color="#ffb15c" stop-opacity="0.22"/>
    <stop offset="100%" stop-color="#ffb15c" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="bottomGlow" cx="0" cy="1" r="0.88">
    <stop offset="0%" stop-color="#8f1c13" stop-opacity="0.38"/>
    <stop offset="100%" stop-color="#8f1c13" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ff5b2e"/>
    <stop offset="100%" stop-color="#ffbc69"/>
  </linearGradient>
  <linearGradient id="strokeGold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ff6a2f"/>
    <stop offset="55%" stop-color="#ffb15c"/>
    <stop offset="100%" stop-color="#7a2b1c"/>
  </linearGradient>
  <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="130%">
    <feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#000000" flood-opacity="0.32"/>
    <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#ff5b2e" flood-opacity="0.08"/>
  </filter>
</defs>''')

    rect(0, 0, width, height, fill="url(#bg)")
    rect(0, 0, width, height, fill="url(#heroGlow)")
    rect(0, 0, width, height, fill="url(#sideGlow)")
    rect(0, 0, width, height, fill="url(#bottomGlow)")
    for index in range(18):
        line(70 + index * 62, 360, 70 + index * 62 - 250, 3720, "#ff8a3d", 1, 0.035)
    for index in range(80):
        circle((index * 151 + 29) % width, (index * 277 + 61) % height, 1.2 + (index % 3), "#ffb15c", 0.13)
    path("M-80 500 C210 400 360 620 620 500 C820 405 950 350 1160 430", "#ff8a3d", 3, 0.11)
    path("M-80 3040 C210 2920 420 3140 720 2980 C900 2890 1010 2850 1160 2920", "#ff8a3d", 3, 0.09)

    text(80, 150, "RYMO岩灼电竞", 76, "#ff7a35", 900, stroke="#2a0d08", sw=10)
    text(80, 250, "爆款趣味 / 七宗罪挑战", 62, "#ffd19a", 900, stroke="#2a0d08", sw=8)
    text(84, 315, "七选三 / 七宗罪全通｜挑战型趣味订单", 30, "#f5d5c0", 750)
    chip(84, 346, "指定地图 +100 / +200", 256)
    chip(366, 346, "价格单位：钻石", 204)

    x = 80
    y = 455
    section_title(x, y, "七宗罪价格表", "SEVEN SINS")
    y += 98
    y = table(x, y, [280, 180, 220, 240], [
        ["服务", "价格", "保底", "指定地图"],
        ["三宗罪自选", "588", "2388W", "+100"],
        ["七宗罪全通", "1188", "4288W", "+200"],
    ], 76, 29) + 60

    section_title(x, y, "七宗罪任务", "TASKS")
    y += 98
    y = table(x, y, [220, 700], [
        ["任务", "说明"],
        ["傲慢", "开局只可穿戴对应限制装备，完成清图并撤离"],
        ["懒惰", "蹲守大门、飞机或桥，三选一固定点位，达到800W+撤离"],
        ["嫉妒", "击败一队满六套队伍，并护送队伍撤离"],
        ["贪婪", "吃10个保险箱，小保险也计算"],
        ["暴怒", "不允许慢走，宣战并清图，慢走视为失败"],
        ["暴食", "带出1111W撤离"],
        ["色欲", "累计击败8名指定性别干员，二选一，不允许刷人头"],
    ], 70, 25) + 58

    rule_card(x, y, "通用规则", [
        "一次撤离最多完成一个罪",
        "非指定地图可在完成一个任务后更换地图",
        "指定地图仅限绝密地图",
        "阵亡按炸单补保底处理",
        "老板需听从指挥",
    ], "说明")

    rect(80, height - 272, 920, 142, 30, fill="#120806", stroke="url(#strokeGold)", sw=2, fill_opacity=0.82, filter_id="cardShadow")
    text(118, height - 218, "具体服务标准以下单页与客服确认为准", 30, "#ffd19a", 900)
    text(118, height - 172, "东东电竞搜 RYMO岩灼电竞｜未成年禁止消费", 27, "#f5d5c0", 700)
    add("</svg>")
    return "\n".join(items)


class AutoPoster:
    def __init__(self, title, subtitle, chips=None, width=1080):
        self.width = width
        self.header_height = 455
        self.bottom_padding = 120
        self.footer_height = 142
        self.title = title
        self.subtitle = subtitle
        self.chips = chips or []
        self.operations = []
        self.y = self.header_height

    def add_section_table(self, title, sub, col_widths, rows, row_height=74, font_size=28, column_font_sizes=None):
        y = self.y
        table_height = row_height * len(rows)
        self.operations.append(("section_title", y, title, sub))
        self.operations.append(("table", y + 98, col_widths, rows, row_height, font_size, column_font_sizes or {}))
        self.y = y + 98 + table_height + 62

    def add_rule_card(self, title, tag, lines):
        y = self.y
        wrapped_lines = []
        for line_text in lines:
            for index, wrapped_line in enumerate(wrap_cn(line_text, 56)):
                wrapped_lines.append(wrapped_line if index == 0 else f"__CONT__{wrapped_line}")
        card_height = 116 + 44 * len(wrapped_lines)
        self.operations.append(("rule_card", y, title, tag, wrapped_lines, card_height))
        self.y = y + card_height + 54

    def height(self):
        return self.y + self.footer_height + self.bottom_padding

    def render(self):
        width = self.width
        height = self.height()
        items = []

        def add(raw):
            items.append(raw)

        def rect(x, y, w, h, rx=0, fill="none", stroke="none", sw=1, fill_opacity=None, opacity=None, dash=None, filter_id=None):
            attrs = [
                f'x="{x}"',
                f'y="{y}"',
                f'width="{w}"',
                f'height="{h}"',
                f'rx="{rx}"',
                f'fill="{fill}"',
                f'stroke="{stroke}"',
                f'stroke-width="{sw}"',
            ]
            if fill_opacity is not None:
                attrs.append(f'fill-opacity="{fill_opacity}"')
            if opacity is not None:
                attrs.append(f'opacity="{opacity}"')
            if dash:
                attrs.append(f'stroke-dasharray="{dash}"')
            if filter_id:
                attrs.append(f'filter="url(#{filter_id})"')
            add(f"<rect {' '.join(attrs)} />")

        def line(x1, y1, x2, y2, stroke="#ff8a3d", sw=2, opacity=None, dash=None):
            attrs = [
                f'x1="{x1}"',
                f'y1="{y1}"',
                f'x2="{x2}"',
                f'y2="{y2}"',
                f'stroke="{stroke}"',
                f'stroke-width="{sw}"',
            ]
            if opacity is not None:
                attrs.append(f'opacity="{opacity}"')
            if dash:
                attrs.append(f'stroke-dasharray="{dash}"')
            add(f"<line {' '.join(attrs)} />")

        def circle(cx, cy, r, fill, opacity=None):
            attrs = [f'cx="{cx}"', f'cy="{cy}"', f'r="{r}"', f'fill="{fill}"']
            if opacity is not None:
                attrs.append(f'opacity="{opacity}"')
            add(f"<circle {' '.join(attrs)} />")

        def path(d, stroke="#ff8a3d", sw=2, opacity=None):
            attrs = [f'd="{d}"', 'fill="none"', f'stroke="{stroke}"', f'stroke-width="{sw}"']
            if opacity is not None:
                attrs.append(f'opacity="{opacity}"')
            add(f"<path {' '.join(attrs)} />")

        def text(x, y, value, size=32, fill="#fff1df", weight=400, anchor="start", family=FONT, stroke=None, sw=0):
            attrs = [
                f'x="{x}"',
                f'y="{y}"',
                f'fill="{fill}"',
                f'text-anchor="{anchor}"',
                f'style="font-family:{family};font-size:{size}px;font-weight:{weight};"',
            ]
            if stroke:
                attrs += [f'stroke="{stroke}"', f'stroke-width="{sw}"', 'paint-order="stroke fill"', 'stroke-linejoin="round"']
            add(f"<text {' '.join(attrs)}>{e(value)}</text>")

        def chip(x, y, label, w=None):
            w = w or max(124, len(label) * 27 + 42)
            rect(x, y, w, 48, 24, fill="#1d0f0b", stroke="#ff8a3d", sw=1.5, fill_opacity=0.82)
            text(x + w / 2, y + 33, label, 24, "#ffd19a", 800, "middle")
            return w

        def section_title(y, title, sub=None):
            x = 80
            rect(x, y, 920, 74, 28, fill="#1b0c08", stroke="url(#strokeGold)", sw=2, fill_opacity=0.86, filter_id="cardShadow")
            rect(x + 16, y + 14, 9, 46, 5, fill="url(#accentGrad)", stroke="none")
            text(x + 42, y + 49, title, 34, "#ffd19a", 900)
            if sub:
                text(x + 892, y + 47, sub, 23, "#d9ad8e", 700, "end")

        def table(y, col_widths, rows, row_height=74, font_size=28, column_font_sizes=None):
            x = 80
            column_font_sizes = column_font_sizes or {}
            total_width = sum(col_widths)
            total_height = row_height * len(rows)
            rect(x, y, total_width, total_height, 24, fill="#120806", stroke="url(#strokeGold)", sw=2, fill_opacity=0.76, filter_id="cardShadow")
            rect(x, y, total_width, row_height, 24, fill="#251008", stroke="none", fill_opacity=0.9)
            rect(x, y + row_height - 24, total_width, 24, 0, fill="#251008", stroke="none", fill_opacity=0.9)
            current_x = x
            for col_width in col_widths[:-1]:
                current_x += col_width
                line(current_x, y, current_x, y + total_height, "#ff8a3d", 1.6, 0.72, "5 7")
            for row_index in range(1, len(rows)):
                line(x, y + row_index * row_height, x + total_width, y + row_index * row_height, "#ff8a3d", 1.6, 0.72, "5 7")
            for row_index, row in enumerate(rows):
                current_x = x
                for col_index, cell in enumerate(row):
                    is_header = row_index == 0
                    is_label = row_index > 0 and col_index == 0
                    fill = "#ffd19a" if is_header or is_label else "#fff1df"
                    is_emphasized = col_index in column_font_sizes
                    weight = 900 if is_header or col_index == 0 or is_emphasized else 750
                    target_size = column_font_sizes.get(col_index, font_size)
                    visual_units = sum(1 if ord(char) < 128 else 2 for char in cell)
                    estimated_width = visual_units * target_size * 0.52
                    available_width = col_widths[col_index] - 24
                    size = target_size if estimated_width <= available_width else max(
                        20,
                        int(target_size * available_width / estimated_width),
                    )
                    family = SERIF if row_index > 0 else FONT
                    text(current_x + col_widths[col_index] / 2, y + row_index * row_height + 46, cell, size, fill, weight, "middle", family)
                    current_x += col_widths[col_index]

        def rule_card(y, title, tag, lines, card_height):
            x = 80
            rect(x, y, 920, card_height, 30, fill="#120806", stroke="url(#strokeGold)", sw=2, fill_opacity=0.78, filter_id="cardShadow")
            rect(x, y, 920, 78, 30, fill="#24100a", stroke="none", fill_opacity=0.94)
            rect(x, y + 52, 920, 26, 0, fill="#24100a", stroke="none", fill_opacity=0.94)
            chip(x + 28, y + 17, tag, 108)
            text(x + 154, y + 51, title, 32, "#ffd19a", 900)
            yy = y + 112
            for line_text in lines:
                is_continuation = line_text.startswith("__CONT__")
                display_text = line_text.replace("__CONT__", "", 1)
                if not is_continuation:
                    circle(x + 42, yy - 10, 6, "#ff8a3d")
                text(x + 66, yy, display_text, 28, "#fff1df", 650)
                yy += 44

        add(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#130504"/>
    <stop offset="38%" stop-color="#21100a"/>
    <stop offset="72%" stop-color="#100806"/>
    <stop offset="100%" stop-color="#050304"/>
  </linearGradient>
  <radialGradient id="heroGlow" cx="0.18" cy="0.03" r="0.72">
    <stop offset="0%" stop-color="#ff6733" stop-opacity="0.50"/>
    <stop offset="100%" stop-color="#ff6733" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="sideGlow" cx="1" cy="0.20" r="0.78">
    <stop offset="0%" stop-color="#ffb15c" stop-opacity="0.20"/>
    <stop offset="100%" stop-color="#ffb15c" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="bottomGlow" cx="0" cy="1" r="0.9">
    <stop offset="0%" stop-color="#8f1c13" stop-opacity="0.36"/>
    <stop offset="100%" stop-color="#8f1c13" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ff5b2e"/>
    <stop offset="100%" stop-color="#ffbc69"/>
  </linearGradient>
  <linearGradient id="strokeGold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ff6a2f"/>
    <stop offset="55%" stop-color="#ffb15c"/>
    <stop offset="100%" stop-color="#7a2b1c"/>
  </linearGradient>
  <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="130%">
    <feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#000000" flood-opacity="0.32"/>
    <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#ff5b2e" flood-opacity="0.08"/>
  </filter>
</defs>''')

        rect(0, 0, width, height, fill="url(#bg)")
        rect(0, 0, width, height, fill="url(#heroGlow)")
        rect(0, 0, width, height, fill="url(#sideGlow)")
        rect(0, 0, width, height, fill="url(#bottomGlow)")
        for index in range(18):
            line(70 + index * 62, 360, 70 + index * 62 - 250, height - 230, "#ff8a3d", 1, 0.035)
        for index in range(max(42, height // 50)):
            circle((index * 151 + 29) % width, (index * 277 + 61) % height, 1.2 + (index % 3), "#ffb15c", 0.13)
        path("M-80 500 C210 400 360 620 620 500 C820 405 950 350 1160 430", "#ff8a3d", 3, 0.11)
        path(f"M-80 {height - 760} C210 {height - 880} 420 {height - 660} 720 {height - 820} C900 {height - 910} 1010 {height - 950} 1160 {height - 880}", "#ff8a3d", 3, 0.09)

        text(82, 154, "RYMO岩灼电竞", 76, "#8d6640", 900, family=SERIF)
        text(80, 150, "RYMO岩灼电竞", 76, "#ffcf8c", 900, family=SERIF)
        text(80, 250, self.title, 62, "#ffd19a", 900, family=SERIF, stroke="#2a0d08", sw=8)
        text(84, 315, self.subtitle, 30, "#f5d5c0", 750)
        chip_x = 84
        for chip_label, chip_width in self.chips:
            chip(chip_x, 346, chip_label, chip_width)
            chip_x += chip_width + 24

        for operation in self.operations:
            kind = operation[0]
            if kind == "section_title":
                _, y, title, sub = operation
                section_title(y, title, sub)
            elif kind == "table":
                _, y, col_widths, rows, row_height, font_size, column_font_sizes = operation
                table(y, col_widths, rows, row_height, font_size, column_font_sizes)
            elif kind == "rule_card":
                _, y, title, tag, lines, card_height = operation
                rule_card(y, title, tag, lines, card_height)

        footer_y = height - self.footer_height - 88
        rect(80, footer_y, 920, self.footer_height, 30, fill="#120806", stroke="url(#strokeGold)", sw=2, fill_opacity=0.82, filter_id="cardShadow")
        text(118, footer_y + 54, "具体服务标准以下单页与客服确认为准", 30, "#ffd19a", 900)
        text(118, footer_y + 100, "东东电竞搜 RYMO岩灼电竞｜未成年禁止消费", 27, "#f5d5c0", 700)
        add("</svg>")
        return "\n".join(items)


def wrap_cn(text, limit):
    result = []
    current = ""
    count = 0
    for char in text:
        char_width = 1 if ord(char) < 128 else 2
        if count + char_width > limit and current:
            result.append(current)
            current = char
            count = char_width
        else:
            current += char
            count += char_width
    if current:
        result.append(current)
    return result


def render_guarantee_clear_polished():
    poster = AutoPoster(
        "保底清图 / 基础护航",
        "绝密保底｜机密保底｜极速清图",
        chips=[("保底护航", 148), ("价格单位：钻石", 204)],
    )
    poster.add_section_table("绝密基础保底", "TOP SECRET", [160, 160, 180, 420], [
        ["档位", "价格", "保底", "说明"],
        ["168档", "168", "688W", "不出红+100W"],
        ["288档", "288", "1288W", "不出红不结单"],
        ["688档", "688", "3088W", "不出大红不结单"],
        ["1088档", "1088", "5088W", "不出超大红不结单"],
    ], 74, 27)
    poster.add_section_table("机密基础保底", "SECRET", [230, 220, 240, 230], [
        ["档位", "价格", "保底", "说明"],
        ["88档", "88", "388W", "基础保底"],
        ["168档", "168", "888W", "基础保底"],
        ["268档", "268", "1388W", "基础保底"],
    ], 74, 28)
    poster.add_section_table("极速清图", "CLEAR MAP", [220, 180, 220, 300], [
        ["服务", "价格", "保底", "说明"],
        ["15分钟", "338", "1188W", "可丢包撤"],
        ["10分钟", "788", "2688W", "可丢包撤"],
        ["7分钟", "1588", "4888W", "禁止撤离"],
    ], 74, 28)
    poster.add_rule_card("红货与结算规则", "规则", [
        "红修、装备、红弹不算红",
        "百万级物资=大红，允许约5W浮动",
        "两百万级物资=超大红，允许约10W浮动",
        "三大红可合一超大红",
        "保底与清图细则以下单页和客服确认为准",
    ])
    return poster.render()


def render_little_giant_polished():
    poster = AutoPoster(
        "爆款趣味 / 小小巨人",
        "血量制挑战｜2名陪玩全程服务",
        chips=[("Q版 + 无上限", 228), ("价格单位：钻石", 204)],
    )
    poster.add_section_table("小小巨人Q版价格表", "Q版", [280, 220, 420], [
        ["版本", "价格", "初始血量"],
        ["基础款", "128", "10滴"],
        ["进阶版", "238", "15滴"],
        ["畅玩版", "338", "20滴"],
        ["高端定制", "788", "25滴"],
    ], 74, 29)
    poster.add_section_table("小小巨人Q版扣血规则", "Q版 RULE", [168, 160, 390, 202], [
        ["版本", "不扣血", "扣血规则", "失败加血"],
        ["基础款", "<500W", "500-900扣5｜>900扣10", "失败+2｜上限20"],
        ["进阶版", "<688W", "688-1000扣5｜>1000扣10", "失败+2｜上限30"],
        ["畅玩版", "<788W", "788-1000扣5｜>1000扣10", "失败+3｜上限40"],
        ["高端定制", "<999W", "999-1200扣10｜>1200扣15", "失败+3｜上限50"],
    ], 78, 22)
    poster.add_section_table("小巨人硬核版（无上限）", "HARDCORE", [280, 200, 220, 220], [
        ["版本", "价格", "初始血量", "说明"],
        ["简单版", "888", "15滴", "血量无上限"],
        ["进阶版", "1288", "20滴", "血量无上限"],
        ["困难版", "1888", "30滴", "血量无上限"],
    ], 76, 28)
    poster.add_rule_card("硬核版规则", "规则", [
        "撤离800W+扣5滴",
        "撤离988W+扣6滴",
        "撤离1188W+扣7滴",
        "撤离1300W+扣8滴",
        "撤离1588W+扣10滴",
        "撤离失败+2滴",
    ])
    poster.add_rule_card("通用说明", "说明", [
        "血量为0即结单",
        "老板丢包撤离按撤离失败处理",
        "老板需听从指挥，恶意影响服务可直接结单",
        "2名陪玩全程服务",
    ])
    return poster.render()


def render_seven_polished():
    poster = AutoPoster(
        "爆款趣味 / 七宗罪挑战",
        "七选三 / 七宗罪全通｜挑战型趣味订单",
        chips=[("指定地图 +100 / +200", 256), ("价格单位：钻石", 204)],
    )
    poster.add_section_table("七宗罪价格表", "SEVEN SINS", [280, 180, 220, 240], [
        ["服务", "价格", "保底", "指定地图"],
        ["三宗罪自选", "588", "2388W", "+100"],
        ["七宗罪全通", "1188", "4288W", "+200"],
    ], 76, 29)
    poster.add_rule_card("七宗罪任务", "TASKS", [
        "傲慢：开局只可穿戴对应限制装备，完成清图并撤离",
        "懒惰：蹲守大门、飞机或桥，三选一固定点位，达到800W+撤离",
        "嫉妒：击败一队满六套队伍，并护送队伍撤离",
        "贪婪：吃10个保险箱，小保险也计算",
        "暴怒：不允许慢走，宣战并清图，慢走视为失败",
        "暴食：带出1111W撤离",
        "色欲：累计击败8名指定性别干员，二选一，不允许刷人头",
    ])
    poster.add_rule_card("通用规则", "说明", [
        "一次撤离最多完成一个罪",
        "非指定地图可在完成一个任务后更换地图",
        "指定地图仅限绝密地图",
        "阵亡按炸单补保底处理",
        "老板需听从指挥",
    ])
    return poster.render()


def render_basic_services_polished():
    poster = AutoPoster(
        "基础服务 / 常规点单",
        "超值体验｜娱乐陪玩｜陪跑任务｜技术教学",
        chips=[("基础服务", 148), ("价格单位：钻石", 204)],
    )
    poster.add_section_table("超值体验", "TRIAL", [330, 230, 360], [
        ["服务", "价格", "内容"],
        ["128元保688W", "128", "2名陪玩"],
        ["258元保1288W", "258", "2名陪玩"],
    ], 76, 29)
    poster.add_section_table("娱乐陪玩", "ENTERTAINMENT", [280, 320, 320], [
        ["分类", "1p1", "1p2"],
        ["女陪", "60/小时", "70/小时"],
        ["男陪", "50/小时", "60/小时"],
        ["娱乐Pro", "80/小时", "90/小时"],
    ], 74, 29)
    poster.add_section_table("陪跑任务", "TASK RUN", [280, 320, 320], [
        ["地图", "1p1", "1p2"],
        ["常规图", "20/小时", "30/小时"],
        ["机密图", "30/小时", "40/小时"],
        ["绝密图", "60/小时", "70/小时"],
        ["9格培培", "60/小时", "-"],
    ], 74, 29)
    poster.add_section_table("技术教学", "TEACHING", [360, 260, 300], [
        ["服务", "价格", "说明"],
        ["1v1教学1p1", "80/小时", "60分钟"],
        ["1v1教学1p2", "90/小时", "含1陪2"],
    ], 76, 29)
    poster.add_rule_card("通用说明", "说明", [
        "1p1 = 1名陪玩服务1名老板",
        "1p2 = 1名陪玩服务2名老板",
        "具体服务标准以下单页与客服确认为准",
    ])
    return poster.render()


def render_trial_polished():
    poster = AutoPoster(
        "超值体验 / 新手体验单",
        "固定2名陪玩｜快速匹配｜保底物资",
        chips=[("体验引流单", 180), ("价格单位：钻石", 204)],
    )
    poster.add_section_table("体验单价格表", "TRIAL", [330, 230, 360], [
        ["服务", "价格", "内容"],
        ["128元保688W", "128", "2名陪玩"],
        ["258元保1288W", "258", "2名陪玩"],
    ], 76, 29)
    poster.add_rule_card("服务说明", "说明", [
        "体验单固定2名陪玩接单",
        "适合首次下单老板快速了解服务",
        "进入抢单大厅，由符合条件的陪玩接单",
        "保底、炸单和售后细则以下单页与客服确认为准",
    ])
    poster.add_rule_card("下单提示", "提示", [
        "下单时请填写需求补充和房间码",
        "匹配成功后可在订单会话中沟通",
        "订单完成后可对接单陪玩进行评价",
    ])
    return poster.render()


def render_entertainment_polished():
    poster = AutoPoster(
        "娱乐陪玩 / 轻松陪伴",
        "女陪｜男陪｜娱乐Pro｜1p1 / 1p2",
        chips=[("娱乐陪玩", 148), ("价格单位：钻石/小时", 260)],
    )
    poster.add_section_table("娱乐陪玩价格表", "ENTERTAINMENT", [280, 320, 320], [
        ["分类", "1p1", "1p2"],
        ["女陪", "60/小时", "70/小时"],
        ["男陪", "50/小时", "60/小时"],
        ["娱乐Pro", "80/小时", "90/小时"],
    ], 74, 29)
    poster.add_rule_card("服务说明", "说明", [
        "主打轻松娱乐陪伴和开黑氛围",
        "1p1 = 1名陪玩服务1名老板",
        "1p2 = 1名陪玩服务2名老板",
        "甜蜜陪模式、绝密地图等后续以具体服务规格展示",
    ])
    poster.add_rule_card("售后边界", "边界", [
        "娱乐陪玩不接受技术投诉",
        "如对服务体验不满意，请及时联系售后客服",
        "具体服务标准以下单页与客服确认为准",
    ])
    return poster.render()


def render_player_exam_rules():
    """入店考核：技术全装队 + 娱乐考核要求。"""
    poster = AutoPoster(
        "三角洲入店考核规则",
        "技术全装队｜娱乐考核｜两把累计｜禁止养猪",
        chips=[
            ("全装队口径", 180),
            ("两把累计", 148),
            ("娱乐考核", 148),
            ("禁止养猪", 148),
        ],
    )
    poster.add_section_table("档位通过标准", "RANK PASS", [180, 220, 520], [
        ["档位", "记法", "通过标准"],
        ["赤岩", "两把累计", "杀够 4 队全装队"],
        ["灼曜", "两把累计", "杀够 5 队全装队"],
        ["圣尊", "两把累计", "杀够 6 队全装队"],
        ["单考", "两把累计", "对应档位通过标准 -1 队"],
    ], 82, 26)
    poster.add_section_table("全装队换算口径", "TEAM UNIT", [300, 620], [
        ["击杀对象 / 情形", "折算全装队"],
        ["标准全装队", "1.0 队"],
        ["Aw", "1.5 队"],
        ["劝架", "0.5 队"],
        ["非四头五甲满改枪（含修脚枪）", "0.5 队"],
        ["单三猛攻", "0.5 队"],
        ["单只老鼠", "不折算队"],
    ], 78, 26)
    poster.add_rule_card("考核记法说明", "记法", [
        "注意：全装 = 四头五甲及以上 + 满改枪（满改修脚枪也算）。",
        "所有考生统一打 2 把，以两局累计全装队与考官复核为准。",
        "考核只计有效击败折算后的全装队，不以撤离物资为硬指标。",
        "禁止养猪刷数据；养猪局该局无效，严重者直接不通过。",
        "劝架、非满改、单三猛攻等按表内折算，不可按完整全装队记。",
        "Aw 按 1.5 队计入；标准全装队按 1.0 队计入。",
        "是否达标以结算截图、对局记录与考官最终复核为准。",
    ])
    poster.add_rule_card("娱乐考核要求", "娱乐", [
        "服务态度良好",
        "情商高，会说话，不冷场，主动找话题",
        "声音好听",
    ])
    return poster.render()


def render_entertainment_exam_rules():
    poster = AutoPoster(
        "娱乐陪考核要求",
        "娱乐｜娱乐Pro 双等级考核",
        chips=[("双等级考核", 180), ("娱乐押金100元", 220), ("均可破格录取", 220)],
    )
    poster.add_section_table("娱乐 / 娱乐Pro 等级标准", "LEVEL", [170, 330, 420], [
        ["等级", "考核方式", "通过标准"],
        ["娱乐", "机密大坝跑刀1局", "带出物资 ≥ 60W"],
        ["娱乐Pro", "指定地图击败", "航天≥2｜巴克什/监狱≥4"],
    ], 76, 27)
    poster.add_rule_card("考核要求说明", "要求", [
        "服务态度良好",
        "情商高，会说话，不冷场，主动找话题",
        "声音好听",
    ])
    poster.add_rule_card("破格录取标准", "破格", [
        "娱乐和娱乐Pro适用同一破格录取标准",
        "声音条件、形象展示、沟通情商或服务表现明显优秀，考官可向俱乐部申请破格录取，申请时需提交对局录像和陪玩资料",
        "破格录取需记录原因，并进入试用观察期",
        "娱乐陪不以技术结果作为主要考核标准",
        "具体考核结果以考官记录和平台复核为准",
    ])
    return poster.render()


def render_task_teaching_polished():
    poster = AutoPoster(
        "陪跑任务 / 技术教学",
        "任务推进｜地图陪跑｜1v1教学",
        chips=[("陪跑教学", 148), ("价格单位：钻石/小时", 260)],
    )
    poster.add_section_table("陪跑任务价格表", "TASK RUN", [280, 320, 320], [
        ["地图", "1p1", "1p2"],
        ["常规图", "20/小时", "30/小时"],
        ["机密图", "30/小时", "40/小时"],
        ["绝密图", "60/小时", "70/小时"],
        ["9格培培", "60/小时", "-"],
    ], 74, 29)
    poster.add_section_table("技术教学价格表", "TEACHING", [360, 260, 300], [
        ["服务", "价格", "说明"],
        ["1v1教学1p1", "80/小时", "60分钟"],
        ["1v1教学1p2", "90/小时", "含1陪2"],
    ], 76, 29)
    poster.add_rule_card("陪跑说明", "陪跑", [
        "陪跑任务以推进任务为主",
        "无需全装，不接人头或撤离率投诉",
        "机密图陪跑可选择指定监狱地图",
        "绝密图默认按绝密陪跑服务执行",
    ])
    poster.add_rule_card("教学说明", "教学", [
        "1v1教学专注技巧、路线、思路指导",
        "1p2教学为1名陪玩服务2名老板",
        "仅限赤岩及以上水平选手接单",
        "教学单不接受撤离率投诉",
    ])
    return poster.render()


def render_all_services_overview_polished():
    poster = AutoPoster(
        "全玩法 / 服务总览",
        "三角洲行动｜RYMO岩灼电竞服务体系",
        chips=[("全玩法总览", 180), ("价格单位：钻石", 204)],
    )
    poster.add_section_table("基础服务", "BASIC", [300, 230, 390], [
        ["玩法", "起步价", "说明"],
        ["超值体验", "128", "2名陪玩，保底物资"],
        ["娱乐陪玩", "50/小时起", "女陪/男陪/Pro"],
        ["陪跑任务", "20/小时起", "常规/机密/绝密"],
        ["技术教学", "80/小时起", "1p1/1p2技术指导"],
    ], 74, 27)
    poster.add_section_table("高阶服务", "ADVANCED", [300, 230, 390], [
        ["玩法", "起步价", "说明"],
        ["技术猛攻", "88/小时起", "赤岩/灼曜/圣尊"],
        ["物资护航", "118/小时起", "单陪/双陪"],
        ["保底清图", "88起", "机密/绝密/极速清图"],
        ["爆款趣味", "128起", "小巨人/七宗罪"],
    ], 74, 27)
    poster.add_rule_card("入口说明", "说明", [
        "老板可在小程序点单页选择对应玩法下单",
        "每类玩法均有单独介绍图，建议下单前先查看规则",
        "最终价格和服务标准以下单页与客服确认为准",
    ])
    return poster.render()


def load_price_book_rows():
    namespace = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with ZipFile(PRICE_BOOK) as archive:
        shared_strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared_root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in shared_root.findall("x:si", namespace):
                shared_strings.append("".join(node.text or "" for node in item.iter() if node.tag.endswith("}t")))
        sheet_root = ElementTree.fromstring(archive.read("xl/worksheets/sheet1.xml"))

    rows = {}
    for row in sheet_root.findall(".//x:sheetData/x:row", namespace):
        values = [None] * 6
        for cell in row.findall("x:c", namespace):
            reference = cell.attrib.get("r", "A1")
            column_letters = "".join(char for char in reference if char.isalpha())
            column = 0
            for char in column_letters:
                column = column * 26 + ord(char.upper()) - 64
            if not 1 <= column <= len(values):
                continue
            cell_type = cell.attrib.get("t")
            value_node = cell.find("x:v", namespace)
            if cell_type == "inlineStr":
                inline = cell.find("x:is", namespace)
                value = "".join(node.text or "" for node in inline.iter() if node.tag.endswith("}t")) if inline is not None else ""
            elif value_node is None:
                value = None
            elif cell_type == "s":
                value = shared_strings[int(value_node.text)]
            else:
                raw = value_node.text or ""
                try:
                    numeric = float(raw)
                    value = int(numeric) if numeric.is_integer() else numeric
                except ValueError:
                    value = raw
            values[column - 1] = value
        rows[int(row.attrib["r"])] = values
    return rows


def current_catalog_data():
    rows = load_price_book_rows()

    experience_row = rows[3]
    experience = [
        ["项目", "价格", "订单标准"],
        ["超值体验·体验款", str(experience_row[1]).split("元", 1)[0], "保888W｜2名陪玩"],
        ["超值体验·两局666W", "218", "两局666W撤离｜2名陪玩"],
        ["超值体验·两局款", "288", "两局888W撤离｜2名陪玩"],
    ]

    companion_basic = [
        ["项目", "陪玩", "价格"],
        ["娱乐单陪", "女陪", "65/小时"],
        ["娱乐单陪", "男陪", "60/小时"],
        ["娱乐双陪", "女陪", "110/小时"],
        ["娱乐双陪", "男陪", "100/小时"],
    ]
    companion_tech = [
        ["项目", "赤岩", "灼曜", "圣尊"],
        ["猛攻单陪", str(int(rows[13][2]) + 10), str(int(rows[13][3]) + 10), str(int(rows[13][4]) + 10)],
        ["猛攻双陪", "178", str(rows[15][3]), str(rows[15][4])],
        ["物资单陪", str(int(rows[16][2]) + 10), str(int(rows[16][3]) + 10), str(int(rows[16][4]) + 10)],
        ["物资双陪", str(rows[18][2]), str(rows[18][3]), str(rows[18][4])],
    ]

    escort_secret = [["分类", "档位", "价格", "保底", "订单标准"]]
    for row_number in range(21, 25):
        row = rows[row_number]
        escort_secret.append([row[0].replace("基础保底", ""), row[1], str(row[2]), row[3], row[4] or "基础保底"])
    escort_clear = [["项目", "时限", "价格", "保底", "订单标准"]]
    for row_number in range(28, 31):
        row = rows[row_number]
        escort_clear.append([row[0], row[1], str(row[2]), row[3], row[4]])

    fun_rows = [33, 34, 36, 47, 46, 42, 39, 38, 37, 35, 77, 44]
    fun = [["项目", "价格", "保底/目标", "玩法摘要"]]
    for row_number in fun_rows:
        row = rows[row_number]
        if row_number == 77:
            fun.append([row[0], str(row[1]).replace(".", "/"), "15 / 20 / 25人头", "人头制挑战"])
        elif row_number == 35:
            fun.append(["打手动物化", str(row[1]), row[2], row[3]])
        else:
            price_overrides = {"八险一金": "388", "倒反天罡": "336"}
            fun.append([row[0], price_overrides.get(row[0], str(row[1])), row[2], row[3]])

    return {
        "experience": experience,
        "companion_basic": companion_basic,
        "companion_tech": companion_tech,
        "escort_secret": escort_secret,
        "escort_clear": escort_clear,
        "fun": fun,
    }


def use_current_footer(svg_text):
    return (
        svg_text
        .replace("微信搜一搜 RYMO岩灼电竞", "东东电竞搜 RYMO岩灼电竞")
        .replace("｜最终解释权归RYMO所有", "")
        .replace("最终解释权归RYMO所有", "")
    )


def render_current_experience_catalog(data):
    poster = AutoPoster(
        "体验单 / 订单标准",
        "当前上架项目｜固定2名陪玩｜保底物资",
        chips=[("价格源：当前价格表", 242), ("价格单位：元", 172)],
    )
    poster.add_section_table(
        "当前上架项目", "EXPERIENCE", [320, 160, 440], data["experience"], 78, 27,
        column_font_sizes={0: 29, 1: 32},
    )
    poster.add_rule_card("体验单订单标准", "标准", [
        "打手包所有过点卡，老板只需携带战备入场",
        "老板死亡即判定炸单，保险塞够80W以上计入保底",
        "炸单保底：机密+25W、航天+60W、巴克什+55W、监狱+80W",
        "单局带出低于机密108W、绝密158W，不计保底并免费归老板",
        "打手阵亡、老板丢包撤离时，带出物资按50%计算保底",
    ])
    poster.add_rule_card("换人与售后", "售后", [
        "开局连续炸3把以上，或中途连续炸6把以上，可联系客服换打手",
        "对赌单前三把对陪玩不满意可免费换人，之后按点单须知执行",
        "需要售后请在三天内及时联系客服，超时不予售后",
        "恶意卡保底或服务态度问题，请及时录屏并联系售后",
    ])
    return use_current_footer(poster.render())


def render_current_companion_catalog(data):
    poster = AutoPoster(
        "陪玩 / 技术服务",
        "娱乐陪玩｜技术猛攻｜物资陪玩",
        chips=[("娱乐单陪 / 双陪", 230), ("价格单位：元/小时", 260)],
    )
    poster.add_section_table(
        "基础服务", "BASIC SERVICE", [360, 220, 340], data["companion_basic"], 76, 25,
        column_font_sizes={0: 29, 2: 31},
    )
    poster.add_section_table(
        "技术服务", "TECH SERVICE", [320, 200, 200, 200], data["companion_tech"], 72, 25,
        column_font_sizes={0: 29, 1: 29, 2: 29, 3: 29},
    )
    poster.add_rule_card("猛攻订单标准", "猛攻", [
        "老板死亡即判定炸单，保险内的物资不计入保底",
        "赤岩单陪：每小时击败数不低于6人",
        "灼曜单陪：每小时击败数不低于8人",
        "圣尊单陪：每小时击败数不低于10人",
        "赤岩双陪每小时不低于11人；灼曜不低于13人；圣尊不低于16人",
        "只按规则要求统计全队有效击败；未达标时该局击败不计入",
        "无撤离率要求；跨地图或跨段位按低段位标准执行",
        "猛攻单不提供战备损失补偿",
    ])
    poster.add_rule_card("物资订单标准", "物资", [
        "赤岩单陪：每小时撤离金额不少于500W",
        "灼曜单陪：每小时撤离金额不低于600W",
        "圣尊单陪：每小时撤离金额不低于800W",
        "赤岩双陪不低于900W；灼曜不低于1200W；圣尊不低于1400W",
        "物资单默认含6张物资卡，地图红卡带齐，其他金卡补齐至6张",
        "默认适用于绝密地图",
        "撤离失败补偿：航天中心+60W、巴克什+55W、监狱+80W",
    ])
    poster.add_rule_card("计费与售后", "售后", [
        "开始后前15分钟可免费更换",
        "开始15–45分钟按半小时计费，超过45分钟按一小时计费",
        "15分钟后因特殊原因更换，需补偿订单金额20%",
        "娱乐陪玩不接受技术投诉",
        "需要售后请在三天内及时联系客服，超时不予售后",
        "未单独标注的订单标准，以点单须知明细为主",
    ])
    return use_current_footer(poster.render())


def render_current_escort_catalog(data):
    poster = AutoPoster(
        "护航单 / 保底清图",
        "绝密保底｜极速清图｜点单须知为主",
        chips=[("当前上架项目", 190), ("价格单位：元", 172)],
    )
    poster.add_section_table(
        "基础保底", "GUARANTEE", [150, 130, 130, 160, 350], data["escort_secret"], 70, 23,
        column_font_sizes={0: 25, 1: 25, 2: 29},
    )
    poster.add_section_table(
        "极速清图", "CLEAR MAP", [170, 150, 140, 170, 290], data["escort_clear"], 74, 25,
        column_font_sizes={0: 27, 2: 29},
    )
    poster.add_rule_card("红货订单标准", "红货", [
        "红修、装备、红弹不算红",
        "百万级物资视为大红，允许约5W浮动",
        "两百万级物资视为超大红，允许约10W浮动",
        "三个大红可合并计算为一个超大红",
    ])
    poster.add_rule_card("炸单与结算", "结算", [
        "老板死亡即判定炸单，保险内的物资不计入保底",
        "炸单保底：机密+25W、航天+60W、巴克什+55W、监狱+80W",
        "单局带出低于机密108W、绝密158W，不计保底并免费归老板",
        "打手阵亡、老板丢包撤离时，带出物资按50%计算保底",
        "除体验单外，超出保底金额100W不视为卡保底；体验单到保底结单",
    ])
    poster.add_rule_card("兜底与配合", "须知", [
        "护航过程中两打手倒地死亡，老板兜底击败：两人头及以上不计保底",
        "老板兜底击败一人头时，该局计50%保底",
        "老板需听从指挥；不听指挥、挂机或跳河导致失败不补单",
        "开局连炸3把以上或中途连炸6把以上，可联系客服换打手",
        "需要售后请在三天内及时联系客服，超时不予售后",
    ])
    return use_current_footer(poster.render())


def render_current_fun_catalog(data):
    poster = AutoPoster(
        "趣味单 / 玩法规则",
        "当前上架项目｜保底目标｜玩法摘要",
        chips=[("价格源：当前价格表", 242), ("价格单位：元", 172)],
    )
    poster.add_section_table(
        "当前上架项目", "FUN SERVICE", [300, 210, 210, 200], data["fun"], 72, 22,
        column_font_sizes={0: 28, 1: 31, 2: 27, 3: 27},
    )
    fun_prices = {row[0]: row[1] for row in data["fun"][1:]}

    def fun_title(name):
        return f"{name}｜{fun_prices[name]}元"

    poster.add_rule_card(fun_title("小小巨人体验版"), "规则", [
        "初始10滴血，血量清空结单，血量上限20滴",
        "撤离金额低于500W不扣血",
        "撤离金额500W–800W扣5滴；高于800W扣10滴",
        "高于1100W扣12滴；高于1400W扣15滴；高于1700W扣20滴",
        "出心出泪减10滴",
        "撤离失败加2滴血",
        "老板丢包撤离按撤离失败处理，需正常携带战备并听从指挥",
    ])
    poster.add_rule_card(fun_title("八险一金"), "规则", [
        "订单保底1588W",
        "单局需摸够8个保险和10个小金",
        "大保险按2次计算，小保险按1次计算",
        "任务保险不计入保险数量",
    ])
    poster.add_rule_card(fun_title("指定称呼单"), "规则", [
        "订单保底888W",
        "称呼内容及称呼对象由老板决定",
        "禁止使用低俗称呼",
        "打手喊错一次，订单保底增加50W",
    ])
    poster.add_rule_card(fun_title("皇上驾到"), "规则", [
        "订单保底888W",
        "打手需称老板为皇上、陛下或娘娘",
        "倒地、出货投喂、遇敌时需说订单指定台词",
        "说错台词或漏称呼一次，订单保底增加50W",
    ])
    poster.add_rule_card(fun_title("我是赌怪"), "规则", [
        "订单基础保底888W",
        "摸出普通扑克牌，保底增加40W；大小王增加60W",
        "摸出对子，保底增加150W；顺子增加200W",
        "摸出王炸，保底增加300W",
    ])
    poster.add_rule_card(fun_title("趣味嘉豪单"), "规则", [
        "订单保底988W",
        "两名打手需使用粤语完成指定自我介绍",
        "击杀后需说：被我豪到了吗，小妹妹（气泡音）",
        "未按要求说指定台词，订单保底增加50W",
        "指定装备名称以订单页展示和客服确认为准",
    ])
    poster.add_rule_card(fun_title("倒反天罡"), "规则", [
        "老板吃饱后，由打手拿剩余物资，累计目标700W",
        "只统计成功撤离对局；打手仅可拿可出售物品",
        "玩法独有规则：撤离失败增加60W剩饭保底",
        "成功撤离后，老板可向客服索要打手收获截图",
    ])
    poster.add_rule_card(fun_title("真假话挑战"), "规则", [
        "老板每局有3次机会向打手说“出货了”",
        "打手只能回答“真的”或“假的”",
        "每答错一次，订单保底增加100W",
        "玩法独有规则：撤离失败增加60W保底，打够保底结单",
        "原资料标注“封底1888W”，具体上限以下单页确认为准",
    ])
    poster.add_rule_card(fun_title("不讲中文单"), "规则", [
        "订单保底888W",
        "打手从进队开始，全程使用中文以外的语言沟通",
        "每说错一次，订单保底增加50W",
    ])
    poster.add_rule_card(fun_title("打手动物化"), "规则", [
        "基础保底888W，封顶2888W",
        "打手每句话前须带老板指定的“哞哞哞”或“喵喵喵”",
        "每违反一次，订单保底增加50W",
        "打手不得故意不说话，否则当局老板带出物资不计入保底",
    ])
    poster.add_rule_card(fun_title("豺狼的日子"), "规则", [
        "简单版888元/15人头；进阶版1288元/20人头；困难版1688元/25人头",
        "每局摸出2格红，目标增加1人头；出红增加的人头仅计算当局",
        "撤离失败增加1人头；只统计成功撤离局的有效人头",
        "撤离成功收益未达到800W时，红和人头均不计算",
        "紫卡算1格红、金卡算2格红、红卡算4格红；巴克什房卡降一级",
        "必须将人头目标清零方可结单；默认航天，指定地图加10%",
        "老板不得故意抢头，需听从指挥；外挂导致失败需凭完整录像核实",
    ])
    poster.add_rule_card(fun_title("欧美猛攻"), "规则", [
        "订单保底1588W，仅统计成功撤离局",
        "成功撤离1–4杀，带出价值按0.5倍计算",
        "成功撤离5–6杀按1倍，7–9杀按1.5倍计算",
        "成功撤离10杀以上按2倍计算；0杀归零",
        "禁止养猪或重复击杀刷数据",
        "双倒、兜底、丢包撤与退单按点单须知和订单页规则执行",
    ])
    poster.add_rule_card("趣味单通用结算", "结算", [
        "老板死亡即判定炸单，保险内的物资不计入保底",
        "炸单保底：机密+25W、航天+60W、巴克什+55W、监狱+80W",
        "单局带出低于机密108W、绝密158W，不计保底并免费归老板",
        "打手阵亡、老板丢包撤离时，带出物资按50%计算保底",
        "具体玩法任务以订单页为准；未单独标注的标准以点单须知为主",
    ])
    poster.add_rule_card("体验与售后", "售后", [
        "老板需听从打手指挥，恶意影响正常结算时俱乐部有权结单",
        "开局连续炸3把以上，或中途连续炸6把以上，可联系客服换打手",
        "需要售后请在三天内及时联系客服，超时不予售后",
        "恶意卡保底或服务态度问题，请及时录屏并联系售后",
    ])
    return use_current_footer(poster.render())


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tech_loot_target = OUTPUT_DIR / "roem-tech-loot-polished.svg"
    tech_loot_target.write_text(render_tech_loot_polished(), encoding="utf-8")
    print(tech_loot_target)
    little_giant_target = OUTPUT_DIR / "roem-little-giant-polished.svg"
    little_giant_target.write_text(render_little_giant_polished(), encoding="utf-8")
    print(little_giant_target)
    seven_target = OUTPUT_DIR / "roem-seven-polished.svg"
    seven_target.write_text(render_seven_polished(), encoding="utf-8")
    print(seven_target)
    guarantee_clear_target = OUTPUT_DIR / "roem-guarantee-clear-polished.svg"
    guarantee_clear_target.write_text(render_guarantee_clear_polished(), encoding="utf-8")
    print(guarantee_clear_target)
    basic_services_target = OUTPUT_DIR / "roem-basic-services-polished.svg"
    basic_services_target.write_text(render_basic_services_polished(), encoding="utf-8")
    print(basic_services_target)
    trial_target = OUTPUT_DIR / "roem-trial-polished.svg"
    trial_target.write_text(render_trial_polished(), encoding="utf-8")
    print(trial_target)
    entertainment_target = OUTPUT_DIR / "roem-entertainment-polished.svg"
    entertainment_target.write_text(render_entertainment_polished(), encoding="utf-8")
    print(entertainment_target)
    player_exam_target = OUTPUT_DIR / "roem-player-exam-rules.svg"
    player_exam_target.write_text(render_player_exam_rules(), encoding="utf-8")
    print(player_exam_target)
    entertainment_exam_target = OUTPUT_DIR / "roem-entertainment-exam-rules.svg"
    entertainment_exam_target.write_text(render_entertainment_exam_rules(), encoding="utf-8")
    print(entertainment_exam_target)
    task_teaching_target = OUTPUT_DIR / "roem-task-teaching-polished.svg"
    task_teaching_target.write_text(render_task_teaching_polished(), encoding="utf-8")
    print(task_teaching_target)
    overview_target = OUTPUT_DIR / "roem-all-services-overview-polished.svg"
    overview_target.write_text(render_all_services_overview_polished(), encoding="utf-8")
    print(overview_target)
    current_data = current_catalog_data()
    current_posters = {
        "roem-price-experience.svg": render_current_experience_catalog(current_data),
        "roem-price-fun.svg": render_current_fun_catalog(current_data),
        "roem-price-escort.svg": render_current_escort_catalog(current_data),
        "roem-price-companion.svg": render_current_companion_catalog(current_data),
    }
    for filename, svg_text in current_posters.items():
        target = OUTPUT_DIR / filename
        target.write_text(svg_text, encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
