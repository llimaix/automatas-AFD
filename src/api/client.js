import axios from "axios";

const DEFAULT_API_PORT = "8001";

function getDefaultApiUrl() {
  // En desarrollo, usar el proxy de Vite
  if (import.meta.env.DEV) {
    return "/api";
  }
  
  // En producción, construir la URL con el puerto 8001
  const { protocol, hostname } = window.location;
  return `${protocol}//${hostname}:${DEFAULT_API_PORT}`;
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || getDefaultApiUrl(),
});

export default api;
