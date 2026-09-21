# Denny Nguyen
# COP 4045
# Assignment 2
# Problem 1

from typing import Tuple, List
import os

# PART A
def line_number(file_in: str, file_out: str) -> None:
    """
    Reads a Python file and writes its contents to another file with
    each line prefixed by its line number.

    Parameters:
        file_in (str): Name of the input file to read.
        file_out (str): Name of the output file to write.

    Raises:
        Exception: Re-raises any file-related errors after printing
                   a user-friendly message.
    """
    try:
        with open(file_in, "r") as fin, open(file_out, "w") as fout:
            for idx, line in enumerate(fin, start=1):
                fout.write(f"{idx}. {line}")
    except Exception as e:
        print(f"Error: Could not process files '{file_in}' → '{file_out}'.")
        raise e


# PART C (your professor’s Part B in the sheet)
def parse_functions(filename: str) -> Tuple[Tuple[str, str, str], ...]:
    """
    Parses a Python file and extracts all function definitions.

    Returns a tuple of tuples, each containing:
        (function_name, docstring, function_code)

    The function code string includes the signature and body, with:
        - comments removed
        - empty lines removed
        - docstrings preserved

    Parameters:
        filename (str): Python file to parse.

    Raises:
        Exception: Re-raises any file-related errors after printing
                   a user-friendly message.
    """
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error: Could not read file '{filename}'.")
        raise e

    results: List[Tuple[str, str, str]] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i].lstrip()

        if line.startswith("def "):
            signature = lines[i].rstrip()
            name_start = signature.find("def ") + 4
            name_end = signature.find("(")
            func_name = signature[name_start:name_end].strip()

            # gathers body of function, skipping comments and empty lines, but preserving docstrings
            body_lines = [signature]
            i += 1

            docstring = ""
            inside_doc = False

            while i < n:
                current = lines[i]
                stripped = current.strip()

                # ends when the indentation returns to top level
                if stripped and (len(current) - len(current.lstrip())) == 0:
                    break

                if stripped.startswith('"""') or stripped.startswith("'''"):
                    if not inside_doc:
                        inside_doc = True
                        docstring = stripped.strip('"""').strip("'''")
                    else:
                        inside_doc = False
                    i += 1
                    continue

                # Skip comments and empty lines
                if stripped.startswith("#") or stripped == "":
                    i += 1
                    continue

                body_lines.append(stripped)
                i += 1

            func_code = "\n".join(body_lines) + "\n"
            results.append((func_name, docstring, func_code))

        else:
            i += 1

    # Sort alphabetically by function name
    results.sort(key=lambda x: x[0])

    return tuple(results)


def main():
    this_file = r"C:\Users\Denny\Desktop\Assignment2\p1_nguyen_denny.py"
    numbered_output = this_file + ".txt"

    print("Running line_number...")
    line_number(this_file, numbered_output)

    print("Running parse_functions...")
    parsed = parse_functions(this_file)
    print(parsed)


if __name__ == "__main__":
    main()
