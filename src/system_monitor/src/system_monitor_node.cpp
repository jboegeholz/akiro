#include "rclcpp/rclcpp.hpp"
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

        // Calculate CPU usage based on difference between measurements
        for (size_t i = 0; i < current_state.size() && i < previous_state_.size(); ++i) {
            const auto& current = current_state[i];
            const auto& previous = previous_state_[i];

            unsigned long long total_diff = current.total() - previous.total();
            unsigned long long active_diff = current.active() - previous.active();

            if (total_diff > 0) {
                double usage_percent = 100.0 * active_diff / total_diff;
                RCLCPP_INFO(this->get_logger(), "%s: Usage %.2f%%",
                           current.name.c_str(), usage_percent);
            }
        }

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