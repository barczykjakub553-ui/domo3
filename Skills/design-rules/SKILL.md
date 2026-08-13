---
name: design-rules
description: Nienaruszalne zasady projektowe dla stron w tym repo. Wczytaj ZAWSZE, zanim dotkniesz czegokolwiek w Template/ albo tworzysz nową stronę na jego bazie: layout/template jest nietykalny, tylko ładne nowoczesne czcionki, delikatna paleta kolorów i gradientów — żadnych "AI fioletów".
---

# Zasady projektowe (twarde, nie do złamania)

Te trzy zasady obowiązują ZAWSZE przy pracy nad UI w tym repo. Nie ma wyjątków,
nie ma "tylko ten raz". Jeśli prośba użytkownika je łamie — najpierw to powiedz
i zapytaj, nie łam ich po cichu.

## 1. NIGDY nie zmieniaj wzoru (template / layout)

- `Template/` to wzór. Struktura sekcji, kolejność, siatka, rozmieszczenie
  elementów, markup w `index.html` — **nietykalne**.
- Wolno: podmieniać treść (teksty, zdjęcia/gradienty produktów), zmieniać
  kolory przez zmienne w `:root`, dodawać nowe strony które **powielają** ten
  sam layout.
- Nie wolno: przestawiać sekcji, zmieniać ich układu, przebudowywać siatki,
  wymyślać nowego layoutu, "poprawiać" struktury HTML.
- Nowa strona = ta sama kość layoutu co `Template/`, tylko inna treść i kolory.

## 2. Tylko ładne, nowoczesne czcionki

- Współczesne, czytelne kroje. Sensowna para: nowoczesny serif na nagłówki +
  czysty grotesk/sans na tekst (albo odwrotnie) — ale spójnie.
- Zero domyślnych/systemowych brzydali (Arial, Times, Comic Sans),
  zero krojów-dziwadeł.
- Font zmieniamy w jednym miejscu (zmienne fontów w `:root` / `<link>` w
  `index.html`), nie rozsypujemy `font-family` po całym CSS.

## 3. Delikatna, przemyślana paleta + gradienty

- Kolory dobrane spokojnie i ze smakiem: stonowane, komplementarne, z jednym
  wyraźnym akcentem. Edytuj przez zmienne w `:root` (`--bg --ink --accent
  --line`), nie hardcoduj kolorów w regułach.
- Gradienty subtelne — jako tło/akcent, nie jako krzyk.
- **ZAKAZ "AI fioletów"**: żadnego generycznego fiolet→róż→błękit, żadnego
  neonu, żadnych jaskrawych tęcz. Jak coś wygląda jak domyślny gradient z
  generatora AI — jest źle.

## Szybki test przed oddaniem

1. Layout identyczny jak w `Template/`? (tak = ok)
2. Czcionki ładne i spójne, nie systemowe? (tak = ok)
3. Kolory stonowane, akcent jeden, gradient subtelny, zero AI-fioletu? (tak = ok)

Któryś na "nie" → popraw, zanim pokażesz.
