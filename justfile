set shell := ["bash", "-uc"]
export UBLUE_ROOT := env_var_or_default("UBLUE_ROOT", "/app/output")
export TARGET := "ublue-update"
export SOURCE_DIR := UBLUE_ROOT + "/" + TARGET
export RPMBUILD := UBLUE_ROOT + "/rpmbuild"

default:
	just --list

venv-create:
	/usr/bin/python -m venv venv
	source venv/bin/activate && pip3 install -e .
	echo 'Enter: `source venv/bin/activate` to enter the venv'

build: format
	python3 -m build

test:
	pytest -v

spec: output
	rpkg spec --outdir "$PWD/output"

build-rpm:
	rpkg local --outdir "$PWD/output"

builddep:
	dnf builddep -y output/ublue-update.spec

container-install-deps:
	#!/usr/bin/env bash
	set -eou pipefail
	dnf install                       \
		--disablerepo='*'             \
		--enablerepo='fedora,updates' \
		--setopt install_weak_deps=0  \
		--nodocs                      \
		--assumeyes                   \
		'dnf-command(builddep)'       \
		rpkg                          \
		rpm-build                     \
		git

# Used internally by build containers
container-rpm-build: container-install-deps spec builddep build-rpm
	#!/usr/bin/env bash
	set -eou pipefail

	# clean up files
	for RPM in ${UBLUE_ROOT}/noarch/*.rpm; do
		NAME="$(rpm -q $RPM --queryformat='%{NAME}')"
		mkdir -p "${UBLUE_ROOT}/ublue-os/rpms/"
		cp "${RPM}" "${UBLUE_ROOT}/ublue-os/rpms/$(rpm -q "${RPM}" --queryformat='%{NAME}.%{ARCH}.rpm')"
	done

output:
	mkdir -p output

format:
	black src tests
	flake8 src tests


dnf-install:
	dnf install -y "output/noarch/*.rpm"

container-build:
	podman build . -t test-container -f Containerfile

container-test:
	#!/usr/bin/env bash
	set -eou pipefail

	podman run -d --replace --name ublue-update-test --security-opt label=disable --device /dev/fuse:rw --privileged --systemd true test-container 
	while [[ "$(podman exec ublue-update-test systemctl is-system-running)" != "running" && "$(podman exec ublue-update-test systemctl is-system-running)" != "degraded" ]]; do
		echo "Waiting for systemd to finish booting..."
		sleep 1
	done
	# podman exec -t ublue-update-test systemd-run --user --machine podman@ --pipe --quiet sudo /usr/bin/ublue-update --dry-run
	podman exec -t ublue-update-test systemd-run --machine 0@ --pipe --quiet /usr/bin/ublue-update --dry-run
	podman rm -f ublue-update-test
clean:
	rm -rf "$UBLUE_ROOT"
