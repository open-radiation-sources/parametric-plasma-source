#!/bin/bash

if [ $1 == "gnu" ] ; then
  FC="gfortran"
  CXX="g++"
elif [ $1 == "intel" ] ; then
  FC="ifort"
  CXX="icpc"
else 
  echo "you must provide a compiler name - either gnu or intel"
  exit
fi
echo Building fortran api plasma source library with $FC and $CXX

rm -rf *.o libplasmasource.a *.mod testprog; $CXX -c ../plasma_source.cpp ../plasma_source_api.cpp -std=c++11; ar cr libplasmasource.a *.o; $FC -o testprog plasma_source_module.F90 testprog.F90 -lplasmasource -L./ -lstdc++


