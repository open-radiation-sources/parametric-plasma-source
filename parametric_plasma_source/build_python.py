import os

plasma_source_cpp = "plasma_source.cpp"
plasma_source_hpp = "plasma_source.hpp"
source_sampling_cpp = "source_sampling.cpp"
make_file = "Makefile"

py_file = "source.py"

def write_disclaimer(py_file_path):
    disclaimer = "\"\"\"\n"
    disclaimer += "Auto-generated file. To edit, run `python build_python.py`.\n"
    disclaimer += "This will need to be run whenever a new C++ version is made available.\n"
    disclaimer += "\"\"\"\n\n"
    with open(py_file_path, "a+") as f_py:
        f_py.write(disclaimer)

def generate_variable(cpp_file_path, variable_name, py_file_path, end_str="\n\n"):
    with open(cpp_file_path, "r") as f_cpp:
        lines = f_cpp.readlines()
        py_lines = variable_name
        py_lines += " = (\n\"\"\""
        py_lines += "".join(lines)
        py_lines += "\"\"\"\n)"
        py_lines += end_str
        with open(py_file_path, "a+") as f_py:
            f_py.write(py_lines)

def build(source_dir="."):
    output_path = os.path.join(source_dir, py_file)

    if os.path.exists(output_path):
        os.remove(output_path)

    write_disclaimer(output_path)
    generate_variable(
        os.path.join(source_dir, source_sampling_cpp),
        "source_sampling_cpp",
        output_path
    )
    generate_variable(
        os.path.join(source_dir, plasma_source_cpp),
        "plasma_source_cpp",
        output_path
    )
    generate_variable(
        os.path.join(source_dir, plasma_source_hpp),
        "plasma_source_hpp",
        output_path
    )
    generate_variable(
        os.path.join(source_dir, make_file),
        "make_file",
        output_path,
        "\n"
    )
