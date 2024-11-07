set shell := ["bash", "-c"]
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
	podman build . -t testing -f Containerfile.test
	podman run -it --security-opt label=disable --device /dev/fuse:rw --privileged testing
#
#builder-image:
#	podman build -t "$TARGET:builder" -f Containerfile.builder .
#
#builder-exec:
#	podman run --rm -it \
#		-v "$PWD:$PWD" \
#		-w "$PWD" \
#		-e DISPLAY \
#		-e DBUS_SESSION_BUS_ADDRESS \
#		-e XDG_RUNTIME_DIR \
#		--ipc host \
#		-v "/tmp/.X11-unix:/tmp/.X11-unix" \
#		-v /var/run/dbus:/var/run/dbus \
#		-v /run/user/1000/bus:/run/user/1000/bus \
#		-v /run/dbus:/run/dbus \
#		-v "${XDG_RUNTIME_DIR}:${XDG_RUNTIME_DIR}" \
#		--security-opt label=disable \
#		$TARGET:builder

clean:
	rm -rf "$UBLUE_ROOT"
