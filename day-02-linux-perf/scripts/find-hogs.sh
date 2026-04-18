#!/bin/bash
# Resource Hog Finder — surfaces processes worth investigating
# Part of Living DevOps Bootcamp Day 02

echo "=== Resource Hogs Report ==="
echo "Generated: $(date)"
echo ""

echo "--- Top 5 CPU Hogs ---"
ps aux --sort=-%cpu | head -6 | tail -5
echo ""

echo "--- Top 5 Memory Hogs ---"
ps aux --sort=-%mem | head -6 | tail -5
echo ""

echo "--- Processes in D state (stuck in I/O wait) ---"
D_PROCS=$(ps aux | awk '$8 ~ /D/ {print $0}')
if [ -z "$D_PROCS" ]; then echo "None"; else echo "$D_PROCS"; fi
echo ""

echo "--- Zombie Processes ---"
Z_PROCS=$(ps aux | awk '$8 ~ /Z/ {print $0}')
if [ -z "$Z_PROCS" ]; then echo "None"; else echo "$Z_PROCS"; fi
echo ""

echo "--- Processes with high nice value (deprioritised) ---"
HIGH_NICE=$(ps -eo pid,ni,cmd | awk '$2 > 10 {print $0}')
if [ -z "$HIGH_NICE" ]; then echo "None"; else echo "$HIGH_NICE"; fi
