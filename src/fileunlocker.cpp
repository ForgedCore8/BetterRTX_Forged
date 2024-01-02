#include <pybind11/pybind11.h>
#include "fileunlocker.h" // Assuming the header code is in fileunlocker.h

namespace py = pybind11;

PYBIND11_MODULE(fileunlocker, m) {
    m.doc() = "Python bindings for file unlocker functionality";

    py::class_<unlocker::File>(m, "File")
        .def(py::init<const tstring&>())
        .def("Unlock", &unlocker::File::Unlock)
        .def("ForceDelete", &unlocker::File::ForceDelete)
        .def("Delete", &unlocker::File::Delete);

    py::class_<unlocker::Dir, unlocker::File>(m, "Dir")
        .def(py::init<const tstring&>())
        .def("Delete", &unlocker::Dir::Delete)
        .def("DeleteDir", &unlocker::Dir::DeleteDir);

    m.def("Exists", &unlocker::Path::Exists);
}