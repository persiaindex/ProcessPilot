import { useState } from "react";

import { login } from "../services/api";

function LoginPage() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [message, setMessage] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      const data = await login(formData);
      setMessage(`Login endpoint reached for ${data.user.username}. Full auth state comes on Day 9.`);
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Login</h2>
        <p>Use your ProcessPilot account to enter the portal.</p>

        <label>
          Username
          <input
            name="username"
            type="text"
            value={formData.username}
            onChange={handleChange}
            placeholder="employee1"
          />
        </label>

        <label>
          Password
          <input
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="••••••••"
          />
        </label>

        <button type="submit">Log in</button>

        {message ? <p className="form-message">{message}</p> : null}
      </form>
    </div>
  );
}

export default LoginPage;