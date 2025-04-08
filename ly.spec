%global commit      a1b38188d0b43ec53250f4919fca118a82141e45
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global bumpver 1

Name:		ly
Version:	1~%{bumpver}.git%{shortcommit}
Release:	1
URL:		https://github.com/fairyglade/ly
Source0:	%{url}/archive/%{commit}/%{name}-%{commit}.tar.gz
Source1:    ly-zig-cache.tar.gz
Summary:	display manager with console UI
License:	WTFPL
Group:		Window Manager/Display Manager

BuildRequires:	zig
BuildRequires:  kernel-devel
BuildRequires:  pkgconfig(xcb)

Recommends:     brightnessctl

%description

%prep
%autosetup -n %{name}-%{commit} -p1
tar -zxf %{SOURCE1}

%build
zig build -Ddest_directory="%{buildroot}" -Dcpu=baseline -Doptimize=ReleaseSafe --system "zig/p"

%install
zig build installexe -Ddest_directory="%{buildroot}" -Dcpu=baseline -Doptimize=ReleaseSafe --system "zig/p"


%post
%systemd_postun ly.service

%preun
%systemd_preun ly.service

%files
%license license.md
%{_sysconfdir}/ly
%{_sysconfdir}/pam.d
%{_bindir}/ly
%{_unitdir}/%{name}.service
