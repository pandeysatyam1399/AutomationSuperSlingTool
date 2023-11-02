#!/bin/bash

# not used 
# Check if at least one argument is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 arg1 arg2 ... argn"
    exit 1
fi

# Run __init__.py with the provided arguments
python ./__init__.py "$@"
