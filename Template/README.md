# ATELIER — modern store template

Static template for a shop that sells products (furniture, bakery, whatever).
Plain HTML/CSS/JS — no build step, no dependencies, no npm.

## Run

Any static server (fonts need http, not `file://`):

```bash
python3 -m http.server 8777
```

Then open http://localhost:8777

## Files

- `index.html` — markup & copy
- `styles.css` — all styling; brand lives in `:root` (top of file)
- `main.js` — cursor, carousels, reveals, parallax, count-up, mobile menu

## Rebrand in 30 seconds

Edit the 4 variables at the top of `styles.css`:

```css
--bg:     #f5f2ec;   /* page background */
--ink:    #1c1a17;   /* text / dark sections */
--accent: #b0724a;   /* single accent color */
--line:   #e5ded3;   /* hairlines */
```

Product/collection "images" are CSS gradients (`.product__media--*`,
`.card__media--*`). Replace with `background-image: url(...)` for real photos.

## Features

- Three carousels: hero (fade), products (native scroll-snap + arrows + drag),
  reviews (fade). Autoplay pauses on hover.
- Custom cursor with trailing ring (desktop only, off for touch / reduced-motion).
- Scroll-reveal, parallax, count-up stats, marquee, scroll-progress bar.
- Native CSS smooth-scroll for nav anchors. Fully responsive + mobile menu.
- Respects `prefers-reduced-motion`.

## Notes

- Smooth scrolling = native CSS (`scroll-behavior: smooth`) + rich scroll
  animations. Momentum wheel-hijack (Lenis) is intentionally skipped — it
  conflicts with the sticky header and scroll-snap carousels. Add it only if
  you drop those.
