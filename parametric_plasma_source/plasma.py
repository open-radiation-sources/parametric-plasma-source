
import os
from pathlib import Path
import tempfile
import shutil
from .source import source_sampling_cpp, plasma_source_cpp, plasma_source_hpp, make_file


class Plasma():

    def __init__(self,
                 elongation=2.,
                 major_radius=450,
                 minor_radius=150,
                 single_null=True,
                 triangularity=0.55,
                 ion_density_pedistal=1.09e20,
                 ion_density_seperatrix=3e19,
                 ion_density_origin=1.09e20,
                 ion_temperature_pedistal=6.09,
                 ion_temperature_seperatrix=0.1,
                 ion_temperature_origin=45.9,
                 pedistal_radius=120,  # 0.8 * minor_radius
                 ion_density_peaking_factor=1,
                 ion_temperature_peaking_factor=8.06,
                 ion_temperature_beta=6.0,
                 shafranov_shift=0.0,
                 number_of_bins=100,
                 plasma_type=1,
                 openmc_install_directory = '/opt/openmc/'
                 ):

        # properties needed for plasma shapes
        self.elongation = elongation
        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.single_null = single_null
        self.triangularity = triangularity
        self.ion_density_pedistal = ion_density_pedistal  # ions per m^3
        self.ion_density_seperatrix = ion_density_seperatrix
        self.ion_density_origin = ion_density_origin
        self.ion_temperature_pedistal = ion_temperature_pedistal
        self.ion_temperature_seperatrix = ion_temperature_seperatrix
        self.ion_temperature_origin = ion_temperature_origin
        self.pedistal_radius = pedistal_radius  # pedistal major rad
        self.ion_density_peaking_factor = ion_density_peaking_factor
        self.ion_temperature_peaking_factor = ion_temperature_peaking_factor
        self.ion_temperature_beta = ion_temperature_beta
        self.shafranov_shift = shafranov_shift
        self.number_of_bins = number_of_bins
        self.plasma_type = plasma_type  # 0 = L mode anything else H/A mode
        self.openmc_install_directory = openmc_install_directory

        self.plasma_source_cpp_file = plasma_source_cpp
        self.plasma_source_hpp_file = plasma_source_hpp
        self.source_sampling_cpp_file = source_sampling_cpp
        self.plasma_make_file = make_file

    @property
    def openmc_install_directory(self):
        return self._openmc_install_directory

    @openmc_install_directory.setter
    def openmc_install_directory(self, value):
        if Path(value).exists() == False:
            raise ValueError('openmc_install_directory is out of range')
        else:
            self._openmc_install_directory = value

    @property
    def plasma_type(self):
        return self._plasma_type

    @plasma_type.setter
    def plasma_type(self, plasma_type):
        if plasma_type < 0:
            raise ValueError('plasma_type is out of range')
        else:
            self._plasma_type = plasma_type

    @property
    def number_of_bins(self):
        return self._number_of_bins

    @number_of_bins.setter
    def number_of_bins(self, number_of_bins):
        if number_of_bins < 0:
            raise ValueError('number_of_bins is out of range')
        else:
            self._number_of_bins = number_of_bins

    @property
    def shafranov_shift(self):
        return self._shafranov_shift

    @shafranov_shift.setter
    def shafranov_shift(self, shafranov_shift):
        if shafranov_shift < 0:
            raise ValueError('shafranov_shift is out of range')
        else:
            self._shafranov_shift = shafranov_shift

    @property
    def ion_temperature_peaking_factor(self):
        return self._ion_temperature_peaking_factor

    @ion_temperature_peaking_factor.setter
    def ion_temperature_peaking_factor(self, ion_temperature_peaking_factor):
        if ion_temperature_peaking_factor < 0:
            raise ValueError('ion_temperature_peaking_factor is out of range')
        else:
            self._ion_temperature_peaking_factor = ion_temperature_peaking_factor

    @property
    def ion_temperature_beta(self):
        return self._ion_temperature_beta

    @ion_temperature_beta.setter
    def ion_temperature_beta(self, ion_temperature_beta):
        if ion_temperature_beta < 0:
            raise ValueError('ion_temperature_beta is out of range')
        else:
            self._ion_temperature_beta = ion_temperature_beta

    @property
    def ion_density_peaking_factor(self):
        return self._ion_density_peaking_factor

    @ion_density_peaking_factor.setter
    def ion_density_peaking_factor(self, ion_density_peaking_factor):
        if ion_density_peaking_factor < 0:
            raise ValueError('ion_density_peaking_factor is out of range')
        else:
            self._ion_density_peaking_factor = ion_density_peaking_factor

    @property
    def pedistal_radius(self):
        return self._pedistal_radius

    @pedistal_radius.setter
    def pedistal_radius(self, pedistal_radius):
        if pedistal_radius < 0:
            raise ValueError('pedistal_radius is out of range')
        else:
            self._pedistal_radius = pedistal_radius

    @property
    def ion_temperature_origin(self):
        return self._ion_temperature_origin

    @ion_temperature_origin.setter
    def ion_temperature_origin(self, ion_temperature_origin):
        if ion_temperature_origin < 0:
            raise ValueError('ion_temperature_origin is out of range')
        else:
            self._ion_temperature_origin = ion_temperature_origin

    @property
    def ion_temperature_seperatrix(self):
        return self._ion_temperature_seperatrix

    @ion_temperature_seperatrix.setter
    def ion_temperature_seperatrix(self, ion_temperature_seperatrix):
        if ion_temperature_seperatrix < 0:
            raise ValueError('ion_temperature_seperatrix is out of range')
        else:
            self._ion_temperature_seperatrix = ion_temperature_seperatrix

    @property
    def ion_temperature_pedistal(self):
        return self._ion_temperature_pedistal

    @ion_temperature_pedistal.setter
    def ion_temperature_pedistal(self, ion_temperature_pedistal):
        if ion_temperature_pedistal < 0:
            raise ValueError('ion_temperature_pedistal is out of range')
        else:
            self._ion_temperature_pedistal = ion_temperature_pedistal

    @property
    def ion_density_origin(self):
        return self._ion_density_origin

    @ion_density_origin.setter
    def ion_density_origin(self, ion_density_origin):
        if ion_density_origin < 0:
            raise ValueError('ion_density_origin is out of range')
        else:
            self._ion_density_origin = ion_density_origin

    @property
    def ion_density_seperatrix(self):
        return self._ion_density_seperatrix

    @ion_density_seperatrix.setter
    def ion_density_seperatrix(self, ion_density_seperatrix):
        if ion_density_seperatrix < 0:
            raise ValueError('ion_density_seperatrix is out of range')
        else:
            self._ion_density_seperatrix = ion_density_seperatrix

    @property
    def triangularity(self):
        return self._triangularity

    @triangularity.setter
    def triangularity(self, triangularity):
        if triangularity > 2000 or triangularity < -2000:
            raise ValueError('triangularity is out of range')
        else:
            self._triangularity = triangularity

    @property
    def single_null(self):
        return self._single_null

    @single_null.setter
    def single_null(self, single_null):
        if type(single_null) != bool :
            raise ValueError('single_null must be True or False')
        else:
            self._single_null = single_null

    @property
    def minor_radius(self):
        return self._minor_radius

    @minor_radius.setter
    def minor_radius(self, minor_radius):
        self._minor_radius = minor_radius

    @property
    def major_radius(self):
        return self._major_radius

    @major_radius.setter
    def major_radius(self, major_radius):
        if major_radius > 2000 or major_radius < 1:
            raise ValueError('major_radius is out of range')
        else:
            self._major_radius = major_radius

    @property
    def elongation(self):
        return self._elongation

    @elongation.setter
    def elongation(self, elongation):
        if elongation > 4 or elongation < 0:
            raise ValueError('elongation is out of range')
        else:
            self._elongation = elongation

    @property
    def ion_density_pedistal(self):
        return self._ion_density_pedistal

    @ion_density_pedistal.setter
    def ion_density_pedistal(self, ion_density_pedistal):
        if ion_density_pedistal > 10e22 or ion_density_pedistal < 1e4:
            raise ValueError('ion_density_pedistal is out of range')
        else:
            self._ion_density_pedistal = ion_density_pedistal

    def replace_variable_value(
        self, input_strings, variable_name, new_value, is_cpp=True
    ):
        """Replaces the value assigned to a variable with the provided value

        param: input_strings: The list of strings to search for the variable.
        type input_strings: List[str]
        
        param: variable_name: The name of the variable to search for.
        type variable_name: str
        
        param: new_value: The value to set the variable to.
        type new_value: Union[str, float, int]

        param is_cpp: Whether the variable is a C++ variable.
                      Optional, by default True.
        type is_cpp: bool

        raises ValueError: variable_name was not found in input_strings.
        """
        if is_cpp:
            strs_to_find = ("const", variable_name, "=", ";")
        else:
            strs_to_find = (variable_name, "=")
        for idx, string in enumerate(input_strings):
            if all(str_to_find in string for str_to_find in strs_to_find):
                equals_idx = string.find("=")
                if equals_idx >= 0:
                    if is_cpp:
                        new_value = f"{new_value};"
                    input_strings[idx] = string.replace(
                        input_strings[idx][equals_idx:], f" = {new_value}"
                    )
                    break
        else:
            file_content = "\n".join(input_strings)
            raise ValueError(
                f"{variable_name} string not found in {file_content}"
            )

    def export_plasma_source(self, output_filename):
        """Writes and compiles custom plasma source for the reactor
        :param output_folder: the output folder where the .so complied plasma source will be created
        :type output_folder: str
        ...
        :return: filename of the compiled source
        :rtype: str
        """

        if self.openmc_install_directory is None:
            raise ValueError('directory must be set to create .so file')

        temp_folder = Path(tempfile.mkdtemp())

        Path(output_filename).parent.mkdir(parents=True, exist_ok=True)

        plasma_make_file_lines = self.plasma_make_file.split("\n")
        self.replace_variable_value(
            plasma_make_file_lines, "OPENMC_DIR", self.openmc_install_directory, False
        )

        with open(temp_folder/'Makefile', "w") as text_file:
            text_file.write("\n".join(plasma_make_file_lines))

        with open(temp_folder/'plasma_source.cpp', "w") as text_file:
            text_file.write(self.plasma_source_cpp_file)

        with open(temp_folder/'plasma_source.hpp', "w") as text_file:
            text_file.write(self.plasma_source_hpp_file)

        plasma_variables = {
            "ion_density_pedistal": self.ion_density_pedistal,
            "ion_density_seperatrix": self.ion_density_seperatrix,
            "ion_density_origin": self.ion_density_origin,
            "ion_temperature_pedistal": self.ion_temperature_pedistal,
            "ion_temperature_seperatrix": self.ion_temperature_seperatrix,
            "ion_temperature_origin": self.ion_temperature_origin,
            "pedistal_radius": self.pedistal_radius,
            "ion_density_peaking_factor": self.ion_density_peaking_factor,
            "ion_temperature_peaking_factor": self.ion_temperature_peaking_factor,
            "ion_temperature_beta": self.ion_temperature_beta,
            "minor_radius": self.minor_radius,
            "major_radius": self.major_radius,
            "elongation": self.elongation,
            "triangularity": self.triangularity,
            "shafranov_shift": self.shafranov_shift,
            "number_of_bins": self.number_of_bins,
            "plasma_type": self.plasma_type,
        }

        source_sampling_cpp_lines = self.source_sampling_cpp_file.split("\n")
        [
            self.replace_variable_value(source_sampling_cpp_lines, *variable)
            for variable in plasma_variables.items()
        ]

        with open(temp_folder/'source_sampling.cpp', "w") as text_file:
            text_file.write("\n".join(source_sampling_cpp_lines))

        cwd = os.getcwd()
        os.chdir(Path(temp_folder))

        os.system('make clean')
        os.system('make')

        os.chdir(cwd)
        shutil.move(temp_folder/'source_sampling.so', output_filename)
        print('parametric plasma source compiled and saved to ',  output_filename)
        shutil.rmtree(temp_folder)

        return output_filename


if __name__ == "__main__":
    p = Plasma()
    p.export_plasma_source("source_sampling.so")
