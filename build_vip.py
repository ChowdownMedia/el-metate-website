#!/usr/bin/env python3
"""Build the 4 VIP pages (Dunlap/Knoxville/Hixson/Soddy-Daisy). Reuses the
location master's head+CSS+footer+modal+scripts so theme + GHL wiring stay
identical; injects the shell's real vip-form + vip-result (preserved verbatim)
so main.js issues the Boomerangme wallet pass. Signal Mountain has no VIP
(not live in GHL) and is skipped."""
import pathlib
ROOT = pathlib.Path(__file__).parent
M = (ROOT / "dunlap" / "index.html").read_text()

MK = '<svg class="mk" viewBox="0 0 100 100" aria-hidden="true"><path fill-rule="evenodd" d="M14 36 a36 11 0 0 1 72 0 C86 62 71 77 50 77 C29 77 14 62 14 36 Z M26 34 a24 7 0 1 0 48 0 a24 7 0 1 0 -48 0 Z"/><path d="M28 74 l-6 17 l9 0 l4 -13 z"/><path d="M45 76 l0 16 l10 0 l0 -16 z"/><path d="M72 74 l6 17 l-9 0 l-4 -13 z"/></svg>'
GMK = '<span class="stamp" style="width:34px;height:34px;box-shadow:2px 2px 0 var(--ink);background:var(--gold);color:var(--ink)">' + MK + '</span>'

VIP_CSS = (".form-row{display:grid;grid-template-columns:1fr 1fr;gap:var(--sp-4)}"
           "@media(max-width:520px){.form-row{grid-template-columns:1fr}}"
           ".vip-result{text-align:center;padding:var(--sp-4) 0}"
           ".vip-result-h{font-size:var(--fs-h3);color:var(--green);margin-bottom:.4rem}"
           ".vip-result-sub{color:var(--ink-2);margin-bottom:var(--sp-4)}"
           ".vip-wallet-btns{display:flex;flex-direction:column;gap:.6rem}"
           ".vip-wallet{justify-content:center;width:100%}")

# Reusable regions from the location master
head = M[:M.index("</head>")].replace("</style>", VIP_CSS + "</style>")
header = M[M.index("<header"):M.index("</header>") + len("</header>")]
tail = M[M.index("<footer"):]   # footer + fab + modal + SITE_CONFIG + scripts

VIP_FORM = ('<form class="lead-form vip-form" autocomplete="on" data-form-type="vip">'
 '<input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
 '<div class="form-row"><div class="form-group"><label for="vf-first">First Name</label><input type="text" id="vf-first" name="firstName" required></div>'
 '<div class="form-group"><label for="vf-last">Last Name</label><input type="text" id="vf-last" name="lastName" required></div></div>'
 '<div class="form-row"><div class="form-group"><label for="vf-phone">Phone</label><input type="tel" id="vf-phone" name="phone" required></div>'
 '<div class="form-group"><label for="vf-email">Email</label><input type="email" id="vf-email" name="email" required></div></div>'
 '<div class="form-group"><label for="vf-dob">Date of Birth</label><input type="date" id="vf-dob" name="dateOfBirth" required></div>'
 '<p class="form-error"></p><button type="submit" class="btn btn--primary btn--lg" style="width:100%;justify-content:center">Get My Pass</button></form>'
 '<div class="vip-result" hidden><h3 class="vip-result-h">You\'re in! Your pass is ready.</h3>'
 '<p class="vip-result-sub">Add your rewards pass to your phone:</p><div class="vip-wallet-btns"></div></div>')

def perk(t):
    return f'<li style="display:flex;align-items:center;gap:.7rem">{GMK}<span style="min-width:0">{t}</span></li>'

