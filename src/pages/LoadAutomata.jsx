import { useState } from "react";
import api from "../api/client";

export default function LoadAutomata({ addNotification }) {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploadMethod, setUploadMethod] = useState("upload"); // "upload" or "path"
  const [pathInput, setPathInput] = useState("/app/data/automatas.txt");
  const [error, setError] = useState(null);

  const validateFile = (selectedFile) => {
    if (!selectedFile) return "No se ha seleccionado ningún archivo";
    
    if (!selectedFile.name.endsWith('.txt')) {
      return "Solo se permiten archivos .txt";
    }
    
    if (selectedFile.size > 5 * 1024 * 1024) { // 5MB
      return "El archivo es demasiado grande (máximo 5MB)";
    }
    
    if (selectedFile.size === 0) {
      return "El archivo está vacío";
    }
    
    return null;
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    const validation = validateFile(selectedFile);
    
    if (validation) {
      setError(validation);
      setFile(null);
      return;
    }
    
    setFile(selectedFile);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Selecciona un archivo primero");
      return;
    }

    const validation = validateFile(file);
    if (validation) {
      setError(validation);
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await api.post("/upload", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000, // 30 segundos
      });
      
      setResponse(res.data);
      
      // Notificación de éxito
      if (addNotification) {
        addNotification(
          `✅ Archivo subido exitosamente. ${res.data.count || 0} autómatas cargados.`,
          'success'
        );
      }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || "Error al subir el archivo";
      setError(errorMessage);
      
      // Notificación de error
      if (addNotification) {
        addNotification(`❌ Error al subir archivo: ${errorMessage}`, 'error');
      }
      
      console.error("Upload error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleLoadFromPath = async () => {
    if (!pathInput.trim()) {
      setError("Ingresa una ruta válida");
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const res = await api.post("/load", { path: pathInput.trim() });
      setResponse(res.data);
      
      // Notificación de éxito
      if (addNotification) {
        addNotification(
          `✅ Carga desde ruta exitosa. ${res.data.count || 0} autómatas cargados.`,
          'success'
        );
      }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || "Error al cargar desde la ruta";
      setError(errorMessage);
      
      // Notificación de error
      if (addNotification) {
        addNotification(`❌ Error al cargar desde ruta: ${errorMessage}`, 'error');
      }
      
      console.error("Load error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = () => {
    if (uploadMethod === "upload") {
      handleUpload();
    } else {
      handleLoadFromPath();
    }
  };

  const getFileInfo = () => {
    if (!file) return null;
    
    const sizeKB = (file.size / 1024).toFixed(1);
    const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
    
    return {
      name: file.name,
      size: file.size < 1024 * 1024 ? `${sizeKB} KB` : `${sizeMB} MB`,
      type: file.type || 'text/plain',
      lastModified: new Date(file.lastModified).toLocaleString()
    };
  };

  return (
    <div className="card max-w-4xl w-full">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
          <span className="text-xl">📁</span>
        </div>
        <h2 className="text-2xl font-bold text-white">Cargar Autómatas</h2>
      </div>

      {/* Method Selection */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-300 mb-3">
          Método de carga
        </label>
        <div className="flex gap-4">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="uploadMethod"
              value="upload"
              checked={uploadMethod === "upload"}
              onChange={(e) => setUploadMethod(e.target.value)}
              className="text-blue-600"
            />
            <span className="text-white">📤 Subir archivo</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="uploadMethod"
              value="path"
              checked={uploadMethod === "path"}
              onChange={(e) => setUploadMethod(e.target.value)}
              className="text-blue-600"
            />
            <span className="text-white">📂 Cargar desde ruta</span>
          </label>
        </div>
      </div>

      <div className="space-y-6">
        {uploadMethod === "upload" ? (
          /* File Upload Section */
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Seleccionar archivo de autómatas (.txt, máx 5MB)
            </label>
            <div className="relative">
              <input
                type="file"
                accept=".txt"
                className="w-full px-4 py-3 bg-gray-700 border-2 border-dashed border-gray-600 rounded-lg text-white file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 file:cursor-pointer cursor-pointer transition-all duration-200 hover:border-blue-500"
                onChange={handleFileSelect}
              />
            </div>
            
            {/* File Info */}
            {file && !error && (
              <div className="mt-3 p-3 bg-green-900/20 border border-green-500/30 rounded-lg">
                <div className="flex items-start gap-3">
                  <span className="text-green-400 text-lg">✓</span>
                  <div className="flex-1">
                    <p className="text-green-400 font-medium">Archivo seleccionado:</p>
                    {(() => {
                      const fileInfo = getFileInfo();
                      return (
                        <div className="text-sm text-gray-300 mt-1 space-y-1">
                          <p><span className="text-gray-400">Nombre:</span> {fileInfo.name}</p>
                          <p><span className="text-gray-400">Tamaño:</span> {fileInfo.size}</p>
                          <p><span className="text-gray-400">Modificado:</span> {fileInfo.lastModified}</p>
                        </div>
                      );
                    })()}
                  </div>
                </div>
              </div>
            )}
          </div>
        ) : (
          /* Path Input Section */
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Ruta del archivo en el servidor
            </label>
            <input
              type="text"
              value={pathInput}
              onChange={(e) => setPathInput(e.target.value)}
              placeholder="/app/data/automatas.txt"
              className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all duration-200"
            />
            <p className="mt-1 text-xs text-gray-400">
              Ruta absoluta del archivo en el contenedor/servidor
            </p>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="p-4 bg-red-900/20 border border-red-500/30 rounded-lg">
            <div className="flex items-start gap-3">
              <span className="text-red-400 text-lg">⚠️</span>
              <div>
                <p className="text-red-400 font-medium">Error</p>
                <p className="text-gray-300 text-sm">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Action Button */}
        <button
          onClick={handleAction}
          disabled={loading || (uploadMethod === "upload" && (!file || error)) || (uploadMethod === "path" && !pathInput.trim())}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-medium px-6 py-3 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl disabled:shadow-none flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              {uploadMethod === "upload" ? "Subiendo..." : "Cargando..."}
            </>
          ) : (
            <>
              <span>🚀</span>
              {uploadMethod === "upload" ? "Subir y Cargar Autómatas" : "Cargar Autómatas"}
            </>
          )}
        </button>
      </div>

      {/* Results */}
      {response && (
        <div className="mt-8 bg-gray-700/50 border border-gray-600 rounded-lg p-6">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-green-400 text-xl">✅</span>
            <h3 className="text-lg font-semibold text-white">Operación exitosa</h3>
          </div>
          
          {/* Response Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div className="bg-gray-800 rounded-lg p-3">
              <p className="text-sm text-gray-400">Mensaje</p>
              <p className="text-white font-medium">{response.message || "Carga completada"}</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <p className="text-sm text-gray-400">Autómatas cargados</p>
              <p className="text-white font-bold text-lg">{response.count || response.loaded?.length || 0}</p>
            </div>
          </div>

          {/* Loaded Automata List */}
          {response.loaded && response.loaded.length > 0 && (
            <div className="bg-gray-800 rounded-lg p-4">
              <h4 className="text-white font-medium mb-3">Autómatas disponibles:</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                {response.loaded.map((a, index) => (
                  <div key={a} className="flex items-center gap-2 text-gray-300 bg-gray-700 rounded px-3 py-2">
                    <span className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-xs font-bold text-white">
                      {index + 1}
                    </span>
                    <span className="font-mono text-sm">{a}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* Additional Info */}
          {response.filename && (
            <div className="mt-3 text-sm text-gray-400">
              <span>Archivo procesado: </span>
              <span className="font-mono text-gray-300">{response.filename}</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
