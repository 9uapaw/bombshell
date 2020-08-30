from typing import List

from numpy import average
import numpy as np
from sklearn.linear_model import LinearRegression

from core.data import ExtractedData
from core.logger import Logger
from core.util import FixedList


class DataSanitizer:
    CHECK_LAST_N = 5
    DEVIATION_THRESHOLD = 0.5

    def __init__(self):
        self._last_ten_data = FixedList(10)

    def sanitize_data(self, data: ExtractedData):
        if len(self._last_ten_data.data) >= self.CHECK_LAST_N:
            self._correct_coords(data)

        self._last_ten_data.append(data)

    def _correct_coords(self, data: ExtractedData):
        last_five_data = self._last_ten_data.last_n(self.CHECK_LAST_N) # type: List[ExtractedData]
        avg_x = average([data.player_position[0] for data in last_five_data])
        avg_y = average([data.player_position[1] for data in last_five_data])
        actual_x = data.player_position[0]
        actual_y = data.player_position[1]

        deviation_x = abs(actual_x - avg_x) / avg_x
        deviation_y = abs(actual_y - avg_y) / avg_y

        if deviation_x > self.DEVIATION_THRESHOLD:
            X = [[data.player_position[1]] for data in last_five_data]
            Y = [[data.player_position[0]] for data in last_five_data]
            predictor = LinearRegression()
            predictor.fit(X, Y)
            new_x = predictor.predict([[data.player_position[1]]])[0][0]
            Logger.info("Correcting coordinate from {} to {}".format(actual_x, new_x))
            data.player_position = (new_x, data.player_position[1])

        if deviation_y > self.DEVIATION_THRESHOLD:
            X = [[data.player_position[0]] for data in last_five_data]
            Y = [[data.player_position[1]] for data in last_five_data]
            predictor = LinearRegression()
            predictor.fit(X, Y)
            new_y = predictor.predict([[data.player_position[0]]])[0][0]
            data.player_position = (data.player_position[0], new_y)

    # def _correct_combat_status(self, data: ExtractedData):
    #
    #
