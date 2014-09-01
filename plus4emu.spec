%define binprefix p4

Name:           plus4emu
Version:        1.2.9.2
Release:        8%{?dist}
Summary:        Portable emulator of the Commodore 264 family of computers
License:        GPLv2+
URL:            http://plus4emu.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:        %{name}.png
Source2:        README_%{name}.Fedora
Source3:        %{name}.desktop
Source4:        p4fliconv.desktop
Source5:        %{binprefix}makecfg.desktop
Patch0:         %{name}-1.2.9-SConstruct.patch
Patch1:         %{name}-1.2.5-fixpathissue.patch
Patch2:         %{name}-1.2.9.2-gcc45.patch
Patch3:         %{name}-1.2.9.2-gcc46.patch
Patch4:         %{name}-1.2.9.2-compat-lua.patch
BuildRequires:  desktop-file-utils
BuildRequires:  fltk-fluid >= 1.1.0
BuildRequires:  libsndfile-devel
%if 0%{?fedora} >= 20
BuildRequires:  compat-lua-devel
%else
BuildRequires:  lua-devel
%endif
BuildRequires:  portaudio-devel >= 18
BuildRequires:  scons
BuildRequires:  SDL-devel
Requires:       hicolor-icon-theme

%description
Plus4emu is an open source, portable emulator of the Commodore 264 family of
computers (C16, C116, and Plus/4), written in C++. It implements accurate, high
quality hardware emulation.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# Fix EOL chars
sed -i 's/\r//' README NEWS

# Rename makecfg to a less generic name to avoid possible conflicts
sed -i 's|makecfg|%{binprefix}makecfg|' gui/main.cpp README

# Rename compress to a less generic name to avoid possible conflicts
sed -i 's|compress -|%{binprefix}compress -|' README

# ROM images are in datadir
sed -i 's|installDirectory + "roms"|"%{_datadir}/%{name}/roms"|' installer/makecfg.cpp


%build
export CXXFLAGS="%{optflags}"
scons %{?_smp_mflags}


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
install -pm0644 %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
install -pm0644 %{SOURCE2} README.Fedora
install -pm0755 p4fliconv p4sconv plus4emu tapconv %{buildroot}%{_bindir}
install -pm0755 makecfg %{buildroot}%{_bindir}/%{binprefix}makecfg
install -pm0755 compress %{buildroot}%{_bindir}/%{binprefix}compress

desktop-file-install --dir %{buildroot}%{_datadir}/applications \
                     %{SOURCE3}

desktop-file-install --dir %{buildroot}%{_datadir}/applications \
                     %{SOURCE4}

desktop-file-install --dir %{buildroot}%{_datadir}/applications \
                     %{SOURCE5}

# install ROM images
mkdir -p %{buildroot}%{_datadir}/%{name}/roms
install -pm0644 roms/* %{buildroot}%{_datadir}/%{name}/roms


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/p4fliconv.desktop
%{_datadir}/applications/%{binprefix}makecfg.desktop
%doc README COPYING NEWS README.Fedora


%changelog
* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 1.2.9.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Dec 31 2013 Andrea Musuruane <musuruan@gmail.com> 1.2.9.2-7
- Built with compat-lua for F20+
- Dropped desktop vendor tag for F19+
- Updated icon cache scriptlets
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Dropped cleaning at the beginning of %%install

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.9.2-6
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Apr 09 2012 Andrea Musuruane <musuruan@gmail.com> 1.2.9.2-5
- Made a new patch to compile with GCC 4.5
- Made a new patch to compile with GCC 4.6

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.2.9.2-4
- Rebuilt for c++ ABI breakage

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.2.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.2.9.2-2
- rebuild for new F11 features

* Thu Dec 25 2008 Andrea Musuruane <musuruan@gmail.com> 1.2.9.2-1
- Updated to upstream 1.2.9.2
- Moved to RPM Fusion nonfree
- ROM images are now shippend in the source and therefore packaged
- Fixed sources to read ROM images from datadir
- Desktop files are no longer generated in the spec file
- Renamed README.dribble in README.Fedora

* Thu Jul 24 2008 Andrea Musuruane <musuruan@gmail.com> 1.2.8.1-1
- Updated to upstream 1.2.8.1

* Tue Jul 22 2008 Andrea Musuruane <musuruan@gmail.com> 1.2.8-1
- Updated to upstream 1.2.8

* Sun Jul 13 2008 Andrea Musuruane <musuruan@gmail.com> 1.2.7-1
- Updated to upstream 1.2.7

* Sat Jun 14 2008 Andrea Musuruane <musuruan@gmail.com> 1.2.6.1-1
- Updated to upstream 1.2.6.1
- Made a new patch to compile with GCC 4.3 (SF #1977560)
- Added a patch from upstream SVN not to require libpng-devel and 
  libjpeg-devel (SF #1977554)
- Minor clean-up

* Sun Feb 03 2008 Ian Chapman <packages[AT]amiga-hardware.com> 1.2.5-3
- GCC 4.3 fixes

* Sun Jan 20 2008 Ian Chapman <packages[AT]amiga-hardware.com> 1.2.5-2
- Dropped fltk-devel BR, fltk-fluid pulls it in anyway
- Minor cleanups

* Fri Jan 11 2008 Ian Chapman <packages[AT]amiga-hardware.com> 1.2.5-1
- Initial release
