#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>

#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl/search/kdtree.h>
#include <pcl/segmentation/extract_clusters.h>

class EuclideanClusterNode : public rclcpp::Node
{
public:
  EuclideanClusterNode() : Node("euclidean_cluster")
  {
    // Declare parameters with defaults
    this->declare_parameter("cluster_tolerance", 0.02);
    this->declare_parameter("min_cluster_size", 100);
    this->declare_parameter("max_cluster_size", 25000);

    cluster_tolerance_ = this->get_parameter("cluster_tolerance").as_double();
    min_cluster_size_ = this->get_parameter("min_cluster_size").as_int();
    max_cluster_size_ = this->get_parameter("max_cluster_size").as_int();

    subscription_ = this->create_subscription<sensor_msgs::msg::PointCloud2>(
      "objects_points",
      10,
      [this](sensor_msgs::msg::PointCloud2::SharedPtr msg) {
        this->callback(msg);
      }
    );

    clusters_pub_ = this->create_publisher<sensor_msgs::msg::PointCloud2>("clustered_points", 10);

    RCLCPP_INFO(this->get_logger(),
      "Euclidean Cluster Node started (tolerance=%.3f, min=%d, max=%d).",
      cluster_tolerance_, min_cluster_size_, max_cluster_size_);
  }

private:
  void callback(const sensor_msgs::msg::PointCloud2::SharedPtr msg)
  {
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
    pcl::fromROSMsg(*msg, *cloud);

    if (cloud->empty())
      return;

    // KdTree for nearest-neighbor search
    pcl::search::KdTree<pcl::PointXYZ>::Ptr tree(new pcl::search::KdTree<pcl::PointXYZ>);
    tree->setInputCloud(cloud);

    // Euclidean Cluster Extraction
    std::vector<pcl::PointIndices> cluster_indices;
    pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
    ec.setClusterTolerance(cluster_tolerance_);
    ec.setMinClusterSize(min_cluster_size_);
    ec.setMaxClusterSize(max_cluster_size_);
    ec.setSearchMethod(tree);
    ec.setInputCloud(cloud);
    ec.extract(cluster_indices);

    if (cluster_indices.empty())
    {
      RCLCPP_WARN(this->get_logger(), "No clusters found.");
      return;
    }

    RCLCPP_INFO(this->get_logger(), "Found %zu clusters.", cluster_indices.size());

    // Combine all clusters into one colored cloud for visualization
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr colored_cloud(new pcl::PointCloud<pcl::PointXYZRGB>);

    // Generate distinct colors per cluster
    int cluster_id = 0;
    for (const auto & indices : cluster_indices)
    {
      uint8_t r = static_cast<uint8_t>((cluster_id * 97 + 50) % 256);
      uint8_t g = static_cast<uint8_t>((cluster_id * 53 + 130) % 256);
      uint8_t b = static_cast<uint8_t>((cluster_id * 151 + 80) % 256);

      for (const auto & idx : indices.indices)
      {
        pcl::PointXYZRGB point;
        point.x = (*cloud)[idx].x;
        point.y = (*cloud)[idx].y;
        point.z = (*cloud)[idx].z;
        point.r = r;
        point.g = g;
        point.b = b;
        colored_cloud->push_back(point);
      }
      cluster_id++;
    }

    sensor_msgs::msg::PointCloud2 output_msg;
    pcl::toROSMsg(*colored_cloud, output_msg);
    output_msg.header = msg->header;
    clusters_pub_->publish(output_msg);
  }

  rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr subscription_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr clusters_pub_;

  double cluster_tolerance_;
  int min_cluster_size_;
  int max_cluster_size_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<EuclideanClusterNode>());
  rclcpp::shutdown();
  return 0;
}
