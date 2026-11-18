import { ArrowUpRight, Sparkles } from 'lucide-react'
import { Badge } from './ui/badge'
import { Button } from './ui/button'
import { Card } from './ui/card'

const soles = new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' })

export default function ProductCard({ product, onOpen }) {
  return (
    <Card className="product-card">
      <div className="product-cover-wrap">
        {product.is_featured && <Badge className="cover-label"><Sparkles size={11} /> Recomendado</Badge>}
        <span className="cover-stock">{product.stock > 0 ? `${product.stock} disponibles` : 'Agotado'}</span>
        <img
          className="product-cover"
          src={product.image_url || '/catalog/cover-default.svg'}
          alt={`Portada de ${product.name}`}
          loading="lazy"
        />
      </div>
      <div className="product-info">
        <p className="product-category">{product.category_name}</p>
        <h3 className="product-title">{product.name}</h3>
        <p className="product-description">{product.description}</p>
        <div className="product-bottom">
          <span className="product-price">{soles.format(Number(product.price))}</span>
          <Button className="detail-button" variant="secondary" onClick={() => onOpen(product)}>
            Ver detalle <ArrowUpRight size={13} />
          </Button>
        </div>
      </div>
    </Card>
  )
}
