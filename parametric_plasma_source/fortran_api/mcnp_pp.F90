module pp_source_mk2_mod

! Modules for use with the parametric plasma source mk2
use cf_plasma_source
use iso_c_binding

! MCNP modules
use mcnp_debug
use pblcom, only   : pbl
use mcnp_params, only   : dknd, i4knd
use mcnp_random, only   : rang

implicit none

contains

    subroutine parametric_plasma_2()
    
        type(plasma_source_f), save :: source
        
        real(c_double) :: ion_density_pedistal 
        real(c_double) :: ion_density_seperatrix
        real(c_double) :: ion_density_origin 
        real(c_double) :: ion_temperature_pedistal
        real(c_double) :: ion_temperature_seperatrix
        real(c_double) :: ion_temperature_origin
        real(c_double) :: ion_density_peaking_factor
        real(c_double) :: ion_temperature_peaking_factor
        real(c_double) :: ion_temperature_beta
        real(c_double) :: minor_radius
        real(c_double) :: major_radius
        real(c_double) :: pedistal_radius
        real(c_double) :: elongation
        real(c_double) :: triangularity
        real(c_double) :: shafranov_shift
        character (len=100) :: plasma_name
        integer(c_int) :: number_of_bins
        integer(c_int) :: plasma_id
        real(c_double) :: min_toroidal_angle
        real(c_double) :: max_toroidal_angle
        
        logical, save :: bInit=.FALSE. !Start uninitialised
        real(c_double), allocatable :: random_numbers(:)
        integer(i4knd), parameter :: num_of_rands = 8
        
        real(c_double) :: xxx
        real(c_double) :: yyy
        real(c_double) :: zzz
        real(c_double) :: uuu
        real(c_double) :: vvv
        real(c_double) :: www
        real(c_double) :: EEE
        
        
        
        ! Set up parameters from the rdum and idum cards
        plasma_name = "parametric_plasma_source"
        ion_density_pedistal           = rdum(1)
        ion_density_seperatrix         = rdum(2)
        ion_density_origin             = rdum(3)
        ion_temperature_pedistal       = rdum(4)
        ion_temperature_seperatrix     = rdum(5)
        ion_temperature_origin         = rdum(6)
        ion_density_peaking_factor     = rdum(7)
        ion_temperature_peaking_factor = rdum(8)
        ion_temperature_beta           = rdum(9)
        minor_radius                   = rdum(10)
        major_radius                   = rdum(11)
        pedistal_radius                = rdum(12)
        elongation                     = rdum(13)
        triangularity                  = rdum(14)
        min_toroidal_angle             = rdum(15)
        max_toroidal_angle             = rdum(16)
        
        number_of_bins                 = idum(2)
        plasma_id                      = idum(3) ! 1 is default; //0 = L mode anything else H/A mode
        
        ! If this is the first time through init the source
        if(.not. bInit) then
            bInit = .True.
            
            source = plasma_source_f(ion_density_pedistal, ion_density_seperatrix,         &
                                     ion_density_origin, ion_temperature_pedistal,         &
                                     ion_temperature_seperatrix, ion_temperature_origin,   &
                                     pedistal_radius, ion_density_peaking_factor,          &
                                     ion_temperature_peaking_factor, ion_temperature_beta, &
                                     minor_radius, major_radius,                           &
                                     elongation, triangularity,                            &
                                     shafranov_shift, plasma_name,                         &
                                     plasma_id, number_of_bins,                            &
                                     min_toroidal_angle,                                   &
                                     max_toroidal_angle )
            
        end if
        
        ! Start here if this isn't the first time this routine has been called and sample source
        
        !source is a cell 
        pbl%i%jsu=0
        !source is neutrons    
        pbl%i%ipt=1
        !time independent   
        pbl%r%tme=0
        !initialise to weight 1.0
        pbl%r%wgt=1.0_dknd
        
        ! Get random numbers
        random_numbers = get_random_numbers(num_of_rands)
        
        ! init variables
        xxx=0.0_c_double
        yyy=0.0_c_double
        zzz=0.0_c_double
        uuu=0.0_c_double
        vvv=0.0_c_double
        www=0.0_c_double
        EEE=0.0_c_double
        
        ! Call C++ sampling routine
        call source%sample(random_numbers,xxx,yyy,zzz,uuu,vvv,www,EEE)
        
        ! Convert into cm
        pbl%r%x = xxx * 100 
        pbl%r%y = yyy * 100
        pbl%r%z = zzz * 100
        pbl%r%erg = EEE
        
        ! Setup the rest of the particle information by calling findlv
        call findlv()
    
    end subroutine parametric_plasma_2
    
    !----------------------------------------------------------------------------------
    ! Function to fill an array with a given quantity of random numbers
    !----------------------------------------------------------------------------------
    function get_random_numbers(quantity) result(random_nums)
        implicit none
        
        integer(i4knd), intent(in) :: quantity
        real(dknd), allocatable :: random_nums(:)
        
        integer(i4knd) :: i
        
        if(allocated(random_nums))deallocate(random_nums)
        allocate(random_nums(quantity))
        do i = 1, quantity
            random_nums(i) = rang()
        end do
    
    end function get_random_numbers


end module pp_source_mk2_mod