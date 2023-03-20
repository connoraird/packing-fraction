# Packing Fraction

This app calculates the packing fraction of a 2D box containing circles via the equation
```
Packing Fraction = (Number of circles x Area of one circle) / Total area of the box
```
The packing fraction is calulated via a monte carlo method where a given number of sample circles are randomly generated within the box and removed if overlapping an existing circle. 

## Prerequisites

In order to run the app you will require the following to be installed.

- pipenv = 2023.2.18
- python = 3.8.15

## Running the app

Firstly, start the virtual env:
```
pipenv shell
```
and install the dependencies (see [Pipfile](./Pipfile))
```
pipenv install
```
Then run the app
- **Serial app:** The serial app can be treated like any other python module, i.e. in a python script you can run 
    ```py
    from serial_app import main
    main(width=100, height=100, radius=1, num_of_samples=1000)
    ```
- **Parallel app:** The parallel app must be ran slightly differently in order to allow parallelisation. 
    ```
    mpiexec -np <number_of_processors> python -m mpi4py parallel_app.py
    ```
    Therefore, to alter the inputs into the parallel app, update the call to `main` in [parallel_app.py](./parallel_app.py)

## Outputs

The program should output two graphs. One graph displays the circles within the box ([coordinates.png](./coordinates.png)) and the other the packing fraction vs the number of samples used ([PF_vs_samples.png](./PF_vs_samples.png)).

## Tests

To run the tests, first activate the virtual env
```
pipenv shell
```
then, run the tests
```
python -m unittest
```