import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./auth/AuthProvider";
import ProtectedRoute from "./auth/ProtectedRoute";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Plugins from "./pages/Plugins";
import { useAuth } from "./auth/useAuth"; 

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/admin/plugins" element={<ProtectedRoute><Plugins /></ProtectedRoute>} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}