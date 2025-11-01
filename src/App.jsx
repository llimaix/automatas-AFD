import { useState } from "react";
import LoadAutomata from "./pages/LoadAutomata";
import CheckWord from "./pages/CheckWord";

export default function App() {
  const [page, setPage] = useState("load");

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white">
      {/* Header */}
      <div className="bg-gray-800/50 backdrop-blur-md border-b border-gray-700">
        <div className="container mx-auto px-6 py-4">
          <h1 className="text-3xl font-bold text-center bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            🤖 Reconocedor de Palabras (AFD)
          </h1>
        </div>
      </div>

      {/* Navigation */}
      <div className="container mx-auto px-6 py-8">
        <div className="flex justify-center gap-4 mb-8">
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
                ? "bg-blue-600 text-white shadow-lg shadow-blue-500/25 scale-105" 
                : "bg-gray-700 text-gray-300 hover:bg-gray-600 hover:text-white"
            }`}
          >
            ✅ Probar Palabra
          </button>
        </div>

        {/* Content */}
        <div className="flex justify-center">
          {page === "load" ? <LoadAutomata /> : <CheckWord />}
        </div>
      </div>
    </div>
  );
}
