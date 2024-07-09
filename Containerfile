ARG FEDORA_MAJOR_VERSION="${FEDORA_MAJOR_VERSION:-40}"

FROM registry.fedoraproject.org/fedora:${FEDORA_MAJOR_VERSION} AS builder

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
    rpkg \
    rpm-build && \
    mkdir -p "$UBLUE_ROOT" && \
    rpkg spec --outdir  "$UBLUE_ROOT" && \
    dnf builddep -y output/ublue-update.spec && \
    make build-rpm

FROM scratch

ENV UBLUE_ROOT=/app/output

# Copy RPMs
COPY --from=builder ${UBLUE_ROOT}/ublue-os/rpms /rpms
# Copy dumped contents
COPY --from=builder ${UBLUE_ROOT}/ublue-os/files /files
