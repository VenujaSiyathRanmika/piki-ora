
import { useState } from "react";
import api from "./api";

function Login({ onLogin }) {
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

      const response = await api.post("/api/accounts/login/", {
        username,
        password,
      });

      setPassword("");
      onLogin(response.data.username);
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Login failed. Check your details and try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="login-container">
      <h2>Patient Login</h2>
      <p>Sign in to manage your appointments.</p>

      <form onSubmit={handleSubmit}>
        <label htmlFor="username">Email / Username</label>
        <input
          id="username"
          type="text"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
          required
        />

        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
        />

        {error && <p className="error">{error}</p>}

        <button type="submit" disabled={loading}>
          {loading ? "Signing in..." : "Sign In"}
        </button>
      </form>
    </main>
  );
}

export default Login;
