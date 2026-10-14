import { Routes, Route, Link } from "react-router-dom"
import ScrollToTop from "./components/scrollToTop"
import Home from "./pages/home/home"
import Auth from "./pages/auth/auth"
import Page404 from "./pages/404"
import Login from "./pages/login"
import VerifyOTP from "./pages/VerifyOTP"
import GoogleCallback from "./pages/callback"
import FacebookCallback from "./pages/callback2"
import CartTest from "./pages/x"

import Dashboard from "./pages/dashboard/dashboard"
import { DASHBOARD_ENDPOINT } from "./config"
import RequireAuth from "./context/auth/RequireAuth"

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
        <Route path="/cart" element={<CartTest />} />

        <Route path={DASHBOARD_ENDPOINT} element={<RequireAuth><Dashboard /></RequireAuth>}>
           <Route index element={<div>Dashboard</div>} />
           <Route path="accounts" element={<div>accounts</div>} />
           <Route path="products" element={<div>products</div>} />
           <Route path="orders" element={<div>orders</div>} />
        </Route>
      </Routes>
    </>
  )
}


