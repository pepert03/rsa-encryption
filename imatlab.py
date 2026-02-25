import os
import sys

import modular
 
def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def run_commands(input_stream, output_stream) -> None:
    """Run commands from a text stream and write results to output_stream."""
    for line in input_stream:
        try:
            command = line.split("(")
            operation = command[0]
            if operation == "resolverSistema":
                raw_args = command[1].split(")")[0]
                result = solve_system(raw_args)
            else:
                raw = command[1].split(")")[0].split(",")
                args = [int(i) for i in raw]
                result = dispatch(operation, args)
            output_stream.write(str(result) + "\n")
        except Exception:
            output_stream.write("ERROR\n")


def solve_system(args: str):
    a_list = []
    b_list = []
    p_list = []
    tokens = args.replace("[", "").replace("]", "").replace(";", ",").split(",")
    for i in range(len(tokens) // 3):
        a_list.append(int(tokens[i * 3]))
        b_list.append(int(tokens[i * 3 + 1]))
        p_list.append(int(tokens[i * 3 + 2]))
    return modular.solve_congruence_system(a_list, b_list, p_list)


def dispatch(operation: str, args: list[int]):
    """Dispatch a parsed operation name to a known function."""
    if operation in COMMANDS:
        return COMMANDS[operation](*args)
    return "Error: Invalid command"
 
 
def main() -> None:
    """Entry point for interactive mode or batch mode."""
    if len(sys.argv) == 1:
        print("Interactive CLI")
        print("    - exit     - help     - clear")

        running = True
        while running:
            raw_command = input("imatlab> ")
            if raw_command == "exit":
                running = False
            elif raw_command == "help":
                print("Available commands:")
                for name in COMMANDS:
                    print(" - ", name, end="")
                    print("()")
            elif raw_command == "clear":
                clear_screen()
            elif raw_command == "":
                continue
            else:
                try:
                    parts = raw_command.split("(")
                    operation = parts[0]
                    if operation == "resolverSistema":
                        raw_args = parts[1].split(")")[0]
                        result = solve_system(raw_args)
                    else:
                        raw = parts[1].split(")")[0].split(",")
                        args = [int(i) for i in raw]
                        result = dispatch(operation, args)
                    print(result)
                except Exception:
                    print("Error: Invalid command")
    elif len(sys.argv) == 2:
        with open(sys.argv[1], "r", encoding="utf-8") as fin:
            with open(sys.argv[1].split(".")[0] + "Output.txt", "w", encoding="utf-8") as fout:
                run_commands(fin, fout)
    elif len(sys.argv) == 3:
        with open(sys.argv[1], "r", encoding="utf-8") as fin:
            with open(sys.argv[2], "w", encoding="utf-8") as fout:
                run_commands(fin, fout)
    else:
        print("Error: Invalid number of arguments")
 
 
COMMANDS = {
    "run_commands": run_commands,
    "primo": modular.is_prime,
    "primos": modular.list_primes,
    "factorizar": modular.factorize,
    "mcd": modular.gcd,
    "coprimos": modular.are_coprime,
    "pow": modular.mod_pow,
    "inv": modular.mod_inverse,
    "euler": modular.euler_totient,
    "legendre": modular.legendre_symbol,
    "resolverSistema": solve_system,
    "raiz": modular.mod_sqrt,
    "ecCuadratica": modular.quadratic_equation_mod_p,
}
 

if __name__ == "__main__":
    clear_screen()
    main()


# Backwards-compatible aliases used by existing benchmark scripts.
clear = clear_screen
resolverSistema = solve_system
llamar_funciones = dispatch
FUNCIONES = COMMANDS
 
