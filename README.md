# ublue-updater

Small update program written in python intended for use in uBlue, executes update scripts in `/etc/update.d`

dependencies (fedora): ```sudo dnf install python3-notify2 python3-psutil```


# Usage

You can add this to your image by simply pulling down and installing the rpm

```
COPY --from=ghcr.io/gerblesh/ublue-update:latest /rpms/ublue-updater.noarch.rpm /rpms/
RUN rpm-ostree override install /rpms/ublue-update.noarch.rpm
```
if you are using a uBlue main image:


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

