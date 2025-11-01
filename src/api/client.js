import axios from "axios";

const DEFAULT_API_PORT = "8001";

function getDefaultApiUrl() {
  // Si el frontend se sirve desde la misma máquina que el backend,
  // construimos por defecto la URL con el puerto 8001.
  const { protocol, hostname } = window.location;
  return `${protocol}//${hostname}:${DEFAULT_API_PORT}`;
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || getDefaultApiUrl(),
});

export default api;
