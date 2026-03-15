import math
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node

try:
    from dynamixel_sdk import COMM_SUCCESS, PacketHandler, PortHandler
except ImportError:  # pragma: no cover - import error is handled at runtime
    COMM_SUCCESS = None
    PacketHandler = None
    PortHandler = None


class OpenRBDriveBot(Node):
    def __init__(self):
        super().__init__("openrb_drive_bot")

        if PacketHandler is None or PortHandler is None:
            raise RuntimeError(
                "dynamixel_sdk nicht gefunden. Installiere z.B. python3-dynamixel-sdk "
                "oder `pip install dynamixel-sdk`."
            )

        self.port_name = self.declare_parameter("port", "/dev/ttyACM0").value
        self.baud_rate = int(self.declare_parameter("baud_rate", 57600).value)
        self.protocol_version = float(self.declare_parameter("protocol_version", 2.0).value)

        self.left_motor_id = int(self.declare_parameter("left_motor_id", 1).value)
        self.right_motor_id = int(self.declare_parameter("right_motor_id", 2).value)

        self.wheel_radius_m = float(self.declare_parameter("wheel_radius_m", 0.05).value)
        self.wheel_base_m = float(self.declare_parameter("wheel_base_m", 0.2).value)
        self.velocity_unit_rpm = float(self.declare_parameter("velocity_unit_rpm", 0.229).value)
        self.max_rpm = float(self.declare_parameter("max_rpm", 120.0).value)
        self.invert_left = bool(self.declare_parameter("invert_left", False).value)
        self.invert_right = bool(self.declare_parameter("invert_right", False).value)

        self.cmd_vel_topic = self.declare_parameter("cmd_vel_topic", "/cmd_vel").value
        self.cmd_timeout_sec = float(self.declare_parameter("cmd_timeout_sec", 0.5).value)
        self.stop_on_shutdown = bool(self.declare_parameter("stop_on_shutdown", True).value)
        self.disable_torque_on_shutdown = bool(
            self.declare_parameter("disable_torque_on_shutdown", False).value
        )

        self.addr_operating_mode = int(self.declare_parameter("addr_operating_mode", 11).value)
        self.addr_torque_enable = int(self.declare_parameter("addr_torque_enable", 64).value)
        self.addr_velocity_limit = int(self.declare_parameter("addr_velocity_limit", 44).value)
        self.addr_goal_velocity = int(self.declare_parameter("addr_goal_velocity", 104).value)
        self.velocity_mode_value = int(self.declare_parameter("velocity_mode_value", 1).value)
        self.max_raw_velocity_fallback = int(
            self.declare_parameter("max_raw_velocity_fallback", 1023).value
        )

        self.port_handler = PortHandler(self.port_name)
        self.packet_handler = PacketHandler(self.protocol_version)
        self.velocity_limit_raw_by_id = {}
        self.last_write_error_log_time = 0.0
        self.last_velocity_clamp_log_time = 0.0

        self._open_port()
        self._configure_motor(self.left_motor_id)
        self._configure_motor(self.right_motor_id)

        self.subscription = self.create_subscription(
            Twist, self.cmd_vel_topic, self._on_cmd_vel, 10
        )

        self.last_cmd_time = time.monotonic()
        self.timeout_triggered = False
        self.timeout_timer = self.create_timer(0.05, self._watchdog_timeout)

        self.get_logger().info(
            "OpenRB-150 verbunden auf "
            f"{self.port_name}@{self.baud_rate}, Motoren IDs {self.left_motor_id}/{self.right_motor_id}"
        )

    def _open_port(self):
        if not self.port_handler.openPort():
            raise RuntimeError(f"Serieller Port konnte nicht geoeffnet werden: {self.port_name}")
        if not self.port_handler.setBaudRate(self.baud_rate):
            raise RuntimeError(f"Baudrate konnte nicht gesetzt werden: {self.baud_rate}")

    def _configure_motor(self, motor_id: int):
        model_number, comm_result, dxl_error = self.packet_handler.ping(self.port_handler, motor_id)
        self._check_comm_result(comm_result, dxl_error, f"Ping DXL ID {motor_id}")
        self.get_logger().info(f"DXL ID {motor_id} gefunden (Model: {model_number})")

        self._write_u8(motor_id, self.addr_torque_enable, 0, "Torque Off")
        self._write_u8(
            motor_id,
            self.addr_operating_mode,
            self.velocity_mode_value,
            "Set Velocity Mode",
        )
        self._write_u8(motor_id, self.addr_torque_enable, 1, "Torque On")

        velocity_limit_raw = self._read_u32(
            motor_id, self.addr_velocity_limit, "Read Velocity Limit"
        )
        if velocity_limit_raw <= 0:
            velocity_limit_raw = self.max_raw_velocity_fallback
            self.get_logger().warn(
                f"DXL ID {motor_id}: ungueltiges Velocity Limit gelesen, nutze Fallback "
                f"{self.max_raw_velocity_fallback}."
            )
        self.velocity_limit_raw_by_id[motor_id] = velocity_limit_raw
        self.get_logger().info(f"DXL ID {motor_id}: Velocity Limit raw = {velocity_limit_raw}")

    def _check_comm_result(self, comm_result: int, dxl_error: int, context: str):
        if comm_result != COMM_SUCCESS:
            raise RuntimeError(
                f"{context} fehlgeschlagen: {self.packet_handler.getTxRxResult(comm_result)}"
            )
        if dxl_error != 0:
            raise RuntimeError(
                f"{context} meldet DXL Fehler: {self.packet_handler.getRxPacketError(dxl_error)}"
            )

    def _write_u8(self, motor_id: int, address: int, value: int, context: str):
        comm_result, dxl_error = self.packet_handler.write1ByteTxRx(
            self.port_handler, motor_id, address, value
        )
        self._check_comm_result(comm_result, dxl_error, f"{context} (ID={motor_id}, addr={address})")

    def _write_u32(self, motor_id: int, address: int, value: int, context: str):
        comm_result, dxl_error = self.packet_handler.write4ByteTxRx(
            self.port_handler, motor_id, address, value
        )
        self._check_comm_result(comm_result, dxl_error, f"{context} (ID={motor_id}, addr={address})")

    def _read_u32(self, motor_id: int, address: int, context: str) -> int:
        value, comm_result, dxl_error = self.packet_handler.read4ByteTxRx(
            self.port_handler, motor_id, address
        )
        self._check_comm_result(comm_result, dxl_error, f"{context} (ID={motor_id}, addr={address})")
        return int(value)

    def _twist_to_rpm(self, linear_x: float, angular_z: float):
        left_mps = linear_x - angular_z * (self.wheel_base_m / 2.0)
        right_mps = linear_x + angular_z * (self.wheel_base_m / 2.0)

        left_rpm = (left_mps / (2.0 * math.pi * self.wheel_radius_m)) * 60.0
        right_rpm = (right_mps / (2.0 * math.pi * self.wheel_radius_m)) * 60.0
        return left_rpm, right_rpm

    def _limit_and_invert(self, rpm: float, invert: bool) -> float:
        if invert:
            rpm = -rpm
        return max(min(rpm, self.max_rpm), -self.max_rpm)

    def _rpm_to_raw_velocity(self, rpm: float) -> int:
        return int(round(rpm / self.velocity_unit_rpm))

    def _clamp_raw_velocity(self, motor_id: int, raw_velocity: int) -> int:
        velocity_limit_raw = self.velocity_limit_raw_by_id.get(
            motor_id, self.max_raw_velocity_fallback
        )
        clamped = max(min(raw_velocity, velocity_limit_raw), -velocity_limit_raw)
        if clamped != raw_velocity and (time.monotonic() - self.last_velocity_clamp_log_time) > 1.0:
            self.get_logger().warn(
                f"DXL ID {motor_id}: Goal Velocity {raw_velocity} auf {clamped} begrenzt "
                f"(Limit: +/-{velocity_limit_raw})."
            )
            self.last_velocity_clamp_log_time = time.monotonic()
        return clamped

    def _to_u32(self, signed_value: int) -> int:
        return signed_value & 0xFFFFFFFF

    def _send_goal_velocity(self, motor_id: int, rpm: float):
        raw_goal_signed = self._rpm_to_raw_velocity(rpm)
        raw_goal_signed = self._clamp_raw_velocity(motor_id, raw_goal_signed)
        raw_goal_u32 = self._to_u32(raw_goal_signed)
        self._write_u32(motor_id, self.addr_goal_velocity, raw_goal_u32, "Write Goal Velocity")

    def _send_wheel_rpms(self, left_rpm: float, right_rpm: float):
        left_rpm = self._limit_and_invert(left_rpm, self.invert_left)
        right_rpm = self._limit_and_invert(right_rpm, self.invert_right)
        self._send_goal_velocity(self.left_motor_id, left_rpm)
        self._send_goal_velocity(self.right_motor_id, right_rpm)

    def _on_cmd_vel(self, msg: Twist):
        left_rpm, right_rpm = self._twist_to_rpm(msg.linear.x, msg.angular.z)
        try:
            self._send_wheel_rpms(left_rpm, right_rpm)
        except Exception as exc:
            now = time.monotonic()
            if now - self.last_write_error_log_time > 0.5:
                self.get_logger().error(f"DXL Schreibfehler bei cmd_vel: {exc}")
                self.last_write_error_log_time = now
            return
        self.last_cmd_time = time.monotonic()
        self.timeout_triggered = False

    def _watchdog_timeout(self):
        if self.cmd_timeout_sec <= 0.0:
            return

        if time.monotonic() - self.last_cmd_time <= self.cmd_timeout_sec:
            return

        if self.timeout_triggered:
            return

        self.get_logger().warn(
            f"Kein cmd_vel fuer {self.cmd_timeout_sec:.2f}s erhalten, stoppe Motoren."
        )
        try:
            self._send_wheel_rpms(0.0, 0.0)
        except Exception as exc:
            self.get_logger().error(f"DXL Schreibfehler beim Timeout-Stop: {exc}")
        self.timeout_triggered = True

    def destroy_node(self):
        try:
            if self.stop_on_shutdown:
                self._send_wheel_rpms(0.0, 0.0)
            if self.disable_torque_on_shutdown:
                self._write_u8(self.left_motor_id, self.addr_torque_enable, 0, "Torque Off")
                self._write_u8(self.right_motor_id, self.addr_torque_enable, 0, "Torque Off")
        except Exception as exc:  # pragma: no cover - best effort during shutdown
            self.get_logger().warn(f"Shutdown cleanup fehlgeschlagen: {exc}")
        finally:
            try:
                self.port_handler.closePort()
            except Exception:  # pragma: no cover - best effort during shutdown
                pass
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = OpenRBDriveBot()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
