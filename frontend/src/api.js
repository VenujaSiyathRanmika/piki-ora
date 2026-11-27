import axios from "axios";

const API = "http://localhost:8000";

const api = axios.create({
  baseURL: API,
  withCredentials: true,
});

export async function getCsrfToken() {
  const response = await api.get("/accounts/api/csrf/");
  return response.data.csrfToken;
}

export async function loginUser(username, password, loginType) {
  const csrfToken = await getCsrfToken();

  const response = await api.post(
    "/accounts/api/login/",
    {
      username: username,
      password: password,
      loginType: loginType,
    },
    {
      headers: {
        "X-CSRFToken": csrfToken,
      },
    }
  );

  return response.data;
}

export default api;
