import { useState } from 'react'
import { ArrowUpRight, BookOpen, Menu, Search, X } from 'lucide-react'
import { Button } from './ui/button'

export default function SiteHeader() {
  const [menuOpen, setMenuOpen] = useState(false)
  return (
    <>
      <div className="announcement">ENVÍO GRATIS EN COMPRAS MAYORES A S/ 120 · LECTURAS PARA CADA MOMENTO</div>
      <header className="site-header">
        <div className="nav-wrap">
          <a className="brand" href="#inicio" aria-label="LibroMundo, inicio">
            <span className="brand-mark"><BookOpen size={19} strokeWidth={2.3} /></span>
            <span>libro<span style={{ color: 'var(--forest)' }}>mundo</span></span>
          </a>
          <nav className={`nav-links ${menuOpen ? 'mobile-open' : ''}`} aria-label="Navegación principal" onClick={() => setMenuOpen(false)}>
            <a href="#inicio">Inicio</a>
            <a href="#catalogo">Catálogo</a>
            <a href="#seleccion">Selección editorial</a>
          </nav>
          <div className="nav-actions">
            <a className="nav-icon" href="#catalogo" aria-label="Buscar en el catálogo"><Search size={17} /></a>
            <Button asChild size="sm" className="nav-cta"><a href="#catalogo">Explorar <ArrowUpRight size={14} /></a></Button>
            <button className="nav-icon mobile-menu" type="button" aria-label={menuOpen ? 'Cerrar navegación' : 'Abrir navegación'} aria-expanded={menuOpen} onClick={() => setMenuOpen((open) => !open)}>{menuOpen ? <X size={18} /> : <Menu size={18} />}</button>
          </div>
        </div>
      </header>
    </>
  )
}
