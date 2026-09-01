# Předávací balíček — Kviz_game (Pomsta Kalkulátora)

Datum předání: 1. 9. 2026. Rodinná kvízová hra pro Petrovy blízké. Tenhle soubor je vstupní bod pro nový chat — přečti ho celý, než něco změníš.

## Co to je
Jednosouborová webová hra `Irca-vs-kalkulator.html` (~2 MB HTML+JS+SVG, běží i z file://). Moderátorem je animovaná SVG postava „Kalkulátor" (na mobilu a ve školním módu „Kalkulátorka" — ženská verze). Herní módy:

- **Klasická hra** — 20 otázek, obecné znalosti.
- **Adélka škola** — aplikovaná chemie, 2. ročník (2430 otázek, `adelka-skola.txt`), výklad namluvený hlasem Verunky. Vybírá se okruh.
- **Verunka — přijímačky** — samostatná appka `verunka-zdroj.html` vložená do hry jako iframe (matematika + čeština, CERMAT 2027, tabule s výkladem po krocích).
- **Ruda to nevzdá!** — otázky pro Petrova tátu (`pro-tatu.txt`, 366 otázek: žatecký tankový pluk, ČSLA, Osečany, srpen 1968, normalizace). Moderuje „major" hlubokým mužským hlasem.
- Další: Mládě, legendy, kalkulátor, duel, „Pojď se učit".

## Kde co je
- **Projekt (lokálně):** `C:\Users\petrp\OneDrive\Desktop\Kviz_game\` — klon veřejného repa.
- **Git:** veřejné repo **`konias12479/Kviz_game`** (gh CLI přihlášen), větev `main`. Hraje se z GitHub Pages: https://konias12479.github.io/Kviz_game/Irca-vs-kalkulator.html
- **Skripty pro namlouvání:** `Kviz_game\nastroje\` — **je v `.gitignore`, protože soubory obsahují ElevenLabs API klíč. NIKDY je necommituj do veřejného repa.**
- Commity: `git -c user.name="petr" -c user.email="petr.poslusny81@gmail.com"`.

### Klíčové soubory
| Soubor | Co to je |
|---|---|
| `Irca-vs-kalkulator.html` | hlavní hra (jeden soubor, veškerá logika) |
| `verunka-zdroj.html` | ZDROJ sekce Verunka — edituje se TADY |
| `slouc-verunku.py` | vloží `verunka-zdroj.html` do hlavní hry (spustit po každé změně!) |
| `adelka-skola.txt` | 2430 otázek chemie (`Otázka?;správná;špatná;špatná;~vysvětlení`) |
| `pro-tatu.txt` | 366 otázek pro Rudu, stejný formát |
| `moje-otazky.txt` | otázky Irča |
| `hlas/` | 184 klipů výkladu Verunka-přijímačky (`<id-okruhu>-<číslo>.mp3`) |
| `hlas-adelka/` | klipy chemie/biologie hlasem Verunky (`o-<hash>.mp3` otázka, `v-<hash>.mp3` vysvětlení) |
| `hlas-tata/` | 583 klipů sekce Ruda hlasem Brian Deep (`o-`/`v-`/`q-<hash>.mp3`) |
| `tata1-3.mp3`, `hra.mp3`, `initial.mp3` | hudba |

**POZOR na `verunka-zdroj.html`:** změny v něm se neprojeví, dokud nespustíš `python slouc-verunku.py` (vloží ho do `Irca-vs-kalkulator.html` mezi značky `VERUNKA-START`/`VERUNKA-KONEC`). Commituj oba soubory.

## Namlouvání (ElevenLabs)
Klíč (jen lokálně, NIKDY do hry ani do repa): `sk_00d272ad5d56305539b233b8fdcbd824c297e2678a1e616b`

| Sekce | Hlas | voice_id | Nastavení |
|---|---|---|---|
| Verunka, Adélka | **Verunka** (klon Petrovy dcery, souhlas dala 31. 8. 2026) | `lUCwXZyNMgc71S2hOoJ3` | stability 0.55, similarity 0.85, style 0.15, **speed 0.92** |
| Ruda (major) | **Brian Deep** (hotový hlas z knihovny, ne klon) | `nPczCjzI2devNBz1zQrb` | stability 0.6, similarity 0.85, style 0.1, **speed 0.80** |

Vždy `eleven_multilingual_v2`, formát `mp3_22050_32`.

### Jak hra páruje text s nahrávkou
Hash je **djb2** z PŘESNÉHO textu, 8 hex znaků — v JS funkce `adHash()`, v Pythonu:
```python
def adhash(s):
    x = 5381
    for ch in s: x = (x*33 + ord(ch)) & 0xFFFFFFFF
    return format(x, "08x")
```
Soubor se pak jmenuje `o-<hash>.mp3` (otázka), `v-<hash>.mp3` (vysvětlení), `q-<hash>.mp3` (hláška majora). **Změníš-li text otázky, hash se změní a nahrávka přestane sedět — musí se přegenerovat.** U hlášek majora se hashuje text PŘED personalizací (před přidáním oslovení „Vojíne Poslušný —"). Když nahrávka chybí, hra automaticky spadne zpět na prohlížečovou syntézu — nic se nerozbije, jen to zní hůř.

### Ticho na začátku klipu — POVINNÝ krok po každém generování
Reproduktor (hlavně Bluetooth) se po spuštění zvuku ~300 ms probouzí a spolkne začátek. Když je na začátku klipu ticho, spolkne ticho místo prvního slova. ElevenLabs vrací klipy, kde řeč začíná hned v prvních 50 ms — **bez doplnění ticha není rozumět prvnímu slovu** (Petr to 1. 9. reklamoval).

Po každém generování spusť:
```bash
cd nastroje && python pad_clips_kviz.py
```
Skript je idempotentní (klipy s dost dlouhým tichem přeskočí), takže se nedá spustit „dvakrát omylem" a nasčítat pauzy. Jako jediný ze skriptů je i v repu — neobsahuje API klíč.

**Pozor na rychlost přehrávání:** hra pouští `hlas/` a `hlas-adelka/` rychlostí **1,3×**, takže tam skript dává 390 ms (po zrychlení = 300 ms). `hlas-tata/` běží 1× a dostane 300 ms. Kdyby se tempo v aplikaci měnilo, uprav tabulku `PAD` ve skriptu.

### Generovací skripty (v `nastroje\`, gitignorováno)
- `extract_adelka_all.py` / `extract_tata_texts.py` — vytáhnou texty z .txt a hry do JSON.
- `gen_adelka_all.py`, `gen_tata_hlas.py`, `gen_kviz_hlas.py` — generují po dávkách 15, po každé dávce commit+push (dá se kdykoli přerušit a spustit znovu, hotové soubory přeskočí).
- `list_voices.py` — vypíše dostupné hlasy na účtu.
- Skripty se pouštějí **ze složky `nastroje/`** (`cd nastroje && python gen_adelka_all.py`) — cestu k repu si dopočítají z umístění souboru.
- **Pozor na souběžný push:** skripty po každé dávce commitují a pushují. Když mezitím pushne někdo jiný, `gen_adelka_all.py` si udělá `pull --rebase` a zkusí to znovu (max 4×); ostatní skripty tuhle pojistku zatím nemají a spadly by. Před spuštěním udělej `git pull` a během běhu do repa raději nepushuj.

## Stav k 1. 9. 2026
Hotovo: 184 klipů Verunka-přijímačky, 518 klipů biologie, 583 klipů Ruda, 3 opravné klipy (poměr „ku"), a velká část chemie a ostatních předmětů pro Adélku.
**Rozpracováno:** zbytek Adélčiny sady (celkem 4850 klipů = 2430 otázek + 2420 vysvětlení). První běh vyčerpal kvótu ElevenLabs (`quota_exceeded` po 4018 klipech), Petr 1. 9. dokoupil kredity a dávka běží dál — zbývalo 734 klipů.
Kolik ještě chybí zjistíš kdykoli: `cd nastroje && python extract_adelka_all.py` (vypíše „chybí vygenerovat"). Dogenerovat: `python gen_adelka_all.py` — přeskočí hotové, takže se dá pouštět opakovaně.
**Kredity ubývají rychle** (~130 k znaků na ~4000 klipů) — před velkým během se Petra zeptej.

## Poslední změny (kontext, ne úkoly)
- **Všem klipům bylo předsazeno ticho** (viz sekce výše). `hlas/` a `hlas-tata/` hotové (767 souborů), `hlas-adelka/` se dodělává až po doběhnutí generování — **zkontroluj to jako první věc** (`cd nastroje && python pad_clips_kviz.py`).
- Sekce Ruda dostala nahraný hlas místo syntézy (otázky, vysvětlení i hlášky majora).
- Opraveno: hra už neskáče na další otázku, dokud nahraný klip nedohraje (`pauseThenNext` čeká i na `adelkaAudio`).
- V Adélčině módu je Kalkulátorka (ženská postava) s vlídným úsměvem, ne mužský Kalkulátor.
- Ve Verunce se slova psaná VELKÝMI písmeny (KDO, CO) čtou jako slova, ne po písmenech.
- Odstraněno tlačítko „Nastavení hlasu Kalkulátora" — hlas se teď namlouvá předem, syntéza je jen záloha.

## Otevřené úkoly
1. **Dokončit namlouvání chemie** (viz Stav výše).
2. **Ikona sekce „Ruda to nevzdá!"** — Petr chce místo emoji 👨 pořádnou komiksovou ilustraci: veselý muž s hnědými vlasy objímá černovlasou usmívající se dívku, k tomu tank, chata a silueta Prahy. Moje ručně kreslené SVG Petr zamítl jako „velmi basic". Claude Design skill nešel použít — na stroji chybí `node` i `bun`. Možnosti: doinstalovat node, najít hotovou komiksovou ilustraci s vhodnou licencí, nebo nechat vygenerovat obrázek jinde a vložit jako PNG.
3. Grafika Kalkulátorky v Adélčině módu — Petr s ní pořád není spokojený (opravil jsem jen výraz, ne kresbu).

## Petrova pravidla (dodržovat!)
- **Stopka:** před každým úkolem 1–2 věty — vhodnost modelu (rutina → ZASTAVIT a nechat ho přepnout na levnější; „dodělám, je to pár minut" je nepřijatelné) a kontrola délky chatu. Platí oběma směry (i slabý model na složitý úkol). Je to i v paměti (`stopka-pred-ukolem`).
- Česky, mužský rod.
- Klonování hlasu: jen Verunka (souhlas má). Cizí/veřejné osoby odmítnout — pro Rudu se proto použil hotový hlas z knihovny, ne klon.
- Hlasitost a tempo hlasu jsou vyladěné — neměnit bez žádosti.
- API klíč nikdy do hry ani do veřejného repa.
