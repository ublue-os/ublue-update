#!/usr/bin/env bash



if [ -x /usr/bin/distrobox ]; then
    SUDO_USER="" # avoid distrobox sudo checks
    /usr/bin/distrobox upgrade -a
fi
