%global commit      a1b38188d0b43ec53250f4919fca118a82141e45
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global bumpver 1

Name:		ly
Version:	1~%{bumpver}.git%{shortcommit}
Release:	1
URL:		https://github.com/fairyglade/ly
Source0:	%{url}/archive/%{commit}/%{name}-%{commit}.tar.gz
Summary:	display manager with console UI
License:	WTFPL
Group:		Window Manager/Display Manager

BuildRequires:	zig
BuildRequires:  kernel-devel
BuildRequires:  pkgconfig(xcb)

%description

%prep
%autosetup -n %{name}-%{commit} -p1

%build
zig build

%install
zig build installexe -Ddest_directory="%{buildroot}" -Dcpu=baseline -Doptimize=ReleaseSafe

%post
%systemd_post ly.service

%postun
%systemd_postun ly.service

%preun
%systemd_preun ly.service

%files
%license license.md
%{_sysconfdir}/ly
%{_sysconfdir}/pam.d
%{_bindir}/ly
%{_unitdir}/%{name}.service
