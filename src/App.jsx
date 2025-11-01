import { useState } from "react";
import LoadAutomata from "./pages/LoadAutomata";
import CheckWord from "./pages/CheckWord";

export default function App() {
  const [page, setPage] = useState("load");

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold mb-8">Reconocedor de Palabras (AFD)</h1>

      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setPage("load")}
          className={`px-4 py-2 rounded ${page === "load" ? "bg-blue-600" : "bg-gray-700"}`}
        >
          Cargar Autómatas
        </button>
        <button
          onClick={() => setPage("check")}
          className={`px-4 py-2 rounded ${page === "check" ? "bg-blue-600" : "bg-gray-700"}`}
        >
          Probar Palabra
        </button>
      </div>

      {page === "load" ? <LoadAutomata /> : <CheckWord />}
    </div>
  );
}
