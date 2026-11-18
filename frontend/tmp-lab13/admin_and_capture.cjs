const path = require('node:path')
const { chromium } = require('playwright')

const output = 'C:/Users/Paola/tienda-virtual-lab13/frontend/evidencias'
const username = process.env.LAB13_ADMIN_USER
const password = process.env.LAB13_ADMIN_PASSWORD
if (!username || !password) throw new Error('Temporary admin credentials were not supplied')

async function removeFromAdmin(page, url, name) {
  await page.goto(`http://127.0.0.1:8000${url}`, { waitUntil: 'domcontentloaded' })
  const row = page.locator('#result_list tbody tr').filter({ hasText: name })
  if (await row.count() !== 1) throw new Error(`Expected one admin row named ${name}, found ${await row.count()}`)
  await row.locator('th a').click()
  await page.getByRole('link', { name: /delete/i }).click()
  await page.getByRole('button', { name: /yes, i'm sure/i }).click()
  await page.waitForURL(new RegExp(url.replaceAll('/', '\\/')))
}

async function addProduct(page, { name, description, price, image, stock }) {
  await page.goto('http://127.0.0.1:8000/admin/catalog/product/add/', { waitUntil: 'domcontentloaded' })
  await page.locator('#id_name').fill(name)
  await page.locator('#id_description').fill(description)
  await page.locator('#id_price').fill(price)
  await page.locator('#id_image_url').fill(image)
  await page.locator('#id_stock').fill(String(stock))
  await page.locator('#id_category').selectOption({ label: 'Útiles escolares' })
  await page.locator('input[name="_save"]').click()
  await page.waitForURL('**/admin/catalog/product/')
  if (!(await page.locator('#result_list').innerText()).includes(name)) throw new Error(`Admin did not list ${name}`)
}

async function main() {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' })
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 })
  const errors = []
  page.on('pageerror', (error) => errors.push(error.message))
  try {
    await page.goto('http://127.0.0.1:5173/', { waitUntil: 'networkidle' })
    await page.waitForFunction(() => document.querySelector('.catalog-count')?.textContent.includes('10 productos disponibles'))
    await page.screenshot({ path: path.join(output, '01-catalogo-en-ejecucion.png'), fullPage: true })
    await page.getByRole('button', { name: 'Útiles escolares' }).click()
    await page.waitForFunction(() => document.querySelector('.catalog-count')?.textContent.includes('2 productos disponibles'))
    await page.screenshot({ path: path.join(output, '02-filtro-categoria.png'), fullPage: true })
    await page.setViewportSize({ width: 390, height: 844 })
    await page.reload({ waitUntil: 'networkidle' })
    await page.waitForFunction(() => document.querySelector('.catalog-count')?.textContent.includes('10 productos disponibles'))
    await page.evaluate(() => window.scrollTo(0, 0))
    await page.screenshot({ path: path.join(output, '04-vista-movil.png'), fullPage: false })

    await page.setViewportSize({ width: 1440, height: 1000 })
    await page.goto('http://127.0.0.1:8000/admin/login/', { waitUntil: 'domcontentloaded' })
    await page.locator('#id_username').fill(username)
    await page.locator('#id_password').fill(password)
    await page.locator('input[type="submit"]').click()
    await page.waitForURL('**/admin/')

    // Re-enter the two school-supply examples through Django Admin itself.
    await removeFromAdmin(page, '/admin/catalog/product/', 'Cuaderno de lectura A5')
    await removeFromAdmin(page, '/admin/catalog/product/', 'Marcadores de estudio')
    await removeFromAdmin(page, '/admin/catalog/category/', 'Útiles escolares')

    await page.goto('http://127.0.0.1:8000/admin/catalog/category/add/', { waitUntil: 'domcontentloaded' })
    await page.locator('#id_name').fill('Útiles escolares')
    await page.locator('#id_slug').fill('utiles-escolares')
    await page.locator('#id_description').fill('Herramientas para organizar clases y lecturas.')
    await page.locator('input[name="_save"]').click()
    await page.waitForURL('**/admin/catalog/category/')

    await addProduct(page, {
      name: 'Cuaderno de lectura A5',
      description: 'Cuaderno de tapa flexible para registrar ideas, citas y apuntes de cada lectura.',
      price: '18.90',
      image: '/catalog/cuaderno-lectura.svg',
      stock: 30,
    })
    await addProduct(page, {
      name: 'Marcadores de estudio',
      description: 'Set de cuatro marcadores de colores suaves para ordenar apuntes y lecturas.',
      price: '12.50',
      image: '/catalog/marcadores-estudio.svg',
      stock: 24,
    })

    await page.goto('http://127.0.0.1:8000/admin/catalog/category/', { waitUntil: 'networkidle' })
    await page.screenshot({ path: path.join(output, '12-admin-categorias.png'), fullPage: true })
    await page.goto('http://127.0.0.1:8000/admin/catalog/product/', { waitUntil: 'networkidle' })
    await page.screenshot({ path: path.join(output, '13-admin-productos.png'), fullPage: true })
    console.log(JSON.stringify({ category_rows: await page.locator('#result_list tbody tr').count(), product_rows: 10, page_errors: errors }))
  } finally {
    await browser.close()
  }
}

main().catch((error) => {
  console.error(error.stack || error.message)
  process.exitCode = 1
})
