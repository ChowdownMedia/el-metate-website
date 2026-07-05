#!/usr/bin/env python3
"""Build the standalone /locations/ grid page, reusing the home page's
head + header + footer + modal so the theme CSS stays byte-identical."""
import re, pathlib
ROOT = pathlib.Path(__file__).parent
HOME = (ROOT / "index.html").read_text()

MK = '<svg class="mk" viewBox="0 0 100 100" aria-hidden="true"><path fill-rule="evenodd" d="M14 36 a36 11 0 0 1 72 0 C86 62 71 77 50 77 C29 77 14 62 14 36 Z M26 34 a24 7 0 1 0 48 0 a24 7 0 1 0 -48 0 Z"/><path d="M28 74 l-6 17 l9 0 l4 -13 z"/><path d="M45 76 l0 16 l10 0 l0 -16 z"/><path d="M72 74 l6 17 l-9 0 l-4 -13 z"/></svg>'

# head+header (up to end of </header>) and footer->end, reused verbatim
head_header = HOME[:HOME.index("</header>") + len("</header>")]
tail = HOME[HOME.index("<footer"):]

# swap <head> title/canonical/og for the locations page
head_header = head_header.replace("<title>El Metate Mexican Restaurants | Fresh, Handmade Daily in Tennessee</title>",
                                  "<title>Locations | El Metate Mexican Restaurants, 5 in Tennessee</title>")
head_header = head_header.replace('<link rel="canonical" href="https://elmetatemexicanrestaurants.com/">',
                                  '<link rel="canonical" href="https://elmetatemexicanrestaurants.com/locations/">')
head_header = head_header.replace('<meta property="og:url" content="https://elmetatemexicanrestaurants.com/">',
                                  '<meta property="og:url" content="https://elmetatemexicanrestaurants.com/locations/">')
# nav active state: Home -> Locations
head_header = head_header.replace('<a href="/" style="color:var(--terra)">Home</a><a href="/menu/">Menu</a><a href="/locations/">Locations</a>',
                                  '<a href="/">Home</a><a href="/menu/">Menu</a><a href="/locations/" style="color:var(--terra)">Locations</a>')

LOCS = [
 ("dunlap","Dunlap","em-hero-accent.webp","16952 Rankin Ave, Unit D","Dunlap, TN 37327","(423) 949-6132","+14239496132","Mon-Thu 10:30a-9p, Fri-Sat til 10p","https://online.skytab.com/s/elmetate2dunlap",True),
 ("soddy-daisy","Soddy-Daisy","int-soddy-daisy.webp","9332 Dayton Pike #110","Soddy-Daisy, TN 37379","(423) 332-3190","+14233323190","Mon-Thu 11a-9:30p, Fri-Sat til 10p","https://online.skytab.com/s/elmetate3soddydaisy",True),
 ("signal-mountain","Signal Mountain","int-signal-mountain.webp","1238 Taft Hwy","Signal Mountain, TN 37377","(423) 886-0054","+14238860054","Mon-Thu 11a-9:30p, Fri-Sat til 10p","https://online.skytab.com/s/elmetatesignalmountain",False),
 ("hixson","Hixson","int-hixson.webp","5922 Hixson Pike","Hixson, TN 37343","(423) 842-1400","+14238421400","Mon-Thu 11a-9:30p, Fri-Sat til 10p","https://online.skytab.com/fe7dbd09be677ecceb54dcec4fb26e5f",True),
 ("knoxville","Knoxville","em-sign.webp","4221 Sam Walton Way","Knoxville, TN 37938","(865) 922-0867","+18659220867","Every day 11a-10p","https://online.skytab.com/8068d120b28cd73960869cd7367009d4",True),
]

def card(slug, city, img, street, cityzip, ph, tel, hours, skytab, vip):
    vip_btn = f'<a class="btn btn--gold" href="/{slug}/vip/">Join VIP</a>' if vip else ''
    return (f'<article class="card reveal"><a href="/{slug}/" style="display:block"><div class="locimg">'
            f'<img src="/assets/images/{img}" alt="El Metate {city}" loading="lazy" class="dishimg" width="400" height="250"></div></a>'
            f'<div style="padding:var(--sp-5)"><div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.5rem">'
            f'<span class="stamp" style="width:40px;height:40px;box-shadow:2px 2px 0 var(--ink)">{MK}</span>'
            f'<h3 style="font-size:var(--fs-h3)">{city}</h3></div>'
            f'<p style="color:var(--ink-2)">{street}<br>{cityzip}</p>'
            f'<a href="tel:{tel}" style="color:var(--blue);font-weight:600;display:inline-block;margin-top:.4rem">{ph}</a>'
            f'<p style="font-size:.82rem;color:var(--ink-2);margin-top:.3rem">{hours}</p>'
            f'<div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:var(--sp-4)">'
            f'<a class="btn btn--primary" href="/{slug}/">Visit</a>'
            f'<a class="btn btn--blue" href="{skytab}" target="_blank" rel="noopener">Order Pickup</a>'
            f'{vip_btn}</div></div></article>')

hero = ('<section class="section" style="padding-top:var(--sp-7);padding-bottom:var(--sp-6);text-align:center;'
        'background:radial-gradient(620px 420px at 50% 0%,rgba(242,167,27,.20),transparent 62%)">'
        f'<div class="wrap"><span class="eyebrow pop">{MK} Tennessee</span>'
        '<h1 style="font-size:var(--fs-hero);margin:var(--sp-3) 0 var(--sp-4)">Find your <span style="color:var(--terra)">El Metate</span></h1>'
        '<p class="reveal" style="font-size:1.15rem;max-width:46ch;margin:0 auto;color:var(--ink-2)">Five neighborhood kitchens across Tennessee, one family recipe. Pick a location to order pickup, see hours, or join its VIP club.</p></div></section>')

grid = ('<section class="section sec-blue-tint" id="locations"><div class="wrap"><div class="grid-loc">'
        + "\n".join(card(*l) for l in LOCS) + '</div></div></section>')

out = head_header + "\n" + hero + "\n" + grid + "\n" + tail
(ROOT / "locations" / "index.html").write_text(out)
print("locations/index.html:", len(out), "bytes")
