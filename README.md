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

## Regole di pubblicazione del recap

Per ogni nuova edizione di Tech News Daily:

1. Creare o aggiornare `docs/archive/YYYY-MM-DD.html` con il recap completo del giorno.
2. Aggiornare direttamente `docs/index.html` con lo stesso recap (titoli, testi, link, ordine e immagini), adattando solo i percorsi relativi, inclusa la favicon.
3. **Nella home page inserire sempre i link alle 5 edizioni precedenti**, selezionando le cinque date più recenti per cui esiste realmente `docs/archive/YYYY-MM-DD.html`. Usare URL relativi `archive/YYYY-MM-DD.html` e verificare che ogni file di destinazione esista. Non includere l'edizione corrente fra le cinque precedenti.
4. Eseguire i commit sul branch `main`, da cui GitHub Pages pubblica la cartella `/docs`.
5. Rileggere entrambi i file dopo il commit e verificare data, contenuto e link alle cinque edizioni precedenti.

Non affidare l'aggiornamento della home a un workflow che copi automaticamente l'archivio; eventuali workflow preesistenti non devono sovrascrivere `docs/index.html`.
