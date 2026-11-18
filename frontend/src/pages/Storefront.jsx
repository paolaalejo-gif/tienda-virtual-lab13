import { useEffect, useMemo, useState } from 'react'
import { ArrowDown, ArrowUpRight, BookOpen, Headphones, Leaf, Search } from 'lucide-react'
import { Input } from '../components/ui/input.tsx'
import SiteHeader from '../components/SiteHeader.jsx'
import CategoryFilter from '../components/CategoryFilter.jsx'
import ProductDetailsDialog from '../components/ProductDetailsDialog.jsx'
import ProductList from '../components/ProductList.jsx'
import { getCatalog } from '../services/catalogService.js'

export default function Storefront() {
  const [catalog, setCatalog] = useState({ categories: [], products: [] })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [search, setSearch] = useState('')
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [reloadToken, setReloadToken] = useState(0)

  useEffect(() => {
    const controller = new AbortController()

    getCatalog(controller.signal)
      .then(setCatalog)
      .catch((requestError) => {
        if (requestError.name !== 'AbortError') setError(requestError.message || 'Ocurrió un problema al consultar la API.')
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false)
      })

    return () => controller.abort()
  }, [reloadToken])

  const visibleProducts = useMemo(() => {
    const normalizedSearch = search.trim().toLocaleLowerCase('es')
    return catalog.products.filter((product) => {
      const matchesCategory = selectedCategory === 'all' || String(product.category) === selectedCategory
      const matchesSearch = !normalizedSearch || `${product.name} ${product.description} ${product.category_name}`.toLocaleLowerCase('es').includes(normalizedSearch)
      return matchesCategory && matchesSearch
    })
  }, [catalog.products, search, selectedCategory])

  const featured = catalog.products.find((product) => product.is_featured) || catalog.products[0]
  const retryCatalog = () => {
    setLoading(true)
    setError('')
    setReloadToken((value) => value + 1)
  }

  return (
    <div id="inicio">
      <SiteHeader />
      <main className="store-shell">
        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-copy">
            <p className="eyebrow">Una librería para descubrir</p>
            <h1 id="hero-title">Historias que abren <span>nuevos mundos.</span></h1>
            <p>Curamos libros para acompañar tus ideas, tus pausas y todo lo que todavía estás por imaginar.</p>
            <a className="hero-cta" href="#catalogo">Descubrir el catálogo <ArrowUpRight size={16} /></a>
          </div>
          <div className="hero-art" aria-label="Selección de lecturas recomendadas">
            <img className="hero-book" src={featured?.image_url || '/catalog/ciudad-mareas.svg'} alt={featured ? `Libro recomendado: ${featured.name}` : 'Libro recomendado de LibroMundo'} />
            <div className="hero-note"><strong>Selección de la semana</strong>Ideas nuevas para tus días.</div>
          </div>
        </section>

        <section className="value-row" aria-label="Beneficios de LibroMundo">
          <div className="value-item"><div className="value-icon"><BookOpen size={17} /></div><div><strong>Lecturas con intención</strong><span>Una selección para cada curiosidad</span></div></div>
          <div className="value-item"><div className="value-icon"><Leaf size={17} /></div><div><strong>Compra consciente</strong><span>Libros que vale la pena conservar</span></div></div>
          <div className="value-item"><div className="value-icon"><Headphones size={17} /></div><div><strong>Atención cercana</strong><span>Te ayudamos a encontrar tu próxima lectura</span></div></div>
        </section>

        <section id="catalogo" aria-labelledby="catalog-title">
          <div className="section-heading">
            <div><p className="eyebrow">Curado para ti</p><h2 id="catalog-title">Explora el catálogo</h2></div>
            <p className="section-caption">Encuentra algo que quieras llevar contigo.</p>
          </div>
          <div className="catalog-tools">
            <CategoryFilter categories={catalog.categories} selected={selectedCategory} onSelect={setSelectedCategory} />
            <label className="catalog-search">
              <Search size={16} aria-hidden="true" />
              <Input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Buscar un producto…" aria-label="Buscar por nombre o descripción" />
            </label>
          </div>
          <div className="catalog-count" aria-live="polite">{loading ? 'Cargando…' : `${visibleProducts.length} ${visibleProducts.length === 1 ? 'producto disponible' : 'productos disponibles'}`}</div>
          <ProductList
            products={visibleProducts}
            loading={loading}
            error={error}
            onOpen={setSelectedProduct}
            onRetry={retryCatalog}
          />
        </section>

        <section className="newsletter" id="seleccion">
          <div><h3>Las buenas historias siempre encuentran su momento.</h3><p>Vuelve pronto para descubrir nuevas incorporaciones al catálogo.</p></div>
          <div className="newsletter-tag">Hecho para lectores curiosos <ArrowDown size={13} /></div>
        </section>
        <footer className="footer"><span>© 2026 LibroMundo · Librería independiente</span><span>Catálogo conectado a servicios REST · Lima, Perú</span></footer>
      </main>
      <ProductDetailsDialog product={selectedProduct} onClose={() => setSelectedProduct(null)} />
    </div>
  )
}
