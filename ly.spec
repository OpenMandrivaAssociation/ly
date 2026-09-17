# Currently broken due to zig update causing errors and previous zig needs old version of llvm
# https://codeberg.org/fairyglade/ly/issues/843

#Untested changes

#define commit_tag 0cf752f3b850d16283e28853bca63e994d8c5e7b

%define commit_date %{nil}
%define ver 1.5.0.rc1
Name:		ly
Version:	%{?commit_date:%{ver}~%{commit_date}}
Release:	1
URL:		https://codeberg.org/fairyglade/ly
%if "%{commit_tag}" != "%{nil}"
Source0:    https://codeberg.org/fairyglade/ly/archive/%{commit_tag}.tar.gz#/%{name}-%{version}.tar.gz
%else
Source0:    https://codeberg.org/fairyglade/ly/archive/v1.5.0-rc1.tar.gz#/%{name}-1.5.0-rc1.tar.gz
%endif

Source1: https://codeberg.org/fairyglade/ly/releases/download/v1.5.0-rc1/vendor.tar.zst


Summary:	display manager with console UI
License:	WTFPL
Group:		Window Manager/Display Manager

BuildRequires:	zig
BuildRequires:  kernel-devel
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pam-devel

Recommends:     brightnessctl

%description

%prep
%autosetup -n %{name}
mkdir -p zig-global-cache
tar zxf %{S:1} -C zig-global-cache --strip-components=1

%build
zig build \
  --search-prefix /usr \
  -Ddest_directory=%{buildroot} \
  -Dname=ly \
  --global-cache-dir zig-global-cache \
  --system zig-global-cache/p \
  -Dcpu=baseline \
  -Doptimize=ReleaseSafe

%install
zig build \
  --search-prefix /usr \
  -Ddest_directory=%{buildroot} \
  -Dname=ly \
  --global-cache-dir zig-global-cache \
  --system zig-global-cache/p \
  -Dcpu=baseline \
  -Doptimize=ReleaseSafe \
  installexe

# Config files (backup them)
install -Dm644 config.ini %{buildroot}/etc/%{name}/config.ini
install -Dm755 setup.sh %{buildroot}/etc/%{name}/setup.sh
install -Dm644 pam.d/ly %{buildroot}/etc/pam.d/%{name}

# Systemd service
install -Dm644 ly.service %{buildroot}/usr/lib/systemd/system/ly.service  # Assume source has this; add if needed


%files
%license license.md
%config(noreplace) %{_sysconfdir}/ly
%config(noreplace) %{_sysconfdir}/pam.d
%{_bindir}/ly
%{_unitdir}/%{name}.service


