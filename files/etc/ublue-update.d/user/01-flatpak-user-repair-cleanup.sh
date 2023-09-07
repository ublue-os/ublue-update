#!/usr/bin/bash


/usr/bin/flatpak uninstall --user --unused -y --noninteractive
/usr/bin/flatpak repair --user
