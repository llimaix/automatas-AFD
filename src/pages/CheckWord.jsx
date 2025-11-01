import { useState, useEffect } from "react";
import api from "../api/client";

export default function CheckWord({ addNotification }) {
  const [automataList, setAutomataList] = useState([]);
  const [selected, setSelected] = useState("");
  const [word, setWord] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [maxLength, setMaxLength] = useState(10000);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [automataInfo, setAutomataInfo] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAutomataList();
  }, []);

  const loadAutomataList = async () => {
    try {
      const res = await api.get("/automata");
      setAutomataList(res.data.automata || []);
    } catch (err) {
      console.error("Error loading automata list:", err);
      setError("Error al cargar la lista de autómatas");
    }
  };

  const loadAutomataInfo = async (automataName) => {
    if (!automataName) {
      setAutomataInfo(null);
      return;
    }

    try {
      const res = await api.get(`/automata/${automataName}/info`);
      setAutomataInfo(res.data);
    } catch (err) {
      console.error("Error loading automata info:", err);
      setAutomataInfo(null);
    }
  };

  const handleAutomataChange = (automataName) => {
    setSelected(automataName);
    setResult(null);
    setError(null);
    loadAutomataInfo(automataName);
  };

  const validateInputs = () => {
    if (!selected) {
      return "Selecciona un autómata";
    }
    if (!word.trim()) {
      return "Ingresa una palabra para verificar";
    }
    if (word.length > maxLength) {
      return `La palabra es demasiado larga (máximo ${maxLength} caracteres)`;
    }
    if (maxLength < 1 || maxLength > 50000) {
      return "El límite máximo debe estar entre 1 y 50000";
    }
    return null;
  };

  const handleCheck = async () => {
    const validation = validateInputs();
    if (validation) {
      setError(validation);
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const res = await api.post("/check", { 
        automata: selected, 
        word: word.trim(),
        max_length: maxLength 
      });
      setResult(res.data);
      
      // Notificación de resultado
      if (addNotification) {
        const message = res.data.accepted 
          ? `✅ Palabra "${res.data.word}" ACEPTADA por ${selected}`
          : `❌ Palabra "${res.data.word}" RECHAZADA por ${selected}`;
        addNotification(message, res.data.accepted ? 'success' : 'warning');
      }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || "Error al verificar palabra";
      setError(errorMessage);
      
      // Notificación de error
      if (addNotification) {
        addNotification(`❌ Error en verificación: ${errorMessage}`, 'error');
      }
      
      console.error("Check error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleCheck();
    }
  };

  const getPathAnalysis = (path) => {
    if (!path || path.length === 0) return null;
    
    const totalSteps = path.length - 1;
    const hasErrors = path.some(state => state.startsWith('#'));
    const errorStep = path.findIndex(state => state.startsWith('#'));
    
    return {
      totalSteps,
      hasErrors,
      errorStep: errorStep >= 0 ? errorStep : null,
      finalState: path[path.length - 1]
    };
  };

  return (
    <div className="card max-w-4xl w-full">
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
            onChange={(e) => handleAutomataChange(e.target.value)}
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
            <div className="mt-2 p-3 bg-yellow-900/20 border border-yellow-500/30 rounded-lg">
              <div className="flex items-center gap-2">
                <span className="text-yellow-400">⚠️</span>
                <p className="text-yellow-400 text-sm">
                  No hay autómatas cargados. Ve a "Cargar Autómatas" primero.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Automata Info */}
        {automataInfo && (
          <div className="bg-gray-700/50 border border-gray-600 rounded-lg p-4">
            <h3 className="text-white font-medium mb-3">📊 Información del Autómata: {automataInfo.name}</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div className="bg-gray-800 rounded p-3">
                <p className="text-gray-400">Estados</p>
                <p className="text-white font-bold">{automataInfo.state_count}</p>
              </div>
              <div className="bg-gray-800 rounded p-3">
                <p className="text-gray-400">Alfabeto</p>
                <p className="text-white font-bold">{automataInfo.alphabet_size}</p>
              </div>
              <div className="bg-gray-800 rounded p-3">
                <p className="text-gray-400">Transiciones</p>
                <p className="text-white font-bold">{automataInfo.transition_count}</p>
              </div>
              <div className="bg-gray-800 rounded p-3">
                <p className="text-gray-400">Completo</p>
                <p className={`font-bold ${automataInfo.is_complete ? 'text-green-400' : 'text-yellow-400'}`}>
                  {automataInfo.is_complete ? '✅ Sí' : '⚠️ No'}
                </p>
              </div>
            </div>
            
            <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div className="bg-gray-800 rounded p-3">
                <p className="text-gray-400 mb-1">Alfabeto:</p>
                <p className="text-white font-mono text-xs">
                  {automataInfo.alphabet.join(', ')}
                </p>
              </div>
              <div className="bg-gray-800 rounded p-3">
                <p className="text-gray-400 mb-1">Estados finales:</p>
                <p className="text-white font-mono text-xs">
                  {automataInfo.finals.join(', ') || 'Ninguno'}
                </p>
              </div>
            </div>
          </div>
        )}

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
            maxLength={maxLength}
          />
          <div className="flex justify-between items-center mt-1">
            <p className="text-xs text-gray-400">
              Presiona Enter para verificar rápidamente
            </p>
            <p className="text-xs text-gray-400">
              {word.length}/{maxLength} caracteres
            </p>
          </div>
        </div>

        {/* Advanced Options */}
        <div>
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center gap-2 text-blue-400 hover:text-blue-300 text-sm"
          >
            <span>{showAdvanced ? '▼' : '▶'}</span>
            Opciones avanzadas
          </button>
          
          {showAdvanced && (
            <div className="mt-3 p-4 bg-gray-700/30 border border-gray-600 rounded-lg">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Límite máximo de longitud
                </label>
                <input
                  type="number"
                  min="1"
                  max="50000"
                  value={maxLength}
                  onChange={(e) => setMaxLength(parseInt(e.target.value) || 10000)}
                  className="w-full md:w-48 px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white text-sm"
                />
                <p className="mt-1 text-xs text-gray-400">
                  Máximo número de caracteres a procesar (1-50000)
                </p>
              </div>
            </div>
          )}
        </div>

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

            {/* Result Stats */}
            {result.word_length !== undefined && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
                <div className="bg-gray-800/50 rounded p-2">
                  <p className="text-xs text-gray-400">Longitud</p>
                  <p className="text-white font-bold">{result.word_length}</p>
                </div>
                <div className="bg-gray-800/50 rounded p-2">
                  <p className="text-xs text-gray-400">Pasos</p>
                  <p className="text-white font-bold">{result.path_length - 1}</p>
                </div>
                <div className="bg-gray-800/50 rounded p-2">
                  <p className="text-xs text-gray-400">Estados visitados</p>
                  <p className="text-white font-bold">{result.path_length}</p>
                </div>
                <div className="bg-gray-800/50 rounded p-2">
                  <p className="text-xs text-gray-400">Límite usado</p>
                  <p className="text-white font-bold">{result.max_length_used}</p>
                </div>
              </div>
            )}

            {/* Path Analysis */}
            {(() => {
              const analysis = getPathAnalysis(result.path);
              return analysis && analysis.hasErrors && (
                <div className="mb-4 p-3 bg-yellow-900/20 border border-yellow-500/30 rounded">
                  <p className="text-yellow-400 text-sm">
                    ⚠️ Error en paso {analysis.errorStep}: {analysis.finalState}
                  </p>
                </div>
              );
            })()}

            {/* Path */}
            <div className="bg-gray-800/50 rounded-lg p-4">
              <h4 className="font-semibold text-white mb-3">🔄 Trayectoria de estados:</h4>
              <div className="flex flex-wrap gap-2">
                {result.path.map((state, index) => (
                  <span key={index} className="flex items-center gap-1">
                    <span className={`px-3 py-1 rounded-full text-sm font-mono ${
                      state.startsWith('#') 
                        ? 'bg-red-600 text-white' 
                        : index === 0 
                        ? 'bg-blue-600 text-white' 
                        : index === result.path.length - 1 && result.accepted
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-600 text-white'
                    }`}>
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
