#!/bin/sh
g++ capture.cpp -o capture `pkg-config --libs --cflags opencv` -ldl
