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

### Section: `checks.scripts`

In addition to the predefined checks above, it is also possible to implement
custom conditions through user-provided scripts and their exit codes.
Each entry in the `checks.scripts` array must specify the following settings:

* `shell`: specifies the shell used to execute the custom script (e.g. `bash`)

* `run`: specifies the script text to be run using the specified shell

* `message`: an optional message that is shown when the check fails

* `name`: an optional human-readable name for this check

The parameters `run` and `file` are mutually exclusive, but at least one must be specified.
The `shell` parameter is mandatory when using `run`.

The custom script should use its exit code to indicate whether the updater should proceed
(`exit code = 0`) or whether updates should be inhibited right now (any non-0 exit code).
If `message` is not specified but the script has written text to `stdout`,
that text will be used as the message.

### Section: `notify`

* `dbus_notify`: enable graphical notifications via dbus

### Full Example

```toml
[checks]
    min_battery_percent = 20.0  # Battery Level >= 20%?
    max_cpu_load_percent = 50.0 #     CPU Usage <= 50%?
    max_mem_percent = 90.0      #     RAM Usage <= 90%?
    network_not_metered = true  # Abort if network connection is metered

    [[checks.scripts]]
        name = "Example script that always fails"
        shell = "bash"
        run = "exit 1"
        message = "Failure message - this message will always appear"

    [[checks.scripts]]
        name = "Example script that always succeeds"
        shell = "bash"
        run = "exit 0"
        message = "Failure message - this message will never appear"

    [[checks.scripts]]
        name = "Example multiline script with custom message"
        shell = "bash"
        run = """
echo "This is a custom message"
exit 1
"""

    [[checks.scripts]]
        name = "Python script"
        shell = "python3"
        run = """
print("Python also works when installed")
exit(1)
"""

    [[checks.scripts]]
        name = "Example external script"
        # shell = "bash" # specifying a shell is optional for external scripts/programs
        file = "/bin/true"

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
