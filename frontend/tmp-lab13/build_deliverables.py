from __future__ import annotations

import hashlib
import os
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.shared import Inches, Pt
from docx.text.paragraph import Paragraph
from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(r"C:\Users\Paola\tienda-virtual-lab13")
FRONT = ROOT / "frontend"
EVIDENCE = FRONT / "evidencias"
DERIVED = EVIDENCE / "para-informe"
WORK = FRONT / "tmp-lab13"
TEMPLATE = FRONT / "GLAB-S13-JMIRANDA-2026-02-plantilla.docx"
OUTPUT = FRONT / "Laboratorio_13_LibroMundo_Paola.docx"
TXT_OUTPUT = FRONT / "Laboratorio_13_LibroMundo_Paola.txt"
EXPECTED_SHA = "f732bba6c1c91ffc5aeefde68371876727764a449a61e882041c2b4f58c41e26"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf")
    return ImageFont.truetype(str(path), size)


def crop_screenshot(name: str, crop: tuple[int, int, int, int] | None = None) -> Path:
    src = EVIDENCE / name
    im = Image.open(src).convert("RGB")
    if crop:
        im = im.crop(crop)
    else:
        # Remove only blank browser/editor margins. The pixels showing code remain intact.
        mask = ImageChops.difference(im, Image.new("RGB", im.size, "white")).convert("L")
        mask = mask.point(lambda px: 255 if px > 25 else 0)
        box = mask.getbbox()
        if box:
            left, top, right, bottom = box
            pad = 26
            im = im.crop((max(0, left - pad), max(0, top - pad), min(im.width, right + pad), min(im.height, bottom + pad)))
    target = DERIVED / (src.stem + "-informe.png")
    im.save(target, optimize=True)
    return target


def make_architecture() -> Path:
    w, h = 1800, 740
    im = Image.new("RGB", (w, h), "#f6f7f2")
    d = ImageDraw.Draw(im)
    d.text((80, 50), "Arquitectura de LibroMundo", fill="#153e32", font=font(52, True))
    d.text((82, 112), "Catálogo web con separación frontend, API y persistencia", fill="#52635c", font=font(29))
    boxes = [
        (80, 260, 480, 545, "React + Vite", "Interfaz del catálogo\nuseState · useEffect\nTailwind + shadcn/ui", "#e5f2e9"),
        (700, 260, 1100, 545, "Django REST", "Endpoints JSON\nSerializadores DRF\nValidación y consulta", "#e6eff4"),
        (1320, 260, 1720, 545, "SQLite", "Category 1 ── N Product\nDatos del catálogo\nMigraciones de Django", "#f2eddf"),
    ]
    for x1, y1, x2, y2, title, body, fill in boxes:
        d.rounded_rectangle((x1, y1, x2, y2), radius=28, fill=fill, outline="#9eb5a8", width=4)
        d.text((x1 + 28, y1 + 28), title, fill="#153e32", font=font(34, True))
        d.multiline_text((x1 + 30, y1 + 105), body, fill="#263a32", font=font(26), spacing=20)
    # REST JSON arrows and database flow.
    d.line((485, 400, 690, 400), fill="#24644f", width=10)
    d.polygon([(690, 400), (660, 382), (660, 418)], fill="#24644f")
    d.text((510, 340), "HTTP / JSON", fill="#24644f", font=font(23, True))
    d.text((510, 430), "GET catálogo", fill="#52635c", font=font(21))
    d.line((1105, 400, 1310, 400), fill="#24644f", width=10)
    d.polygon([(1310, 400), (1280, 382), (1280, 418)], fill="#24644f")
    d.text((1133, 340), "ORM", fill="#24644f", font=font(23, True))
    # Reverse direction for refresh response.
    d.line((700, 485, 490, 485), fill="#92a93e", width=6)
    d.polygon([(490, 485), (520, 470), (520, 500)], fill="#92a93e")
    d.text((520, 500), "Respuesta JSON", fill="#65772a", font=font(20))
    d.text((82, 635), "El navegador solicita categorías y productos; Django consulta la base y devuelve datos serializados.", fill="#52635c", font=font(24))
    target = DERIVED / "diagrama-arquitectura-libromundo.png"
    im.save(target, optimize=True)
    return target


