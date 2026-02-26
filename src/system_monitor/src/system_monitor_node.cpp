#include "rclcpp/rclcpp.hpp"
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

struct CpuLoad {
    std::string name;        // "cpu", "cpu0", "cpu1", …
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
        timer_ = this->create_wall_timer(std::chrono::seconds(1), 
                                         std::bind(&MyNode::timerCallback, this));
    }
private:
    void timerCallback()
    {
        auto current_state = read_cpu_times();
        if (current_state.empty()) {
            RCLCPP_ERROR(this->get_logger(), "Failed to read CPU times");
            return;
        }
        for (const auto &ct : current_state) {
            RCLCPP_INFO(this->get_logger(), "%s: Active %.2f%%", ct.name.c_str(), 100.0 * ct.active() / ct.total());
        }
    }
    std::vector<CpuLoad> read_cpu_times() {
        std::vector<CpuLoad> result;
        std::ifstream f("/proc/stat");
        std::string line;
        while (std::getline(f, line)) {
            if (line.rfind("cpu", 0) != 0) break;          // lines stop starting with "cpu"
            std::istringstream ss(line);
            CpuLoad ct{};
            ss >> ct.name >> ct.user >> ct.nice >> ct.system >> ct.idle
               >> ct.iowait >> ct.irq >> ct.softirq >> ct.steal;
            result.emplace_back(ct);
        }
        return result;
    }
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyNode>();

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}