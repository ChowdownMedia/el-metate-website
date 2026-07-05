#!/usr/bin/env python3
"""Re-chrome /menu/ onto the El Metate theme. CONTENT FROZEN: the <main>...</main>
block is copied byte-for-byte from the harvested shell. We only swap head/header/
footer to the new theme and append the menu component CSS (ported from the old
brand-tokens/styles/components stylesheets to the new theme tokens) so the frozen
markup still renders. main.js already drives the section filter (menu-chip ->
menu-category.is-hidden) and is reused unchanged."""
import pathlib
ROOT = pathlib.Path(__file__).parent
HOME = (ROOT / "index.html").read_text()
SHELL_MENU = (ROOT / "menu" / "index.html").read_text()

# 1. Frozen content, verbatim
main = SHELL_MENU[SHELL_MENU.index("<main"):SHELL_MENU.index("</main>") + len("</main>")]
assert len(main) == 94779, f"main byte-len drifted: {len(main)}"  # 94779 = post em-dash cleanup

# 2. Reuse home head+header and footer->end (theme chrome, modal, SITE_CONFIG, main.js)
head_header = HOME[:HOME.index("</header>") + len("</header>")]
tail = HOME[HOME.index("<footer"):]

# 3. Swap head meta + nav active state for the menu page
head_header = head_header.replace(
    "<title>El Metate Mexican Restaurants | Fresh, Handmade Daily in Tennessee</title>",
    "<title>Menu | El Metate Mexican Restaurants, Fresh Mexican in Tennessee</title>")
head_header = head_header.replace(
    '<link rel="canonical" href="https://elmetatemexicanrestaurants.com/">',
    '<link rel="canonical" href="https://elmetatemexicanrestaurants.com/menu/">')
head_header = head_header.replace(
    '<meta property="og:url" content="https://elmetatemexicanrestaurants.com/">',
    '<meta property="og:url" content="https://elmetatemexicanrestaurants.com/menu/">')
head_header = head_header.replace(
    '<meta property="og:title" content="El Metate Mexican Restaurants | Fresh, Handmade Daily">',
    '<meta property="og:title" content="Menu | El Metate Mexican Restaurants">')
# nav active: Home -> Menu (both desktop nav and mobnav)
head_header = head_header.replace(
    '<a href="/" style="color:var(--terra)">Home</a><a href="/menu/">Menu</a><a href="/locations/">Locations</a>',
    '<a href="/">Home</a><a href="/menu/" style="color:var(--terra)">Menu</a><a href="/locations/">Locations</a>')

