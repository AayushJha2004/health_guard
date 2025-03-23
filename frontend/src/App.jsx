import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Patients from "./pages/Patients";
import Alerts from "./pages/Alerts";
import PrivateRoute from "./routes/PrivateRoute";
import PatientDetail from "./pages/PatientDetail";
import AddPatient from "./pages/AddPatient";
import PatientMetrics from "./pages/PatientMetrics";
import PatientECG from "./pages/PatientECG";
import { AuthProvider } from "./context/AuthContext";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={<PrivateRoute element={<Dashboard />} />}
          />
          <Route
            path="/patients"
            element={<PrivateRoute element={<Patients />} />}
          />
          <Route
            path="/alerts"
            element={<PrivateRoute element={<Alerts />} />}
          />
          
          {/* Redirect to dashboard after login */}
          <Route path="/" element={<PrivateRoute element={<Dashboard />} />} />
          <Route path="/patients/:id" element={<PrivateRoute element={<PatientDetail />} />} />
          <Route path="/patients/add" element={<PrivateRoute element={<AddPatient />} />} />
          <Route path="/patients/:id/metrics" element={<PrivateRoute element={<PatientMetrics />} />} />
          <Route path="/patients/:id/ecg" element={<PrivateRoute element={<PatientECG />} />} />  
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
