#!/usr/bin/env python3

import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse
from rclpy.action.server import ServerGoalHandle
from my_robot_interfaces.action import CountUntil


class CountUnitlServerNode(Node):
    def __init__(self):
        super().__init__("count_until_server")
        self.count_until_server_ = ActionServer(self, CountUntil, "count_until", goal_callback=self.goal_callback, execute_callback=self.execute_callback)


    def goal_callback(self, goal_request:CountUntil.Goal):
        self.get_logger().info('Received a Goal')

        if goal_request.target_number <= 0:
            self.get_logger().warn('Target number must be greater than 0')
            return GoalResponse.REJECT

        self.get_logger().info('Accepting the Goal')
        return GoalResponse.ACCEPT


    def execute_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info("Starting the Goal Execution")

        # Extract data from the goal
        target_number = goal_handle.request.target_number
        delay = goal_handle.request.delay
        result = CountUntil.Result()
        counter = 0

        self.get_logger().info("Executing the goal")
        # Do the processing/execution
        for i in range(target_number):
            counter +=1
            self.get_logger.inf(f"the current counter value is {counter}")
            time.sleep()


        # Set the final state of the goal (abort/success/cancel)
        goal_handle.succeed()

        # return the result to client
        result.reached_number = counter
        return result

        



def main(args=None):
    rclpy.init(args=args)
    node = CountUnitlServerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()