#!/usr/bin/env python3
"""Run script.
"""
import logging.config
import os
import shlex
import sys
from typing import List

import uvicorn
from clinner.command import Type as CommandType
from clinner.command import command
from clinner.run import Main as ClinnerMain
from uvicorn.config import get_logger
from uvicorn.reloaders.statreload import StatReload

APP = "goobox-nodes"

sys.path.insert(0, os.getcwd())


@command(command_type=CommandType.SHELL, parser_opts={"help": "Start server"})
def start(*args, **kwargs) -> List[List[str]]:
    cmd = shlex.split("supervisord -c server/supervisor.ini")
    cmd += list(args)
    return [cmd]


@command(command_type=CommandType.PYTHON, parser_opts={"help": "Start development server"})
def development(*args, **kwargs):
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"}},
            "handlers": {"default": {"level": "DEBUG", "formatter": "standard", "class": "logging.StreamHandler"}},
            "loggers": {
                "goobox_nodes": {"handlers": ["default"], "level": "DEBUG", "propagate": False},
                "nodes": {"handlers": ["default"], "level": "DEBUG", "propagate": False},
            },
        }
    )

    StatReload(get_logger("debug")).run(
        uvicorn.run,
        {
            "app": "goobox_nodes.app:app",
            "host": os.environ["APP_HOST"],
            "port": int(os.environ["APP_PORT"]),
            "debug": True,
        },
    )


@command(command_type=CommandType.SHELL, parser_opts={"help": "Run shell"})
def shell(*args, **kwargs) -> List[List[str]]:
    cmd = shlex.split("ipython")
    cmd += list(args)
    return [cmd]


@command(command_type=CommandType.SHELL, parser_opts={"help": "Run migrations"})
def migrations(*args, **kwargs) -> List[List[str]]:
    cmd = shlex.split("alembic")
    cmd += list(args)
    return [cmd]


class Main(ClinnerMain):
    commands = (
        "clinner.run.commands.black.black",
        "clinner.run.commands.flake8.flake8",
        "clinner.run.commands.isort.isort",
        "clinner.run.commands.pytest.pytest",
        "start",
        "development",
        "shell",
        "migrations",
    )

    def inject_app_settings(self):
        """
        Injecting own settings.
        """
        os.environ.setdefault("APP_HOST", "0.0.0.0")
        os.environ.setdefault("APP_PORT", "8000")
        os.environ.setdefault("STARLETTE_APP", f"{APP}.app:app")
        os.environ.setdefault("ENVIRONMENT", self.args.environment)

    def add_arguments(self, parser):
        parser.add_argument(
            "-e",
            "--environment",
            help="Environment in which to run the application",
            choices=("local", "development", "production"),
            default="local",
        )


def main():
    sys.exit(Main().run())


if __name__ == "__main__":
    main()
