"""Předsadí každému namluvenému klipu 300 ms ticha.

Proč: reproduktor (hlavně Bluetooth) se po spuštění zvuku chvíli probouzí
a spolkne úplný začátek. Když je na začátku ticho, spolkne ticho — ne první
slovo. Stejný trik používá appka Klid.

Pouštět po každém generování:  cd nastroje && python pad_clips_kviz.py
Skript je idempotentní — klipy, které ticho už mají, přeskočí, takže se
nedá spustit "dvakrát omylem".
"""
import os, subprocess, array, glob, sys
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
# Kolik ticha předsadit. Hra přehrává Verunku i Adélku rychlostí 1,3×,
# takže tam musí být ticho delší, aby po zrychlení vyšlo zhruba na 300 ms.
# Sekce Ruda běží rychlostí 1×, tam stačí 300 ms.
PAD = {"hlas": 390, "hlas-adelka": 390, "hlas-tata": 300}
FOLDERS = list(PAD)
TICHO = 328              # ~1 % z plné výchylky

def leading_silence_ms(path, look_ms=500):
    """Kolik ms ticha je na začátku souboru."""
    out = subprocess.run([FF, "-v", "quiet", "-i", path, "-f", "s16le",
                          "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
    a = array.array("h")
    a.frombytes(out[:len(out) // 2 * 2])
    sr, win, ms = 16000, 160, 0        # okno 10 ms
    for i in range(0, min(len(a), sr * look_ms // 1000), win):
        chunk = a[i:i + win]
        if not chunk:
            break
        if max(abs(x) for x in chunk) > TICHO:
            break
        ms += 10
    return ms

def pad(path, pad_ms=300):
    tmp = path + ".tmp.mp3"
    r = subprocess.run([FF, "-y", "-v", "quiet", "-i", path,
                        "-af", "adelay=%d:all=1" % pad_ms,
                        "-c:a", "libmp3lame", "-b:a", "32k", "-ar", "22050", "-ac", "1", tmp],
                       capture_output=True)
    if r.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 500:
        os.replace(tmp, path)
        return True
    if os.path.exists(tmp):
        os.remove(tmp)
    return False

def main():
    folders = sys.argv[1:] or FOLDERS
    total_new = total_skip = total_bad = 0
    for folder in folders:
        d = os.path.join(REPO, folder)
        if not os.path.isdir(d):
            print("neni slozka:", folder, flush=True)
            continue
        files = sorted(glob.glob(os.path.join(d, "*.mp3")))
        pad_ms = PAD.get(folder, 300)
        min_ok = pad_ms - 60          # klip s dost dlouhým tichem se přeskočí
        new = skip = bad = 0
        for i, f in enumerate(files, 1):
            if leading_silence_ms(f, pad_ms + 200) >= min_ok:
                skip += 1
            elif pad(f, pad_ms):
                new += 1
            else:
                bad += 1
                print("  CHYBA:", os.path.basename(f), flush=True)
            if i % 200 == 0:
                print("  %s: %d/%d" % (folder, i, len(files)), flush=True)
        print("%s: doplneno %d, preskoceno %d, chyb %d (celkem %d)"
              % (folder, new, skip, bad, len(files)), flush=True)
        total_new += new; total_skip += skip; total_bad += bad
    print("HOTOVO: doplneno %d, preskoceno %d, chyb %d" % (total_new, total_skip, total_bad), flush=True)

if __name__ == "__main__":
    main()
