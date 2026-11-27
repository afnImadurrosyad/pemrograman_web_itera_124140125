import { useEffect, useState } from 'react'
import './App.css'

const API_URL = 'http://localhost:6543/api/v1'

const emptyProduct = {
  name: '',
  description: '',
  price: '',
  sku: '',
  category_id: '',
}

function formatPrice(value) {
  return '$' + Number(value).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}

export default function App() {
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [filterCategory, setFilterCategory] = useState('')
  const [form, setForm] = useState(emptyProduct)
  const [editingId, setEditingId] = useState(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [newCategory, setNewCategory] = useState({ name: '', description: '' })

  async function loadData() {
    try {
      const [productsRes, categoriesRes] = await Promise.all([
        fetch(`${API_URL}/products`),
        fetch(`${API_URL}/categories`),
      ])
      setProducts(await productsRes.json())
      setCategories(await categoriesRes.json())
    } catch (err) {
      setError('Tidak dapat terhubung ke API di http://localhost:6543. Pastikan pserve berjalan.')
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  function handleFormChange(event) {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  function startEdit(product) {
    setEditingId(product.id)
    setForm({
      name: product.name,
      description: product.description || '',
      price: String(product.price),
      sku: product.sku,
      category_id: String(product.category_id),
    })
    setError('')
    setMessage('')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  function cancelEdit() {
    setEditingId(null)
    setForm(emptyProduct)
    setError('')
  }

  async function submitProduct(event) {
    event.preventDefault()
    setError('')
    setMessage('')
    const payload = {
      name: form.name,
      description: form.description,
      price: parseFloat(form.price),
      category_id: parseInt(form.category_id, 10),
    }
    if (!editingId) {
      payload.sku = form.sku
    }
    const url = editingId
      ? `${API_URL}/products/${editingId}`
      : `${API_URL}/products`
    const method = editingId ? 'PUT' : 'POST'
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      const firstError = data.errors
        ? Object.values(data.errors).flat().join(' ')
        : 'Gagal menyimpan produk.'
      setError(firstError)
      return
    }
    setMessage(editingId ? 'Produk berhasil diperbarui.' : 'Produk berhasil ditambahkan.')
    cancelEdit()
    loadData()
  }

  async function deleteProduct(id, name) {
    if (!window.confirm(`Hapus produk "${name}"?`)) {
      return
    }
    const res = await fetch(`${API_URL}/products/${id}`, { method: 'DELETE' })
    if (res.ok || res.status === 204) {
      setMessage('Produk berhasil dihapus.')
      loadData()
    } else {
      setError('Gagal menghapus produk.')
    }
  }

  async function submitCategory(event) {
    event.preventDefault()
    setError('')
    setMessage('')
    const res = await fetch(`${API_URL}/categories`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCategory),
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      const firstError = data.errors
        ? Object.values(data.errors).flat().join(' ')
        : 'Gagal menyimpan kategori.'
      setError(firstError)
      return
    }
    setMessage('Kategori berhasil ditambahkan.')
    setNewCategory({ name: '', description: '' })
    loadData()
  }

  async function deleteCategory(id, name) {
    if (!window.confirm(`Hapus kategori "${name}"? Produk di dalamnya tetap tersimpan.`)) {
      return
    }
    const res = await fetch(`${API_URL}/categories/${id}`, { method: 'DELETE' })
    if (res.ok || res.status === 204) {
      setMessage('Kategori berhasil dihapus.')
      loadData()
    } else {
      setError('Gagal menghapus kategori.')
    }
  }

  const visibleProducts = filterCategory
    ? products.filter((p) => String(p.category_id) === filterCategory)
    : products

  return (
    <div className="page">
      <header className="header">
        <h1>ProductsAPI</h1>
        <p>Manajemen kategori dan produk — Praktikum PAW Pertemuan 7</p>
      </header>

      {error && <div className="alert alert-error">{error}</div>}
      {message && <div className="alert alert-success">{message}</div>}

      <section className="card">
        <h2>{editingId ? 'Ubah Produk' : 'Tambah Produk'}</h2>
        <form onSubmit={submitProduct} className="form">
          <label>
            Nama produk
            <input
              name="name"
              value={form.name}
              onChange={handleFormChange}
              required
              minLength={2}
              maxLength={100}
              placeholder="Contoh: Laptop Premium"
            />
          </label>
          <label>
            Deskripsi
            <input
              name="description"
              value={form.description}
              onChange={handleFormChange}
              maxLength={500}
              placeholder="Deskripsi singkat produk"
            />
          </label>
          <label>
            Harga
            <input
              name="price"
              type="number"
              step="0.01"
              min="0.01"
              value={form.price}
              onChange={handleFormChange}
              required
              placeholder="99.99"
            />
          </label>
          <label>
            SKU
            <input
              name="sku"
              value={form.sku}
              onChange={handleFormChange}
              required
              minLength={5}
              maxLength={50}
              disabled={!!editingId}
              placeholder="Contoh: LP1001"
            />
          </label>
          <label>
            Kategori
            <select
              name="category_id"
              value={form.category_id}
              onChange={handleFormChange}
              required
            >
              <option value="">Pilih kategori</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </label>
          <div className="form-actions">
            <button type="submit" className="btn btn-primary">
              {editingId ? 'Simpan Perubahan' : 'Tambah Produk'}
            </button>
            {editingId && (
              <button type="button" className="btn" onClick={cancelEdit}>
                Batal
              </button>
            )}
          </div>
        </form>
      </section>

      <section className="card">
        <div className="section-head">
          <h2>Daftar Produk ({visibleProducts.length})</h2>
          <label className="filter">
            Kategori
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
            >
              <option value="">Semua kategori</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </label>
        </div>
        {visibleProducts.length === 0 ? (
          <p className="empty">Belum ada produk untuk kategori ini.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Nama</th>
                <th>Kategori</th>
                <th>SKU</th>
                <th>Harga</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              {visibleProducts.map((product) => (
                <tr key={product.id}>
                  <td>
                    <strong>{product.name}</strong>
                    {product.description && (
                      <div className="muted">{product.description}</div>
                    )}
                  </td>
                  <td>{product.category ? product.category.name : '-'}</td>
                  <td>{product.sku}</td>
                  <td>{formatPrice(product.price)}</td>
                  <td className="actions">
                    <button
                      className="btn btn-small"
                      onClick={() => startEdit(product)}
                    >
                      Ubah
                    </button>
                    <button
                      className="btn btn-small btn-danger"
                      onClick={() => deleteProduct(product.id, product.name)}
                    >
                      Hapus
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section className="card">
        <h2>Kategori ({categories.length})</h2>
        <form onSubmit={submitCategory} className="form form-inline">
          <label>
            Nama kategori
            <input
              value={newCategory.name}
              onChange={(e) => setNewCategory({ ...newCategory, name: e.target.value })}
              required
              minLength={2}
              maxLength={100}
              placeholder="Contoh: Aksesoris"
            />
          </label>
          <label>
            Deskripsi
            <input
              value={newCategory.description}
              onChange={(e) => setNewCategory({ ...newCategory, description: e.target.value })}
              maxLength={500}
              placeholder="Deskripsi singkat kategori"
            />
          </label>
          <button type="submit" className="btn btn-primary">
            Tambah Kategori
          </button>
        </form>
        <ul className="category-list">
          {categories.map((category) => (
            <li key={category.id}>
              <span>
                <strong>{category.name}</strong>
                <span className="muted">
                  {' '}
                  — {category.products ? category.products.length : 0} produk
                </span>
              </span>
              <button
                className="btn btn-small btn-danger"
                onClick={() => deleteCategory(category.id, category.name)}
              >
                Hapus
              </button>
            </li>
          ))}
        </ul>
      </section>

      <footer className="footer">
        Backend: Pyramid + SQLAlchemy + Alembic di http://localhost:6543
      </footer>
    </div>
  )
}
