import { useState } from "react";
import api from "../api/client";

export default function LoadAutomata() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLoad = async () => {
    if (!file) return alert("Selecciona un archivo primero");

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);

      // Subir y cargar el archivo seleccionado
      const res = await api.post("/upload", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResponse(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || "Error al cargar el archivo");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card max-w-2xl w-full">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
          <span className="text-xl">📁</span>
        </div>
        <h2 className="text-2xl font-bold text-white">Cargar Autómatas</h2>
      </div>

      <div className="space-y-6">
        {/* File Input */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Seleccionar archivo de autómatas (.txt)
          </label>
          <div className="relative">
            <input
              type="file"
              accept=".txt"
              className="w-full px-4 py-3 bg-gray-700 border-2 border-dashed border-gray-600 rounded-lg text-white file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 file:cursor-pointer cursor-pointer transition-all duration-200 hover:border-blue-500"
              onChange={(e) => setFile(e.target.files[0])}
            />
          </div>
          {file && (
            <p className="mt-2 text-sm text-green-400">
              ✓ Archivo seleccionado: {file.name}
            </p>
          )}
        </div>

        {/* Load Button */}
        <button
          onClick={handleLoad}
          disabled={!file || loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-medium px-6 py-3 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl disabled:shadow-none flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Cargando...
            </>
          ) : (
            <>
              <span>🚀</span>
              Cargar Autómatas
            </>
          )}
        </button>
      </div>

      {/* Results */}
      {response && (
        <div className="mt-8 bg-gray-700/50 border border-gray-600 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-green-400 text-xl">✅</span>
            <h3 className="text-lg font-semibold text-white">
              {response.filename ? `Archivo "${response.filename}" cargado exitosamente` : 'Autómatas cargados exitosamente'}
            </h3>
          </div>
          {response.message && (
            <p className="text-gray-300 mb-4">{response.message}</p>
          )}
          <div className="bg-gray-800 rounded-lg p-4">
            <h4 className="text-white font-medium mb-2">Autómatas encontrados:</h4>
            <ul className="space-y-2">
              {response.loaded?.map((a, index) => (
                <li key={a} className="flex items-center gap-2 text-gray-300">
                  <span className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-xs font-bold text-white">
                    {index + 1}
                  </span>
                  <span className="font-mono">{a}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
