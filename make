#!/usr/bin/env python3
"""Run script.
"""
import logging
import os
import shlex
import shutil
import subprocess
import sys
from time import sleep
from typing import List

logger = logging.getLogger("cli")

try:
    from clinner.command import Type, command
    from clinner.run import Main
except Exception:
    logger.error("Package clinner is not installed, run 'pip install clinner' to install it")
    sys.exit(1)

try:
    import jinja2

    templates = jinja2.Environment(loader=jinja2.FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True)
except Exception:
    logger.error("Package jinja2 is not installed, run 'pip install jinja2' to install it")
    sys.exit(1)


APP = "goobox-nodes"
IMAGE = f"goobox/{APP}"
APP_PATH = f"/srv/apps/{APP}/app"


@command(
    command_type=Type.PYTHON,
    args=(
        (("-t", "--tag"), {"help": "Docker image tag", "default": f"{IMAGE}:latest"}),
        (("-p", "--production"), {"help": "Build production image", "action": "store_true"}),
    ),
    parser_opts={"help": "Build docker image"},
)
def build(*args, **kwargs):
    context = {
        "from_image": "python:3.7-slim",
        "labels": ['maintainer="GooBox <perdy@perdy.io>"'],
        "project": APP,
        "app": APP.replace("-", "_"),
        "runtime_packages": ["supervisor", "nginx"],
        "build_packages": ["build-essential"],
        "production": kwargs["production"],
    }

    dockerfile = templates.get_template("Dockerfile.j2").render(**context)
    logger.debug("---- Dockerfile ----\n%s\n--------------------", dockerfile)
    subprocess.run(shlex.split(f"docker build -t {kwargs['tag']} -f- .") + list(args), input=dockerfile.encode("utf-8"))


@command(command_type=Type.PYTHON, parser_opts={"help": "Clean directory"})
def clean(*args, **kwargs):
    if os.getuid() != 0:
        logger.error("It is necessary to call clean with sudo")
        return None

    for path in (".pytest_cache", ".coverage", "test-results", "uvicorn.pid"):
        try:
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
            logger.info("Removed successfully: %s", path)
        except Exception:
            logger.error("Cannot remove: %s", path)


@command(command_type=Type.SHELL, parser_opts={"help": "Start docker compose stack"})
def up(*args, **kwargs) -> List[List[str]]:
    return [shlex.split(f"docker-compose up") + list(args)]


@command(command_type=Type.SHELL, parser_opts={"help": "Stop docker compose stack"})
def down(*args, **kwargs) -> List[List[str]]:
    return [shlex.split(f"docker-compose down") + list(args)]


@command(
    command_type=Type.SHELL,
    args=((("--compose",), {"help": "Docker compose file", "default": "docker-compose.yml"}),),
    parser_opts={"help": "Run command through entrypoint"},
)
def run(*args, **kwargs) -> List[List[str]]:
    environment = " ".join([f"-e {i}" for i in kwargs["environment"]])

    if kwargs["alone"]:
        return [shlex.split(f"docker run {environment} {IMAGE}") + list(args)]
    else:
        return [
            shlex.split(f"docker-compose -f {kwargs['compose']} pull --ignore-pull-failures"),
            shlex.split(f"docker-compose -f {kwargs['compose']} run {environment} api") + list(args),
        ]


@command(command_type=Type.SHELL, parser_opts={"help": "Black code formatting"})
def black(*args, **kwargs):
    kwargs["alone"] = True
    return run("black", *args, **kwargs)


@command(command_type=Type.SHELL, parser_opts={"help": "Flake8 code analysis"})
def flake8(*args, **kwargs):
    kwargs["alone"] = True
    return run("flake8", *args, **kwargs)


@command(command_type=Type.SHELL, parser_opts={"help": "Isort imports formatting"})
def isort(*args, **kwargs):
    kwargs["alone"] = True
    return run("isort", *args, **kwargs)


@command(command_type=Type.SHELL, parser_opts={"help": "Run lint"})
def lint(*args, **kwargs) -> List[List[str]]:
    return black("--check", ".", **kwargs) + flake8(**kwargs) + isort("--check-only", **kwargs)


@command(command_type=Type.SHELL, parser_opts={"help": "Run tests"})
def test(*args, **kwargs) -> List[List[str]]:
    if not kwargs["alone"]:
        sleep(5)
        kwargs["compose"] = "docker-compose-testing.yml"

    kwargs["environment"].append("TESTING=true")
    return run("pytest", *args, **kwargs)


class Make(Main):
    def add_arguments(self, parser):
        parser.add_argument("--alone", help="Run app container alone", action="store_true")
        parser.add_argument("-e", "--environment", help="Environment variable", action="append", default=[])


if __name__ == "__main__":
    sys.exit(Make().run())
