import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './assets/css/App.css'
import './assets/css/reset.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
