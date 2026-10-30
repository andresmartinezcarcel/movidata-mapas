"""Añade un botón «← Volver a las métricas» a un mapa exportado con qgis2web.

Uso:  python anadir_volver.py ..\sp01\index.html salud-publica
(el segundo argumento es el eje: salud-publica, cambio-climatico o equidad)
"""
import sys
from pathlib import Path

ruta, eje = Path(sys.argv[1]), sys.argv[2]
html = ruta.read_text(encoding="utf-8")
marca = "<!-- movidata-volver -->"
if marca in html:
    sys.exit("El botón ya estaba añadido.")
boton = (
    f'{marca}<a href="https://citmovucuenca.com/movidata/{eje}/" '
    'style="position:fixed;left:12px;bottom:24px;z-index:10000;background:#062817;'
    'color:#F6F4ED;padding:8px 14px;border-radius:4px;font:600 14px system-ui,sans-serif;'
    'text-decoration:none;box-shadow:0 1px 4px rgba(0,0,0,.3)">← Volver a las métricas</a>\n'
)
html = html.replace("</body>", boton + "</body>", 1)
ruta.write_text(html, encoding="utf-8")
print("Botón añadido a", ruta)
