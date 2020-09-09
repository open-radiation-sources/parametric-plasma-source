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
                          py::arg("ion_density_pedistal"),
                          py::arg("ion_density_seperatrix"),
                          py::arg("ion_density_origin"),
                          py::arg("ion_temperature_pedistal"),
                          py::arg("ion_temperature_seperatrix"),
                          py::arg("ion_temperature_origin"),
                          py::arg("pedistal_radius"),
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
