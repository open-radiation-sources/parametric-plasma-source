add_executable(tests ${PROJECT_SOURCE_DIR}/tests/src/test_plasma_source.cpp)

target_include_directories(tests PUBLIC ${PROJECT_SOURCE_DIR}/parametric_plasma_source/src ${PROJECT_SOURCE_DIR}/tests/src)
target_link_libraries(tests source_sampling)
