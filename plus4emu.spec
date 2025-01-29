Name:           plus4emu
Version:        1.2.10.1
Release:        20%{?dist}
Summary:        Portable emulator of the Commodore 264 family of computers
License:        GPLv2+
URL:            https://github.com/istvan-v/plus4emu
Source0:        https://github.com/istvan-v/plus4emu/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        README_%{name}.Fedora
Source2:        p4fliconv.desktop
Source3:        p4makecfg.desktop
Patch0:         %{name}-1.2.10.1-scons-python3.patch
Patch1:         %{name}-1.2.10-SConstruct.patch
Patch2:         %{name}-1.2.5-fixpathissue.patch

BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  fltk-fluid
BuildRequires:  libsndfile-devel
BuildRequires:  lua-devel
BuildRequires:  portaudio-devel
BuildRequires:  python3-scons
BuildRequires:  SDL-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXinerama-devel
Requires:       hicolor-icon-theme

%description
Plus4emu is an open source, portable emulator of the Commodore 264 family of
computers (C16, C116, and Plus/4), written in C++. It implements accurate, high
quality hardware emulation.


%prep
%autosetup -p1

# Remove fltk_jpeg, fltk_png, and fltk_z libraries from SConstruct
sed -i 's/ -lfltk_jpeg//' SConstruct
sed -i 's/ -lfltk_png//' SConstruct
sed -i 's/ -lfltk_z//' SConstruct

# Fix EOL chars
sed -i 's/\r//' README NEWS

# ROM images are in datadir
sed -i 's|installDirectory + "roms"|"%{_datadir}/%{name}/roms"|' installer/makecfg.cpp


%build
%set_build_flags
# Use nopkgconfig=1 to disable package checking because it fails on Fedora
scons %{?_smp_mflags} \
  VERBOSE=1 \
  nopkgconfig=1 \
  debug=1 


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 p4compress p4fliconv p4makecfg p4sconv p4tapconv plus4emu \
  %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -pm0644 resource/Cbm4.png \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps

install -pm0644 %{SOURCE1} README.Fedora

desktop-file-install --dir %{buildroot}%{_datadir}/applications \
  resource/plus4emu.desktop

desktop-file-install --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE2}

desktop-file-install --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE3}

# install ROM images
mkdir -p %{buildroot}%{_datadir}/%{name}/roms
install -pm0644 roms/* %{buildroot}%{_datadir}/%{name}/roms


%files
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/Cbm4.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/p4fliconv.desktop
%{_datadir}/applications/p4makecfg.desktop
%doc README NEWS README.Fedora
%license COPYING resource/Read_me.txt


%changelog
* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.10.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Aug 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.10.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.10.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.10.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.10.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.10.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.10.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.10.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.10.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Feb 08 2020 Andrea Musuruane <musuruan@gmail.com> - 1.2.10.1-11
- Fix FTBFS for F32

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.10.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 Andrea Musuruane <musuruan@gmail.com> - 1.2.10.1-9
- Fixed building with python3 scons (BZ #5344)
- Used %%set_build_flags macro
- Removed desktop scriptlets

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.10.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.10.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.10.1-6
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 1.2.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.2.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.2.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.2.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 23 2017 Andrea Musuruane <musuruan@gmail.com> 1.2.10.1-1
- Updated to upstream 1.2.10.1

* Sat Feb 11 2017 Andrea Musuruane <musuruan@gmail.com> 1.2.10-1
- Updated to upstream 1.2.10
- Updated URL and Source0

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
