#!/usr/bin/env python3
"""Generate El Metate location pages from the approved Dunlap master.
Ordered, specific replacements (URLs/paths first, then display text) so we
never corrupt the SkyTab slug or the /dunlap/ paths."""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
MASTER = (ROOT / "dunlap" / "index.html").read_text()

def review_card(text, name, city):
    stamp = ('<span class="stamp" style="width:38px;height:38px;box-shadow:2px 2px 0 var(--ink)">'
             '<svg class="mk" viewBox="0 0 100 100" aria-hidden="true"><path fill-rule="evenodd" d="M14 36 a36 11 0 0 1 72 0 C86 62 71 77 50 77 C29 77 14 62 14 36 Z M26 34 a24 7 0 1 0 48 0 a24 7 0 1 0 -48 0 Z"/><path d="M28 74 l-6 17 l9 0 l4 -13 z"/><path d="M45 76 l0 16 l10 0 l0 -16 z"/><path d="M72 74 l6 17 l-9 0 l-4 -13 z"/></svg></span>')
    return ('<article class="card" style="padding:var(--sp-5);display:flex;flex-direction:column;gap:.7rem">'
            '<div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
            f'<p style="font-size:1.05rem">"{text}"</p>'
            '<div style="margin-top:auto;display:flex;align-items:center;gap:.6rem;padding-top:.6rem;border-top:1.5px dashed var(--line)">'
            f'{stamp}<div><b style="font-family:\'Baloo 2\';font-weight:700">{name}</b>'
            f'<div style="font-size:.8rem;color:var(--ink-2)">{city}</div></div></div></article>')

