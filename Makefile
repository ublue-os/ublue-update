UBLUE_ROOT := $(UBLUE_ROOT)
TARGET := ublue-update
SOURCE_DIR := $(UBLUE_ROOT)/$(TARGET)
RPMBUILD := $(UBLUE_ROOT)/rpmbuild
ifeq ($(GITHUB_REF),)
export GITHUB_REF := refs/tags/v1.0.0+$(shell git rev-parse --short HEAD)
endif

all: build-rpm

build:
	flake8 --check src
	black --check src
	python3 -m build

format:
	flake8 src
	black src

spec: output
	rpkg spec --outdir $(PWD)/output

build-rpm: output
	rpkg local --outdir $(PWD)/output
output:
	mkdir -p output

clean: $(SOURCE_DIR) $(RPMBUILD)
	rm -rf $^
