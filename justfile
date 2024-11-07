set shell := ["bash", "-uc"]
export UBLUE_ROOT := env_var_or_default("UBLUE_ROOT", "/app/output")
export TARGET := "ublue-update"
export SOURCE_DIR := UBLUE_ROOT + "/" + TARGET
export RPMBUILD := UBLUE_ROOT + "/rpmbuild"

export GITHUB_REF := env_var_or_default("GITHUB_REF","refs/tags/v1.0.0+" + `git rev-parse --short HEAD`)

# Define the GITHUB_REF variable if it's not already set
venv-create:
	/usr/bin/python -m venv venv
	source venv/bin/activate && pip3 install .
	echo 'Enter: `source venv/bin/activate` to enter the venv'

default:
	just --list

build:
	black --check src
	python3 -m build

test:
	pytest -v

spec: output
	rpkg spec --outdir "$PWD/output"

build-rpm:
	rpkg local --outdir "$PWD/output"

output:
	mkdir -p output

format:
	black src
	flake8 src

dnf-install:
	dnf install -y "output/noarch/*.rpm"

build-test:
	#!/usr/bin/env bash

	podman build . -t testing -f Containerfile
	podman run -d --name ublue_update_test --security-opt label=disable --device /dev/fuse:rw --privileged testing
	while [[ "$(podman exec ublue_update_test systemctl is-system-running)" != "running" && "$(podman exec ublue_update_test systemctl is-system-running)" != "degraded" ]]; do
		echo "Waiting for systemd to finish booting..."
		sleep 1
	done

	podman exec -it ublue_update_test systemd-run --user --machine podman@ --pipe --quiet sudo /usr/bin/ublue-update --dry-run
clean:
	rm -rf "$UBLUE_ROOT"