LOCS = {
 "hixson": {
   "city":"Hixson","zip":"37343","street":"5922 Hixson Pike","street_name":"Hixson Pike",
   "phone_disp":"(423) 842-1400","phone_tel":"+14238421400",
   "skytab":"https://online.skytab.com/fe7dbd09be677ecceb54dcec4fb26e5f",
   "delivery":"https://www.ubereats.com/store/el-metate-hixson-pike/oyqAIRg2VFu8RUvg9bf9jw",
   "client":366,"hero":"int-hixson.webp","story":"int-hixson-2.webp",
   "reviews":[
     ("Our family loves El Metate. The kids always enjoy their food, and on date night we love the atmosphere and margaritas. The passion margarita is the best ever, and there are plenty of meatless options with tons of flavor.","Bri M."),
     ("Great food. Well worth the drive from Chattanooga. Best margarita I have had.","Nancy H."),
     ("It is delicious. The wait staff is attentive. Just a really good place to grab a bite to eat.","Wanda D."),
     ("What a nice Mexican restaurant! We came for a friend's going away party and the staff was super friendly. The salsa was very fresh and the cheese dip was great. I had the grande steak quesadilla and it was awesome, and the margaritas were great too!","Lee C."),
     ("Always enjoy our evening out at El Metate. We have made it a weekly thing. The food has always been hot and fresh, the servers have been great, and the Texas margaritas are awesome!","Raymond S."),
   ],
 },
 "knoxville": {
   "city":"Knoxville","zip":"37938","street":"4221 Sam Walton Way","street_name":"Sam Walton Way",
   "phone_disp":"(865) 922-0867","phone_tel":"+18659220867",
   "skytab":"https://online.skytab.com/8068d120b28cd73960869cd7367009d4",
   "delivery":None,"client":365,"hero":"em-sign.webp","story":"em-story.webp",
   "reviews":[
     ("Very clean, and the service was excellent as always. We literally sat down and our waiter quickly brought out hot fresh chips and salsa within three minutes. Food was very good and the portions were huge.","Ron A."),
     ("An excellent example of a fine Mexican eatery! Wonderful staff, and they make the best fried ice cream around. Their shredded beef and chicken tacos are flavorful and generous, and the chicken tortilla soup is amazing. Service is always friendly and attentive. Highly recommend!","Joyce W."),
     ("Ordered the birria tacos and was absolutely blown away, they were so delicious! Definitely will come back and highly recommend.","Jordan F."),
     ("Great food and friendly staff! I always bring my friends here.","Carlos I."),
     ("El Metate has been our go to whenever we want Mexican food in our area.","Rowena E."),
   ],
 },
 "soddy-daisy": {
   "city":"Soddy-Daisy","zip":"37379","street":"9332 Dayton Pike #110","street_name":"Dayton Pike",
   "phone_disp":"(423) 332-3190","phone_tel":"+14233323190",
   "skytab":"https://online.skytab.com/s/elmetate3soddydaisy",
   "delivery":None,"client":367,"hero":"int-soddy-daisy.webp","story":"int-soddy-daisy-2.webp",
   "reviews":[
     ("This is my favorite local Mexican restaurant. The service is fast and the food is always hot and comes out quickly.","Ash V."),
     ("I have lived in Texas my entire life and consider myself a Mexican food enthusiast, and the Hawaiian burrito is one of the best burritos I have ever had. The salsa may be the best I have ever had. 10 out of 10.","Charles W."),
     ("Just passing through and thought we would stop. Had the Hawaiian Burrito and it was amazing, huge, and had a bit of everything. The salsa was up there with the best from back home. Service was super fast and friendly.","Ricki T."),
     ("We had a large take-out taco bar order for our wedding. The food was prepared on time, delicious, and exactly as ordered. The price was very affordable and convenient.","Jeanette M."),
     ("Drove all the way from Alabama and this is a perfect ten Mexican spot. Mouth watering, jaw dropping, heaven sent, no notes!","Lillie P."),
   ],
 },
 "signal-mountain": {
   "city":"Signal Mountain","zip":"37377","street":"1238 Taft Hwy","street_name":"Taft Hwy",
   "phone_disp":"(423) 886-0054","phone_tel":"+14238860054",
   "skytab":"https://online.skytab.com/s/elmetatesignalmountain",
   "delivery":None,"client":None,"hero":"int-signal-mountain.webp","story":"int-signal-mountain-2.webp",
   "reviews":[
     ("The locals' number one spot to enjoy great food and drinks. Friendly staff and management treat regulars like family, with excellent service. Clean restaurant, good atmosphere, and a great place to celebrate a birthday with friends.","Michael L."),
     ("Hidden gem. The food here was so good and our waiter Luis was superb. Huge portions for the price, and the standout was the al pastor. The drinks were also fantastic and the dessert was absolutely delicious!","Katiria O."),
     ("The staff on Signal Mountain are fantastic! Food is always on point and margaritas can be made custom. Recommend the Don Julio Blanco and the chicken tortilla soup.","Jason G."),
     ("Get a pastor-filled burrito with fresh grilled jalapenos. It is phenomenal! They actually season the jalapenos too, which is a first among places I have ordered grilled jalapenos.","Michael M."),
     ("Our favorite Mexican restaurant here on the mountain! The staff are super friendly and always so welcoming.","Jennifer M."),
   ],
 },
}

DUN_SKYTAB = "https://online.skytab.com/s/elmetate2dunlap"

