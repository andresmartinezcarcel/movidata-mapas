# movidata-mapas

Mapas interactivos (exportados con qgis2web) de las métricas georreferenciadas de MOVIDATA.
Se publican con GitHub Pages en `https://andresmartinezcarcel.github.io/movidata-mapas/`
y se enlazan desde las páginas de ejes de https://citmovucuenca.com/movidata/.

## Estructura

Una carpeta por métrica, con el código en minúsculas: `sp01/`, `cc02/`, `ep04/`…
Cada carpeta contiene el `index.html` que genera qgis2web (más sus carpetas `css/`, `js/`, `data/`, …).
Excepción: `sp01/` no sale de qgis2web. Es la capa «Tasa de mortalidad» del visor de MOVIDATA
compilada como página estática desde el repositorio `movidata` (`frontend/publico/sp01/`, ver la
sección «Mapa público de SP01» de `frontend/README.md`): para actualizarla, se regeneran los datos,
se ejecuta `npm run build:sp01`, se copia `publico/sp01/dist/` aquí y se vuelve a añadir el botón.

## Publicar un mapa nuevo

1. En QGIS: Web → qgis2web → Leaflet. En *Export* elige como carpeta `movidata-mapas/<código>/`
   (qgis2web crea una subcarpeta `qgis2web_fecha`: mueve su contenido a `<código>/`).
   Recomendado: en *Data export* reduce la precisión de coordenadas (p. ej. 5–6 decimales) y
   activa *Minify GeoJSON*; exporta solo las capas y atributos que se van a mostrar.
2. Añade el botón de volver: `python herramientas/anadir_volver.py <código>/index.html <eje>`
3. Añade la métrica a la lista de `index.html` de la raíz.
4. `git add . && git commit -m "Añade mapa <código>" && git push`
5. En WordPress, en la página del eje, cambia el botón «Próximamente» de esa métrica por
   «Ver mapa →» con enlace a `https://andresmartinezcarcel.github.io/movidata-mapas/<código>/`.

Ojo: todo lo que se sube aquí es público. Publica solo datos agregados o ya autorizados por la EMOV.
