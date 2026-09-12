import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

// Telegram WebApp integration
const tg = window.Telegram.WebApp

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

function App() {
  const [activeTab, setActiveTab] = useState('cars')
  const [cars, setCars] = useState([])
  const [requests, setRequests] = useState([])
  const [faqs, setFaqs] = useState([])
  const [showModal, setShowModal] = useState(false)
  const [editingCar, setEditingCar] = useState(null)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: '',
    year: '',
    mileage: '',
    condition: 'Не бита/не крашена',
    photo_url: ''
  })

  useEffect(() => {
    // Инициализация Telegram WebApp
    tg.ready()
    tg.expand()
    
    // Настройка темы
    document.body.style.backgroundColor = tg.themeParams.bg_color || '#f5f5f5'
    document.body.style.color = tg.themeParams.text_color || '#333'
    
    fetchCars()
    fetchRequests()
    fetchFaqs()
  }, [])

  const fetchCars = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/cars`)
      setCars(response.data)
    } catch (error) {
      console.error('Error fetching cars:', error)
    }
  }

  const fetchRequests = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/requests`)
      setRequests(response.data)
    } catch (error) {
      console.error('Error fetching requests:', error)
    }
  }

  const fetchFaqs = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/faq`)
      setFaqs(response.data)
    } catch (error) {
      console.error('Error fetching FAQs:', error)
    }
  }

  const handleAddCar = () => {
    setEditingCar(null)
    setFormData({
      title: '',
      description: '',
      price: '',
      year: '',
      mileage: '',
      condition: 'Не бита/не крашена',
      photo_url: ''
    })
    setShowModal(true)
  }

  const handleEditCar = (car) => {
    setEditingCar(car)
    setFormData({
      title: car.title,
      description: car.description,
      price: car.price,
      year: car.year,
      mileage: car.mileage,
      condition: car.condition,
      photo_url: car.photo_url || ''
    })
    setShowModal(true)
  }

  const handleSaveCar = async () => {
    try {
      if (editingCar) {
        await axios.put(`${API_URL}/api/cars/${editingCar.id}`, formData)
      } else {
        await axios.post(`${API_URL}/api/cars`, formData)
      }
      setShowModal(false)
      fetchCars()
    } catch (error) {
      console.error('Error saving car:', error)
    }
  }

  const handleDeleteCar = async (carId) => {
    try {
      await axios.delete(`${API_URL}/api/cars/${carId}`)
      fetchCars()
    } catch (error) {
      console.error('Error deleting car:', error)
    }
  }

  const handlePublishCar = async (carId) => {
    try {
      await axios.post(`${API_URL}/api/cars/${carId}/publish`)
      fetchCars()
    } catch (error) {
      console.error('Error publishing car:', error)
    }
  }

  const handleProcessRequest = async (requestId) => {
    try {
      await axios.put(`${API_URL}/api/requests/${requestId}/process`)
      fetchRequests()
    } catch (error) {
      console.error('Error processing request:', error)
    }
  }

  const handleAddFaq = async () => {
    const question = prompt('Вопрос:')
    const answer = prompt('Ответ:')
    if (question && answer) {
      try {
        await axios.post(`${API_URL}/api/faq`, { question, answer })
        fetchFaqs()
      } catch (error) {
        console.error('Error adding FAQ:', error)
      }
    }
  }

  const handleDeleteFaq = async (faqId) => {
    try {
      await axios.delete(`${API_URL}/api/faq/${faqId}`)
      fetchFaqs()
    } catch (error) {
      console.error('Error deleting FAQ:', error)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🚗 Админ-панель перекупа</h1>
        <nav className="nav">
          <button 
            className={activeTab === 'cars' ? 'active' : ''} 
            onClick={() => setActiveTab('cars')}
          >
            Автомобили
          </button>
          <button 
            className={activeTab === 'requests' ? 'active' : ''} 
            onClick={() => setActiveTab('requests')}
          >
            Заявки
          </button>
          <button 
            className={activeTab === 'faq' ? 'active' : ''} 
            onClick={() => setActiveTab('faq')}
          >
            FAQ
          </button>
        </nav>
      </header>

      <main className="main">
        {activeTab === 'cars' && (
          <div className="section">
            <div className="section-header">
              <h2>Автомобили</h2>
              <button className="btn btn-primary" onClick={handleAddCar}>
                + Добавить автомобиль
              </button>
            </div>
            <div className="cars-list">
              {cars.map(car => (
                <div key={car.id} className="car-card">
                  {car.photo_url && (
                    <img src={car.photo_url} alt={car.title} className="car-photo" />
                  )}
                  <div className="car-info">
                    <h3>{car.title}</h3>
                    <p className="price">{car.price.toLocaleString()} ₽</p>
                    <p className="details">
                      {car.year} г. • {car.mileage.toLocaleString()} км • {car.condition}
                    </p>
                    <p className="description">{car.description}</p>
                    <div className="car-actions">
                      <button className="btn btn-secondary" onClick={() => handleEditCar(car)}>
                        Редактировать
                      </button>
                      <button className="btn btn-success" onClick={() => handlePublishCar(car.id)}>
                        Опубликовать
                      </button>
                      <button className="btn btn-danger" onClick={() => handleDeleteCar(car.id)}>
                        Удалить
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'requests' && (
          <div className="section">
            <div className="section-header">
              <h2>Заявки</h2>
            </div>
            <div className="requests-list">
              {requests.map(request => (
                <div key={request.id} className={`request-card ${request.is_processed ? 'processed' : ''}`}>
                  <h3>Заявка #{request.id}</h3>
                  <p>Автомобиль ID: {request.car_id}</p>
                  <p>Пользователь ID: {request.user_id}</p>
                  <p className="message">{request.message}</p>
                  <p className="date">{new Date(request.created_at).toLocaleString()}</p>
                  {!request.is_processed && (
                    <button className="btn btn-success" onClick={() => handleProcessRequest(request.id)}>
                      Отметить как обработанную
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'faq' && (
          <div className="section">
            <div className="section-header">
              <h2>Частые вопросы</h2>
              <button className="btn btn-primary" onClick={handleAddFaq}>
                + Добавить FAQ
              </button>
            </div>
            <div className="faq-list">
              {faqs.map(faq => (
                <div key={faq.id} className="faq-card">
                  <h3>{faq.question}</h3>
                  <p>{faq.answer}</p>
                  <button className="btn btn-danger" onClick={() => handleDeleteFaq(faq.id)}>
                    Удалить
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <h2>{editingCar ? 'Редактировать автомобиль' : 'Добавить автомобиль'}</h2>
            <form onSubmit={(e) => { e.preventDefault(); handleSaveCar(); }}>
              <div className="form-group">
                <label>Название:</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Описание:</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Цена (₽):</label>
                <input
                  type="number"
                  value={formData.price}
                  onChange={(e) => setFormData({...formData, price: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Год:</label>
                <input
                  type="number"
                  value={formData.year}
                  onChange={(e) => setFormData({...formData, year: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Пробег (км):</label>
                <input
                  type="number"
                  value={formData.mileage}
                  onChange={(e) => setFormData({...formData, mileage: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Состояние:</label>
                <input
                  type="text"
                  value={formData.condition}
                  onChange={(e) => setFormData({...formData, condition: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>URL фото:</label>
                <input
                  type="text"
                  value={formData.photo_url}
                  onChange={(e) => setFormData({...formData, photo_url: e.target.value})}
                />
              </div>
              <div className="form-actions">
                <button type="submit" className="btn btn-primary">
                  Сохранить
                </button>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Отмена
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
