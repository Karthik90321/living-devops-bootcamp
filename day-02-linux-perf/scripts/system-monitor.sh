#!/bin/bash
# System Monitor — quick health snapshot
# Part of Living DevOps Bootcamp Day 02

echo "=============================="
echo " System Monitor Report"
echo " Generated: $(date)"
echo " Host: $(hostname)"
echo "=============================="
echo ""

echo "--- System Load ---"
uptime
echo ""

echo "--- CPU Cores ---"
echo "Cores: $(nproc)"
echo ""

echo "--- Memory Usage ---"
free -h | grep -E "^Mem|^Swap"
echo ""

echo "--- Top 5 CPU Processes ---"
ps aux --sort=-%cpu | head -6 | awk 'NR>1 {print $2, $11, "CPU:"$3"%", "MEM:"$4"%"}'
echo ""

echo "--- Top 5 Memory Processes ---"
ps aux --sort=-%mem | head -6 | awk 'NR>1 {print $2, $11, "CPU:"$3"%", "MEM:"$4"%"}'
echo ""

echo "--- Disk Usage ---"
df -h | grep -v -E "tmpfs|devtmpfs"
echo ""

echo "--- I/O Wait ---"
iostat | awk '/avg-cpu/{getline; print "IOWait: "$4"%"}'
echo ""

echo "=============================="
