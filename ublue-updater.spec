Name:     ublue-updater
Vendor: ublue-os
Version:  0.1
Release:  1%{?dist}
Summary:  Centralized update service/checker made for Universal Blue
License:  Apache-2.0
URL:      https://github.com/gerblesh/ublue-auto-update

BuildArch:      noarch
Supplements:    rpm-ostree flatpak
BuildRequires: make
Requires: python3-notify2
Requires: python3-psutil
Source0:    %{NAME}.tar.gz 
Source1:    %{NAME}-data.tar.gz

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^ublue%-", ""); print(t)}

%description
Installs and configures ublue-os-updater services and timers for auto update

%prep
%setup -q -c

%install
mkdir -p -m0755 %{buildroot}%{_datadir}/%{VENDOR} %{buildroot}%{_bindir}
tar xzf %{SOURCE1} -C %{buildroot} . --strip-components=1
tar xzf %{SOURCE0} -C %{buildroot}%{_datadir}/${VENDOR} --directory ./%{VENDOR} --strip-components=1
sudo install -m 0755 update-ublue %{buildroot}%{_bindir}/update-ublue

%post
%systemd_post ublue-updater.service
%systemd_post ublue-updater.timer

%preun
%systemd_preun ublue-updater.service
%systemd_preun ublue-updater.timer

%files
%license LICENSE
%doc README.md
%{_bindir}/update-ublue
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/system/%{NAME}.service
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/system/%{NAME}.timer
%attr(0755,root,root) %{_exec_prefix}/etc/ublue-updater/ublue-updater.conf
%attr(0644,root,root) %{_sysconfdir}/update.d/flatpak-user-update.sh
%attr(0644,root,root) %{_sysconfdir}/etc/update.d/system-update.sh
%exclude %{_datadir}/%{VENDOR}/*

%changelog
%autochangelog
