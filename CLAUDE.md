# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A static GitHub Pages site (custom domain `mapas.citmovucuenca.com`, via `CNAME`; `.nojekyll` disables Jekyll) hosting the public maps and history pages of MOVIDATA (Universidad de Cuenca · CITMOV). The pages are linked from the axis pages at https://citmovucuenca.com/movidata/. There is no build, lint or test step here. Pushing to `main` publishes.

**Everything committed here is public.** Only publish aggregated data, or data the EMOV has already authorized. Never publish individual people's data or free-text fields.

## Where the content comes from

Every folder here is **build output**. The source lives in the sibling repo `C:\movidata` (`frontend/publico/<name>/`). Never edit `assets/*.js|css` or `data/*` by hand: change the source there, rebuild, and copy the result here.

- `sp01/`, `sp02/`, `sp04/`, `sp05/`, `sp08/`: Vite + React + MapLibre maps that reuse the main viewer's `src/` modules. Each reads its precomputed `data/*.json|geojson` instead of calling the API.
- `historico/salud-publica/`, `historico/cambio-climatico/`, `historico/equidad/`: each axis's "Histórico" block as a static page (`data/historico.json`). They take query params for the metric and granularity, such as `?m=SP02&t=mes` or `?m=CC03&t=anio`.
- The `movidata` repo has three skills for this flow: `crear-mapa-publico` covers the source side, `publicar-mapa-publico` covers publishing here and `publicar-mapa-wordpress` links a new map from its WordPress axis page.

Updating a page, run from `C:\movidata\frontend` with the stack running:

```powershell
python scripts/generar-<código>-publico.py --desde 2019 --hasta 2025   # regenerate the data (see each publico/<name>/README.md)
npm run build:publico -- <name>        # e.g. sp08, historico-equidad → publico/<name>/dist/
```

(`build:sp01`, `build:sp02`, `build:sp04` and `build:sp05` also exist as legacy aliases.)

Then here:

1. Replace the folder's contents with `publico/<name>/dist/`. Asset filenames are content-hashed, so remove the old `assets/` files instead of copying on top of them.
2. Re-add the back button, because the build overwrites `index.html`:
   `python herramientas/anadir_volver.py <folder>/index.html <eje>`, where `<eje>` is `salud-publica`, `cambio-climatico` or `equidad`. The script is idempotent: it checks for the `<!-- movidata-volver -->` marker.
3. For a new page, add a card to the root `index.html` list (maps under the first `<ul>`, histories under "Históricos").
4. After the site is live, switch the WordPress axis page's «Próximamente» button for that metric to «Ver mapa →» `https://mapas.citmovucuenca.com/<código>/`. It happens outside the repo, through Claude in Chrome: follow the `publicar-mapa-wordpress` skill in `C:\movidata\.claude\skills\`. Find the card **by its metric title**, not by its code (see the next section).

Folder names are the lowercase **platform** metric code (`sp01`, `cc02`, `ep04`…).

## Metric numbering: WordPress cards vs. platform codes

Metrics have two different codes, and in Cambio climático and Equidad **they do not match**:

- **Official number (Nº)**: from the Phase 1 sheet, 1–9 per axis. The WordPress axis pages (`citmovucuenca.com/movidata/<eje>/`) label their cards with it: card «EP07» is Equidad Nº 7.
- **Platform code**: the internal label used by the viewer, the API and the DWH. **This repo uses it everywhere**: folder names, the `?m=` parameter of `historico/<eje>/`, the keys of `historico/<eje>/data/historico.json` and the «Métrica» dropdown of the history pages.

Source of truth: `docs/metricas/README.md` in the `movidata` repo (table «Numeración oficial»). The tables below are copied from it (commit `ebc85be`, 2026-10-30); update them if that file changes.

Rules when linking a WordPress card to a page here:

1. **Match by the metric's title, never by its code.** Read the card's title and look it up in the tables below.
2. The link uses the **platform code**: card «EP07 · Asequibilidad…» links to `historico/equidad/?m=EP06`, not `?m=EP07`.
3. When done, check on the published page that each card's title matches the `?m=` of its button.
4. If a metric is missing from the tables or anything is unclear, ask before linking.

Salud pública: they match. WordPress card `SPnn` is platform code `SPnn` (SP01–SP09).

Cambio climático:

| WordPress card (Nº) | Metric | Platform code |
|---|---|---|
| CC01 | Emisiones de gases de efecto invernadero del sector movilidad | CC01 (pending) |
| CC02 | Calidad del aire | **CC02** |
| CC03 | Tasa de motorización de vehículos matriculados en el cantón | **CC03** |
| CC04 | Proporción de vehículos según etiqueta ambiental | — |
| CC05 | Distribución modal de viajes | CC04 |
| CC06 | Arbolado en vías principales | CC07 |
| CC07 | Tasa de bicicletas públicas disponibles por cada 1.000 habitantes | **CC08** |
| CC08 | Número de viajes en modos de transporte público sostenible | — |
| CC09 | Número de iniciativas institucionales de promoción de movilidad activa implementadas | CC09 (pending) |

Equidad:

| WordPress card (Nº) | Metric | Platform code |
|---|---|---|
| EP01 | Proporción de la red vial con aceras | — |
| EP02 | Proporción de aceras con accesibilidad | — |
| EP03 | Longitud de infraestructura ciclística (km) | **EP03** |
| EP04 | Longitud de infraestructura ciclística por habitante | **EP04** |
| EP05 | Proporción de edificaciones con cobertura al transporte público colectivo | EP01 |
| EP06 | Proporción de corredores de transporte público colectivo con carril preferencial | — |
| EP07 | Asequibilidad al transporte público colectivo | **EP06** |
| EP08 | Calidad del transporte público colectivo | — |
| EP09 | Disponibilidad de servicios digitales en el transporte público (colectivo y comercial) | EP10 |
| (no card) | Red vial por 1.000 habitantes: not one of the 27 catalogue metrics | EP05 |

«—» = no platform code yet. Bold = has a published history page here.

«Ver histórico →» buttons on WordPress as of 2026-11-04: Salud pública SP01, SP02, SP03, SP04, SP05, SP07, SP08 and SP09, each to its own code; Cambio climático CC02 → `?m=CC02`, CC03 → `?m=CC03`, **CC07 → `?m=CC08`**; Equidad EP03 → `?m=EP03`, EP04 → `?m=EP04`, **EP07 → `?m=EP06`** (platform EP05 has no card).

## Conventions

- Commit messages are in Spanish, in the imperative third person, and name the affected pages. Examples: «Añade el mapa público de SP08 (…)», «Actualiza los mapas públicos de SP01, SP02… (…)».
- `README.md` documents where each folder comes from. Update it when you add a page or change how one is produced.
