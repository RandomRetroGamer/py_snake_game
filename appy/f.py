import json
import os

class fancy:
    @staticmethod
    def read_config(file_path):
        config = {}
        with open(file_path, "r") as file:
            config = json.load(file)
        return config
    @staticmethod
    def write_config(file_path, config_data):
        with open(file_path, "w") as file:
            json.dump(config_data, file, indent=4)
    @staticmethod
    def update_high(file_path, new_score):
        config = fancy.read_config(file_path)

        current_score = fancy.read_config(file_path)
        if new_score > current_score:
            config["high_score"] = new_score
            fancy.write_config(file_path, config)

            print(f"new high score: {new_score}")
        else:
            print(f"current core: {current_score}, new: {new_score}")

class config:
    path = "wind_config.json"

class color:
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

class snake_game:
    snake_speed = 15
    snake_position = [100, 50]

    snake_body = [  [100, 50],
                    [90, 50],
                    [80, 50],
                    [70, 50]
                  ]

    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

    cell_size = 10

