export default function CategoryFilter({ categories, selected, onSelect }) {
  return (
    <div className="category-list" role="group" aria-label="Filtrar por categoría">
      <button
        className={`category-pill ${selected === 'all' ? 'active' : ''}`}
        onClick={() => onSelect('all')}
        type="button"
        aria-pressed={selected === 'all'}
      >
        Todos los libros
      </button>
      {categories.map((category) => (
        <button
          className={`category-pill ${selected === String(category.id) ? 'active' : ''}`}
          key={category.id}
          onClick={() => onSelect(String(category.id))}
          type="button"
          aria-pressed={selected === String(category.id)}
        >
          {category.name}
        </button>
      ))}
    </div>
  )
}
