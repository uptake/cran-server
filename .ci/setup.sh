#!/bin/bash

# configure CI environment

# Failure is a natural part of life
set -e

# Other packages needed for CI tasks
pip install \
    coverage \
    codecov \
    pytest-cov \
    requests
