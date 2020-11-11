# Ensure submodules are available and up to date
find_package(Catch2 REQUIRED)

add_executable(tests ${PROJECT_SOURCE_DIR}/tests/src/test_plasma_source.cpp)

target_include_directories(tests PUBLIC ${PROJECT_SOURCE_DIR}/parametric_plasma_source/src)
target_link_libraries(tests Catch2::Catch2WithMain source_sampling)

include(CTest)
include(Catch)
catch_discover_tests(tests)
