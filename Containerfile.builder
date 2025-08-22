FROM registry.fedoraproject.org/fedora:latest@sha256:7899eceb9d240c8a6669a0cf961ef963289a354dcd5c27c716526a32bac5e0c7 AS builder

ENV UBLUE_ROOT=/app/output

WORKDIR /app 

ADD . /app

RUN dnf install --assumeyes python3-pip && pip install topgrade

RUN dnf install \
    --disablerepo='*' \
    --enablerepo='fedora,updates' \
    --setopt install_weak_deps=0 \
    --nodocs \
    --assumeyes \
    'dnf-command(builddep)' \
    rpkg \
    rpm-build && \
    mkdir -p "$UBLUE_ROOT" && \
    rpkg spec --outdir  "$UBLUE_ROOT" && \
    dnf builddep -y output/ublue-update.spec

FROM builder AS rpm

RUN make build-rpm
