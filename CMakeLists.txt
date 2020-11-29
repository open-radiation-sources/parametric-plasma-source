cmake_minimum_required(VERSION 3.3 FATAL_ERROR)
project(parametric_plasma_source)
# look in the cmake folder
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/cmake)

set(CMAKE_VERBOSE_MAKEFILE OFF)

set(SRC_DIR parametric_plasma_source)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_CXX_FLAGS "-Wall")
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

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

# Use output paths from OpenMC install
# If OpenMC isn't available then we won't be able to build the plugin
# However, the package can still be run by using the sampling methods directly
# So don't terminate the build
find_package(OpenMC QUIET)

if(OPENMC_FOUND)
  # Build the source_sampling OpenMC plugin if OpenMC is available
  set(OPENMC_INC_DIR ${OPENMC_DIR}/include)
  set(OPENMC_LIB_DIR ${OPENMC_DIR}/lib)

  message(STATUS ${OPENMC_INC_DIR})
  add_library(source_sampling SHARED ${source_sampling_SOURCES})

  find_library(OpenMC::libopenmc openmc HINTS ${OPENMC_LIB_DIR} OPTIONAL)

  set_target_properties(source_sampling PROPERTIES PREFIX "")
  set_target_properties(source_sampling PROPERTIES POSITION_INDEPENDENT_CODE ON)
  target_include_directories(source_sampling PUBLIC ${OPENMC_INC_DIR})
  target_link_libraries(source_sampling OpenMC::libopenmc gfortran)
else()
  message(WARNING "Unable to find OpenMC installation - the source_sampling plugin will not be built.")
endif()

# Build plasma_source Python bindings
list(APPEND plasma_source_pybind_SOURCES
  ${SRC_DIR}/plasma_source.cpp
  ${SRC_DIR}/plasma_source_pybind.cpp
)

add_subdirectory(pybind11)

pybind11_add_module(plasma_source ${plasma_source_pybind_SOURCES})

add_subdirectory(pugixml)

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
target_link_libraries(source_generator OpenMC::libopenmc pugixml ${HDF5_LIBRARIES} stdc++fs)
