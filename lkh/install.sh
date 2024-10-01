#!/usr/bin/env bash

# Download and compile LKH Solver

#VERSION=2.0.7
VERSION=2.0.9

#wget http://www.akira.ruc.dk/~keld/research/LKH/LKH-$VERSION.tgz
tar xvfz LKH-$VERSION.tgz
cd LKH-$VERSION
make -j 4
