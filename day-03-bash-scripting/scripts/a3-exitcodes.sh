#!/bin/bash
echo "About to run a successful command..."
ls /tmp > /dev/null
echo "Exit code: $?"

echo "About to run a failing command..."
ls /this/path/does/not/exist 2> /dev/null
echo "Exit code: $?"

echo "Now exiting with custom code 42..."
exit 42
