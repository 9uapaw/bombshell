from etc.const import TURN_THRESHOLD
from game.character import Character
from game.control.control import CharacterController
from game.position.position import Position, Trajectory, Direction, CharacterDirection
from game.position.transform import calculate_trajectory, transform_turn
import matplotlib.pyplot as plt


class PositionFollower:

    def __init__(self, controller: CharacterController):
        self.controller = controller

    def move_to(self, character: Character, waypoint: Position):
        self.turn_to(CharacterDirection(character.position, character.facing), waypoint)
        if not character.is_moving:
            self.controller.move_forward()
            character.is_moving = True

    def turn_to(self, char_direction: CharacterDirection, waypoint: Position) -> (float, Direction) or None:
        current_trajectory = calculate_trajectory(char_direction.position, char_direction.facing)
        waypoint_trajectory = Trajectory(char_direction.position, waypoint)

        angle_difference, direction = current_trajectory.calculate_turn(waypoint_trajectory)
        self._show_on_plot(current_trajectory, waypoint_trajectory)

        if angle_difference <= TURN_THRESHOLD:
            return None

        print('Angle: {} - Direction: {}'.format(angle_difference, direction))

        if direction == Direction.left:
            self.controller.turn_left(transform_turn(angle_difference))
        else:
            self.controller.turn_right(transform_turn(angle_difference))

        return angle_difference, direction

    def _show_on_plot(self, current_trajectory: Trajectory, waypoint_trajectory: Trajectory):
        x1, y1 = [current_trajectory.start_point[0], current_trajectory.end_point[0]], [current_trajectory.start_point[1], current_trajectory.end_point[1]]
        x2, y2 = [waypoint_trajectory.start_point[0], waypoint_trajectory.end_point[0]], [waypoint_trajectory.start_point[1], waypoint_trajectory.end_point[1]]
        ax1, ax2 = [x1[0] - 2, x1[1] + 2], [y1[0], y1[0]]
        ay1, ay2 = [x1[0], x1[0]], [y1[0] + 2, y1[0] - 2]

        plt.plot(x1, y1, x2, y2, marker='o')
        plt.plot(ax1, ax2, ay1, ay2, color='black', marker='^')
        plt.grid()

        plt.show()
