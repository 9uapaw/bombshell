import json
import signal
import time
from pathlib import Path
from typing import Dict

from core.config import Config, GlobalConfig
from core.logger import Logger
from game.control.control import CharacterController
from game.position.position import Position
from image.extractor import ImageExtractor
from image.screeninterceptor import ScreenInterceptor


class RecordComponent:

    def __init__(self, controller: CharacterController, extractor: ImageExtractor, interceptor: ScreenInterceptor):
        self.screen = interceptor
        self.extractor = extractor
        self.waypoints = {}

    def record(self, record_data: Dict[str, str]):
        self.waypoints = {'format': record_data['wp_format'], 'waypoints': []}

        signal.signal(signal.SIGINT, lambda *args: self.screen.stop_capturing())
        signal.signal(signal.SIGTERM, lambda *args: self.screen.stop_capturing())

        try:
            for screen in self.screen.capture():
                data = self.extractor.extract_data_from_screen(screen)

                current_position = Position(data.player_position[0], data.player_position[1])
                if not self.waypoints['waypoints']:
                    self.waypoints['waypoints'].append(data.player_position)
                else:
                    last_recorded_coordinates = self.waypoints['waypoints'][len(self.waypoints['waypoints']) - 1]
                    last_recorded_position = Position(last_recorded_coordinates[0], last_recorded_coordinates[1])
                    if current_position.calculate_distance_from(last_recorded_position) >= GlobalConfig.config.core.difference_between_two_waypoints:
                        Logger.info('Recording position: ' + str(data.player_position))
                        self.waypoints['waypoints'].append(data.player_position)
        finally:
            Logger.info('Saving file to: {}'.format(record_data.get('waypoint', 'NO PATH')))

            file = Path(record_data['waypoint'])
            if file.is_file():
                self._save_if_file_exist(record_data)
            else:
                self._save_if_file_not_exist(record_data)

    def _save_if_file_exist(self, data: dict):
        with open(data['waypoint'], 'r+') as wp:
            file = json.load(wp)
            if data['wp_type'] in file:
                file[data['wp_type']].append(self.waypoints)
            else:
                file[data['wp_type']] = [self.waypoints]
            wp.seek(0)
            json.dump(file, wp)

    def _save_if_file_not_exist(self, data: dict):
        with open(data['waypoint'], 'w+') as wp:
            file = {data['wp_type']: []}
            file[data['wp_type']].append(self.waypoints)
            json.dump(file, wp)


