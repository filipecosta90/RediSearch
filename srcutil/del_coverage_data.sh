#!/bin/sh
# Run this from the toplevel directory of the source code tree
COVERAGE_DIR_NAME=coverage

find . -name '*.gcov' -delete
find . -name '*.gcda' -delete
find . -name '*.gcno' -delete
rm -rf ./$COVERAGE_DIR_NAME/*
