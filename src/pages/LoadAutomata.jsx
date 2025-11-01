import { useState } from "react";
import api from "../api/client";

export default function LoadAutomata() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleLoad = async () => {
    if (!file) return alert("Selecciona un archivo primero");

    try {
      const formData = new FormData();
      formData.append("file", file);

      // Sube el archivo al backend (opcional, si habilitas /upload)
      // const upload = await api.post("/upload", formData);

      // Para este proyecto asumimos que el archivo ya está en /app/data/automatas.txt
      const res = await api.post("/load", { path: "/app/data/automatas.txt" });
      setResponse(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || "Error al cargar el archivo");
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg w-full max-w-xl">
      <h2 className="text-xl font-semibold mb-4">Cargar Autómatas</h2>

      <input
        type="file"
        accept=".txt"
        className="mb-4"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button
        onClick={handleLoad}
        className="bg-blue-500 px-4 py-2 rounded hover:bg-blue-600"
      >
        Cargar
      </button>

      {response && (
        <div className="mt-4 bg-gray-700 p-3 rounded">
          <h3 className="font-semibold">Autómatas cargados:</h3>
          <ul className="list-disc ml-6">
            {response.loaded?.map((a) => (
              <li key={a}>{a}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
