#!/bin/sh
# Run this from the toplevel directory of the source code tree
COVERAGE_DIR_NAME=coverage

mkdir -p ./$COVERAGE_DIR_NAME/
cd ./$COVERAGE_DIR_NAME/

gcovr -r ../src/ --object-directory=../build-compat/CMakeFiles/rscore.dir/src/ --html --html-details -o coverage.html
