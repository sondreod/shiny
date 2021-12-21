import subprocess
from typing import Iterable
from io import BytesIO
from getpass import getpass
import os

PYTHON_V = "python3.9"

APT_PACKAGES = [
    "apt",
    "vim",
    "git",
    "ssh",
    "binutils",
    PYTHON_V,
    "python3-pip",
    PYTHON_V + "-venv",
]

PIP_PACKAGES = ["numpy", "matplotlib", "pipx"]
PIPX_PACKAGES = ["black", "tox"]

pw = bytes(getpass().encode("utf-8"))


def run_command(command, sudo=False, username="ubuntu"):

    if sudo:
        command = f"sudo -S {command}"
    print(command)
    options = {}
    if sudo:
        options["input"] = pw
    cp = subprocess.run(command, capture_output=True, shell=True, **options)
    stdout = cp.stdout.decode("utf-8")
    if cp.returncode != 0:
        raise RuntimeError(
            f"Shit just got real. \nSTDOUT:{cp.stdout}\nSTDERR:{cp.stderr}\n"
        )
    return stdout


class Apt:
    @staticmethod
    def update():
        return run_command("apt-get update", sudo=True)

    @staticmethod
    def upgrade():
        return run_command("apt-get upgrade -y", sudo=True)

    @staticmethod
    def install(package: Iterable):
        packages = " ".join(package)
        return run_command(f"apt-get install {packages}", sudo=True)


class Pip:
    @staticmethod
    def update():
        return run_command(f"{PYTHON_V} -m pip install pip --upgrade --user")

    @staticmethod
    def install(package: Iterable):
        packages = " ".join(package)
        return run_command(f"{PYTHON_V} -m pip install {packages}")

    @staticmethod
    def install_with_pipx(package: Iterable):
        installed_apps = set()
        for line in run_command("pipx list").splitlines():
            if line.startswith("   package "):
                installed_apps.add(line[11:].split(" ")[0])

        for p in set(package) - installed_apps:
            run_command(f"pipx install {p}")
        run_command(f"{PYTHON_V} -m pipx ensurepath")

class Dotfiles():
    pass

def make_shiny():
    Apt.update()
    Apt.upgrade()
    Apt.install(APT_PACKAGES)

    Pip.update()
    Pip.install(PIP_PACKAGES)
    Pip.install_with_pipx(PIPX_PACKAGES)


make_shiny()
