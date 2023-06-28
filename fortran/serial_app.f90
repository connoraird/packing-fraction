program serial_app
    use, intrinsic :: iso_fortran_env, only: sp=>real32, dp=>real64
    implicit none
    
    !inputs
    real(dp) :: width, height, radius
    integer :: num_of_samples

    ! calculation variables
    real(dp) :: pi, diameter, circle_area, box_area, x, y, packing_fraction, randx, randy
    integer :: batch_size, sample_number, num_of_circles, i
    real(dp), allocatable :: x_coordinates(:), y_coordinates(:)
    logical :: overlapping

    print *, 'Box width:'
    read(*, *) width
    print *, 'Box height:'
    read(*, *) height
    print *, 'Circle radius:'
    read(*, *) radius
    print *, 'Total number of samples:'
    read(*, *) num_of_samples

    print*, 'Input are:' 
    print *, 'Box width: ', width
    print *, 'Box height: ', height
    print *, 'Circle radius: ', radius
    print *, 'Total number of samples: ', num_of_samples

    allocate(x_coordinates(num_of_samples))
    allocate(y_coordinates(num_of_samples))

    pi = 3.141592653589793238_dp
    diameter = 2.0_dp * radius
    circle_area = pi * (radius ** 2)
    box_area = width * height
    batch_size = floor(num_of_samples * 0.01)
    num_of_circles = 0

    do sample_number = 0, num_of_samples
        call random_number(randx)
        call random_number(randy)
        x = radius + randx * (width - diameter)
        y = radius + randy * (height - diameter)

        overlapping = .FALSE.
        do i = 0, num_of_circles
            overlapping = (((x_coordinates(i) - x)**2 + (y_coordinates(i) - y)**2) ** 0.5) < diameter
            if (overlapping) then
                exit
            end if 
        end do

        if (.not.overlapping) then
            x_coordinates(num_of_circles) = x
            y_coordinates(num_of_circles) = y
            num_of_circles = num_of_circles + 1
        end if
    end do

    ! Calculate outputs 
    packing_fraction = (num_of_circles * circle_area) / box_area
    print *, 'Packing fraction for ', num_of_samples, ' samples and ', num_of_circles, ' circles is ', packing_fraction
    open (unit=0, file="coordinates.csv")
    do i = 0, num_of_circles
        write(0, *) x_coordinates(i), y_coordinates(i)
    end do
    close (0)

end program serial_app
    