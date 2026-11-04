# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A static GitHub Pages site (custom domain `mapas.citmovucuenca.com`, via `CNAME`; `.nojekyll` disables Jekyll) hosting the public maps and history pages of MOVIDATA (Universidad de Cuenca · CITMOV). The pages are linked from the axis pages at https://citmovucuenca.com/movidata/. There is no build, lint or test step here. Pushing to `main` publishes.

**Everything committed here is public.** Only publish aggregated data, or data the EMOV has already authorized. Never publish individual people's data or free-text fields.

## Where the content comes from

Every folder here is **build output**. The source lives in the sibling repo `C:\movidata` (`frontend/publico/<name>/`). Never edit `assets/*.js|css` or `data/*` by hand: change the source there, rebuild, and copy the result here.

- `sp01/`, `sp02/`, `sp04/`, `sp05/`, `sp08/`: Vite + React + MapLibre maps that reuse the main viewer's `src/` modules. Each reads its precomputed `data/*.json|geojson` instead of calling the API.
- `historico/salud-publica/`, `historico/cambio-climatico/`, `historico/equidad/`: each axis's "Histórico" block as a static page (`data/historico.json`). They take query params for the metric and granularity, such as `?m=SP02&t=mes` or `?m=CC03&t=anio`.
- The `movidata` repo has two skills for this flow: `crear-mapa-publico` covers the source side and `publicar-mapa-publico` covers publishing here.

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
4. After the site is live, the WordPress axis page's «Próximamente» button for that metric gets switched to «Ver mapa →» `https://mapas.citmovucuenca.com/<código>/`. This happens outside the repo.

Folder names are the lowercase metric code (`sp01`, `cc02`, `ep04`…).

## Conventions

- Commit messages are in Spanish, in the imperative third person, and name the affected pages. Examples: «Añade el mapa público de SP08 (…)», «Actualiza los mapas públicos de SP01, SP02… (…)».
- `README.md` documents where each folder comes from. Update it when you add a page or change how one is produced.
