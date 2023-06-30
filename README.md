# ublue-updater

Small update program written in python intended for use in uBlue, executes update scripts/tasks placed in `/etc/ublue-update.d` (make sure each script has exec perms)

dependencies (fedora): ```sudo dnf install python3-notify2 python3-psutil```


# Usage


## Installation

You can add this to your image by simply pulling down and installing the rpm

```
COPY --from=ghcr.io/gerblesh/ublue-update:latest /rpms/ublue-update.noarch.rpm /tmp/rpms/
RUN rpm-ostree override install /tmp/rpms/ublue-update.noarch.rpm
```

if you are using a uBlue main image (or any derivitaves):

```
COPY --from=ghcr.io/gerblesh/ublue-update:latest /rpms/ublue-update.noarch.rpm /tmp/rpms/
RUN rpm-ostree override replace ublue-os-update-services --install=/tmp/rpms/ublue-update.noarch.rpm
```

Enable the systemd timer:

```RUN systemctl --global enable ublue-update.timer```


## Command Line

```
usage: ublue-update [-h] [-f]

options:
  -h, --help   show this help message and exit
  -f, --force  force manual update, skipping update checks
```


# Configuration


## Location
valid config paths (in order of priority)

```"$HOME"/.config/ublue-update/ublue-update.conf```

```/etc/ublue-updater/ublue-update.conf```

```/usr/etc/ublue-update/ublue-update.conf```


## Config Variables
section: `checks`

`battery_percent`: checks if battery is above specified percent

`cpu_load`: checks if cpu average load is under specified percent

