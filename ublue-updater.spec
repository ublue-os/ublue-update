Name:     ublue-updater
Version:  0.1
Release:  1%{?dist}
Summary:  centralized update service/checker made for universal blue
License:  Apache-2.0
URL:      https://github.com/gerblesh/ublue-auto-update


BuildArch:      noarch
Supplements:    rpm-ostree flatpak

Source0:        ublue-os-update-services.tar.gz

%description
Installs and configures ublue-updater services and timers for auto update

%prep
%setup -q -c -T

%build

mkdir -p -m0755 %{buildroot}%{_datadir}/%{VENDOR}

tar xf %{SOURCE0} -C %{buildroot}%{_datadir}/%{VENDOR} --strip-components=1

tar xf %{SOURCE0} -C %{buildroot} --strip-components=2


%post
%systemd_post ublue-updater.timer

%preun
%systemd_preun ublue-updater.timer

%files


%changelog
%autochangelog
