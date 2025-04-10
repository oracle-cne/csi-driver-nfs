%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%global app_name                csi-driver-nfs
%global app_version             4.11.0
%global oracle_release_version  1
%global _buildhost              build-ol%{?oraclelinux}-%{?_arch}.oracle.com
%global image_name	            nfsplugin

Name:       %{app_name}
Version:    %{app_version}
Release:    %{oracle_release_version}%{dist}
Vendor:     Oracle America
Summary:    NFS CSI driver for Kubernetes
License:    Apache 2.0
Group:      Development/Tools
Url:        https://github.com/kubernetes-csi/csi-driver-nfs
Source0:    %{name}-%{version}.tar.bz2
BuildRequires:  golang
BuildRequires:  make
BuildRequires:  git

Patch0:         go.mod.patch

%description
NFS CSI driver for Kubernetes

%prep
%setup -q
#%patch0

%build
export GOPATH=`pwd`/go
export GOTOOLCHAIN=local
make nfs

%global docker_image container-registry.oracle.com/olcne/%{image_name}:v%{version}

podman build --pull \
    --build-arg https_proxy=${https_proxy} \
    -t %{docker_image} -f ./olm/builds/Dockerfile .
podman save -o %{app_name}.tar %{docker_image}

%install
%__install -D -m 644 %{app_name}.tar %{buildroot}/usr/local/share/olcne/%{app_name}.tar

%files
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/local/share/olcne/%{app_name}.tar

%changelog
* Thu Apr 10 2025 Michael Gianatassio <michael.gianatassio@oracle.com> - 4.11.0-1
- Initial release of the csi-driver-nfs.


