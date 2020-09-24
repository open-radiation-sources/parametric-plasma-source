cmake_minimum_required(VERSION 3.3 FATAL_ERROR)
project(parametric_plasma_source)

set(CMAKE_VERBOSE_MAKEFILE OFF)

set(SRC_DIR parametric_plasma_source)

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

# Ensure submodules are available and up to date
find_package(Git QUIET)
if(GIT_FOUND AND EXISTS "${PROJECT_SOURCE_DIR}/.git")
  # Update submodules as needed
  option(GIT_SUBMODULE "Check submodules during build" ON)
  if(GIT_SUBMODULE)
    message(STATUS "Submodule update")
    execute_process(COMMAND ${GIT_EXECUTABLE} submodule update --init --recursive
                    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                    RESULT_VARIABLE GIT_SUBMOD_RESULT)
    if(NOT GIT_SUBMOD_RESULT EQUAL "0")
      message(FATAL_ERROR "git submodule update --init failed with ${GIT_SUBMOD_RESULT}, please checkout submodules")
    endif()
  endif()
endif()

if(NOT EXISTS "${PROJECT_SOURCE_DIR}/pybind11/CMakeLists.txt")
  message(FATAL_ERROR "The submodules were not downloaded! GIT_SUBMODULE was turned off or failed. Please update submodules and try again.")
endif()

# Build source_sampling
list(APPEND source_sampling_SOURCES
  ${SRC_DIR}/source_sampling.cpp
  ${SRC_DIR}/plasma_source.cpp
)

add_library(source_sampling SHARED ${source_sampling_SOURCES})

find_library(OPENMC_LIB openmc HINTS ${OPENMC_LIB_DIR} OPTIONAL)

if (OPENMC_LIB)
  set_target_properties(source_sampling PROPERTIES PREFIX "")
  set_target_properties(source_sampling PROPERTIES POSITION_INDEPENDENT_CODE ON)
  target_include_directories(source_sampling PUBLIC ${OPENMC_INC_DIR})
  target_include_directories(source_sampling PUBLIC ${OPENMC_DIR}/vendor/pugixml)
  target_link_libraries(source_sampling ${OPENMC_LIB} gfortran)
endif()

# Build plasma_source Python bindings
list(APPEND plasma_source_pybind_SOURCES
  ${SRC_DIR}/plasma_source.cpp
  ${SRC_DIR}/plasma_source_pybind.cpp
)

add_subdirectory(pybind11)

pybind11_add_module(plasma_source ${plasma_source_pybind_SOURCES})

# Build source_generator
list(APPEND source_generator_SOURCES
  ${SRC_DIR}/source_generator.cpp
)

add_executable(source_generator ${source_generator_SOURCES})

find_package(HDF5 REQUIRED)

set_target_properties(source_generator PROPERTIES POSITION_INDEPENDENT_CODE ON)
target_include_directories(source_generator PUBLIC ${OPENMC_INC_DIR})
target_include_directories(source_generator PUBLIC ${HDF5_INCLUDE_DIRS})
target_include_directories(source_generator PUBLIC ${OPENMC_DIR}/vendor/pugixml)
target_link_libraries(source_generator ${OPENMC_LIB} ${HDF5_LIBRARIES} stdc++fs)