def create_para_after(anchor: Paragraph, text: str = "", bold_prefix: str | None = None, page_break: bool = False) -> Paragraph:
    p = OxmlElement("w:p")
    anchor._p.addnext(p)
    para = Paragraph(p, anchor._parent)
    para.style = "Normal"
    para.paragraph_format.space_before = Pt(4)
    para.paragraph_format.space_after = Pt(6)
    para.paragraph_format.line_spacing = 1.08
    if page_break:
        para.paragraph_format.page_break_before = True
    if bold_prefix and text.startswith(bold_prefix):
        r = para.add_run(bold_prefix)
        r.bold = True
        para.add_run(text[len(bold_prefix):])
    else:
        para.add_run(text)
    for run in para.runs:
        run.font.name = "Calibri"
        run.font.size = Pt(10.5)
    return para


def add_solution(anchor: Paragraph, paragraphs: list[str]) -> Paragraph:
    current = create_para_after(anchor, "Desarrollo realizado")
    current.runs[0].bold = True
    current.runs[0].font.size = Pt(11)
    for body in paragraphs:
        current = create_para_after(current, body)
    return current


def add_figure(anchor: Paragraph, image: Path, label: str, note: str, number: str, max_width: float = 6.2, force_page: bool = True) -> Paragraph:
    p = OxmlElement("w:p")
    anchor._p.addnext(p)
    pic = Paragraph(p, anchor._parent)
    pic.style = "Normal"
    pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pic.paragraph_format.page_break_before = force_page
    pic.paragraph_format.keep_with_next = True
    pic.paragraph_format.space_before = Pt(4)
    pic.paragraph_format.space_after = Pt(3)
    with Image.open(image) as im:
        ratio = im.height / im.width
    width = min(max_width, 6.35 / ratio)
    pic.add_run().add_picture(str(image), width=Inches(width))
    prefix = number if number.startswith("Figura ") else f"Evidencia {number}"
    cap = create_para_after(pic, f"{prefix}. {label}")
    cap.paragraph_format.keep_with_next = True
    cap.paragraph_format.space_before = Pt(4)
    cap.paragraph_format.space_after = Pt(2)
    cap.runs[0].bold = True
    note_p = create_para_after(cap, "")
    note_p.paragraph_format.space_after = Pt(10)
    note_lead = note_p.add_run("Nota. ")
    note_lead.bold = True
    note_body = note_p.add_run(note)
    for run in (note_lead, note_body):
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
    return note_p


def find_anchor(doc: Document, needle: str) -> Paragraph:
    for p in doc.paragraphs:
        if needle.casefold() in p.text.casefold():
            return p
    raise ValueError(f"Missing template anchor: {needle}")


