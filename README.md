# ublue-updater

Small update program written in python, executes update scripts in `/etc/update.d`

## intended for use in uBlue, however can be used anywhere as a simple update runner/checker

dependencies (fedora): ```sudo dnf install python3-notify2 python3-psutil```

# Configuration

## Location
valid config paths (in order of priority)

```"$HOME"/.config/ublue-updater/ublue-updater.conf```

```/etc/ublue-updater/ublue-updater.conf```

```/usr/etc/ublue-updater/ublue-updater.conf```


## Config Variables
section: `checks`

`battery_percent`: checks if battery is above specified percent

`cpu_load`: checks if cpu average load is under specified percent



