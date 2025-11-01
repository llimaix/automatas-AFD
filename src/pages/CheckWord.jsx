import { useState, useEffect } from "react";
import api from "../api/client";

export default function CheckWord() {
  const [automataList, setAutomataList] = useState([]);
  const [selected, setSelected] = useState("");
  const [word, setWord] = useState("");
  const [result, setResult] = useState(null);

  useEffect(() => {
    api.get("/automata").then((res) => setAutomataList(res.data.automata));
  }, []);

  const handleCheck = async () => {
    if (!selected || !word) return alert("Selecciona un autómata y una palabra");

    try {
      const res = await api.post("/check", { automata: selected, word });
      setResult(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || "Error al verificar palabra");
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg w-full max-w-xl">
      <h2 className="text-xl font-semibold mb-4">Probar Palabra</h2>

      <select
        className="w-full mb-4 text-black p-2 rounded"
        onChange={(e) => setSelected(e.target.value)}
        value={selected}
      >
        <option value="">-- Selecciona un Autómata --</option>
        {automataList.map((a) => (
          <option key={a}>{a}</option>
        ))}
      </select>

      <input
        type="text"
        placeholder="Palabra"
        className="w-full mb-4 text-black p-2 rounded"
        value={word}
        onChange={(e) => setWord(e.target.value)}
      />

      <button
        onClick={handleCheck}
        className="bg-green-500 px-4 py-2 rounded hover:bg-green-600"
      >
        Verificar
      </button>

      {result && (
        <div className="mt-4 bg-gray-700 p-3 rounded">
          <h3 className="font-semibold">Resultado:</h3>
          <p>
            Palabra: <b>{result.word}</b> —{" "}
            {result.accepted ? (
              <span className="text-green-400">ACEPTADA ✅</span>
            ) : (
              <span className="text-red-400">RECHAZADA ❌</span>
            )}
          </p>
          <p className="mt-2">Ruta: {result.path.join(" → ")}</p>
        </div>
      )}
    </div>
  );
}
