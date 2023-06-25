FROM registry.fedoraproject.org/fedora:latest AS builder

WORKDIR /app 

ADD . /app

RUN dnf install --disablerepo='*' --enablerepo='fedora,updates' --setopt install_weak_deps=0 --nodocs --assumeyes rpm-build make

RUN make


FROM scratch

# Copy build RPMs
COPY --from=builder /tmp/ublue-os/rpms /rpms
