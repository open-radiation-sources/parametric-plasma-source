cmake_minimum_required(VERSION 3.3 FATAL_ERROR)
project(parametric_plasma_source)

set(CMAKE_VERBOSE_MAKEFILE OFF)

set(SRC_DIR parametric_plasma_source)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${SRC_DIR})

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_CXX_FLAGS "-Wall")
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

# Use output paths from OpenMC install - change if needed
set(OPENMC_DIR /opt/openmc)
set(OPENMC_INC_DIR ${OPENMC_DIR}/include)
set(OPENMC_LIB_DIR ${OPENMC_DIR}/lib)

# Build source_sampling
list(APPEND source_sampling_SOURCES
  ${SRC_DIR}/source_sampling.cpp
  ${SRC_DIR}/plasma_source.cpp
)

add_library(source_sampling SHARED ${source_sampling_SOURCES})

find_library(OPENMC_LIB openmc HINTS ${OPENMC_LIB_DIR})

set_target_properties(source_sampling PROPERTIES PREFIX "")
set_target_properties(source_sampling PROPERTIES POSITION_INDEPENDENT_CODE ON)
target_include_directories(source_sampling PUBLIC ${OPENMC_INC_DIR})
target_include_directories(source_sampling PUBLIC ${OPENMC_DIR}/vendor/pugixml)
target_link_libraries(source_sampling ${OPENMC_LIB} gfortran)

# Build plasma_source Python bindings
list(APPEND plasma_source_pybind_SOURCES
  ${SRC_DIR}/plasma_source.cpp
  ${SRC_DIR}/plasma_source_pybind.cpp
)

add_subdirectory(pybind11)

pybind11_add_module(plasma_source ${plasma_source_pybind_SOURCES})
