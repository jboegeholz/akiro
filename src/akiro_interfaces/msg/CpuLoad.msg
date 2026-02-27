# CPU Load Message
# Contains information about system CPU utilization

# Overall CPU usage as percentage (0.0 to 100.0)
float64 cpu_usage_percent

# Number of CPU cores
int32 cpu_cores

# CPU usage per core as percentage array
float64[] cpu_per_core_usage

# 1, 5, and 15 minute load averages
float64 load_avg_1min
float64 load_avg_5min
float64 load_avg_15min

# CPU frequency in MHz
float64 cpu_frequency_mhz

# RAM total in MB
float64 ram_total_mb

# RAM used in MB
float64 ram_used_mb

# RAM usage as percentage (0.0 to 100.0)
float64 ram_usage_percent

# Header with timestamp and frame information
std_msgs/Header header
