#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>

#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/segmentation/sac_segmentation.h>

class PlaneSegmentation : public rclcpp::Node
{
public:
  PlaneSegmentation() : Node("plane_segmentation")
  {
    subscription_ = this->create_subscription<sensor_msgs::msg::PointCloud2>(
      "/voxel_points",
      10,
    	[this](sensor_msgs::msg::PointCloud2::SharedPtr msg) {
        this->callback(msg);
    	}
    );

    plane_pub_ = this->create_publisher<sensor_msgs::msg::PointCloud2>("plane_points", 10);
    objects_pub_ = this->create_publisher<sensor_msgs::msg::PointCloud2>("objects_points", 10);
    RCLCPP_INFO(this->get_logger(), "Plane Segmentation Node started.");
  }

private:
  void callback(const sensor_msgs::msg::PointCloud2::SharedPtr msg)
  {
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
    pcl::fromROSMsg(*msg, *cloud);

    if (cloud->empty())
      return;

    // RANSAC Plane Segmentation
    pcl::SACSegmentation<pcl::PointXYZ> seg;
    pcl::PointIndices::Ptr inliers(new pcl::PointIndices);
    pcl::ModelCoefficients::Ptr coefficients(new pcl::ModelCoefficients);

    seg.setOptimizeCoefficients(true);
    seg.setModelType(pcl::SACMODEL_PLANE);
    seg.setMethodType(pcl::SAC_RANSAC);
    seg.setDistanceThreshold(0.01);
    seg.setInputCloud(cloud);
    seg.segment(*inliers, *coefficients);

    if (inliers->indices.empty())
    {
      RCLCPP_WARN(this->get_logger(), "No plane found.");
      return;
    }

    pcl::ExtractIndices<pcl::PointXYZ> extract;
    extract.setInputCloud(cloud);
    extract.setIndices(inliers);

    // Plane points
    pcl::PointCloud<pcl::PointXYZ>::Ptr plane(new pcl::PointCloud<pcl::PointXYZ>);
    extract.setNegative(false);
    extract.filter(*plane);

    // Remaining object points
    pcl::PointCloud<pcl::PointXYZ>::Ptr objects(new pcl::PointCloud<pcl::PointXYZ>);
    extract.setNegative(true);
    extract.filter(*objects);

    sensor_msgs::msg::PointCloud2 plane_msg;
    pcl::toROSMsg(*plane, plane_msg);
    plane_msg.header = msg->header;
    plane_pub_->publish(plane_msg);

    sensor_msgs::msg::PointCloud2 objects_msg;
    pcl::toROSMsg(*objects, objects_msg);
    objects_msg.header = msg->header;
    objects_pub_->publish(objects_msg);
  }

  rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr subscription_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr plane_pub_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr objects_pub_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PlaneSegmentation>());
  rclcpp::shutdown();
  return 0;
}
