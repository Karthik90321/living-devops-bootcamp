#!/bin/bash
# Demonstrates stdout vs stderr redirection
echo "This goes to stdout"
echo "This goes to stderr" >&2
ls /nonexistent
