%global gittag 88eaeed872841dabce2d6385b585464d6e270e8b
%global gitshorttag 88eaeed

%global debug_package %{nil}

Name:		razer-chroma-userland
Version:	0.0
Release:	2.git%{gitshorttag}%{?dist}
Summary:	Userland tools for controlling Razer Chroma devices

License:	GPLv2
URL:		https://github.com/pez2001/razer_chroma_drivers
Source0:	https://github.com/pez2001/razer_chroma_drivers/archive/%{gittag}.tar.gz

Provides:	razer-chroma-kmod-common
Provides:	python-razer-chroma-libs

BuildRequires:	python3-devel
BuildRequires:	dbus-devel
BuildRequires:	systemd

Requires:	razer-chroma-kmod >= 0.0
Requires:	python3
Requires:	systemd
Requires:	python-appindicator
Requires:	jq

%description
Services and bindings to allow interaction with the Razer Chroma driver.

%prep
%setup -q -n razer_chroma_drivers-%{gittag}


%build
#make %{?_smp_mflags} librazer_chroma daemon daemon_controller
make librazer_chroma daemon daemon_controller


%install
rm -rf %{buildroot}

# Share
mkdir -p %{buildroot}/%{_datadir}/razer_bcd/fx
install -m 0644 %{_builddir}/razer_chroma_drivers-%{gittag}/{LICENSE,README.md} %{buildroot}/%{_datadir}/razer_bcd
install -m 0644 %{_builddir}/razer_chroma_drivers-%{gittag}/install_files/share/bash_keyboard_functions.sh %{buildroot}/%{_datadir}/razer_bcd
install -m 0755 %{_builddir}/razer_chroma_drivers-%{gittag}/install_files/share/systemd_helpers.sh %{buildroot}/%{_datadir}/razer_bcd
install -m 0755 %{_builddir}/razer_chroma_drivers-%{gittag}/daemon/fx/{pez2001_collection.so,pez2001_mixer.so,pez2001_light_blast.so,pez2001_progress_bar.so} %{buildroot}/%{_datadir}/razer_bcd/fx

# Daemon
mkdir -p %{buildroot}/usr/sbin
install -m 0755 %{_builddir}/razer_chroma_drivers-%{gittag}/daemon/razer_bcd %{buildroot}/usr/sbin

# Controller
install -m 0755 %{_builddir}/razer_chroma_drivers-%{gittag}/daemon_controller/razer_bcd_controller %{buildroot}/usr/sbin

# Python Libs
mkdir -p %{buildroot}/%{python3_sitelib}/razer
install -m 0644 %{_builddir}/razer_chroma_drivers-%{gittag}/pylib/* %{buildroot}/%{python3_sitelib}/razer

# Udev Rules
mkdir -p %{buildroot}/%{_udevrulesdir}
install -m 0644 %{_builddir}/razer_chroma_drivers-%{gittag}/install_files/udev/95-razerkbd.rules %{buildroot}/%{_udevrulesdir}/

# DBus
mkdir -p %{buildroot}/etc/dbus-1/system.d
install -m 0644 %{_builddir}/razer_chroma_drivers-%{gittag}/install_files/dbus/org.voyagerproject.razer.daemon.conf %{buildroot}/etc/dbus-1/system.d/

# Systemd
mkdir -p %{buildroot}/%{_unitdir}
install -m 0644 %{_builddir}/razer_chroma_drivers-%{gittag}/install_files/systemd/razer_bcd.service %{buildroot}/%{_unitdir}

# Razer lib
mkdir -p %{buildroot}/%{_libdir}
install -m 755 %{_builddir}/razer_chroma_drivers-%{gittag}/lib/{librazer_chroma.so,librazer_chroma_controller.so} %{buildroot}/%{_libdir}/

%files
%doc LICENSE README.md
%{_datadir}/razer_bcd/
%{python3_sitelib}/razer/
%{_udevrulesdir}/95-razerkbd.rules
%{_unitdir}/razer_bcd.service
%{_libdir}/librazer_chroma.so
%{_libdir}/librazer_chroma_controller.so
/etc/dbus-1/system.d/org.voyagerproject.razer.daemon.conf
/usr/sbin/razer_bcd_controller
/usr/sbin/razer_bcd


%changelog
* Thu Aug 18 2016 Michael Donnelly <mike@donnellyonline.com> 0.0-1
- Initial RPM for the Razer Chroma Userland Tools
