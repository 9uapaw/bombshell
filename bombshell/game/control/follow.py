import time

from etc.const import TURN_THRESHOLD, WAYPOINT_DIFFERENCE_THRESHOLD
from game.character.character import Character
from game.control.control import CharacterController
from game.position.position import Position, Trajectory, Direction, CharacterDirection
from game.position.transform import calculate_trajectory, transform_turn
import matplotlib.pyplot as plt

from game.position.waypoint import PositionStorage


class PositionFollower:

    def __init__(self, controller: CharacterController, waypoints: PositionStorage):
        self.controller = controller
        self.waypoints = waypoints

    def move(self, character: Character):
        print("Following waypoint {} out of {}. Character is currently moving: {}".format(character.current_waypoint, len(self.waypoints.waypoints) - 1, character.is_moving))
        if character.position.is_close_to(self.waypoints.waypoints[character.current_waypoint],
                                          WAYPOINT_DIFFERENCE_THRESHOLD):
            print("Close to waypoint")
            self.controller.stop()
            character.is_moving = False

            if character.current_waypoint == len(self.waypoints.waypoints):
                character.current_waypoint = 0
            else:
                character.current_waypoint += 1

        if not self.turn(character):
            if not character.is_moving:
                print('Moving')
                self.controller.move_forward()
                character.switch_moving()

    def turn(self, character: Character) -> (float, Direction) or None:
        current_trajectory = calculate_trajectory(character.position, character.facing)
        waypoint_trajectory = Trajectory(character.position, self.waypoints.peek(character.current_waypoint))

        angle_difference, direction = current_trajectory.calculate_turn(waypoint_trajectory)
        # self._show_on_plot(current_trajectory, waypoint_trajectory)

        if angle_difference <= TURN_THRESHOLD:
            return None

        if character.is_moving:
            self.controller.stop()
            character.switch_moving()

        print('Current angle: {}'.format(character.facing))
        print('Waypoint: {} - {} rad on the {}'.format(waypoint_trajectory.end_point, angle_difference, direction.name))

        if direction == Direction.left:
            self.controller.turn_left(transform_turn(angle_difference))
        else:
            self.controller.turn_right(transform_turn(angle_difference))

        return angle_difference, direction

    def _show_on_plot(self, current_trajectory: Trajectory, waypoint_trajectory: Trajectory):
        plt.clf()
        x1, y1 = [current_trajectory.start_point[0], current_trajectory.end_point[0]], [current_trajectory.start_point[1], current_trajectory.end_point[1]]
        x2, y2 = [waypoint_trajectory.start_point[0], waypoint_trajectory.end_point[0]], [waypoint_trajectory.start_point[1], waypoint_trajectory.end_point[1]]
        ax1, ax2 = [x1[0] - 2, x1[1] + 2], [y1[0], y1[0]]
        ay1, ay2 = [x1[0], x1[0]], [y1[0] + 2, y1[0] - 2]

        plt.plot(x1, y1, x2, y2, marker='o')
        plt.plot(ax1, ax2, ay1, ay2, color='black', marker='^')
        plt.grid()

        # plt.show()
        plt.draw()
        plt.pause(0.01)
