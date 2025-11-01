import { useState, useEffect } from "react";
import api from "../api/client";

export default function AutomataExplorer({ addNotification }) {
  const [automataList, setAutomataList] = useState([]);
  const [selected, setSelected] = useState("");
  const [automataInfo, setAutomataInfo] = useState(null);
  const [loading, setLoading] = useState(false);
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

    setLoading(true);
    setError(null);

    try {
      const res = await api.get(`/automata/${automataName}/info`);
      setAutomataInfo(res.data);
      
      // Notificación informativa
      if (addNotification) {
        const completeStatus = res.data.is_complete ? 'completo' : 'incompleto';
        addNotification(
          `📊 Información de ${automataName} cargada: ${res.data.state_count} estados, ${completeStatus}`,
          'info'
        );
      }
    } catch (err) {
      console.error("Error loading automata info:", err);
      setError(`Error al cargar información de ${automataName}`);
      setAutomataInfo(null);
      
      // Notificación de error
      if (addNotification) {
        addNotification(`❌ Error al cargar información de ${automataName}`, 'error');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAutomataChange = (automataName) => {
    setSelected(automataName);
    loadAutomataInfo(automataName);
  };

  const formatTransition = (transition) => {
    return `δ(${transition.from}, ${transition.symbol}) = ${transition.to}`;
  };

  return (
    <div className="card max-w-6xl w-full">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center">
          <span className="text-xl">🔍</span>
        </div>
        <h2 className="text-2xl font-bold text-white">Explorar Autómatas</h2>
      </div>

      {/* Automata Selection */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Seleccionar Autómata para Explorar
        </label>
        <select
          className="w-full md:w-96 px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all duration-200"
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
          <div className="mt-3 p-3 bg-yellow-900/20 border border-yellow-500/30 rounded-lg">
            <div className="flex items-center gap-2">
              <span className="text-yellow-400">⚠️</span>
              <p className="text-yellow-400 text-sm">
                No hay autómatas cargados. Ve a "Cargar Autómatas" primero.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
          <span className="ml-3 text-gray-300">Cargando información...</span>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="mb-6 p-4 bg-red-900/20 border border-red-500/30 rounded-lg">
          <div className="flex items-start gap-3">
            <span className="text-red-400 text-lg">⚠️</span>
            <div>
              <p className="text-red-400 font-medium">Error</p>
              <p className="text-gray-300 text-sm">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Automata Information */}
      {automataInfo && !loading && (
        <div className="space-y-6">
          {/* Basic Info */}
          <div className="bg-gray-700/50 border border-gray-600 rounded-lg p-6">
            <h3 className="text-xl font-bold text-white mb-4">📊 Información General</h3>
            
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="bg-gray-800 rounded-lg p-4 text-center">
                <p className="text-gray-400 text-sm">Estados</p>
                <p className="text-white font-bold text-2xl">{automataInfo.state_count}</p>
              </div>
              <div className="bg-gray-800 rounded-lg p-4 text-center">
                <p className="text-gray-400 text-sm">Alfabeto</p>
                <p className="text-white font-bold text-2xl">{automataInfo.alphabet_size}</p>
              </div>
              <div className="bg-gray-800 rounded-lg p-4 text-center">
                <p className="text-gray-400 text-sm">Transiciones</p>
                <p className="text-white font-bold text-2xl">{automataInfo.transition_count}</p>
              </div>
              <div className="bg-gray-800 rounded-lg p-4 text-center">
                <p className="text-gray-400 text-sm">Estados Finales</p>
                <p className="text-white font-bold text-2xl">{automataInfo.finals.length}</p>
              </div>
              <div className="bg-gray-800 rounded-lg p-4 text-center">
                <p className="text-gray-400 text-sm">Completo</p>
                <p className={`font-bold text-lg ${automataInfo.is_complete ? 'text-green-400' : 'text-yellow-400'}`}>
                  {automataInfo.is_complete ? '✅' : '⚠️'}
                </p>
              </div>
            </div>
          </div>

          {/* States and Alphabet */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* States */}
            <div className="bg-gray-700/50 border border-gray-600 rounded-lg p-6">
              <h4 className="text-lg font-bold text-white mb-4">🏷️ Estados</h4>
              <div className="space-y-2">
                <div>
                  <span className="text-blue-400 font-medium">Inicial: </span>
                  <span className="bg-blue-600 text-white px-2 py-1 rounded font-mono text-sm">
                    {automataInfo.start}
                  </span>
                </div>
                <div>
                  <span className="text-green-400 font-medium">Finales: </span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {automataInfo.finals.map((state) => (
                      <span key={state} className="bg-green-600 text-white px-2 py-1 rounded font-mono text-sm">
                        {state}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <span className="text-gray-400 font-medium">Todos: </span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {automataInfo.states.map((state) => (
                      <span key={state} className={`px-2 py-1 rounded font-mono text-sm ${
                        state === automataInfo.start ? 'bg-blue-600 text-white' :
                        automataInfo.finals.includes(state) ? 'bg-green-600 text-white' :
                        'bg-gray-600 text-white'
                      }`}>
                        {state}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Alphabet */}
            <div className="bg-gray-700/50 border border-gray-600 rounded-lg p-6">
              <h4 className="text-lg font-bold text-white mb-4">🔤 Alfabeto</h4>
              <div className="flex flex-wrap gap-2">
                {automataInfo.alphabet.map((symbol) => (
                  <span key={symbol} className="bg-purple-600 text-white px-3 py-1 rounded font-mono">
                    {symbol}
                  </span>
                ))}
              </div>
              <p className="text-gray-400 text-sm mt-3">
                Total de símbolos: {automataInfo.alphabet.length}
              </p>
            </div>
          </div>

          {/* Transition Function */}
          <div className="bg-gray-700/50 border border-gray-600 rounded-lg p-6">
            <h4 className="text-lg font-bold text-white mb-4">⚡ Función de Transición</h4>
            
            {automataInfo.transitions.length === 0 ? (
              <p className="text-gray-400">No hay transiciones definidas</p>
            ) : (
              <div className="space-y-3">
                {/* Transitions by State */}
                {automataInfo.states.map((state) => {
                  const stateTransitions = automataInfo.transitions.filter(t => t.from === state);
                  if (stateTransitions.length === 0) return null;
                  
                  return (
                    <div key={state} className="bg-gray-800 rounded-lg p-4">
                      <h5 className="text-white font-medium mb-2">
                        Desde estado: <span className="font-mono text-blue-400">{state}</span>
                      </h5>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
                        {stateTransitions.map((transition, index) => (
                          <div key={index} className="bg-gray-700 rounded p-2">
                            <span className="text-gray-300 font-mono text-sm">
                              {formatTransition(transition)}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
            
            {!automataInfo.is_complete && (
              <div className="mt-4 p-3 bg-yellow-900/20 border border-yellow-500/30 rounded">
                <p className="text-yellow-400 text-sm">
                  ⚠️ Este autómata no es completo. Algunas combinaciones (estado, símbolo) no tienen transición definida.
                </p>
              </div>
            )}
          </div>

          {/* Completeness Analysis */}
          {!automataInfo.is_complete && (
            <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-6">
              <h4 className="text-lg font-bold text-red-400 mb-4">🚨 Análisis de Completitud</h4>
              <p className="text-gray-300 mb-3">
                Este autómata no tiene función de transición total. Las siguientes combinaciones no tienen transición definida:
              </p>
              <div className="bg-gray-800 rounded p-3 max-h-40 overflow-y-auto">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-1">
                  {automataInfo.states.map((state) => 
                    automataInfo.alphabet.map((symbol) => {
                      const hasTransition = automataInfo.transitions.some(
                        t => t.from === state && t.symbol === symbol
                      );
                      if (hasTransition) return null;
                      return (
                        <span key={`${state}-${symbol}`} className="text-red-400 font-mono text-sm">
                          ({state}, {symbol})
                        </span>
                      );
                    })
                  ).flat().filter(Boolean)}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}