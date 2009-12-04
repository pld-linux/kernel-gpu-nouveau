# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose         # verbose build (V=1)

%define		_rel	1
Summary:	Linux driver for DRM
Summary(pl.UTF-8):	Sterownik dla Linuksa do DRM
Name:		kernel%{_alt_kernel}-gpu-nouveau
Version:	20091203
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://people.freedesktop.org/~pq/nouveau-drm/master.tar.gz
# Source0-md5:	c16b18fe85b84641e3ffcac531caac6e
URL:		http://nouveau.freedesktop.org/wiki/InstallDRM
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.31}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
Obsoletes:	kernel-drm = %{_kernel_ver_str}
Conflicts:	kernel-drm = %{_kernel_ver_str}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The DRM (Direct Rendering Manager) is a Linux kernel module that gives
direct hardware access to DRI clients.

%description -l pl.UTF-8
DRM (Direct Rendering Manager) to moduł jądra Linuksa dający
bezpośredni dostęp do sprzętu klientom DRI.

%package -n kernel%{_alt_kernel}-gpu-drm-nouveau
Summary:	Linux driver for DRM
Summary(pl.UTF-8):	Sterownik dla Linuksa do DRM
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel

%description -n kernel%{_alt_kernel}-gpu-drm-nouveau
The DRM (Direct Rendering Manager) is a Linux kernel module that gives
direct hardware access to DRI clients.

%description -n kernel%{_alt_kernel}-gpu-drm-nouveau -l pl.UTF-8
DRM (Direct Rendering Manager) to moduł jądra Linuksa dający
bezpośredni dostęp do sprzętu klientom DRI.

%prep
%setup -q -n master

%build
TOPDIR=$(pwd)
cd drivers/gpu/drm
%build_kernel_modules -m drm,drm_kms_helper,nouveau/nouveau,ttm/ttm \
	CONFIG_ACPI=m \
	CONFIG_DRM=m \
	CONFIG_DRM_TTM=m \
	CONFIG_DRM_KMS_HELPER=m \
	CONFIG_DRM_NOUVEAU=m \
	CONFIG_DRM_NOUVEAU_KMS=n \
	CONFIG_DRM_NOUVEAU_BACKLIGHT=y \
	CONFIG_DRM_TDFX=n \
	CONFIG_DRM_R128=n \
	CONFIG_DRM_RADEON=n \
	CONFIG_DRM_MGA=n \
	CONFIG_DRM_I810=n \
	CONFIG_DRM_I830=n \
	CONFIG_DRM_I915=n \
	CONFIG_DRM_SIS=n \
	CONFIG_DRM_SAVAGE=n \
	CONFIG_DRM_VIA=n \
	KCPPFLAGS="-I$TOPDIR/include/drm -DCONFIG_DRM_NOUVEAU_BACKLIGHT"

%install
rm -rf $RPM_BUILD_ROOT

cd drivers/gpu/drm
%install_kernel_modules -m drm -d kernel/drivers/gpu/drm
%install_kernel_modules -m drm_kms_helper -d kernel/drivers/gpu/drm
%install_kernel_modules -m nouveau/nouveau -d kernel/drivers/gpu/drm
%install_kernel_modules -m ttm/ttm -d kernel/drivers/gpu/drm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-gpu-drm-nouveau
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-gpu-drm-nouveau
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-gpu-drm-nouveau
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/gpu
