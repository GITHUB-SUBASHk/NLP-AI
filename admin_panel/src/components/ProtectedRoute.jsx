import React from "react";
import { Navigate } from "react-router-dom";

// React Router v6+ version of ProtectedRoute
// Usage: <ProtectedRoute><Dashboard /></ProtectedRoute>
export default function ProtectedRoute({ children }) {
  const token = localStorage.getItem("jwt"); // Use "jwt" for consistency with your login
  return token ? children : <Navigate to="/login" replace />;
}