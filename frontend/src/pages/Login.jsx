import axios from "axios";
import { useState } from "react";

export default function Login() {
  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const handleLogin = async () => {
    try {
      const res = await axios.post(
        "http://localhost:8000/login",
        form, // send JSON in body
        { headers: { "Content-Type": "application/json" } }, // optional but explicit
      );

      localStorage.setItem("token", res.data.access_token);
      alert("Login successful");
    } catch (err) {
      alert(err.response?.data?.detail);
    }
  };

  return (
    <div
      style={{ maxWidth: "400px", margin: "50px auto", textAlign: "center" }}
    >
      <h2>Login</h2>

      <input
        style={{ width: "100%", padding: "10px", margin: "10px 0" }}
        placeholder="Email"
        value={form.email}
        onChange={(e) => setForm({ ...form, email: e.target.value })}
      />

      <input
        type="password"
        style={{ width: "100%", padding: "10px", margin: "10px 0" }}
        placeholder="Password"
        value={form.password}
        onChange={(e) => setForm({ ...form, password: e.target.value })}
      />

      <button
        style={{ padding: "10px 20px", cursor: "pointer" }}
        onClick={handleLogin}
        disabled={!form.email || !form.password}
      >
        Login
      </button>
    </div>
  );
}
