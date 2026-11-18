const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

async function request(path, signal) {
  const response = await fetch(`${API_BASE}${path}`, { signal })
  if (!response.ok) {
    throw new Error(`El servicio respondió con el código ${response.status}.`)
  }
  return response.json()
}

export async function getCatalog(signal) {
  const [categories, products] = await Promise.all([
    request('/categories/', signal),
    request('/products/', signal),
  ])

  return { categories, products }
}
