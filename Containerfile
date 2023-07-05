FROM registry.fedoraproject.org/fedora:latest AS builder

ENV UBLUE_ROOT=/app/output

WORKDIR /app 

ADD . /app

RUN dnf install \
    --disablerepo='*' \
    --enablerepo='fedora,updates' \
    --setopt install_weak_deps=0 \
    --nodocs \
    --assumeyes \
    'dnf-command(builddep)' \
    rpmlint \
    rpm-build  && \
    dnf builddep -y ublue-update.spec
