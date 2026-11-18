from decimal import Decimal

from django.core.management.base import BaseCommand

from catalog.models import Category, Product


CATALOG = [
    {
        "category": ("Narrativa", "narrativa", "Historias para leer sin prisa."),
        "name": "La ciudad de las mareas",
        "description": "Una novela sobre memoria, viajes y las pequeñas decisiones que transforman una ciudad.",
        "price": "58.00",
        "stock": 12,
        "image_url": "/catalog/ciudad-mareas.svg",
        "is_featured": True,
    },
    {
        "category": ("Narrativa", "narrativa", "Historias para leer sin prisa."),
        "name": "Cartas desde el sur",
        "description": "Relatos íntimos ambientados entre montañas, costa y barrios de Lima.",
        "price": "46.50",
        "stock": 8,
        "image_url": "/catalog/cartas-sur.svg",
        "is_featured": True,
    },
    {
        "category": ("Diseño", "diseno", "Ideas visuales y herramientas creativas."),
        "name": "Diseñar con intención",
        "description": "Una guía práctica para construir identidades visuales claras y con propósito.",
        "price": "89.00",
        "stock": 5,
        "image_url": "/catalog/disenar-intencion.svg",
        "is_featured": True,
    },
    {
        "category": ("Bienestar", "bienestar", "Lecturas para aprender y cuidarse."),
        "name": "Pequeños hábitos, grandes días",
        "description": "Ideas simples para organizar el tiempo, descansar mejor y sostener nuevos hábitos.",
        "price": "64.90",
        "stock": 16,
        "image_url": "/catalog/pequenos-habitos.svg",
        "is_featured": False,
    },
    {
        "category": ("Infantil", "infantil", "Libros ilustrados para lectores curiosos."),
        "name": "El jardín de los planetas",
        "description": "Una aventura ilustrada para descubrir el sistema solar y cuidar la imaginación.",
        "price": "42.00",
        "stock": 9,
        "image_url": "/catalog/jardin-planetas.svg",
        "is_featured": True,
    },
    {
        "category": ("Tecnología", "tecnologia", "Conocimiento para crear y resolver problemas."),
        "name": "Interfaces que acompañan",
        "description": "Principios de diseño de productos digitales accesibles, útiles y coherentes.",
        "price": "96.00",
        "stock": 4,
        "image_url": "/catalog/interfaces.svg",
        "is_featured": False,
    },
    {
        "category": ("Infantil", "infantil", "Libros ilustrados para lectores curiosos."),
        "name": "Atlas de animales andinos",
        "description": "Un recorrido visual por especies, paisajes y ecosistemas de los Andes.",
        "price": "53.50",
        "stock": 7,
        "image_url": "/catalog/atlas-andino.svg",
        "is_featured": False,
    },
    {
        "category": ("Tecnología", "tecnologia", "Conocimiento para crear y resolver problemas."),
        "name": "Código con propósito",
        "description": "Una introducción accesible a la lógica, la colaboración y el desarrollo responsable.",
        "price": "78.00",
        "stock": 10,
        "image_url": "/catalog/codigo-proposito.svg",
        "is_featured": False,
    },
    {
        "category": ("Útiles escolares", "utiles-escolares", "Herramientas para organizar clases y lecturas."),
        "name": "Cuaderno de lectura A5",
        "description": "Cuaderno de tapa flexible para registrar ideas, citas y apuntes de cada lectura.",
        "price": "18.90",
        "stock": 30,
        "image_url": "/catalog/cuaderno-lectura.svg",
        "is_featured": False,
    },
    {
        "category": ("Útiles escolares", "utiles-escolares", "Herramientas para organizar clases y lecturas."),
        "name": "Marcadores de estudio",
        "description": "Set de cuatro marcadores de colores suaves para ordenar apuntes y lecturas.",
        "price": "12.50",
        "stock": 24,
        "image_url": "/catalog/marcadores-estudio.svg",
        "is_featured": False,
    },
    {
        "category": ("Papel y escritura", "papel-escritura", "Agendas y cuadernos para acompañar cada lectura."),
        "name": "Agenda de lecturas",
        "description": "Agenda semanal para anotar libros pendientes, citas favoritas y notas de lectura.",
        "price": "22.90",
        "stock": 20,
        "image_url": "/catalog/agenda-lecturas.svg",
        "is_featured": False,
    },
]


class Command(BaseCommand):
    help = "Crea o actualiza las categorías y productos de ejemplo de LibroMundo."

    def handle(self, *args, **options):
        for data in CATALOG:
            category_name, slug, description = data["category"]
            product_data = {key: value for key, value in data.items() if key != "category"}
            category, _ = Category.objects.update_or_create(
                slug=slug,
                defaults={"name": category_name, "description": description},
            )
            Product.objects.update_or_create(
                name=product_data["name"],
                defaults={
                    **product_data,
                    "price": Decimal(product_data["price"]),
                    "category": category,
                },
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"Catálogo listo: {Category.objects.count()} categorías y {Product.objects.count()} productos."
            )
        )
