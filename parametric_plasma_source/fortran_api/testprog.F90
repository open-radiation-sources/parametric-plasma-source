program test

use cf_plasma_source
use iso_c_binding

implicit none

    type(plasma_source_f), save :: source
    
    real(c_double), parameter :: ion_density_pedistal = 1.09e+20
    real(c_double), parameter :: ion_density_seperatrix = 3e+19
    real(c_double), parameter :: ion_density_origin = 1.09e+20
    real(c_double), parameter :: ion_temperature_pedistal = 6.09
    real(c_double), parameter :: ion_temperature_seperatrix = 0.1
    real(c_double), parameter :: ion_temperature_origin = 45.9
    real(c_double), parameter :: ion_density_peaking_factor = 1
    real(c_double), parameter :: ion_temperature_peaking_factor = 8.06
    real(c_double), parameter :: ion_temperature_beta = 6.0
    real(c_double), parameter :: minor_radius = 1.56
    real(c_double), parameter :: major_radius = 2.5
    real(c_double), parameter :: pedistal_radius = 0.8 * minor_radius
    real(c_double), parameter :: elongation = 2.0
    real(c_double), parameter :: triangularity = 0.55
    real(c_double), parameter :: shafranov_shift = 0.0
    character (len=*), parameter :: plasma_name="parametric_plasma_source"
    integer(c_int), parameter :: number_of_bins  = 100
    integer(c_int), parameter :: plasma_id = 1
    real(c_double), parameter :: min_toroidal_angle = 0
    real(c_double), parameter :: max_toroidal_angle = 360

    real(c_double) :: x
    real(c_double) :: y
    real(c_double) :: z
    real(c_double) :: u 
    real(c_double) :: v
    real(c_double) :: w
    real(c_double) :: E
    
    real(c_double), dimension(8) :: rand_nums
    
    integer :: i
    integer, parameter :: num_points = 1000
    character (len=*), parameter :: filename="starting_points.o"
    
    write(*,*)"Initialising source"
    ! Create source type
    source = plasma_source_f(ion_density_pedistal, ion_density_seperatrix, &
                           ion_density_origin, ion_temperature_pedistal, &
                           ion_temperature_seperatrix, ion_temperature_origin,    &
                           pedistal_radius, ion_density_peaking_factor,   &
                           ion_temperature_peaking_factor, ion_temperature_beta,     &
                           minor_radius, major_radius,       &
                           elongation, triangularity,        &
                           shafranov_shift, plasma_name,         &
                           plasma_id, number_of_bins,        &
                           min_toroidal_angle,               &
                           max_toroidal_angle )


    ! Open a file to output results to
    open(unit=100, file=filename)
    
    write(*,*)"Sampling ", num_points," points and writing them to ", filename
    ! Sample the source and return the starting variables
    do i=1,1000
      ! write(*,*)"calling random number"
      call random_number(rand_nums)
      ! write(*,*)rand_nums
      call source%sample(rand_nums,x,y,z,u,v,w,E)
      write(100,*)x,y,z,u,v,w,E
    end do
    close(100)

end program test
