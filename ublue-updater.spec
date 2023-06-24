Name:     ublue-updater
Version:  0.1
Release:  %autorelease
Summary:  centralized update service/checker made for universal blue
License:  Apache-2.0
URL:      https://github.com/gerblesh/ublue-auto-update
Source:   http://ftp.gnu.org/gnu/hello/hello-%{version}.tar.gz

%description
The GNU Hello program produces a familiar, friendly greeting. Yes, this is
another implementation of the classic program that prints "Hello, world!" when
you run it.

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install

%files

%changelog
%autochangelog
