import os

plasma_source_cpp = "plasma_source.cpp"
plasma_source_hpp = "plasma_source.hpp"
source_sampling_cpp = "source_sampling.cpp"
make_file = "Makefile"

py_file = "source.py"

if os.path.exists(py_file):
    os.remove(py_file)

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

write_disclaimer(py_file)
generate_variable(source_sampling_cpp, "source_sampling_cpp", py_file)
generate_variable(plasma_source_cpp, "plasma_source_cpp", py_file)
generate_variable(plasma_source_hpp, "plasma_source_hpp", py_file)
generate_variable(make_file, "make_file", py_file, "\n")
