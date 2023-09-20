#!/usr/bin/env bash

if [ -x /usr/bin/distrobox ]; then
    unset SUDO_USER # avoid distrobox sudo checks
    /usr/bin/distrobox upgrade -a
fi
