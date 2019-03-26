#!/usr/bin/env python3
"""Run script.
"""
import logging
import shlex
import shutil
import sys
from typing import List

logger = logging.getLogger("cli")

try:
    from clinner.command import Type, command
    from clinner.run import Main
except Exception:
    logger.error("Package clinner is not installed, run 'pip install clinner' to install it")
    sys.exit(-1)


APP_NAME = "goobox-nodes"
IMAGE_NAME = f"goobox/{APP_NAME}"
APP_PATH = f"/srv/apps/{APP_NAME}/app"


@command(command_type=Type.SHELL, parser_opts={"help": "Build docker image"})
def build(*args, **kwargs) -> List[List[str]]:
    tag = ["-t", f"{kwargs['image']}:{kwargs['tag']}"]
    return [shlex.split(f"docker build") + tag + ["."] + list(args)]


@command(command_type=Type.PYTHON, parser_opts={"help": "Clean directory"})
def clean(*args, **kwargs):
    for path in (".pytest_cache", ".coverage", "test-results"):
        shutil.rmtree(path, ignore_errors=True)


@command(command_type=Type.SHELL, parser_opts={"help": "Start docker compose stack"})
def up(*args, **kwargs) -> List[List[str]]:
    return [shlex.split(f"docker-compose up") + list(args)]


@command(command_type=Type.SHELL, parser_opts={"help": "Stop docker compose stack"})
def down(*args, **kwargs) -> List[List[str]]:
    return [shlex.split(f"docker-compose down") + list(args)]


@command(command_type=Type.SHELL, parser_opts={"help": "Run command through entrypoint"})
def run(*args, testing: bool = False, **kwargs) -> List[List[str]]:
    return [shlex.split(f"docker-compose run {'-e TESTING=true' if testing else ''} api") + list(args)]


@command(command_type=Type.SHELL, parser_opts={"help": "Black code formatting"})
def black(*args, **kwargs):
    return run("black", *args)


@command(command_type=Type.SHELL, parser_opts={"help": "Flake8 code analysis"})
def flake8(*args, **kwargs):
    return run("flake8", *args)


@command(command_type=Type.SHELL, parser_opts={"help": "Isort imports formatting"})
def isort(*args, **kwargs):
    return run("isort", *args)


@command(command_type=Type.SHELL, parser_opts={"help": "Run lint"})
def lint(*args, **kwargs) -> List[List[str]]:
    return black("--check", ".") + flake8() + isort("--check-only")


@command(
    command_type=Type.SHELL,
    args=((("--alone",), {"help": "Run docker container instead of compose", "action": "store_true"}),),
    parser_opts={"help": "Run tests"},
)
def test(*args, **kwargs) -> List[List[str]]:
    return run("pytest", *args, testing=True, **kwargs)


class Make(Main):
    def add_arguments(self, parser):
        parser.add_argument("-i", "--image", help="Docker image name", default=IMAGE_NAME)
        parser.add_argument("-t", "--tag", help="Docker tag", default="latest")


if __name__ == "__main__":
    sys.exit(Make().run())
