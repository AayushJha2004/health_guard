import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../utils/api";
import { useAuth } from "../context/AuthContext";
import Header from "../components/Header";
import Footer from "../components/Footer";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("/auth/login", { email, password });
      login(res.data.access_token);
      console.log("Logged in successfully");
      navigate("/dashboard");
    } catch (error) {
      console.error("❌ Login failed:", error);
      alert("Login failed. Please check your credentials.");
    }
  };

  return (
    <>
      <Header />
      <div className="min-h-screen flex flex-col justify-center items-center bg-gray-100">
        <h2 className="text-2xl font-bold mb-4">Login</h2>
        <form
          onSubmit={handleSubmit}
          className="bg-white p-6 rounded shadow-md w-96"
        >
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border p-2 mb-2 rounded"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border p-2 mb-2 rounded"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white w-full p-2 rounded hover:bg-blue-600 transition"
          >
            Login
          </button>
        </form>
      </div>
      <Footer />
    </>
  );
};

export default Login;