# 4. Menu component CSS ported to the new theme tokens, injected before </style>
MENU_CSS = """
/* --- Menu (frozen content chrome, ported from shell CSS to El Metate theme) --- */
.container{width:90%;max-width:1280px;margin:0 auto}
@media(max-width:600px){.container{width:94%}}
.page-hero{margin-top:0;background:var(--cream);color:var(--ink);padding:56px 0 28px;text-align:center}
.page-hero h1{font-family:'Baloo 2',sans-serif;font-weight:800;letter-spacing:.01em;font-size:clamp(2rem,1.5rem + 2vw,3.2rem);margin:0;color:var(--ink)}
.page-hero p{font-family:'Hanken Grotesk',system-ui,sans-serif;color:var(--ink-2);margin-top:8px}
.menu-section{padding:20px 0 56px;background:var(--cream);position:relative}
.menu-section > .container{position:relative;z-index:1}
.menu-panel{display:none}
.menu-panel.active{display:block}
.menu-rail{position:sticky;top:80px;z-index:30;margin:0 0 32px;padding:8px 0;background:color-mix(in srgb,var(--cream) 88%,transparent);backdrop-filter:saturate(1.1) blur(6px);border-bottom:1px solid rgba(43,27,16,.10)}
.menu-rail-track{display:flex;gap:8px;justify-content:safe center;overflow-x:auto;scrollbar-width:none;max-width:1100px;margin:0 auto;padding:2px 4px;-webkit-overflow-scrolling:touch}
.menu-rail-track::-webkit-scrollbar{display:none}
.menu-chip{flex:0 0 auto;font-family:'Baloo 2',sans-serif;text-transform:uppercase;letter-spacing:.03em;font-size:.8rem;white-space:nowrap;cursor:pointer;appearance:none;padding:8px 16px;border-radius:999px;text-decoration:none;color:var(--ink-2);background:transparent;border:1.5px solid rgba(43,27,16,.16);transition:all .2s;min-height:36px;display:flex;align-items:center}
.menu-chip:hover{border-color:var(--terra);color:var(--terra)}
.menu-chip.active{background:var(--terra);color:#fff;border-color:var(--terra)}
.menu-category{margin-bottom:16px}
.menu-category.is-hidden{display:none}
.menu-category > h2{font-family:'Baloo 2',sans-serif;font-weight:800;text-transform:uppercase;color:var(--ink);font-size:1.8rem;text-align:center;margin-bottom:6px}
.menu-category-rule{width:60px;height:3px;background:var(--gold);margin:0 auto 14px;border-radius:2px}
.menu-cat-desc{max-width:760px;margin:0 auto 26px;text-align:center;font-family:'Hanken Grotesk',system-ui,sans-serif;color:var(--ink-2);font-size:.92rem;line-height:1.55}
.menu-items{column-count:3;column-gap:40px;max-width:1100px;margin:0 auto}
@media(max-width:992px){.menu-items{column-count:2}}
@media(max-width:600px){.menu-items{column-count:1}}
.menu-item{break-inside:avoid;margin-bottom:16px;padding-bottom:14px;border-bottom:1px dashed rgba(43,27,16,.14)}
.menu-item-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.menu-item-name{font-family:'Hanken Grotesk',system-ui,sans-serif;font-weight:700;color:var(--ink);font-size:1.05rem}
.menu-item-price{font-family:'Baloo 2',sans-serif;color:var(--terra-deep);white-space:nowrap;font-size:1rem}
.menu-item-desc{font-family:'Hanken Grotesk',system-ui,sans-serif;color:var(--ink-2);font-size:.92rem;line-height:1.5;margin-top:4px}
.menu-item-photo{width:100%;height:210px;object-fit:cover;border-radius:12px;margin-top:12px;display:block;box-shadow:0 4px 14px rgba(43,27,16,.12)}
.menu-panel.all-mode .menu-item-photo{display:none}
.menu-allergen{max-width:820px;margin:48px auto 0;padding-top:22px;border-top:1px solid rgba(43,27,16,.10);font-size:.78rem;color:#9b8a72;font-style:italic;text-align:center;line-height:1.5;font-family:'Hanken Grotesk',system-ui,sans-serif}
.menu-large .menu-rail-track{justify-content:flex-start;scrollbar-width:thin;padding-bottom:8px}
.menu-large .menu-rail-track::-webkit-scrollbar{display:block;height:4px}
.menu-large .menu-rail-track::-webkit-scrollbar-track{background:transparent}
.menu-large .menu-rail-track::-webkit-scrollbar-thumb{background:rgba(43,27,16,.16);border-radius:2px}
.menu-large .menu-item-head{flex-wrap:wrap}
.menu-large .menu-item-name{min-width:0;flex:1 1 auto;overflow-wrap:anywhere}
.menu-large .menu-item-price{white-space:normal;flex:0 1 auto;text-align:right;overflow-wrap:anywhere}
"""
assert "</style>" in head_header
head_header = head_header.replace("</style>", MENU_CSS + "</style>", 1)

out = head_header + "\n" + main + "\n" + tail
(ROOT / "menu" / "index.html").write_text(out)
print("menu/index.html:", len(out), "bytes | main preserved:", len(main))
