import { useState } from "react";
import LoadAutomata from "./pages/LoadAutomata";
import CheckWord from "./pages/CheckWord";
import AutomataExplorer from "./pages/AutomataExplorer";
import { useNotifications } from "./hooks/useNotifications";
import { NotificationContainer } from "./components/NotificationSystem";

export default function App() {
  const [page, setPage] = useState("load");
  const { notifications, addNotification, removeNotification } = useNotifications();

  // Proporcionar las notificaciones a través del contexto global podría ser mejor,
  // pero para simplicidad las pasamos como props cuando sea necesario

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white">
      {/* Notification System */}
      <NotificationContainer 
        notifications={notifications}
        onRemove={removeNotification}
      />

      {/* Header */}
      <div className="bg-gray-800/50 backdrop-blur-md border-b border-gray-700">
        <div className="container mx-auto px-6 py-4">
          <h1 className="text-3xl font-bold text-center bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Reconocedor de Palabras (AFD)
          </h1>
          <p className="text-center text-gray-400 text-sm mt-2">
            Sistema con validaciones avanzadas y análisis detallado
          </p>
        </div>
      </div>

      {/* Navigation */}
      <div className="container mx-auto px-6 py-8">
        <div className="flex justify-center gap-4 mb-8 flex-wrap">
          <button
            onClick={() => setPage("load")}
            className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
              page === "load" 
                ? "bg-blue-600 text-white shadow-lg shadow-blue-500/25 scale-105" 
                : "bg-gray-700 text-gray-300 hover:bg-gray-600 hover:text-white"
            }`}
          >
            📁 Cargar Autómatas
          </button>
          <button
            onClick={() => setPage("check")}
            className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
              page === "check" 
                ? "bg-green-600 text-white shadow-lg shadow-green-500/25 scale-105" 
                : "bg-gray-700 text-gray-300 hover:bg-gray-600 hover:text-white"
            }`}
          >
            ✅ Probar Palabra
          </button>
          <button
            onClick={() => setPage("explore")}
            className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
              page === "explore" 
                ? "bg-purple-600 text-white shadow-lg shadow-purple-500/25 scale-105" 
                : "bg-gray-700 text-gray-300 hover:bg-gray-600 hover:text-white"
            }`}
          >
            🔍 Explorar Autómatas
          </button>
        </div>

        {/* Quick Demo Button 
        <div className="flex justify-center mb-6">
          <button
            onClick={() => {
              addNotification("¡Bienvenido al sistema AFD mejorado! Carga un archivo para comenzar.", "info");
            }}
            className="text-sm px-4 py-2 bg-gray-700/50 hover:bg-gray-600/50 rounded-lg text-gray-300 hover:text-white transition-all duration-200"
          >
            💡 Ver notificación de ejemplo
          </button>
        </div>
        */}

        {/* Content */}
        <div className="flex justify-center">
          {page === "load" && <LoadAutomata addNotification={addNotification} />}
          {page === "check" && <CheckWord addNotification={addNotification} />}
          {page === "explore" && <AutomataExplorer addNotification={addNotification} />}
        </div>
      </div>

      {/* Footer with Features */}
      {/*      
      <div className="bg-gray-800/30 border-t border-gray-700 mt-16">
        <div className="container mx-auto px-6 py-8">
          <div className="text-center">
            <h3 className="text-lg font-semibold text-white mb-4">🚀 Características Mejoradas</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
              <div className="bg-gray-700/30 rounded-lg p-3">
                <span className="block text-blue-400 font-medium">🔒 Validación Robusta</span>
                <span className="text-gray-400">Límites de seguridad y sanitización</span>
              </div>
              <div className="bg-gray-700/30 rounded-lg p-3">
                <span className="block text-green-400 font-medium">📤 Upload Mejorado</span>
                <span className="text-gray-400">Validación de archivos y feedback detallado</span>
              </div>
              <div className="bg-gray-700/30 rounded-lg p-3">
                <span className="block text-purple-400 font-medium">🔍 Análisis Detallado</span>
                <span className="text-gray-400">Exploración completa de autómatas</span>
              </div>
              <div className="bg-gray-700/30 rounded-lg p-3">
                <span className="block text-yellow-400 font-medium">⚡ Simulación Avanzada</span>
                <span className="text-gray-400">Límites configurables y mejor debugging</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* */}
    </div>
  );
}