for slug, d in LOCS.items():
    h = MASTER
    city = d["city"]
    has_vip = d["client"] is not None

    # 1) Reviews block (inside id="reviews"): replace the scroller's inner cards
    cards = "\n".join(review_card(t, n, city) for (t, n) in d["reviews"])
    h = re.sub(r'(<section class="section" id="reviews".*?<div class="scroller">).*?(</div></div></section>)',
               lambda m: m.group(1) + "\n" + cards + "\n" + m.group(2), h, count=1, flags=re.S)

    # 2) Images
    h = h.replace("/assets/images/em-hero-accent.webp", f"/assets/images/{d['hero']}")
    h = h.replace("/assets/images/em-story.webp", f"/assets/images/{d['story']}")

    # 3) Order links (SkyTab) -> location's; add UberEats delivery button only where real
    h = h.replace(DUN_SKYTAB, d["skytab"])
    if d["delivery"]:
        # add a delivery button right after each pickup button (hero + order CTA + visit)
        h = h.replace('<a class="btn btn--blue btn--lg" href="/menu/">View Menu</a>',
                      f'<a class="btn btn--blue btn--lg" href="{d["delivery"]}" target="_blank" rel="noopener">Order Delivery</a>', 1)

    # 4) Phone
    h = h.replace("+14239496132", d["phone_tel"]).replace("(423) 949-6132", d["phone_disp"])

    # 5) Address / zip / map query (before blanket city swap)
    h = h.replace("16952 Rankin Ave, Unit D", d["street"])
    h = h.replace("Dunlap, TN 37327", f"{city}, TN {d['zip']}")
    h = h.replace('"streetAddress":"16952 Rankin Ave, Unit D"', f'"streetAddress":"{d["street"]}"')
    h = h.replace('"postalCode":"37327"', f'"postalCode":"{d["zip"]}"')
    h = h.replace("16952+Rankin+Ave+Unit+D+Dunlap+TN+37327",
                  (d["street"] + " " + city + " TN " + d["zip"]).replace(",", "").replace(" ", "+"))

    # 6) Paths + canonical/OG
    h = h.replace("/dunlap/", f"/{slug}/")

    # 7) Location-specific copy
    h = h.replace("on Rankin Ave", f"on {d['street_name']}")
    h = h.replace("Dunlap-proud", f"{city}-proud")
    h = h.replace("our Dunlap cooks", f"our {city} cooks")
    h = h.replace("What Dunlap orders", f"What {city} orders")
    h = h.replace("From our Dunlap regulars", f"From our {city} regulars")
    h = h.replace("Dunlap, dinner's ready when you are.", f"{city}, dinner's ready when you are.")
    h = h.replace("Come see us in Dunlap", f"Come see us in {city}")
    h = h.replace("El Metate - Dunlap", f"El Metate - {city}")  # SMS consent + JSON-LD name
    # remaining standalone "Dunlap" -> city (titles, eyebrow, hero H1, alt, breadcrumb)
    h = h.replace("Dunlap", city)

    # 8) SITE_CONFIG client (forms + vip share the location client)
    if has_vip:
        h = h.replace('"forms": {"endpoint": "https://chowdownos.onrender.com/api/public/forms/submit", "client": 364}',
                      f'"forms": {{"endpoint": "https://chowdownos.onrender.com/api/public/forms/submit", "client": {d["client"]}}}')
        h = h.replace('"vip": {"endpoint": "https://chowdownos.onrender.com/api/public/vip/signup", "client": 364}',
                      f'"vip": {{"endpoint": "https://chowdownos.onrender.com/api/public/vip/signup", "client": {d["client"]}}}')
    else:
        # Signal Mountain: not live in GHL yet. No forms/vip client -> contact falls back to
        # "coming soon"; VIP page held. Strip VIP links so nothing 404s.
        h = h.replace(', "forms": {"endpoint": "https://chowdownos.onrender.com/api/public/forms/submit", "client": 364}', "")
        h = h.replace(', "vip": {"endpoint": "https://chowdownos.onrender.com/api/public/vip/signup", "client": 364}', "")
        # nav + mobnav VIP link -> Locations picker; visit-section VIP button -> drop
        h = h.replace(f'<a href="/{slug}/vip/">Become a VIP</a>', '')
        h = h.replace(f'<a class="btn btn--gold" href="/{slug}/vip/">Become a VIP</a>', '')

    out = ROOT / slug / "index.html"
    out.write_text(h)
    print(f"{slug}: {len(h)} bytes  vip={has_vip}  delivery={bool(d['delivery'])}")

print("done")
