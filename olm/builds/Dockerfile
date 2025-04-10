FROM container-registry.oracle.com/os/oraclelinux:8-slim

ARG ARCH
ARG binary=./bin/${ARCH}/nfsplugin
COPY ${binary} /nfsplugin

RUN microdnf install -y ca-certificates nfs-utils libcap-devel && \
    microdnf clean all

ENTRYPOINT ["/nfsplugin"]