def load_txt() -> str:
    return """LABORATORIO 13 — LIBROMUNDO
Guía de ejecución y explicación detallada del trabajo
Fecha: 16 de noviembre de 2026
Proyecto: C:\\Users\\Paola\\tienda-virtual-lab13

1. Alcance del trabajo

Se completó la primera etapa de una tienda virtual llamada LibroMundo, con libros físicos y útiles escolares. El catálogo demostrativo contiene once productos en siete categorías para validar las fichas, la relación de datos y el filtrado. La aplicación no incorpora carrito, pagos, pedidos ni cuentas de clientes, de acuerdo con el alcance del laboratorio.

2. Estructura preparada

tienda-virtual-lab13/
  frontend/  React, Vite, Tailwind CSS, shadcn/ui, componentes y páginas
  backend/   Django, Django REST Framework, catálogo y SQLite
  README.md
  .gitignore

Dentro de frontend/src se separó el código en components, pages, services y lib. Los recursos gráficos de portada son SVG locales en frontend/public/catalog. En backend/catalog se encuentran los modelos, serializadores, vistas REST, rutas, administración y el comando de carga de datos.

3. Instalación y ejecución reproducible

Requisitos verificados en el entorno de trabajo: Node.js 24.15.0, npm 11.1.0, Python 3.12.10 y Git 2.55.0. El frontend usa React 19.3.1, Vite 8.3.6, Tailwind CSS 4.3.5 y shadcn/ui 4.23.0. El backend usa Django 6.1.3 y Django REST Framework 3.18.3.

En una terminal de Windows, desde la carpeta raíz:

Terminal 1 — backend:
  .\\backend\\.venv\\Scripts\\python.exe .\\backend\\manage.py migrate
  .\\backend\\.venv\\Scripts\\python.exe .\\backend\\manage.py seed_catalog
  .\\backend\\.venv\\Scripts\\python.exe .\\backend\\manage.py runserver 127.0.0.1:8000

Terminal 2 — frontend:
  cd frontend
  npm install
  npm run dev

Abrir http://127.0.0.1:5173/. Para comprobar la API, abrir http://127.0.0.1:8000/api/categories/ y http://127.0.0.1:8000/api/products/. El comando seed_catalog se puede ejecutar nuevamente para cargar de forma idempotente siete categorías y once productos de ejemplo. Para administrar registros en el panel Django, crear una cuenta propia con:
  .\\backend\\.venv\\Scripts\\python.exe .\\backend\\manage.py createsuperuser

Luego abrir http://127.0.0.1:8000/admin/. Los modelos Category y Product están registrados en ese panel. En esta entrega los datos de muestra se cargaron con el comando repetible, no mediante una sesión manual del panel; la interfaz administrativa permite editarlos después de iniciar sesión.

4. Implementación del frontend

SiteHeader presenta la marca y navegación. ProductCard recibe un producto por props y muestra portada, categoría, nombre, descripción, precio, stock y disponibilidad. ProductList construye las tarjetas con un array de productos. CategoryFilter presenta las categorías obtenidas del backend y comunica la selección a Storefront. ProductDetailsDialog utiliza el componente Dialog de shadcn/ui para mostrar el detalle accesible del libro.

En Storefront se usa useState para categorías, productos, filtro activo, búsqueda, carga, errores y producto seleccionado. useEffect ejecuta la consulta inicial mediante getCatalog y cancela solicitudes al desmontar la página mediante AbortController. La interfaz permite filtrar por categoría y buscar por nombre o descripción. Cuando la API falla, se muestra un error y la opción de reintentar.

5. Implementación del backend

Category guarda nombre, slug y descripción. Product guarda nombre, descripción, precio decimal, ruta/URL de imagen, stock, categoría, indicador de destacado y fecha de creación. La clave foránea Product.category establece la relación uno a muchos; cada categoría puede tener varios productos y cada producto pertenece a una categoría. Se generaron y ejecutaron migraciones sobre SQLite.

CategorySerializer y ProductSerializer convierten los modelos a JSON. El ViewSet de solo lectura expone GET /api/categories/ y GET /api/products/; también admite el parámetro de categoría. La ruta /api/health/ devuelve el estado de la API. El registro de admin.py añade búsquedas y filtros por categoría y destacado. El comando seed_catalog crea siete categorías y once productos.

6. Integración verificada

El servicio frontend centralizado en frontend/src/services/catalogService.js ejecuta fetch a la base API configurable por VITE_API_BASE_URL, valida el estado HTTP y devuelve los JSON. Storefront carga ambos recursos al entrar. Se verificó que /api/products/ respondió HTTP 200 con application/json y datos que incluyen id, nombre, descripción, precio, image_url, stock, categoría, nombre y slug de categoría y estado destacado. La interfaz mostró once productos; al elegir Útiles escolares presentó dos. Se abrió el detalle de un producto y se revisó la página en un viewport móvil.

7. Evidencias incorporadas al Word

Cada captura del Word se obtuvo del proyecto real, de su navegador local o de los archivos fuente. Las imágenes para el informe solo recortan márgenes vacíos para que el contenido sea legible; no se recreó una interfaz ni se inventó código. La nota bajo cada captura identifica qué actividad acredita.

8. Comprobaciones realizadas

  - npm run build: finalizó correctamente y generó frontend/dist.
  - npm run lint: finalizó sin errores.
  - Django system check: se revisó el proyecto y se corrigió un contexto de plantilla que impedía cargar la vista navegable de Django REST Framework.
  - Migraciones y base SQLite: tablas aplicadas; carga de catálogo completada con siete categorías y once productos.
  - HTTP local: endpoint de salud y endpoints del catálogo respondieron; listado de productos con HTTP 200 y JSON.
  - Navegador: catálogo, filtro de categoría, diálogo de detalle y presentación móvil comprobados sin errores de consola reportados.

9. Decisiones y límites

Los productos de demostración se cargan con seed_catalog para que otra persona pueda recrear la base de datos con una instrucción. Para usar Django Admin, cada usuario debe crear su propio superusuario. Se verificó el cambio de stock de Agenda de lecturas de 18 a 20 unidades desde el panel, y la interfaz React reflejó el nuevo dato después de consultar la API. El comando seed_catalog conserva la carga reproducible de siete categorías y once productos, incluida la actualización del stock. La aplicación utiliza SQLite y servidores de desarrollo locales. Para desplegarla se necesitaría configurar secretos, base de datos de producción, HTTPS, almacenamiento de imágenes y controles de seguridad.

10. GitHub

El proyecto todavía no tiene URL de repositorio. Se comprobó que el conector GitHub no está conectado en esta sesión, por lo que no se publicó ni se fabricó un enlace. Para completar este punto de la rúbrica, conectar GitHub y publicar la carpeta raíz tienda-virtual-lab13; después añadir la URL real en la línea siguiente.
URL del repositorio: pendiente de publicación y verificación.

"""


