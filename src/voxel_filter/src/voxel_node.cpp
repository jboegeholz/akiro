#include <memory>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>

#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl/filters/voxel_grid.h>

class VoxelFilterNode : public rclcpp::Node
{
public:
    VoxelFilterNode() : Node("voxel_filter_node")
    {
        this->declare_parameter("leaf_size", 0.005);

        subscription_ = this->create_subscription<sensor_msgs::msg::PointCloud2>(
          "/kinect/points",
          10,
          [this](const sensor_msgs::msg::PointCloud2::SharedPtr msg) {callback(msg);}
          );

        publisher_ = this->create_publisher<sensor_msgs::msg::PointCloud2>(
          "/voxel_points", 10);

        RCLCPP_INFO(this->get_logger(), "Voxel Filter Node started.");
    }

private:
    void callback(const sensor_msgs::msg::PointCloud2::SharedPtr msg) const
    {
        const float leaf_size = static_cast<float>(this->get_parameter("leaf_size").as_double());

        const auto cloud = std::make_shared<pcl::PointCloud<pcl::PointXYZ>>();
        pcl::fromROSMsg(*msg, *cloud);

        if (cloud->empty())
            return;

        const auto filtered = std::make_shared<pcl::PointCloud<pcl::PointXYZ>>();

        pcl::VoxelGrid<pcl::PointXYZ> voxel_filter;
        voxel_filter.setInputCloud(cloud);
        voxel_filter.setLeafSize(leaf_size, leaf_size, leaf_size);
        voxel_filter.filter(*filtered);

        sensor_msgs::msg::PointCloud2 output;
        pcl::toROSMsg(*filtered, output);
        output.header = msg->header;

        publisher_->publish(output);
    }

    rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr subscription_;
    rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr publisher_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<VoxelFilterNode>());
    rclcpp::shutdown();
    return 0;
}
