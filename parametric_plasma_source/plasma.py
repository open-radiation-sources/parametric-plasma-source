
import os
from pathlib import Path
import tempfile
import shutil


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
                 pedistal_radius=0.8,
                 ion_density_peaking_factor=1,
                 ion_temperature_peaking_factor=8.06,
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
        self.shafranov_shift = shafranov_shift
        self.number_of_bins = number_of_bins
        self.plasma_type = plasma_type  # 0 = L mode anything else H/A mode
        self.openmc_install_directory = openmc_install_directory

        # parametric plasma source files read into memory
        self.plasma_make_file = Path(Path(__file__).parent/'Makefile').read_text()
        self.plasma_source_cpp_file = Path(Path(__file__).parent/'plasma_source.cpp').read_text()
        self.plasma_source_hpp_file = Path(Path(__file__).parent/'plasma_source.hpp').read_text()
        self.source_sampling_cpp_file = Path(Path(__file__).parent/'source_sampling.cpp').read_text()

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
        if minor_radius > 2000 or minor_radius < 1:
            raise ValueError('minor_radius is out of range')
        else:
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

        editted_plasma_make_file = self.plasma_make_file.replace('OPENMC_DIR = /opt/openmc', 'OPENMC_DIR = '+self.openmc_install_directory)
        with open(temp_folder/'Makefile', "w") as text_file:
            text_file.write(editted_plasma_make_file)

        with open(temp_folder/'plasma_source.cpp', "w") as text_file:
            text_file.write(self.plasma_source_cpp_file)

        with open(temp_folder/'plasma_source.hpp', "w") as text_file:
            text_file.write(self.plasma_source_hpp_file)

        plasma_varibles = [
            ('const double ion_density_pedistal = 1.09e+20', 'const double ion_density_pedistal = ' + str(self.ion_density_pedistal)),
            ('const double ion_density_seperatrix = 3e+19', 'const double ion_density_seperatrix = ' + str(self.ion_density_seperatrix)),
            ('const double ion_density_origin = 1.09e+20', 'const double ion_density_origin = ' + str(self.ion_density_origin)),
            ('const double ion_temperature_pedistal = 6.09', 'const double ion_temperature_pedistal = ' + str(self.ion_temperature_pedistal)),
            ('const double ion_temperature_seperatrix = 0.1','const double ion_temperature_seperatrix = ' + str(self.ion_temperature_seperatrix)),
            ('const double ion_temperature_origin = 45.9', 'const double ion_temperature_origin = ' + str(self.ion_temperature_origin)),
            ('const double pedistal_radius = 0.8', 'const double pedistal_radius = ' + str(self.pedistal_radius)),
            ('const double ion_density_peaking_factor = 1', 'const double ion_density_peaking_factor = ' + str(self.ion_density_peaking_factor)),
            ('const double ion_temperature_peaking_factor = 8.06', 'const double ion_temperature_peaking_factor = ' + str(self.ion_temperature_peaking_factor)),
            ('const double minor_radius = 1.56', 'const double minor_radius = ' + str(self.minor_radius / 100.)),
            ('const double major_radius = 2.5', 'const double major_radius = ' + str(self.major_radius / 100.)),
            ('const double elongation = 2.0', 'const double elongation = ' + str(self.elongation)),
            ('const double triangularity = 0.55', 'const double triangularity = ' + str(self.triangularity)),
            ('const double shafranov_shift = 0.0', 'const double shafranov_shift = ' + str(self.shafranov_shift / 100.)),
            ('const int number_of_bins  = 100', 'const int number_of_bins = ' + str(self.number_of_bins)),
            ('const int plasma_type = 1', 'const int plasma_type = 1' + str(self.plasma_type))
        ]

        editted_source_sampling_cpp_file = self.source_sampling_cpp_file
        for entry in plasma_varibles:
            if entry[0] in self.source_sampling_cpp_file:
                editted_source_sampling_cpp_file = editted_source_sampling_cpp_file.replace(entry[0], entry[1])
            else:
                raise ValueError(entry[0],' string not found in ', self.source_sampling_cpp_file)


        with open(temp_folder/'source_sampling.cpp', "w") as text_file:
            text_file.write(editted_source_sampling_cpp_file)

        cwd = os.getcwd()
        os.chdir(Path(temp_folder))

        os.system('make clean')
        os.system('make')

        os.chdir(cwd)
        shutil.move(temp_folder/'source_sampling.so', output_filename)
        print('parametric plasma source compiled and saved to ',  output_filename)
        shutil.rmtree(temp_folder)

        return output_filename
