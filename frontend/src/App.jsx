import { Routes, Route, Link } from "react-router-dom"
import ScrollToTop from "./components/scrollToTop"
import Home from "./pages/home/home"
import Auth from "./pages/auth/auth"
import Page404 from "./pages/404"
import Login from "./pages/login"
import VerifyOTP from "./pages/VerifyOTP"
import GoogleCallback from "./pages/callback"
import FacebookCallback from "./pages/callback2"

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
        <Route path="/auth/google/callback" element={<GoogleCallback />} />
        <Route path="/auth/facebook/callback" element={<FacebookCallback />} />
      </Routes>
    </>
  )
}


