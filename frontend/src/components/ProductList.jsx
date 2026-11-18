import ProductCard from './ProductCard.jsx'

export default function ProductList({ products, loading, error, onOpen, onRetry }) {
  if (loading) {
    return <div className="product-grid" aria-live="polite"><div className="loading-state"><div><div className="loading-spinner" /><strong>Estamos preparando tu catálogo</strong><p>Conectando con el servicio de productos…</p></div></div></div>
  }

  if (error) {
    return <div className="product-grid" role="alert"><div className="error-state"><div><strong>No pudimos cargar el catálogo</strong><p>{error} Comprueba que Django esté ejecutándose y vuelve a intentar.</p><button className="retry-button" onClick={onRetry} type="button">Volver a intentar</button></div></div></div>
  }

  if (products.length === 0) {
    return <div className="product-grid"><div className="empty-state"><div><strong>No encontramos libros con esos criterios</strong><p>Prueba con otra categoría o cambia el texto de búsqueda.</p></div></div></div>
  }

  return <div className="product-grid">{products.map((product) => <ProductCard key={product.id} product={product} onOpen={onOpen} />)}</div>
}
