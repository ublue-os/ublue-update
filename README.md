# Universal Blue Update

Small update program written in python intended for use in Universal Blue that uses [`topgrade`](https://github.com/topgrade-rs/topgrade) for executing updates.

Includes systemd timers and services for auto update

dependencies (fedora): ```sudo dnf install python3-psutil libnotify```


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

> **Note**
> If you are on an image derived from uBlue main, you will need to remove or disable automatic updates with rpm-ostreed, to do this, you need to remove or change this line in the config file: `AutomaticUpdatePolicy=stage` (set to `none` if you don't want to remove the line)


## Command Line

To run a complete system update, it's recommended to use systemd:

```
$ systemctl start ublue-update.service
```

This allows for passwordless system updates (user must be in `wheel` group)


### Run updates from command line (not recommended)

Only run user updates (rootless):
```
$ ublue-update
```

Only run system updates (requires root):
```
$ pkexec ublue-update --system
```

```
usage: ublue-update [-h] [-f] [-c] [-u] [-w] [--system]

options:
  -h, --help         show this help message and exit
  -f, --force        force manual update, skipping update checks
  -c, --check        run update checks and exit
  -u, --updatecheck  check for updates and exit
  -w, --wait         wait for transactions to complete and exit
  --config CONFIG    use the specified config file
  --system           only run system updates (requires root)
```

## Troubleshooting

You can check the ublue-update logs by running this command:
```
$ journalctl -exu 'ublue-update.service'
```

# Configuration

## Update Scripts
Update scripts are separated into two files inside of `/usr/share/ublue-update`

### `/usr/share/ublue-update/topgrade-system.toml`
Topgrade config ran as root, handles rpm-ostree and flatpaks.

### `/usr/share/ublue-update/topgrade-user.toml`
Topgrade config ran as user, handles flatpaks and distrobox containers.

See [`topgrade`](https://github.com/topgrade-rs/topgrade)'s GitHub for configuring these files.


## Location

### Valid config paths (in order of priority from highest to lowest):

1. ```/etc/ublue-update/ublue-update.toml```

2. ```/usr/etc/ublue-update/ublue-update.toml```


## Config Variables
### Section: `checks`

* `min_battery_percent`: checks if battery is above specified percent

* `max_cpu_load_percent`: checks if cpu average load is under specified percent

* `max_mem_percent`: checks if memory usage is below specified percent

* `network_not_metered`: if true, checks if the current network connection is not marked as metered

### Section: `notify`

* `dbus_notify`: enable graphical notifications via dbus

### Full Example

```toml
[checks]
    min_battery_percent = 20.0  # Battery Level >= 20%?
    max_cpu_load_percent = 50.0 #     CPU Usage <= 50%?
    max_mem_percent = 90.0      #     RAM Usage <= 90%?
    network_not_metered = true  # Abort if network connection is metered
[notify]
    dbus_notify = false         # Do not show notifications
```

## How do I build this?

You can build and test this package in a container by using the provided container file.

1. `make builder-image` will create a container image with all dependencies installed
2. `make builder-exec` will execute a shell inside the builder container to allow you easily build the rpm package with `make build-rpm`
3. `make` will trigger the build process and generate a `.whl` package that can be installed
4. `pip install --user -e .` will allow to install an editable version of this package so you quickly edit and test the program

# Special Thanks

Special thanks to [cukmekerb](https://github.com/cukmekerb) for helping troubleshoot/add features early in project development
