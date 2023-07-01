Name:   ublue-update
Vendor: ublue-os
Version:  1.0
Release:  1%{?dist}
Summary:  Centralized update service/checker made for Universal Blue
License:  Apache-2.0
URL:      https://github.com/gerblesh/%{NAME}

BuildArch:      noarch
Supplements:    rpm-ostree flatpak
BuildRequires: make
BuildRequires: systemd-rpm-macros
BuildRequires: black
BuildRequires: ShellCheck
BuildRequires: python-flake8
Requires: python3-notify2
Requires: python3-psutil
Source0:    %{NAME}.tar.gz
Source1:    %{NAME}-data.tar.gz

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^ublue%-", ""); print(t)}

%description
Installs and configures ublue-update script, systemd services, and systemd timers for auto update

%prep
%setup -D -c -a 0
%setup -c -a 1

%build
black %{NAME}
flake8 %{NAME}
shellcheck etc/%{NAME}.d/*.sh

%install
mkdir -p -m0755 %{buildroot}%{_datadir}/%{VENDOR} %{buildroot}%{_bindir} %{buildroot}/%{_docdir}/%{VENDOR}
install -m 0755 %{NAME} %{buildroot}%{_bindir}/%{NAME}
install -m 0644 README.md LICENSE %{buildroot}%{_docdir}/%{VENDOR}
cp -rp etc usr %{buildroot}

%post
%systemd_user_post %{NAME}.timer

%preun
%systemd_user_preun %{NAME}.timer

%files
%license %{_docdir}/%{VENDOR}/LICENSE
%doc %{_docdir}/%{VENDOR}/README.md
%attr(0755,root,root) %{_bindir}/%{NAME}
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/user/%{NAME}.service
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/user/%{NAME}.timer
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/user-preset/00-%{NAME}.preset
%attr(0644,root,root) %{_exec_prefix}/etc/%{NAME}/%{NAME}.conf
%attr(0755,root,root) %{_sysconfdir}/%{NAME}.d/00-system-update.sh
%attr(0755,root,root) %{_sysconfdir}/%{NAME}.d/01-flatpak-system-update.sh
%attr(0755,root,root) %{_sysconfdir}/%{NAME}.d/02-flatpak-user-update.sh
%attr(0755,root,root) %{_sysconfdir}/%{NAME}.d/03-flatpak-system-repair-cleanup.sh
%attr(0755,root,root) %{_sysconfdir}/%{NAME}.d/04-flatpak-user-repair-cleanup.sh
%attr(0755,root,root) %{_sysconfdir}/%{NAME}.d/05-distrobox-user-update.sh

%changelog
%autochangelog
