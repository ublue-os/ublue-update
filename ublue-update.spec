Name:          {{{ git_dir_name }}}
Vendor:        ublue-os
Version:       {{{ ublue_update_version }}}
Release:       1%{?dist}
Summary:       Centralized update service/checker made for Universal Blue
License:       Apache-2.0
URL:           https://github.com/%{vendor}/%{name}
# Detailed information about the source Git repository and the source commit
# for the created rpm package
VCS:           {{{ git_dir_vcs }}}

# git_dir_pack macro places the repository content (the source files) into a tarball
# and returns its filename. The tarball will be used to build the rpm.
Source:        {{{ git_dir_pack }}}

BuildArch:     noarch
Supplements:   rpm-ostree flatpak
BuildRequires: make
BuildRequires: systemd-rpm-macros
BuildRequires: black
BuildRequires: ShellCheck
BuildRequires: python-flake8
BuildRequires: python-build
BuildRequires: python-setuptools
BuildRequires: python
BuildRequires: python-pip
BuildRequires: python-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: python-setuptools_scm
BuildRequires: python-wheel
Requires:      skopeo
Requires:      libnotify
Requires:      sudo
Requires:      jq

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^ublue%-", ""); print(t)}

%description
Installs and configures ublue-update script, systemd services, and systemd timers for auto update

%prep
{{{ git_dir_setup_macro }}}

%build
ls
ls src
black src
flake8 src
shellcheck files/etc/%{NAME}.d/user/*.sh
shellcheck files/etc/%{NAME}.d/system/*.sh
black files/etc/%{NAME}.d/system/*.py
flake8 files/etc/%{NAME}.d/system/*.py
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files ublue_update
cp -rp files/etc files/usr %{buildroot}

%post
%systemd_post %{NAME}.timer

%preun
%systemd_preun %{NAME}.timer

%files -f %{pyproject_files}
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/system/%{NAME}.service
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/system/%{NAME}.timer
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/system-preset/00-%{NAME}.preset
%attr(0644,root,root) %{_exec_prefix}/etc/%{NAME}/%{NAME}.toml
%attr(0755,root,root) %{_sysconfdir}/%{NAME}.d/user/*
%attr(0755,root,root) %{_sysconfdir}/%{NAME}.d/system/*
%attr(0644,root,root) %{_exec_prefix}/etc/polkit-1/rules.d/%{NAME}.rules

%changelog
%autochangelog
