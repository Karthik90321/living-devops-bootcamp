
#!/bin/bash
# sys-monitor.sh — generate a system health report using bash functions
# Usage: ./sys-monitor.sh [output-file]
# If no output file given, prints to stdout

REPORT_FILE="${1:-/dev/stdout}"

# ---------- Functions ----------

print_header() {
    echo "==============================="
    echo " System Monitoring Report"
    echo " Generated: $(date)"
    echo " Host: $(hostname)"
    echo "==============================="
    echo ""
}

system_info() {
    echo "--- System Info ---"
    uname -a
    echo ""
}

cpu_info() {
    echo "--- CPU Info ---"
    echo "Cores: $(nproc)"
    lscpu | grep -E "Model name|Architecture" | sed 's/^[ \t]*//'
    echo ""
}

load_average() {
    echo "--- Load Average ---"
    # uptime output: " 10:30:45 up 2 days, ... load average: 0.52, 0.58, 0.59"
    # awk extracts the three load values
    LOAD=$(uptime | awk -F'load average:' '{print $2}' | sed 's/^ *//')
    echo "Load (1/5/15 min): $LOAD"
    echo ""
}

memory_info() {
    echo "--- Memory Usage ---"
    free -h | grep -E "^Mem|^Swap"
    # Calculate used % using awk
    USED_PCT=$(free | awk '/^Mem/ {printf "%.1f", $3/$2 * 100}')
    echo "Memory used: ${USED_PCT}%"
    echo ""
}

disk_info() {
    echo "--- Disk Usage ---"
    df -h | grep -v -E "tmpfs|devtmpfs|loop"
    echo ""
}

top_processes() {
    echo "--- Top 5 CPU Consumers ---"
    ps aux --sort=-%cpu | head -6 | awk 'NR>1 {print $2, $11, "CPU:"$3"%"}'
    echo ""
    echo "--- Top 5 Memory Consumers ---"
    ps aux --sort=-%mem | head -6 | awk 'NR>1 {print $2, $11, "MEM:"$4"%"}'
    echo ""
}

# ---------- Main ----------

main() {
    print_header
    system_info
    cpu_info
    load_average
    memory_info
    disk_info
    top_processes
    echo "==============================="
    echo "End of report."
}

# Run main, send all output to the report file
main > "$REPORT_FILE"
echo "Report written to: $REPORT_FILE" >&2

