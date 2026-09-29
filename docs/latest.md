# Recap tech — 29 settembre 2026

Sul fronte dei grandi modelli AI, non emerge una nuova major release ufficiale di OpenAI, Anthropic, Google DeepMind o DeepSeek nelle ultime 24 ore: oggi è meglio non riciclare annunci precedenti.

## 1. Flatpak 1.18.4: aggiornamento di sicurezza da installare

Corregge sei vulnerabilità; le più importanti possono permettere a un'app malevola di cancellare o svuotare file arbitrari dell'host. Conviene aggiornare a 1.18.4 appena disponibile.

Fonte: https://www.phoronix.com/news/Flatpak-1.18.4-Released

## 2. Firefox 157: arriva Nova, il maggiore restyling da anni

Introduce il tema Nova con interfaccia più arrotondata, modalità compatta, decodifica hardware AV1 per WebRTC e avviso SSLKEYLOGFILE.

Fonte: https://www.omgubuntu.co.uk/2026/09/firefox-157-released-nova-theme

## 3. Git 2.56: conflitti più sicuri e manutenzione più scalabile

Aggiunge staging dedicato dei file già risolti, nuovi comandi di maintenance e ottimizzazioni per grandi repository.

Fonte: https://github.blog/open-source/git/highlights-from-git-2-56/

## 4. Valve abilita la code cache FEX in Proton Experimental ARM

La code cache evita di ricompilare continuamente lo stesso codice tradotto x86→ARM64, riducendo stutter e migliorando soprattutto gli 1% low nelle esecuzioni successive.

Fonte: https://www.gamingonlinux.com/2026/09/fex-code-cache-enabled-for-proton-experimental-arm-to-improve-frame-timings/

## 5. F-Droid 2.0: il maggiore rifacimento del client in un decennio

Riscrive l'interfaccia in Kotlin + Jetpack Compose; migliora ricerca e categorie, consente download/aggiornamenti contemporanei e segnala problemi come cambiamenti della chiave di firma.

Fonte: https://f-droid.org/packages/org.fdroid.basic/

## 6. Shotcut 26.9: audio ducking automatico e FFmpeg 9

Aggiunge Automatic Audio Ducking, controlli volume e meter nelle intestazioni delle tracce, Adjustment Clips e pipeline audio a 32-bit float; passa a FFmpeg 9.0 e corregge su Linux VA-API HEVC e progetti su CIFS/SMB.

Fonte: https://www.phoronix.com/news/Shotcut-26.9

## 7. openSUSE Leap 16.1 RC aggiunge una modalità immutabile

La release candidate introduce una nuova modalità immutabile opzionale, offrendo nel medesimo ecosistema Leap sia il modello tradizionale sia un sistema base più controllato e resistente alle modifiche accidentali.

Fonte: https://www.phoronix.com/news/openSUSE-Leap-16.1-RC

## 8. Linux 7.4: nuovo “steal governor” per le macchine virtuali

Usa il tempo “rubato” dall’hypervisor, quando una vCPU vorrebbe lavorare ma l’host esegue altro, per adattare meglio il comportamento del guest.

Fonte: https://www.phoronix.com/news/Linux-7.4-Land-Steal-Governor

## Da tenere d'occhio

- Flatpak 1.18.4
- FEX + Proton ARM
- F-Droid 2.0
- Linux 7.4 e virtualizzazione (steal governor)