def page(slug, city, street, cityzip, ph, tel, skytab, client, td, fs):
    mapq = (street + " " + city.replace("-", " ") + " TN " + cityzip.split()[-1]).replace(",", "").replace(" ", "+")
    hero = ('<section class="section" style="padding-top:var(--sp-7);background:var(--blue);border-bottom:2.5px solid var(--ink);color:var(--cream)"><div class="wrap two"><div>'
     f'<span class="eyebrow pop" style="color:var(--gold-soft)">{MK} {city} &middot; VIP Club</span>'
     f'<h1 class="reveal" style="font-size:var(--fs-hero);margin:var(--sp-4) 0;color:var(--paper)">Join the<br>{city} <span style="color:var(--gold)">VIP</span>.</h1>'
     f'<p class="reveal" style="font-size:1.15rem;max-width:40ch;color:rgba(251,242,222,.9)">Become a regular at <a href="/{slug}/" style="color:var(--gold-soft);text-decoration:underline">El Metate {city}</a>. Free chips &amp; queso on us, a treat on your birthday, and first dibs on fiesta nights. Sign up in 30 seconds.</p>'
     '<ul class="reveal" style="list-style:none;padding:0;margin:var(--sp-5) 0 0;display:flex;flex-direction:column;gap:.7rem">'
     + perk("A free birthday dessert, every year") + perk(f"Members-only {city} specials &amp; early event access") + perk("Chips &amp; queso on the house when you join")
     + '</ul></div><div style="position:relative">'
     f'<span class="stamp spin pop" style="position:absolute;top:-28px;right:14px;width:88px;height:88px;background:var(--gold);color:var(--ink);z-index:2">{MK}</span>'
     '<div class="card reveal" style="padding:var(--sp-6);background:var(--paper);color:var(--ink)">'
     f'<h2 style="font-size:var(--fs-h3);margin-bottom:.25rem">Become a {city} VIP</h2>'
     f'<p style="color:var(--ink-2);margin-bottom:var(--sp-5)">Joining at <b>El Metate {city}</b> is free. Just tell us where to send the good stuff.</p>'
     + VIP_FORM + '</div></div></div></section>')
    marquee = M[M.index('<div class="marquee"'):M.index('</div></div>', M.index('<div class="marquee"'))+len('</div></div>')]
    visit = ('<section class="section" id="visit-loc"><div class="wrap"><div style="text-align:center;margin-bottom:var(--sp-6)">'
     f'<span class="eyebrow reveal">{MK} Your Home Kitchen</span>'
     f'<h2 class="reveal" style="font-size:var(--fs-h1);margin-top:var(--sp-3)">Redeem at El Metate {city}</h2>'
     '<p class="reveal" style="max-width:46ch;margin:var(--sp-3) auto 0;color:var(--ink-2)">Show your VIP perks next time you stop in. Here is where to find us.</p></div>'
     '<div class="two" style="align-items:stretch"><div class="ph ph--wide reveal" style="aspect-ratio:4/3;min-height:280px;padding:0">'
     f'<button type="button" class="map-facade" data-map-src="https://www.google.com/maps?q={mapq}&output=embed" aria-label="Load map for El Metate {city}">{MK}'
     f'<b>{street}</b><span>{cityzip}</span><span class="btn btn--blue">View Map</span></button></div>'
     '<div class="card reveal" style="padding:var(--sp-6)"><h3 style="font-size:var(--fs-h3);margin-bottom:var(--sp-3)">Business Hours</h3>'
     '<table style="width:100%;border-collapse:collapse;font-size:1rem">'
     f'<tr><td style="padding:.5rem 0;border-bottom:1.5px dashed var(--line);font-weight:600">Mon - Thu</td><td style="padding:.5rem 0;border-bottom:1.5px dashed var(--line);text-align:right;color:var(--ink-2)">{td}</td></tr>'
     f'<tr><td style="padding:.5rem 0;border-bottom:1.5px dashed var(--line);font-weight:600">Friday</td><td style="padding:.5rem 0;border-bottom:1.5px dashed var(--line);text-align:right;color:var(--ink-2)">{fs}</td></tr>'
     f'<tr><td style="padding:.5rem 0;border-bottom:1.5px dashed var(--line);font-weight:600">Saturday</td><td style="padding:.5rem 0;border-bottom:1.5px dashed var(--line);text-align:right;color:var(--ink-2)">{fs}</td></tr>'
     f'<tr><td style="padding:.5rem 0;font-weight:600">Sunday</td><td style="padding:.5rem 0;text-align:right;color:var(--ink-2)">{td}</td></tr></table>'
     f'<div style="margin-top:var(--sp-5)"><div style="font-family:\'Baloo 2\';font-weight:700;color:var(--terra);font-size:.85rem;letter-spacing:.1em">CONTACT</div>'
     f'<p style="margin-top:.3rem">{street}<br>{cityzip}</p><a href="tel:{tel}" style="color:var(--blue);font-weight:600;display:inline-block;margin-top:.4rem">{ph}</a></div>'
     f'<div style="display:flex;gap:.6rem;flex-wrap:wrap;margin-top:var(--sp-5)"><a class="btn btn--primary" href="{skytab}" target="_blank" rel="noopener">Order Online</a>'
     f'<a class="btn btn--gold" href="/{slug}/">Visit {city} Page</a></div></div></div></div></section>')

    # head per page
    h = head.replace("<title>El Metate | Dunlap, TN</title>", f"<title>Become a VIP | El Metate {city}</title>")
    h = h.replace('<link rel="canonical" href="https://elmetatemexicanrestaurants.com/dunlap/">',
                  f'<link rel="canonical" href="https://elmetatemexicanrestaurants.com/{slug}/vip/">')
    h = h.replace('content="https://elmetatemexicanrestaurants.com/dunlap/"', f'content="https://elmetatemexicanrestaurants.com/{slug}/vip/"')
    h = h.replace("El Metate | Dunlap, TN", f"Become a VIP | El Metate {city}")
    # strip the location-page Restaurant/Breadcrumb JSON-LD (not needed on VIP); keep it simple
    # header per page: nav active = Become a VIP; order link = skytab
    hd = header.replace('<a href="/dunlap/vip/">Become a VIP</a>', f'<a href="/{slug}/vip/" style="color:var(--terra)">Become a VIP</a>')
    hd = hd.replace('<a href="/locations/" style="color:var(--terra)">Locations</a>', '<a href="/locations/">Locations</a>')
    hd = hd.replace("https://online.skytab.com/s/elmetate2dunlap", skytab)
    hd = hd.replace("/dunlap/", f"/{slug}/")
    # tail per page: swap skytab, client, city refs, address (modal SMS consent), map/paths
    t = tail.replace("https://online.skytab.com/s/elmetate2dunlap", skytab)
    t = t.replace('"forms": {"endpoint": "https://chowdownos.onrender.com/api/public/forms/submit", "client": 364}',
                  f'"forms": {{"endpoint": "https://chowdownos.onrender.com/api/public/forms/submit", "client": {client}}}')
    t = t.replace('"vip": {"endpoint": "https://chowdownos.onrender.com/api/public/vip/signup", "client": 364}',
                  f'"vip": {{"endpoint": "https://chowdownos.onrender.com/api/public/vip/signup", "client": {client}}}')
    t = t.replace("El Metate - Dunlap", f"El Metate - {city}")   # modal SMS consent
    t = t.replace("/dunlap/", f"/{slug}/")

    out = h + "</head><body>\n" + hd + hero + marquee + visit + t
    (ROOT / slug / "vip" / "index.html").write_text(out)
    print(f"{slug}/vip: {len(out)} bytes  client={client}")

# per-location VIP data (Signal Mountain excluded: not live in GHL)
page("dunlap","Dunlap","16952 Rankin Ave, Unit D","Dunlap, TN 37327","(423) 949-6132","+14239496132","https://online.skytab.com/s/elmetate2dunlap",364,"10:30 AM - 9:00 PM","10:30 AM - 10:00 PM")
page("knoxville","Knoxville","4221 Sam Walton Way","Knoxville, TN 37938","(865) 922-0867","+18659220867","https://online.skytab.com/8068d120b28cd73960869cd7367009d4",365,"11:00 AM - 10:00 PM","11:00 AM - 10:00 PM")
page("hixson","Hixson","5922 Hixson Pike","Hixson, TN 37343","(423) 842-1400","+14238421400","https://online.skytab.com/fe7dbd09be677ecceb54dcec4fb26e5f",366,"11:00 AM - 9:30 PM","11:00 AM - 10:00 PM")
page("soddy-daisy","Soddy-Daisy","9332 Dayton Pike #110","Soddy-Daisy, TN 37379","(423) 332-3190","+14233323190","https://online.skytab.com/s/elmetate3soddydaisy",367,"11:00 AM - 9:30 PM","11:00 AM - 10:00 PM")
print("done")
