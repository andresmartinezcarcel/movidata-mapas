# movidata-mapas

Mapas interactivos e históricos de las métricas de MOVIDATA, como páginas estáticas.
Se publican con GitHub Pages en `https://mapas.citmovucuenca.com/` (dominio propio: archivo `CNAME` + registro CNAME `mapas` → `andresmartinezcarcel.github.io` en el DNS de WordPress.com)
y se enlazan desde las páginas de ejes de https://citmovucuenca.com/movidata/.

## Estructura

Una carpeta por métrica, con el código en minúsculas: `sp01/`, `cc02/`, `ep04/`…
Cada carpeta es el `dist/` de una página Vite del repositorio `movidata`
(`frontend/publico/<código>/`), que reutiliza los módulos del visor y lee datos precalculados de
su carpeta `data/` en vez de la API. No se editan aquí: se cambia la fuente, se regeneran los
datos, se compila y se copia el resultado (ver «Publicar o actualizar una página»).

- `sp01/`: la capa «Tasa de mortalidad» del visor (`frontend/publico/sp01/`, sección «Mapa
  público de SP01» de `frontend/README.md`): cifras agregadas por territorio.
- `sp02/`: los siniestros con fallecidos con su ficha pública (mes y franja horaria, sin datos de
  las personas), de `frontend/publico/sp02/` (sección «Mapa público de SP02»).
- `sp03/`: la capa «Fallecidos en movilidad activa por parroquia» del visor: la proporción de
  peatones y ciclistas entre los fallecidos de cada parroquia, por año o de 2019 a 2025
  (solo recuentos por parroquia), de `frontend/publico/sp03/` (ver su `README.md`).
- `sp04/`: los siniestros con lesionados con su ficha pública (mes y franja horaria, sin datos de
  las personas), de `frontend/publico/sp04/` (sección «Mapa público de SP04»).
- `sp05/`: todos los siniestros reportados, con su gravedad y su ficha pública (mes y franja
  horaria, sin datos de las personas), de `frontend/publico/sp05/` (sección «Mapa público de
  SP05»).
- `sp08/`: las acciones de fiscalización de tránsito (operativos cumplidos) agregadas por
  ubicación, sin direcciones escritas por los agentes, responsables ni observaciones, de
  `frontend/publico/sp08/` (ver su `README.md`).
- `cc07/`: «Árboles por kilómetro», la tarjeta CC06 de WordPress (arbolado en vías): los árboles
  por km de vía de cada parroquia, los árboles del inventario de la EMAC como puntos y su mapa de
  calor, con filtros de área, parroquia y calle; de `frontend/publico/cc07/` (ver su `README.md`).
  Solo es un inventario de árboles: ningún dato de personas.
- `ep02/`: «Red vial con aceras», la tarjeta EP01 de WordPress: el % de la red vial levantada
  con aceras por parroquia (solo la cabecera en las rurales) y cada tramo con su código de acera
  (`frontend/publico/ep02/`).
- `historico/salud-publica/` no es un mapa: es el bloque «Histórico» de la pestaña Salud pública
  del visor, de `frontend/publico/historico-salud-publica/` (ver su `README.md`). Lleva las series
  por año y por mes de 2019 a 2025, sin filtros y nunca por día; se enlaza con `?m=SP02&t=mes`.
- `historico/cambio-climatico/` e `historico/equidad/` son lo mismo para los otros dos ejes, de
  `frontend/publico/historico-cambio-climatico/` y `frontend/publico/historico-equidad/`: CC02 por
  año, mes y día, CC03 y CC08 por año (`?m=CC03&t=anio`), y EP03–EP06 solo por año (`?m=EP03`).

## Ojo: dos numeraciones de métricas

Las tarjetas de las páginas de ejes de WordPress usan el **Nº oficial** de la lámina (del 1 al 9
por eje). Este repo usa el **código de plataforma** del visor: en las carpetas, en el `?m=` de los
históricos y en `historico.json`. En Salud pública coinciden, pero en Cambio climático y Equidad
no. Por ejemplo, la tarjeta CC07 (bicicletas públicas) enlaza a `?m=CC08`, y la tarjeta EP07
(asequibilidad) a `?m=EP06`. Antes de enlazar una tarjeta, búscala siempre por el título de la
métrica. La tabla completa está en [`CLAUDE.md`](CLAUDE.md), copiada de `docs/metricas/README.md`
del repositorio `movidata`.

## Publicar o actualizar una página

1. Desde `frontend/` del repositorio `movidata`, con la pila levantada, regenera los datos
   (`python scripts/generar-<código>-publico.py --api http://127.0.0.1 --desde 2019 --hasta 2025`,
   si la página tiene script) y compila: `npm run build:publico -- <carpeta de publico/>`
   (p. ej. `sp08`, `historico-equidad`).
2. Borra la carpeta de aquí, si ya existía, y copia en su lugar `frontend/publico/<…>/dist/`. Los
   nombres de los assets cambian en cada compilación y los viejos quedarían colgando.
3. Añade el botón de volver (la compilación lo pierde):
   `python herramientas/anadir_volver.py <carpeta>/index.html <eje>`, con el eje según el prefijo:
   `sp` → `salud-publica`, `cc` → `cambio-climatico`, `ep` → `equidad`.
4. Si la página es nueva, añádela a la lista de `index.html` de la raíz y a la «Estructura» de
   este README.
5. `git add <carpeta> index.html README.md && git commit -m "Añade el mapa público de <CÓDIGO> (<métrica>)" && git push`
6. Si es nueva, en WordPress, en la página del eje, cambia el botón «Próximamente» de esa métrica
   por «Ver mapa →» con enlace a `https://mapas.citmovucuenca.com/<código>/`. Busca la tarjeta por
   el título de la métrica, porque su código puede no coincidir con el de la carpeta (ver «Ojo: dos
   numeraciones de métricas»).

Ojo: todo lo que se sube aquí es público. Publica solo datos agregados o ya autorizados por la EMOV.
