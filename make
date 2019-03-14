#!/usr/bin/env python3
"""Run script.
"""
import logging
import os
import shlex
import sys
from typing import List

from clinner.command import Type as CommandType
from clinner.command import command
from clinner.run.main import Main as ClinnerMain

logger = logging.getLogger("cli")

APP_NAME = "goobox-nodes-api"
IMAGE_NAME = f"goobox/{APP_NAME}"
APP_PATH = f"/srv/apps/{APP_NAME}/app"


@command(command_type=CommandType.SHELL, parser_opts={"help": "Build docker image"})
def build(*args, **kwargs) -> List[List[str]]:
    tag = ["-t", f"{kwargs['image']}:{kwargs['tag']}"]
    return [shlex.split(f"docker build") + tag + ["."] + list(args)]


@command(command_type=CommandType.SHELL, parser_opts={"help": "Start docker compose stack"})
def up(*args, **kwargs) -> List[List[str]]:
    return [shlex.split(f"docker-compose up") + list(args)]


@command(command_type=CommandType.SHELL, parser_opts={"help": "Stop docker compose stack"})
def down(*args, **kwargs) -> List[List[str]]:
    return [shlex.split(f"docker-compose down") + list(args)]


@command(command_type=CommandType.SHELL, parser_opts={"help": "Run command through entrypoint"})
def run(*args, testing: bool = False, **kwargs) -> List[List[str]]:
    return [shlex.split(f"docker-compose run {'-e TESTING=true' if testing else ''} api") + list(args)]


@command(
    command_type=CommandType.SHELL,
    args=((("--alone",), {"help": "Run docker container instead of compose", "action": "store_true"}),),
    parser_opts={"help": "Run tests"},
)
def test(*args, **kwargs) -> List[List[str]]:
    return run("pytest", *args, testing=True, **kwargs)


@command(command_type=CommandType.SHELL, parser_opts={"help": "Run lint"})
def lint(*args, **kwargs) -> List[List[str]]:
    return (
        run(*shlex.split("black --check ."), **kwargs)
        + run(*shlex.split("flake8"), **kwargs)
        + run(*shlex.split("isort --check-only"), **kwargs)
    )


class Main(ClinnerMain):
    def add_arguments(self, parser):
        parser.add_argument("-i", "--image", help="Docker image name", default=IMAGE_NAME)
        parser.add_argument("-t", "--tag", help="Docker tag", default="latest")


if __name__ == "__main__":
    sys.exit(Main().run())
