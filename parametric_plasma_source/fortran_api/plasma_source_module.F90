module cf_plasma_source

    use iso_c_binding

    implicit none
    
    !private
    public :: plasma_source_f

    ! Interfaces to C routines    
  interface

    function create_plasmasource_c(ion_density_ped, ion_density_sep, &
                                   ion_density_origin, ion_temp_ped, &
                                   ion_temp_sep, ion_temp_origin,    &
                                   pedistal_rad, ion_density_peak,   &
                                   ion_temp_peak, ion_temp_beta,     &
                                   minor_radius, major_radius,       &
                                   elongation, triangularity,        &
                                   shafranov, plasma_type,           &
                                   plasma_id, number_of_bins,        &
                                   min_toroidal_angle,               &
                                   max_toroidal_angle ) result(plasmasource_c) bind(C, name="create_plasmasource")
                                 
                                 
        use iso_c_binding
        implicit none

        type(c_ptr) :: plasmasource_c
        
        real(c_double), intent(in), value :: ion_density_ped
        real(c_double), intent(in), value :: ion_density_sep
        real(c_double), intent(in), value :: ion_density_origin
        real(c_double), intent(in), value :: ion_temp_ped
        real(c_double), intent(in), value :: ion_temp_sep
        real(c_double), intent(in), value :: ion_temp_origin
        real(c_double), intent(in), value :: pedistal_rad
        real(c_double), intent(in), value :: ion_density_peak
        real(c_double), intent(in), value :: ion_temp_peak
        real(c_double), intent(in), value :: ion_temp_beta
        real(c_double), intent(in), value :: minor_radius
        real(c_double), intent(in), value :: major_radius
        real(c_double), intent(in), value :: elongation
        real(c_double), intent(in), value :: triangularity
        real(c_double), intent(in), value :: shafranov
        character(len=1, kind=c_char), intent(in) :: plasma_type(*)
        integer(c_int), intent(in), value :: plasma_id
        integer(c_int), intent(in), value :: number_of_bins
        real(c_double), intent(in), value :: min_toroidal_angle
        real(c_double), intent(in), value :: max_toroidal_angle
        
    end function create_plasmasource_c

    subroutine delete_plasmasource_c(source) bind(C, name="delete_plasmasource")
    
        use iso_c_binding
        implicit none
    
        type(c_ptr), value :: source
    
    end subroutine delete_plasmasource_c
    
    subroutine Sample_Plasma_Source_c(source, random_numbers, x, y, z, u, v, w, E) bind(C, name="Sample_Plasma_Source")

        use iso_c_binding
        implicit none
        
        type(c_ptr), intent(in), value :: source
        real(c_double), dimension(8), intent(in) :: random_numbers
        real(c_double), intent(out) :: x
        real(c_double), intent(out) :: y
        real(c_double), intent(out) :: z
        real(c_double), intent(out) :: u
        real(c_double), intent(out) :: v
        real(c_double), intent(out) :: w
        real(c_double), intent(out) :: E
        
    end subroutine Sample_Plasma_Source_c

  end interface
  
    type plasma_source_f
        type(c_ptr) :: ptr
  
        contains
        
#ifdef __GNUC__
            procedure :: delete => delete_plasmasource_polymorph_f ! Destructor for gfortran
#else
            final :: delete_plasmasource_f ! Destructor
#endif
        
            procedure :: sample => samplesource_f
    end type
    
    interface plasma_source_f
        procedure create_plasmasource_f
    end interface
   
    
    contains
    
        function create_plasmasource_f(ion_density_ped, ion_density_sep, &
                                     ion_density_origin, ion_temp_ped, &
                                     ion_temp_sep, ion_temp_origin,    &
                                     pedistal_rad, ion_density_peak,   &
                                     ion_temp_peak, ion_temp_beta,     &
                                     minor_radius, major_radius,       &
                                     elongation, triangularity,        &
                                     shafranov, f_plasma_type,         &
                                     plasma_id, number_of_bins,        &
                                     min_toroidal_angle,               &
                                     max_toroidal_angle ) result(plasmasource)
        
            type(plasma_source_f) :: plasmasource
        
            real(c_double), intent(in) :: ion_density_ped
            real(c_double), intent(in) :: ion_density_sep
            real(c_double), intent(in) :: ion_density_origin
            real(c_double), intent(in) :: ion_temp_ped
            real(c_double), intent(in) :: ion_temp_sep
            real(c_double), intent(in) :: ion_temp_origin
            real(c_double), intent(in) :: pedistal_rad
            real(c_double), intent(in) :: ion_density_peak
            real(c_double), intent(in) :: ion_temp_peak
            real(c_double), intent(in) :: ion_temp_beta
            real(c_double), intent(in) :: minor_radius
            real(c_double), intent(in) :: major_radius
            real(c_double), intent(in) :: elongation
            real(c_double), intent(in) :: triangularity
            real(c_double), intent(in) :: shafranov
            character(len=*), intent(in) :: f_plasma_type
            integer(c_int), intent(in) :: plasma_id
            integer(c_int), intent(in) :: number_of_bins
            real(c_double), intent(in) :: min_toroidal_angle
            real(c_double), intent(in) :: max_toroidal_angle
    
            character(len=1, kind=C_CHAR) :: c_str(len_trim(f_plasma_type) + 1)
            integer :: n, i
            
            do i = 1, len_trim(f_plasma_type)
              c_str(i)=f_plasma_type(i:i)
            end do
            c_str(len_trim(f_plasma_type)+1) = C_NULL_CHAR
            
            plasmasource%ptr = create_plasmasource_c(ion_density_ped, ion_density_sep, &
                                                     ion_density_origin, ion_temp_ped, &
                                                     ion_temp_sep, ion_temp_origin,    &
                                                     pedistal_rad, ion_density_peak,   &
                                                     ion_temp_peak, ion_temp_beta,     &
                                                     minor_radius, major_radius,       &
                                                     elongation, triangularity,        &
                                                     shafranov, c_str,                 &
                                                     plasma_id, number_of_bins,        &
                                                     min_toroidal_angle,               &
                                                     max_toroidal_angle )              
            
    
        end function create_plasmasource_f
        
        subroutine delete_plasmasource_f(this)
            implicit none
            type(plasma_source_f) :: this
            call delete_plasmasource_c(this%ptr)
        end subroutine delete_plasmasource_f

        ! Bounds procedure needs to take a polymorphic (class) argument
        subroutine delete_plasmasource_polymorph_f(this)
            implicit none
            class(plasma_source_f) :: this
            call delete_plasmasource_c(this%ptr)
        end subroutine delete_plasmasource_polymorph_f
        
        subroutine samplesource_f(this, random_numbers, x, y, z, u, v, w, E)
            
            class(plasma_source_f) :: this
            real(c_double), dimension(8), intent(in) :: random_numbers
            real(c_double), intent(out) :: x
            real(c_double), intent(out) :: y
            real(c_double), intent(out) :: z
            real(c_double), intent(out) :: u
            real(c_double), intent(out) :: v
            real(c_double), intent(out) :: w
            real(c_double), intent(out) :: E
        
            call Sample_Plasma_Source_c(this%ptr, random_numbers, x, y, z, u, v, w, E)
        
        end subroutine samplesource_f

end module cf_plasma_source
