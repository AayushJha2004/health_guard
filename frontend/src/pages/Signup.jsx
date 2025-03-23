import { useState } from "react";
import axios from "../utils/api";

const Signup = () => {
  const [form, setForm] = useState({ email: "", full_name: "", password: "" });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("/auth/signup", form);
      alert("Signup successful. Please login.");
    } catch (error) {
      console.error("Signup failed:", error);
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md w-96">
        <input
          type="email"
          placeholder="Enter your Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          className="w-full border p-2 mb-4 rounded"
        />
        <input
          type="text"
          placeholder="Enter your Full Name"
          value={form.full_name}
          onChange={(e) => setForm({ ...form, full_name: e.target.value })}
          className="w-full border p-2 mb-4 rounded"
        />
        <input
          type="password"
          placeholder="Enter your Password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          className="w-full border p-2 mb-4 rounded"
        />
        <button
          type="submit"
          className="bg-green-500 text-white w-full p-2 rounded hover:bg-green-600 transition"
        >
          Signup
        </button>
      </form>
    </div>
  );
};

export default Signup;
