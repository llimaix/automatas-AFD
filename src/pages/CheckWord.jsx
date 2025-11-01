import { useState, useEffect } from "react";
import api from "../api/client";

export default function CheckWord() {
  const [automataList, setAutomataList] = useState([]);
  const [selected, setSelected] = useState("");
  const [word, setWord] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.get("/automata").then((res) => setAutomataList(res.data.automata));
  }, []);

  const handleCheck = async () => {
    if (!selected || !word.trim()) {
      alert("Selecciona un autómata y escribe una palabra");
      return;
    }

    setLoading(true);
    try {
      const res = await api.post("/check", { automata: selected, word: word.trim() });
      setResult(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || "Error al verificar palabra");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleCheck();
    }
  };

  return (
    <div className="card max-w-2xl w-full">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center">
          <span className="text-xl">✅</span>
        </div>
        <h2 className="text-2xl font-bold text-white">Probar Palabra</h2>
      </div>

      <div className="space-y-6">
        {/* Automata Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Seleccionar Autómata
          </label>
          <select
            className="select-field"
            onChange={(e) => setSelected(e.target.value)}
            value={selected}
          >
            <option value="">-- Selecciona un Autómata --</option>
            {automataList.map((a) => (
              <option key={a} value={a}>
                {a}
              </option>
            ))}
          </select>
          {automataList.length === 0 && (
            <p className="mt-2 text-sm text-yellow-400">
              ⚠️ No hay autómatas cargados. Ve a "Cargar Autómatas" primero.
            </p>
          )}
        </div>

        {/* Word Input */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Palabra a verificar
          </label>
          <input
            type="text"
            placeholder="Escribe la palabra aquí..."
            className="input-field"
            value={word}
            onChange={(e) => setWord(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <p className="mt-1 text-xs text-gray-400">
            Presiona Enter para verificar rápidamente
          </p>
        </div>

        {/* Check Button */}
        <button
          onClick={handleCheck}
          disabled={!selected || !word.trim() || loading}
          className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-medium px-6 py-3 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl disabled:shadow-none flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Verificando...
            </>
          ) : (
            <>
              <span>🔍</span>
              Verificar Palabra
            </>
          )}
        </button>
      </div>

      {/* Results */}
      {result && (
        <div className="mt-8">
          <div className={`rounded-lg p-6 border-2 ${
            result.accepted 
              ? 'bg-green-900/30 border-green-500 shadow-lg shadow-green-500/20' 
              : 'bg-red-900/30 border-red-500 shadow-lg shadow-red-500/20'
          }`}>
            <div className="flex items-center gap-3 mb-4">
              <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                result.accepted ? 'bg-green-500' : 'bg-red-500'
              }`}>
                <span className="text-2xl">
                  {result.accepted ? '✅' : '❌'}
                </span>
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">
                  {result.accepted ? 'Palabra Aceptada' : 'Palabra Rechazada'}
                </h3>
                <p className="text-gray-300">
                  Palabra: <span className="font-mono font-bold">"{result.word}"</span>
                </p>
              </div>
            </div>

            {/* Path */}
            <div className="bg-gray-800/50 rounded-lg p-4">
              <h4 className="font-semibold text-white mb-2">Ruta de estados:</h4>
              <div className="flex flex-wrap gap-2">
                {result.path.map((state, index) => (
                  <span key={index} className="flex items-center gap-1">
                    <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-mono">
                      {state}
                    </span>
                    {index < result.path.length - 1 && (
                      <span className="text-gray-400">→</span>
                    )}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
