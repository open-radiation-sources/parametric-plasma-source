#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "plasma_source.hpp"

namespace py = pybind11;
namespace ps = plasma_source;

PYBIND11_MODULE(plasma_source, m) {
    m.doc() = "A parametric plasma source";

    py::class_<ps::PlasmaSource>(m, "PlasmaSource")
        .def(py::init<const double &, const double &, const double &, const double &,
                      const double &, const double &, const double &, const double &,
                      const double &, const double &, const double &, const double &,
                      const double &, const double &, const double &, const std::string &,
                      const int &, const int &, const double &, const double &>(),
                          py::arg("ion_density_pedestal"),
                          py::arg("ion_density_separatrix"),
                          py::arg("ion_density_origin"),
                          py::arg("ion_temperature_pedestal"),
                          py::arg("ion_temperature_separatrix"),
                          py::arg("ion_temperature_origin"),
                          py::arg("pedestal_radius"),
                          py::arg("ion_density_peaking_factor"),
                          py::arg("ion_temperature_peaking_factor"),
                          py::arg("ion_temperature_beta"),
                          py::arg("minor_radius"),
                          py::arg("major_radius"),
                          py::arg("elongation"),
                          py::arg("triangularity"),
                          py::arg("shafranov_shift"),
                          py::arg("plasma_type")="plasma",
                          py::arg("plasma_id")=1,
                          py::arg("number_of_bins")=100,
                          py::arg("min_toroidal_angle")=0.0,
                          py::arg("max_toridal_angle")=360.0)
        .def_property_readonly("ion_density_pedestal", &ps::PlasmaSource::getIonDensityPedestal)
        .def_property_readonly("ion_density_separatrix", &ps::PlasmaSource::getIonDensitySeparatrix)
        .def_property_readonly("ion_density_origin", &ps::PlasmaSource::getIonDensityOrigin)
        .def_property_readonly("ion_temperature_pedestal", &ps::PlasmaSource::getIonTemperaturePedestal)
        .def_property_readonly("ion_temperature_separatrix", &ps::PlasmaSource::getIonTemperatureSeparatrix)
        .def_property_readonly("ion_temperature_origin", &ps::PlasmaSource::getIonTemperatureOrigin)
        .def_property_readonly("pedestal_radius", &ps::PlasmaSource::getPedestalRadius)
        .def_property_readonly("ion_density_peaking_factor", &ps::PlasmaSource::getIonDensityPeaking)
        .def_property_readonly("ion_temperature_peaking_factor", &ps::PlasmaSource::getIonTemperaturePeaking)
        .def_property_readonly("ion_temperature_beta", &ps::PlasmaSource::getIonTemperatureBeta)
        .def_property_readonly("minor_radius", &ps::PlasmaSource::getMinorRadius)
        .def_property_readonly("major_radius", &ps::PlasmaSource::getMajorRadius)
        .def_property_readonly("elongation", &ps::PlasmaSource::getElongation)
        .def_property_readonly("triangularity", &ps::PlasmaSource::getTriangularity)
        .def_property_readonly("shafranov_shift", &ps::PlasmaSource::getShafranov)
        .def_property_readonly("plasma_type", &ps::PlasmaSource::getPlasmaType)
        .def_property_readonly("plasma_id", &ps::PlasmaSource::getPlasmaId)
        .def_property_readonly("number_of_bins", &ps::PlasmaSource::getNumberOfBins)
        .def_property_readonly("min_toroidal_angle", &ps::PlasmaSource::getMinToroidalAngle)
        .def_property_readonly("max_toridal_angle", &ps::PlasmaSource::getMaxToroidalAngle)
        .def("ion_density",
             &ps::PlasmaSource::ion_density,
             "Calculate the ion density at a specific minor radius",
             py::arg("minor_radius"))
        .def("ion_temperature",
             &ps::PlasmaSource::ion_temperature,
             "Calculate the ion temperature at a specific minor radius",
             py::arg("minor_radius"))
        .def("dt_xs",
             &ps::PlasmaSource::dt_xs,
             "Determine the value of the dt xs cross sections at a specific ion temperature",
             py::arg("ion_temperature"))
        .def("sample",
             [](ps::PlasmaSource &source, std::array<double,8> random_numbers) {
                 double x, y, z;
                 double u, v, w;
                 double e;
                 source.sample(random_numbers, x, y, z, u, v, w, e);
                 return py::make_tuple(x, y, z, u, v, w, e);
             },
             R"(
                  Sample the source.

                  Parameters
                  ----------
                  random_numbers : List[float[8]]
                      The set of eight random numbers to use when sampling the source.
                  
                  Returns
                  -------
                  x : float
                      The initial x-coordinate of the particle.
                  y : float
                      The initial y-coordinate of the particle.
                  z : float
                      The initial z-coordinate of the particle.
                  x : float
                      The initial x direction of the particle.
                  y : float
                      The initial y direction of the particle.
                  z : float
                      The initial z direction of the particle.
                  e : float
                      The initial energy of the particle.
             )",
             py::arg("random_numbers"))  
        .def("__str__",
             (std::string (ps::PlasmaSource::*)()) &ps::PlasmaSource::to_string,
             "Write out the PlasmaSource as a key-value string")
        .def_static("from_string",
                    &ps::PlasmaSource::from_string,
                    "Load the PlasmaSource from a key-value string.",
                    py::arg("parameters"));
}
