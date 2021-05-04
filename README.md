# actymath

Actuarial formulae and commutation functions for life insurance products (with a fast Pandas backend)

## Read this first

This started out as a package to build up the various actuarial formulae using the Pandas backend for speed.

The way it works is to create a 'grid' of actuarial calculation vectors in a pandas DataFrame that you can use for a single policy or a single cohort.

When you ask for a particular actuarial formula or calculation to be created, it will spawn the columns needed to generate it.

Everything is using Pandas in the backend, so you can use any normal Pandas machinery you like.

This is very much 'in development'.

## Usage

### Installation

Install using pip

    pip install actymath

### Getting started

This [getting started notebook](https://github.com/ttamg/actymath/blob/main/notebooks/01_getting_started.ipynb) illustrates how to use the package with a simple example.

### Actuarial formula

The formula definitions are called **columns** in this package as they spawn columns in a pandas DataFrame.

These formulae can be explored in the [actymath/columns directory](https://github.com/ttamg/actymath/tree/main/actymath/columns).

### Mortality tables

Currently only a few old standard mortality tables are implemented, but there is support for 1D and 2D mortality tables [here](https://github.com/ttamg/actymath/blob/main/actymath/tables.py).

## Contributing

Feel free to contribute or suggest improvements.

- Add suggested improvements as a GitHub issue on this project

- Pull requests also welcomed, particularly for any fixes, new tables or useful actuarial formulae

### Developer setup

Clone this repository using

    git clone git@github.com:ttamg/actymath.git

Dependencies use **poetry** so make sure you have [poetry already installed](https://python-poetry.org/docs/) on you development machine.

With poetry, you create a new virtual environment for yourself and activate it using

    poetry shell

To install all the dependencies in your new virtual environment, use

    poetry install

### Running tests

We use **pytest** for all testing. Run the test pack using

    pytest
