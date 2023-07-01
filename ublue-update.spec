Name:   ublue-update
Vendor: ublue-os
Version:  1.0
Release:  1%{?dist}
Summary:  Centralized update service/checker made for Universal Blue
License:  Apache-2.0
URL:      https://github.com/gerblesh/%{name}

BuildArch:      noarch
Supplements:    rpm-ostree flatpak
BuildRequires: make
BuildRequires: systemd-rpm-macros
BuildRequires: black
BuildRequires: ShellCheck
BuildRequires: python-flake8
Requires: python3-notify2
Requires: python3-psutil
Source0:    %{name}.tar.gz
Source1:    %{name}-data.tar.gz

%global sub_name %{lua:t=string.gsub(rpm.expand("%{name}"), "^ublue%-", ""); print(t)}

%description
Installs and configures ublue-update script, systemd services, and systemd timers for auto update

%prep
%setup -D -c -a 0
%setup -c -a 1

%build
black %{name}
flake8 %{name}
shellcheck etc/%{name}.d/*.sh

%install
mkdir -p -m0755 %{buildroot}%{_datadir}/%{vendor} %{buildroot}%{_bindir} %{buildroot}/%{_docdir}/%{vendor}
install -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -m 0644 README.md LICENSE %{buildroot}%{_docdir}/%{vendor}
cp -rp etc usr %{buildroot}

%post
%systemd_user_post %{name}.timer

%preun
%systemd_user_preun %{name}.timer

%files
%license %{_docdir}/%{vendor}/LICENSE
%doc %{_docdir}/%{vendor}/README.md
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/user/%{name}.service
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/user/%{name}.timer
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/user-preset/00-%{name}.preset
%attr(0644,root,root) %{_exec_prefix}/etc/%{name}/%{name}.conf
%attr(0755,root,root) %{_sysconfdir}/%{name}.d/00-system-update.sh
%attr(0755,root,root) %{_sysconfdir}/%{name}.d/01-flatpak-system-update.sh
%attr(0755,root,root) %{_sysconfdir}/%{name}.d/02-flatpak-user-update.sh
%attr(0755,root,root) %{_sysconfdir}/%{name}.d/03-flatpak-system-repair-cleanup.sh
%attr(0755,root,root) %{_sysconfdir}/%{name}.d/04-flatpak-user-repair-cleanup.sh
%attr(0755,root,root) %{_sysconfdir}/%{name}.d/05-distrobox-user-update.sh

%changelog
%autochangelog
