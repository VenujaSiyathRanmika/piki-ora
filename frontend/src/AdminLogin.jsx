import { useState } from "react";
import api from "./api";

function AdminLogin({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      await api.get("/api/accounts/csrf/");
      const response = await api.post("/api/accounts/admin-login/", {
        username,
        password,
      });
      setPassword("");
      onLogin(response.data.username);
    } catch (err) {
      setError(
        err.response?.data?.error ||
        "Administrator login failed. Check your credentials."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="login-container">
      <h2>Administrator Login</h2>
      <p>Sign in to manage Piki Ora Medical Centre.</p>

      <form onSubmit={handleSubmit}>
        <label htmlFor="admin-username">Username</label>
        <input
          id="admin-username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          autoComplete="username"
          required
        />

        <label htmlFor="admin-password">Password</label>
        <input
          id="admin-password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
          required
        />

        {error && <p className="error">{error}</p>}

        <button type="submit" disabled={loading}>
          {loading ? "Signing in..." : "Sign In as Administrator"}
        </button>
      </form>
    </main>
  );
}

export default AdminLogin;
