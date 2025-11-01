import argparse
from .store import store

def main():
    parser = argparse.ArgumentParser(
        description="Programa reconocedor de palabras con AFD (CLI)"
    )
    parser.add_argument("--file", "-f", help="Ruta de archivo de entrada (formato del enunciado)")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="Listar autómatas cargados")

    check = sub.add_parser("check", help="Verificar si un AFD reconoce una palabra")
    check.add_argument("name", help="Nombre del autómata")
    check.add_argument("word", help="Palabra a verificar")

    args = parser.parse_args()

    if args.file:
        loaded = store.load_from_file(args.file)
        print(f"Cargados: {', '.join(loaded)}")

    if args.cmd == "list":
        print("\n".join(store.list()))
    elif args.cmd == "check":
        res = store.check(args.name, args.word)
        status = "ACEPTADA" if res["accepted"] else "RECHAZADA"
        print(f"[{res['automata']}] '{res['word']}' => {status}")
        print("Ruta:", " -> ".join(res["path"]))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
