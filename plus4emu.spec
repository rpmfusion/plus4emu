%define binprefix p4

Name:           plus4emu
Version:        1.2.9.2
Release:        4%{?dist}
Summary:        Portable emulator of the Commodore 264 family of computers
Group:          Applications/Emulators
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
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  desktop-file-utils
BuildRequires:  fltk-fluid >= 1.1.0
BuildRequires:  libsndfile-devel
BuildRequires:  lua-devel
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
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
install -pm0644 %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
install -pm0644 %{SOURCE2} README.Fedora
install -pm0755 p4fliconv p4sconv plus4emu tapconv %{buildroot}%{_bindir}
install -pm0755 makecfg %{buildroot}%{_bindir}/%{binprefix}makecfg
install -pm0755 compress %{buildroot}%{_bindir}/%{binprefix}compress

desktop-file-install --vendor dribble \
                     --dir %{buildroot}%{_datadir}/applications \
                     %{SOURCE3}

desktop-file-install --vendor '' \
                     --dir %{buildroot}%{_datadir}/applications \
                     %{SOURCE4}

desktop-file-install --vendor '' \
                     --dir %{buildroot}%{_datadir}/applications \
                     %{SOURCE5}

# install ROM images
mkdir -p %{buildroot}%{_datadir}/%{name}/roms
install -pm0644 roms/* %{buildroot}%{_datadir}/%{name}/roms

%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/applications/p4fliconv.desktop
%{_datadir}/applications/%{binprefix}makecfg.desktop
%doc README COPYING NEWS README.Fedora


%changelog
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

* Sun Jan 21 2008 Ian Chapman <packages[AT]amiga-hardware.com> 1.2.5-2
- Dropped fltk-devel BR, fltk-fluid pulls it in anyway
- Minor cleanups

* Fri Jan 11 2008 Ian Chapman <packages[AT]amiga-hardware.com> 1.2.5-1
- Initial release
