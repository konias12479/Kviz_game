#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vloží obsah verunka.html do Irca-vs-kalkulator.html jako izolovaný srcdoc rámec.
   verunka.html zůstává zdrojem pravdy — po každé úpravě spusť tenhle skript znovu."""
import re,sys,os
HRA="Irca-vs-kalkulator.html"; VER="verunka.html"
ZAC="/* ==== VERUNKA-START (generováno skriptem slouc-verunku.py — needituj ručně) ==== */"
KON="/* ==== VERUNKA-KONEC ==== */"

v=open(VER,encoding="utf-8").read()
# escapování pro vložení do JS template literalu
esc=v.replace("\\","\\\\").replace("`","\\`").replace("${","\\${")
# </script> uvnitř řetězce by předčasně ukončil skript hry
esc=esc.replace("</script>","<\\/script>")
blok=ZAC+"\nconst VERUNKA_HTML=`"+esc+"`;\n"+KON

h=open(HRA,encoding="utf-8").read()
if ZAC in h:
    i=h.index(ZAC); j=h.index(KON)+len(KON)
    h=h[:i]+blok+h[j:]
else:
    print("CHYBA: v souboru hry chybí značky VERUNKA-START/KONEC",file=sys.stderr); sys.exit(1)
open(HRA,"w",encoding="utf-8").write(h)
print("Vloženo %d znaků Verunky do %s"%(len(esc),HRA))
