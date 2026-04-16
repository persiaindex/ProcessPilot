const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const errorMessage =
      data?.detail ||
      data?.message ||
      "Something went wrong while calling the API.";

    throw new Error(errorMessage);
  }

  return data;
}

export function login(credentials) {
  return apiRequest("/auth/login/", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
}

export function getRequests() {
  return apiRequest("/requests/");
}

export function getRequestById(requestId) {
  return apiRequest(`/requests/${requestId}/`);
}