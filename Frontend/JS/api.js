const API_BASE_URL = "http://127.0.0.1:5000/api";

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(payload.error || payload.message || "Request failed");
  }

  return payload;
}

const api = {
  login: (email, password) => apiRequest("/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  }),
  signup: (username, email, password) => apiRequest("/register", {
    method: "POST",
    body: JSON.stringify({ username, email, password }),
  }),
  currentUser: () => apiRequest("/me"),
  logout: () => apiRequest("/logout", { method: "POST" }),
  bills: () => apiRequest("/bills"),
  addBill: (bill) => apiRequest("/bills", {
    method: "POST",
    body: JSON.stringify(bill),
  }),
  updateBill: (id, bill) => apiRequest(`/bills/${id}`, {
    method: "PUT",
    body: JSON.stringify(bill),
  }),
  deleteBill: (id) => apiRequest(`/bills/${id}`, { method: "DELETE" }),
  payBill: (id) => apiRequest(`/bills/${id}/pay`, { method: "PATCH" }),
  schedule: () => apiRequest("/schedule"),
  reminders: () => apiRequest("/reminders"),
  sendReminders: () => apiRequest("/reminders/send", { method: "POST" }),
};
