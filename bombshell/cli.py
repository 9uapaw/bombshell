import logging
import sys

import click

from core.config import GlobalConfig
from core.game_loop import GameLoop


@click.command()
@click.argument('path')
@click.option("--meta", default="grind", help="Waypoint type(grind, vendor, ghost)")
@click.option("--format", default="circle", help="Waypoint format(circle, line)")
def record_waypoint(path: str, meta: str, format: str):
    game_loop = GameLoop(GlobalConfig.config)

    game_loop.record_waypoints({"wp_type": meta, "wp_format": format, "waypoint": path})


@click.command()
@click.argument('config')
def start(config: str):
    GlobalConfig.load_from_file(config)

    game_loop = GameLoop(GlobalConfig.config)
    game_loop.start()


@click.group()
@click.option("--debug", is_flag=True, help="Set this for verbose log messages")
def main(debug: bool):
    if debug:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)


main.add_command(start)
main.add_command(record_waypoint)


if __name__ == "__main__":
    main()