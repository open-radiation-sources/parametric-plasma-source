#include <iostream>
#include <experimental/filesystem>

#include "openmc/bank.h"
#include "openmc/constants.h"
#include "openmc/message_passing.h"
#include "openmc/settings.h"
#include "openmc/simulation.h"
#include "openmc/source.h"

namespace source_generator
{
  void print_settings(std::string path_source_library, std::string source_parameters)
  {
    using namespace openmc;

    std::cout << "Settings:" << std::endl;
    std::cout << " Number of particles: " << settings::n_particles << std::endl;
    std::cout << " Source library: " << path_source_library << std::endl;
    std::cout << " Source parameters: " << source_parameters << std::endl;
    std::cout << " Output path: " << settings::path_output << std::endl;
    std::cout << " Verbosity: " << settings::verbosity << std::endl;
    std::cout << std::endl;
  }

  void print_help()
  {
    std::cout << "Usage:" << std::endl;
    std::cout << "source_generator [OPTIONS]" << std::endl;
    std::cout << std::endl;
    std::cout << "Options:" << std::endl;
    std::cout << " -l,--library      Source library, mandatory" << std::endl;
    std::cout << " -i,--input        Source definition, mandatory" << std::endl;
    std::cout << " -n,--particles    Number of particles, default 1000" << std::endl;
    std::cout << " -o,--output       Output directory, default {current directory}" << std::endl;
    std::cout << " -v,--verbosity    Verbosity, default 5" << std::endl; 
  }

  void set_defaults()
  {
    using namespace openmc;
    using namespace std::experimental;

    std::string current_path = filesystem::current_path().string();

    // These are static to make sure we get some output...
    settings::run_mode = RunMode::EIGENVALUE;
    settings::write_initial_source = true;

    // Variables with sensible default values
    settings::n_particles = 1000;
    settings::path_output = current_path + "/";
    settings::verbosity = 5;
  }

  int parse_command_line(int argc, char* argv[], std::string &path_source_library, std::string &source_parameters)
  {
    using namespace openmc;

    for (int i=1; i < argc; ++i)
    {
      std::string arg {argv[i]};
      if (arg[0] == '-')
      {
        if (arg == "-n" || arg == "--particles")
        {
          i += 1;
          settings::n_particles = std::stoll(argv[i]);
        }
        else if (arg == "-l" || arg == "--library")
        {
          i += 1;
          path_source_library = argv[i];
        }
        else if (arg == "-i" || arg == "--input")
        {
          i += 1;
          source_parameters = argv[i];
        }
        else if (arg == "-o" || arg == "--output")
        {
          i += 1;
          settings::path_output = argv[i];
        }
        else if (arg == "-v" || arg == "--verbosity")
        {
          i += 1;
          settings::verbosity = std::stoi(argv[i]);
        }
        else
        {
          source_generator::print_help();
          return -1;
        }
      }
    }

    bool missing_arg = false;

    if (path_source_library.empty())
    {
      std::cout << "The --library or -l argument is mandatory and must be set." << std::endl;
      missing_arg = true;
    }

    if (source_parameters.empty())
    {
      std::cout << "The --input or -i argument is mandatory and must be set." << std::endl;
      missing_arg = true;
    }

    if (missing_arg)
    {
      source_generator::print_help();
      return -1;
    }
    else
    {
      return 0;
    }
  }
}

int main(int argc, char* argv[])
{
  std::string path_source_library;
  std::string source_parameters;

  source_generator::set_defaults();

  int run = source_generator::parse_command_line(argc, argv, path_source_library, source_parameters);

  if (run < 0)
  {
    return run;
  }

  if (openmc::settings::verbosity >= 5)
  {
    source_generator::print_settings(path_source_library, source_parameters);
  }

  std::cout << "Sampling source:" << std::endl;
  openmc::model::external_sources.push_back(std::make_unique<openmc::CustomSourceWrapper>(path_source_library, source_parameters));
  openmc::calculate_work();
  openmc::allocate_banks();
  openmc::initialize_source();
  std::cout << "Source sampling completed." << std::endl;

  return 0;
}
