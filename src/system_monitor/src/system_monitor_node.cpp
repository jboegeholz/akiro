#include "rclcpp/rclcpp.hpp"
#include "akiro_interfaces/msg/cpu_load.hpp"
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

struct CpuLoad {
    std::string name;
    unsigned long long user, nice, system, idle, iowait, irq, softirq, steal;

    unsigned long long total() const {
        return user + nice + system + idle + iowait + irq + softirq + steal;
    }
    unsigned long long active() const { return total() - idle - iowait; }
};

class MyNode: public rclcpp::Node
{
public:
    MyNode(): Node("system_monitor")
    {
        RCLCPP_INFO(this->get_logger(), "Hello from System Monitor Node!");

        // Create publisher for CPU load data
        cpu_load_publisher_ = this->create_publisher<akiro_interfaces::msg::CpuLoad>("cpu_load", 10);

        // Initialize previous state
        previous_state_ = read_cpu_times();

        timer_ = this->create_wall_timer(std::chrono::seconds(1),
                                         std::bind(&MyNode::timerCallback, this));
    }
private:
    void timerCallback()
    {
        auto current_state = read_cpu_times();
        if (current_state.empty() || previous_state_.empty()) {
            RCLCPP_ERROR(this->get_logger(), "Failed to read CPU times");
            return;
        }

        // Create CPU load message
        auto cpu_load_msg = akiro_interfaces::msg::CpuLoad();
        cpu_load_msg.header.stamp = this->get_clock()->now();
        cpu_load_msg.header.frame_id = "system";

        // Calculate overall CPU usage (first entry is total)
        if (current_state.size() > 0) {
            const auto& current_total = current_state[0];
            const auto& previous_total = previous_state_[0];

            unsigned long long total_diff = current_total.total() - previous_total.total();
            unsigned long long active_diff = current_total.active() - previous_total.active();

            if (total_diff > 0) {
                cpu_load_msg.cpu_usage_percent = 100.0 * active_diff / total_diff;
            }
        }

        // Set number of cores (excluding the first 'cpu' entry which is total)
        cpu_load_msg.cpu_cores = static_cast<int32_t>(current_state.size() - 1);

        // Calculate per-core usage
        cpu_load_msg.cpu_per_core_usage.clear();
        for (size_t i = 1; i < current_state.size() && i < previous_state_.size(); ++i) {
            const auto& current = current_state[i];
            const auto& previous = previous_state_[i];

            unsigned long long total_diff = current.total() - previous.total();
            unsigned long long active_diff = current.active() - previous.active();

            if (total_diff > 0) {
                double usage_percent = 100.0 * active_diff / total_diff;
                cpu_load_msg.cpu_per_core_usage.push_back(usage_percent);
            }
        }

        // Read load averages from /proc/loadavg
        std::ifstream loadavg_file("/proc/loadavg");
        if (loadavg_file.is_open()) {
            loadavg_file >> cpu_load_msg.load_avg_1min >> cpu_load_msg.load_avg_5min >> cpu_load_msg.load_avg_15min;
            loadavg_file.close();
        }

        // Read CPU frequency from multiple sources
        cpu_load_msg.cpu_frequency_mhz = 0.0; // Default value

        // Try to read current frequency from /sys filesystem first (more accurate)
        std::ifstream freq_file("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq");
        if (freq_file.is_open()) {
            std::string freq_str;
            if (std::getline(freq_file, freq_str)) {
                try {
                    // scaling_cur_freq is in kHz, convert to MHz
                    double freq_khz = std::stod(freq_str);
                    cpu_load_msg.cpu_frequency_mhz = freq_khz / 1000.0;
                    RCLCPP_DEBUG(this->get_logger(), "CPU frequency from scaling_cur_freq: %.2f MHz",
                                cpu_load_msg.cpu_frequency_mhz);
                } catch (const std::exception& e) {
                    RCLCPP_WARN(this->get_logger(), "Failed to parse scaling_cur_freq: %s", e.what());
                }
            }
            freq_file.close();
        } else {
            // Fallback to /proc/cpuinfo
            std::ifstream cpuinfo_file("/proc/cpuinfo");
            std::string line;
            while (std::getline(cpuinfo_file, line)) {
                if (line.find("cpu MHz") != std::string::npos || line.find("clock") != std::string::npos) {
                    size_t pos = line.find(':');
                    if (pos != std::string::npos) {
                        try {
                            std::string freq_part = line.substr(pos + 1);
                            // Remove leading/trailing whitespace
                            freq_part.erase(0, freq_part.find_first_not_of(" \t"));
                            freq_part.erase(freq_part.find_last_not_of(" \t") + 1);
                            cpu_load_msg.cpu_frequency_mhz = std::stod(freq_part);
                            RCLCPP_DEBUG(this->get_logger(), "CPU frequency from cpuinfo: %.2f MHz",
                                        cpu_load_msg.cpu_frequency_mhz);
                            break;
                        } catch (const std::exception& e) {
                            RCLCPP_WARN(this->get_logger(), "Failed to parse cpuinfo frequency: %s", e.what());
                        }
                    }
                }
            }
            cpuinfo_file.close();
        }

        if (cpu_load_msg.cpu_frequency_mhz == 0.0) {
            RCLCPP_WARN_THROTTLE(this->get_logger(), *this->get_clock(), 10000,
                                 "Could not determine CPU frequency");
        }

        // Publish the message
        cpu_load_publisher_->publish(cpu_load_msg);

        // Update previous state for next calculation
        previous_state_ = current_state;
    }

    std::vector<CpuLoad> read_cpu_times() {
        std::vector<CpuLoad> result;
        std::ifstream f("/proc/stat");
        std::string line;
        while (std::getline(f, line)) {
            if (line.rfind("cpu", 0) != 0) break;
            std::istringstream ss(line);
            CpuLoad ct{};
            ss >> ct.name >> ct.user >> ct.nice >> ct.system >> ct.idle
               >> ct.iowait >> ct.irq >> ct.softirq >> ct.steal;
            result.emplace_back(ct);
        }
        return result;
    }

    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<akiro_interfaces::msg::CpuLoad>::SharedPtr cpu_load_publisher_;
    std::vector<CpuLoad> previous_state_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyNode>();

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}