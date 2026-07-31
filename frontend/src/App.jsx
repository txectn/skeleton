import { Routes, Route, Link } from "react-router-dom"
import ScrollToTop from "./components/scrollToTop"
import Home from "./pages/home/home"
import Auth from "./pages/auth/auth"
import Page404 from "./pages/404"
import Login from "./pages/login"
import VerifyOTP from "./pages/VerifyOTP"

export default function App() {
  return (
    <>
      <ScrollToTop />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/auth" element={<Auth />} />
        <Route path="*" element={<Page404 />} />
        <Route path="/login" element={<Login />} />
        <Route path="/verify-otp" element={<VerifyOTP />} />
      </Routes>
    </>
  )
}


