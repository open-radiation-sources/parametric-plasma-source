#include <pybind11/pybind11.h>
#include "plasma_source.hpp"

namespace py = pybind11;
namespace ps = plasma_source;

PYBIND11_MODULE(plasma_source, m) {
    m.doc() = "A parametric plasma source";

    py::class_<ps::PlasmaSource>(m, "PlasmaSource")
        .def(py::init<const double &, const double &, const double &, const double &,
                      const double &, const double &, const double &, const double &,
                      const double &, const double &, const double &, const double &,
                      const double &, const double &, const std::string &, const int &,
                      const int &, const double &, const double &>(),
                          py::arg("ion_density_pedistal")=1.09e20,
                          py::arg("ion_density_seperatrix")=3e19,
                          py::arg("ion_density_origin")=1.09e20,
                          py::arg("ion_temperature_pedistal")=6.09,
                          py::arg("ion_temperature_seperatrix")=0.1,
                          py::arg("ion_temperature_origin")=45.9,
                          py::arg("pedistal_radius")=0.8,
                          py::arg("ion_density_peaking_factor")=1.0,
                          py::arg("ion_temperature_peaking_factor")=8.06,
                          py::arg("minor_radius")=1.5,
                          py::arg("major_radius")=4.5,
                          py::arg("elongation")=2.0,
                          py::arg("triangularity")=0.55,
                          py::arg("shafranov_shift")=0.0,
                          py::arg("plasma_type")="plasma",
                          py::arg("plasma_id")=1,
                          py::arg("number_of_bins")=100,
                          py::arg("min_toroidal_angle") = 0.0,
                          py::arg("max_toridal_angle") = 360.0)
        .def("ion_density",
             &ps::PlasmaSource::ion_density,
             "Calculate the ion density at a specific minor radius",
             py::arg("minor_radius"))
        .def("ion_temperature",
             &ps::PlasmaSource::ion_temperature,
             "calculate the ion temperature at a specific minor radius",
             py::arg("minor_radius"))
        .def("dt_xs",
             &ps::PlasmaSource::dt_xs,
             "determine the value of the dt xs cross sections at a specific ion temperature",
             py::arg("ion_temperature"));
}
