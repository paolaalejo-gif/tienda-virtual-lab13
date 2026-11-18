import { X } from 'lucide-react'
import { Badge } from './ui/badge'
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogTitle,
} from './ui/dialog'

const soles = new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' })

export default function ProductDetailsDialog({ product, onClose }) {
  return (
    <Dialog open={Boolean(product)} onOpenChange={(open) => !open && onClose()}>
      {product && (
        <DialogContent className="dialog-content" showCloseButton={false}>
          <DialogClose className="dialog-close" aria-label="Cerrar detalle"><X size={17} /></DialogClose>
          <div className="dialog-layout">
            <div className="dialog-cover-bg">
              <img className="dialog-cover" src={product.image_url || '/catalog/cover-default.svg'} alt={`Portada de ${product.name}`} />
            </div>
            <div className="dialog-details">
              <Badge variant="secondary">{product.category_name}</Badge>
              <DialogTitle>{product.name}</DialogTitle>
              <DialogDescription>{product.description}</DialogDescription>
              <div className="dialog-price">{soles.format(Number(product.price))}</div>
              <div className="dialog-meta">
                <span className="meta-chip">Stock: {product.stock} unidades</span>
                <span className="meta-chip">{product.stock > 0 ? 'Disponible' : 'Sin stock'}</span>
              </div>
            </div>
          </div>
        </DialogContent>
      )}
    </Dialog>
  )
}
