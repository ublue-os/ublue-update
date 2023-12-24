#!/usr/bin/env bash

if [ -x /nix/var/nix/profiles/default/bin/nix ]; then
    /nix/var/nix/profiles/default/bin/nix upgrade '.*' --profile ~/.nix-profile
fi
