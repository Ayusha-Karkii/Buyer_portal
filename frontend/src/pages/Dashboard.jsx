// Dashboard.jsx
import { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [property, setProperty] = useState("");

  const token = localStorage.getItem("token");

  const headers = { Authorization: `Bearer ${token}` };

  const fetchDashboard = async () => {
    try {
      const res = await axios.get("http://localhost:8000/dashboard", {
        headers,
      });
      setUser(res.data);
    } catch (err) {
      alert("Error fetching dashboard");
    }
  };

  const addFavourite = async () => {
    try {
      await axios.post(
        "http://localhost:8000/favourite",
        { property_name: property },
        { headers },
      );
      setProperty("");
      fetchDashboard();
    } catch (err) {
      alert(err.response?.data?.detail);
    }
  };

  const removeFavourite = async (name) => {
    try {
      await axios.delete("http://localhost:8000/favourite", {
        headers,
        data: { property_name: name },
      });
      fetchDashboard();
    } catch (err) {
      alert(err.response?.data?.detail);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  if (!user) return <div>Loading...</div>;

  return (
    <div style={{ maxWidth: "500px", margin: "50px auto" }}>
      <h2>
        Welcome, {user.name} ({user.role})
      </h2>

      <h3>My Favourites</h3>
      <ul>
        {user.favourites.map((f) => (
          <li key={f}>
            {f}{" "}
            <button
              onClick={() => removeFavourite(f)}
              style={{ marginLeft: "10px" }}
            >
              Remove
            </button>
          </li>
        ))}
      </ul>

      <input
        placeholder="Property name"
        value={property}
        onChange={(e) => setProperty(e.target.value)}
        style={{ padding: "5px", marginRight: "5px" }}
      />
      <button onClick={addFavourite}>Add Favourite</button>
    </div>
  );
}
