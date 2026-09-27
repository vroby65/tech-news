# Tech News Daily

Rassegna tecnologica quotidiana automatica, pubblicata alle **06:00 Europe/Rome**.

## Cosa fa

- legge feed RSS/Atom selezionati;
- raccoglie le notizie recenti;
- elimina i duplicati;
- opzionalmente usa DeepSeek per produrre un recap italiano più leggibile;
- genera `docs/index.html`;
- conserva un archivio giornaliero in `docs/archive/`;
- esegue commit automatico dell'edizione;
- pubblica il sito con GitHub Pages.

## Attivazione

1. In **Settings → Pages → Build and deployment → Source**, scegli **GitHub Actions**.
2. Facoltativo ma consigliato: in **Settings → Secrets and variables → Actions** crea `DEEPSEEK_API_KEY`.
3. Apri **Actions → Daily Tech News → Run workflow** per il primo test.

Il workflow è programmato alle 06:00 nel fuso `Europe/Rome`.

## Fonti

Le fonti sono configurate in `sources.json` e possono essere modificate liberamente.
