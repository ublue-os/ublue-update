# auto-update

# intended for use in uBlue, however can be used anywhere as a simple update runner/checker

dependencies (fedora): `sudo dnf install python3-notify2 python3-psutil`

end goal is to just have an rpm SPEC file that will most likely end up in ublue-os/config

# Reads values from configuration

section: `checks`
`battery_percent`: checks if battery is above specified percent
`cpu_load`: checks if cpu average load is under specified percent

# executes update scripts in `/etc/update.d`
