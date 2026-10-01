# vapsoloes.com

Sitio estático de catálogo VapSolo para España: HTML, CSS y JavaScript sin dependencias ni compilación.

## Uso local

Desde la carpeta raíz, iniciar un servidor estático, por ejemplo `python -m http.server 8080`, y abrir `http://localhost:8080/`.

## Publicación

Subir el contenido completo de esta carpeta a la raíz pública del hosting de `vapsoloes.com`. Mantener la carpeta `pages/`, `images/`, `style.css`, `script.js`, `robots.txt` y `sitemap.xml` con su estructura actual. No hace falta npm ni base de datos.

## Mantenimiento

- Los tramos de descuentos se documentan en `discounts.json` y se reflejan en las tablas HTML accesibles de las fichas. Actualizar ambos al volver a comprobar la fuente externa.
- Las imágenes requeridas y sus textos alternativos están en `images/IMAGE-MANIFEST.md`.
- Cuando se valide una URL externa, añadir el botón de compra solo a la página del mismo modelo.
- Para publicar un artículo, crear `pages/blog-mi-articulo.html` con la misma cabecera, menú y pie que las demás páginas; después añadir una tarjeta en `pages/blog.html` con su título, resumen, espacio para imagen y enlace relativo `blog-mi-articulo.html`. No añadir la tarjeta hasta que el archivo HTML exista.
