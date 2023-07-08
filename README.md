# Universal Blue Update

Small update program written in python intended for use in Universal Blue, executes update scripts/tasks placed in `/etc/ublue-update.d` (make sure each script has exec perms)

Includes systemd timers and services for auto update

dependencies (fedora): ```sudo dnf install python3-notify2 python3-psutil```


# Usage


## Installation

You can add this to your image by simply pulling down and installing the rpm:

```
COPY --from=ghcr.io/ublue-os/ublue-update:latest /rpms/ublue-update.noarch.rpm /tmp/rpms/
RUN rpm-ostree install /tmp/rpms/ublue-update.noarch.rpm
```

If you are on an image derived from uBlue main:

```
COPY --from=ghcr.io/ublue-os/ublue-update:latest /rpms/ublue-update.noarch.rpm /tmp/rpms/
RUN rpm-ostree override remove ublue-os-update-services && rpm-ostree install /tmp/rpms/ublue-update.noarch.rpm
```

## Command Line

```
usage: ublue-update [-h] [-f] [-c]

options:
  -h, --help   show this help message and exit
  -f, --force  force manual update, skipping update checks
  -c, --check  run update checks and exit
```


# Configuration


## Location
valid config paths (in order of priority)

```"$HOME"/.config/ublue-update/ublue-update.conf```

```/etc/ublue-update/ublue-update.conf```

```/usr/etc/ublue-update/ublue-update.conf```


## Config Variables
section: `checks`

`battery_percent`: checks if battery is above specified percent

`cpu_load`: checks if cpu average load is under specified percent


## How do I build this?

You can build and test this package in a container by using the provided container file.

1. `make builder-image` will create a container image with all dependencies installed
2. `make builder-exec` will execute a shell inside the builder container to allow you easily build the rpm package with `make build-rpm`
3. `make` will trigger the build process and generate a `.whl` package that can be installed
4. `pip install --user -e .` will allow to install an editable version of this package so you quickly edit and test the program

# Special Thanks

Special thanks to https://github.com/cukmekerb for helping troubleshoot/add features early in project development