def main() -> None:
    if not TEMPLATE.exists():
        raise FileNotFoundError(TEMPLATE)
    actual = hashlib.sha256(TEMPLATE.read_bytes()).hexdigest()
    if actual != EXPECTED_SHA:
        raise ValueError(f"Template copy changed; expected {EXPECTED_SHA}, got {actual}")
    DERIVED.mkdir(parents=True, exist_ok=True)

    images = {
        "structure": crop_screenshot("00-estructura-proyecto.png", (0, 0, 420, 245)),
        "catalog": crop_screenshot("01-catalogo-en-ejecucion.png", (0, 740, 1440, 1940)),
        "filter": crop_screenshot("02-filtro-categoria.png", (70, 735, 760, 1500)),
        "detail": crop_screenshot("03-detalle-producto.png", (280, 100, 740, 555)),
        "mobile": crop_screenshot("04-vista-movil.png", (0, 0, 390, 760)),
        "api": crop_screenshot("05-api-productos-json.png", (0, 0, 390, 790)),
        "shadcn": crop_screenshot("06-config-shadcn-tailwind.png", (0, 0, 760, 460)),
        "package": crop_screenshot("07-dependencias-frontend.png", (0, 0, 660, 1000)),
        "card": crop_screenshot("08-codigo-productcard.png"),
        "service": crop_screenshot("09-codigo-servicio-rest.png"),
        "models": crop_screenshot("10-codigo-modelos-django.png"),
        "serializers": crop_screenshot("11-codigo-serializadores.png"),
        "admin": crop_screenshot("12-admin-productos.png"),
        "admin_update": crop_screenshot("14-producto-actualizado-admin.png", (0, 1300, 1440, 2200)),
        "architecture": make_architecture(),
    }

    doc = Document(TEMPLATE)
    # Fill only the cover metadata slots; the instructor's grade remains blank.
    cover = doc.tables[0]
    cover.cell(1, 0).text = "Paola"
    cover.cell(2, 1).text = "No indicado"
    cover.cell(3, 1).text = "16 de noviembre de 2026"

    # Exercise 01
    anchor = find_anchor(doc, "Elaborar un esquema sencillo que represente la comunicación")
    current = add_solution(anchor, [
        "Rubro elegido: librería. Nombre comercial: LibroMundo. La tienda propone vender libros físicos de distintos géneros y útiles escolares. Para esta primera versión se implementó un catálogo demostrativo de once productos organizados en siete categorías; así se puede verificar la relación entre los datos, el filtro y la interfaz antes de incorporar otros productos.",
        "La primera versión permite consultar el catálogo, buscar por nombre o descripción, filtrar por categoría, abrir la ficha de un producto y revisar precio, imagen, disponibilidad y stock. Para cada producto se almacenan nombre, descripción, precio en soles, categoría, ruta de imagen y cantidad disponible. También se usa un indicador de producto destacado.",
        "La interfaz se organiza con encabezado y marca, navegación, presentación principal, filtro de categorías, búsqueda, cuadrícula de tarjetas y diálogo de detalle. Cada tarjeta prioriza la portada, nombre, categoría, descripción breve, precio y stock.",
    ])
    current = add_figure(current, images["architecture"], "Esquema de comunicación entre React, Django REST Framework y SQLite", "Diagrama elaborado para esta práctica. React solicita el catálogo mediante HTTP; Django REST Framework serializa los modelos y el ORM consulta SQLite. La relación Category 1:N Product mantiene una categoría para cada producto y permite varios productos por categoría.", "Figura 1", 6.2)

    # Exercise 02
    anchor = find_anchor(doc, "Verificar que ambos proyectos puedan ejecutarse correctamente en el entorno local.")
    current = add_solution(anchor, [
        "Se organizó el repositorio local en una carpeta raíz con frontend y backend independientes. React con Vite se instaló en frontend; Django y Django REST Framework quedaron en backend. La estructura de React separa componentes, páginas y servicios, y el archivo raíz README.md documenta los comandos de ejecución.",
        "Tailwind CSS se configuró con su complemento de Vite. shadcn/ui quedó preparado con components.json, alias de importación y componentes reutilizables Button, Card, Badge, Input y Dialog. El ejemplo de dependencias y scripts está en package.json.",
        "Los dos servidores se ejecutaron en puertos locales separados: Vite en 5173 y Django en 8000. CORS permite que el frontend local consulte la API durante el desarrollo.",
    ])
    current = add_figure(current, images["structure"], "Estructura real de la carpeta del proyecto", "Captura del listado local del directorio raíz. Se distinguen frontend, backend, README.md y .gitignore, creados para separar las dos aplicaciones y sus instrucciones.", "1", 6.2, force_page=False)
    current = add_figure(current, images["shadcn"], "Configuración de shadcn/ui y Tailwind CSS", "Captura del archivo components.json del proyecto. La configuración define el estilo de componentes, el archivo CSS y los alias usados en el código React.", "2", 5.4)
    current = add_figure(current, images["package"], "Dependencias y comandos del frontend", "Captura real de package.json con scripts de Vite y dependencias instaladas de React, Tailwind CSS, Radix UI y shadcn/ui.", "3", 4.5)

    # Exercise 03
    anchor = find_anchor(doc, "Aplicar estilos utilizando Tailwind CSS y componentes de shadcn/ui")
    current = add_solution(anchor, [
        "SiteHeader presenta el logotipo tipográfico de LibroMundo y sus opciones principales. ProductCard recibe el objeto product y la función onOpen mediante props; ProductList recorre el arreglo y crea una tarjeta por producto. CategoryFilter emite la categoría elegida, y el estado de Storefront actualiza la lista que se muestra.",
        "La identidad visual utiliza verde bosque, lima suave y fondos marfil, con tipografía Geist. La cuadrícula, los controles y las tarjetas se adaptan a pantallas estrechas. Los componentes de shadcn/ui aportan botones, tarjetas, insignias, entradas y un diálogo de detalle.",
    ])
    current = add_figure(current, images["card"], "Componente ProductCard con datos recibidos por props", "Código fuente real de ProductCard.jsx. La tarjeta obtiene sus datos desde product, representa la portada, categoría, nombre, descripción, precio y stock, y usa onOpen para pedir a la página el detalle del producto.", "4", 6.2, force_page=False)

    # Exercise 04
    anchor = find_anchor(doc, "Verificar que los servicios devuelvan correctamente la información en formato JSON.")
    current = add_solution(anchor, [
        "La aplicación catalog define Category y Product. Product.category es una clave foránea protegida que expresa la relación uno a muchos. El modelo de producto contiene los campos mínimos solicitados y valida precio no negativo; la imagen se guarda como una ruta o URL y el stock como entero no negativo.",
        "Se generaron y aplicaron migraciones en SQLite. Ambos modelos se registraron en Django Admin con búsqueda y filtros. El comando idempotente seed_catalog creó siete categorías y once productos de ejemplo para que el estado inicial pueda reconstruirse. Los serializadores exponen los atributos del producto y el nombre/slug de su categoría; el serializador de categoría agrega el recuento de productos.",
        "Los ViewSets de solo lectura publican los listados de categorías y productos. La respuesta de productos puede filtrarse por categoría y se comprobó que la API devuelve JSON con estado HTTP 200.",
    ])
    current = add_figure(current, images["models"], "Modelos Category y Product y relación de uno a muchos", "Código fuente real de catalog/models.py. La clave foránea Product.category apunta a Category; los campos cubren nombre, descripción, precio, imagen, stock y categoría.", "5", 6.2)
    current = add_figure(current, images["serializers"], "Serializadores de categorías y productos", "Código fuente real de catalog/serializers.py. Los campos category_name y category_slug permiten que la interfaz muestre la categoría sin una consulta adicional.", "6", 6.2)
    current = add_figure(current, images["api"], "Respuesta JSON del endpoint de productos", "Captura real del endpoint GET /api/products/. Django REST Framework respondió HTTP 200 y application/json; los registros incluyen nombre, precio, ruta de imagen, stock y datos de categoría.", "7", 3.5)

    # Exercise 05
    anchor = find_anchor(doc, "Verificar que los cambios realizados en los productos desde el administrador de Django")
    current = add_solution(anchor, [
        "El módulo catalogService centraliza las solicitudes fetch a /api/categories/ y /api/products/. La dirección base puede cambiarse mediante VITE_API_BASE_URL. El servicio comprueba response.ok y propaga errores HTTP para que la página informe un problema de carga.",
        "Storefront usa useEffect para consultar el servicio cuando se monta la página y useState para conservar los datos y estados de interfaz. CategoryFilter se alimenta con las categorías recibidas por la API. El filtro y la búsqueda se aplican a la colección cargada, y la acción de reintento vuelve a consultar el backend. Al recargar el navegador, los cambios guardados en el panel de Django vuelven a consultarse.",
    ])
    current = add_figure(current, images["service"], "Servicio React que consulta los endpoints REST", "Código fuente real de catalogService.js. La función getCatalog consulta categorías y productos con fetch, comparte la señal de cancelación y devuelve ambos arreglos a Storefront.", "8", 6.2)
    current = add_figure(current, images["filter"], "Filtrado del catálogo con categorías recibidas desde la API", "Captura del sitio local con Útiles escolares seleccionado. La interfaz muestra los dos productos de esa categoría recibidos desde la API y comprueba que la selección actualiza la lista visible.", "9", 5.6)
    current = add_figure(current, images["admin"], "Productos registrados en Django Admin", "Captura real del panel administrativo. Se observan categorías, precios, stock y estado destacado; desde este listado se abre el formulario de edición del producto.", "10", 5.8)
    current = add_figure(current, images["admin_update"], "Cambio de stock aplicado desde la administración", "Captura real del producto Agenda de lecturas con 20 unidades disponibles, después de actualizar el campo stock en Django Admin. La carga reproducible seed_catalog conserva el valor actualizado.", "11", 5.8)

    # Exercise 06
    anchor = find_anchor(doc, "Identificar qué funcionalidades adicionales serían necesarias")
    current = add_solution(anchor, [
        "La revisión confirmó que las tarjetas presentan la información necesaria, el filtro responde a la selección y la ficha muestra categoría, descripción, precio y disponibilidad. El catálogo se consultó desde el backend y la vista móvil conserva controles legibles. Una siguiente etapa podría añadir carrito, pedidos, cuentas de cliente, pagos, almacenamiento de imágenes y controles de seguridad, funciones que exceden el alcance del laboratorio.",
    ])
    current = add_figure(current, images["catalog"], "Catálogo conectado y presentación de los productos", "Captura del navegador local con las once tarjetas recibidas desde Django, imágenes, categorías, precios en soles y cantidades disponibles.", "12", 6.2)
    current = add_figure(current, images["detail"], "Detalle de un producto en un diálogo accesible", "Captura real del diálogo de LibroMundo para “Cartas desde el sur”; confirma la presentación de categoría, descripción, precio y stock.", "13", 6.2)
    current = add_figure(current, images["mobile"], "Vista del catálogo en una pantalla móvil", "Captura tomada a 390 × 844 px. El encabezado, las categorías, la búsqueda y la tarjeta de producto se reorganizan para una columna estrecha.", "14", 3.6)

    # Replace the template's five blank list items in each final section, preserving their bullets.
    observations = [
        "El frontend y el backend requieren dos terminales durante el desarrollo local; React consulta la API mediante CORS en los puertos 5173 y 8000.",
        "El primer acceso a la API navegable mostró un error de contexto de Django. Se eliminó la referencia inválida al procesador de mensajes y se volvió a comprobar el JSON.",
        "Los libros de demostración se cargan con seed_catalog para repetir el estado inicial. Los modelos están registrados en Django Admin, que requiere crear un superusuario antes de iniciar sesión. Se actualizó desde el panel el stock de Agenda de lecturas de 18 a 20; el nuevo valor apareció en la tienda tras actualizar la consulta REST y se conservó en el comando seed_catalog.",
        "El catálogo incorpora útiles escolares, junto con libros de distintas categorías, y puede ampliarse con nuevos productos desde el panel de administración.",
        "El proyecto y las pruebas locales están preparados, pero falta publicar el repositorio GitHub porque la sesión no tiene una conexión GitHub confirmada; por eso el informe no muestra un enlace inventado.",
    ]
    conclusions = [
        "La separación entre React y Django permitió construir una interfaz que obtiene productos y categorías desde una API real. El contrato JSON mantiene los componentes de presentación independientes de las consultas HTTP.",
        "La relación uno a muchos entre Category y Product resuelve la clasificación del catálogo y permite filtrar productos por categoría. Las migraciones hacen reproducible la estructura SQLite.",
        "La división del frontend en componentes, página y servicio facilitó localizar responsabilidades. El diálogo de detalle reutiliza shadcn/ui y recibe los datos de la tarjeta seleccionada.",
        "Las comprobaciones locales mostraron el catálogo completo, el filtro de Narrativa, la respuesta JSON y la adaptación móvil. El ajuste del contexto de Django REST Framework permitió verificar también su vista navegable.",
        "La entrega deja una base funcional y ampliable. Antes de convertirla en una tienda transaccional se necesitan cuentas, pedidos, pagos y controles de seguridad; además, el catálogo se puede extender con nuevas líneas de productos desde Django Admin.",
    ]
    blanks_obs = [p for p in doc.paragraphs if p.text.strip().startswith("____")]
    # The first 10 underscore paragraphs belong to the two rubric sections.
    if len(blanks_obs) < 10:
        raise ValueError(f"Expected 10 blank conclusion/observation lines, found {len(blanks_obs)}")
    for para, text in zip(blanks_obs[:5], observations):
        para.text = text
    for para, text in zip(blanks_obs[5:10], conclusions):
        para.text = text
        para.paragraph_format.space_after = Pt(5)
    find_anchor(doc, "CONCLUSIONES:").paragraph_format.page_break_before = True

    doc.save(OUTPUT)
    TXT_OUTPUT.write_text(load_txt(), encoding="utf-8")
    print(f"DOCX={OUTPUT}")
    print(f"TXT={TXT_OUTPUT}")
    print(f"Figures={len(images)}")
    print(f"Reference SHA-256 verified={actual}")


if __name__ == "__main__":
    main()
