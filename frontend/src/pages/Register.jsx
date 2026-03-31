import axios from "axios";
import { useState } from "react";

export default function Register() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
  });

  const handleSubmit = async () => {
    try {
      await axios.post(
        "http://localhost:8000/register",
        form,
        { headers: { "Content-Type": "application/json" } }, // explicitly set JSON
      );
      alert("Registered successfully");
    } catch (err) {
      alert(err.response?.data?.detail);
    }
  };

  return (
   <div style={{ maxWidth: "400px", margin: "50px auto", textAlign: "center" }}>
  <h2>Register</h2>

  <input
    style={{ width: "100%", padding: "10px", margin: "10px 0" }}
    placeholder="Name"
    value={form.name}
    onChange={(e) => setForm({ ...form, name: e.target.value })}
  />

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
    onClick={handleSubmit}
  >
    Register
  </button>
</div>
  )}
