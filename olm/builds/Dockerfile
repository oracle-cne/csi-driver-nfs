FROM container-registry.oracle.com/os/oraclelinux:9 AS builder

RUN dnf config-manager --enable ol9_codeready_builder && \
    dnf -y install git make golang patch && \
    go version

# Copy the contents of the repository
COPY . /workspace/go/src/github.com/csi-driver-nfs

ENV GOPATH=/workspace/go CGO_ENABLED=0
WORKDIR /workspace/go/src/github.com/csi-driver-nfs

RUN patch  --no-backup-if-mismatch -p0 --fuzz=0 < olm/Makefile.patch && \
    make nfs

FROM container-registry.oracle.com/os/oraclelinux:9-slim

# COPY LICENSE NOTICE THIRD_PARTY_LICENSES.txt olm/SECURITY.md /usr/share/licenses/
COPY --from=builder /workspace/go/src/github.com/csi-driver-nfs/LICENSE \
     /workspace/go/src/github.com/csi-driver-nfs/olm/SECURITY.md \
     /workspace/go/src/github.com/csi-driver-nfs/THIRD_PARTY_LICENSES.txt /usr/share/licenses/

RUN microdnf update -y && \
    microdnf install -y ca-certificates nfs-utils libcap-devel && \
    microdnf clean all && \
    rm -rf /var/cache/yum/* && \
    test -d /LICENSES || ln -s /usr/share/licenses /LICENSES

WORKDIR /

COPY --from=builder /workspace/go/src/github.com/csi-driver-nfs/bin/nfsplugin /

ENTRYPOINT ["/nfsplugin"]
