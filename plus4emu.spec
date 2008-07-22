Name:           plus4emu
Version:        1.2.8
Release:        1%{?dist}
Summary:        Portable emulator of the Commodore 264 family of computers
Group:          Applications/Emulators
License:        GPLv2+
URL:            http://plus4emu.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:        %{name}.png
Source2:        README_%{name}.dribble
Patch0:         %{name}-1.2.7-userpmopts.patch
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
%patch0 -p0
%patch1 -p1

# Insert the compiler optflags
sed -i 's|insertrpmflags|%{optflags}|' SConstruct

# Fix EOL chars
sed -i 's/\r//' README NEWS

# Rename makecfg to a less generic name to avoid possible conflicts
sed -i 's|makecfg|%{name}-makecfg|' gui/main.cpp README


%build
scons %{?_smp_mflags}

# Build desktop icon
cat >%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=Plus4emu
GenericName=Commodore 264 series emulator
Comment=%{summary}
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;Emulator;
EOF


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
install -pm0644 %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
install -pm0644 %{SOURCE2} README.dribble
install -pm0755 plus4emu tapconv %{buildroot}%{_bindir}
install -pm0755 makecfg %{buildroot}%{_bindir}/%{name}-makecfg

desktop-file-install --vendor dribble \
                     --dir %{buildroot}%{_datadir}/applications \
                     %{name}.desktop


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
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/applications/dribble-%{name}.desktop
%doc README COPYING NEWS README.dribble


%changelog
* Tue Jul 22 2008 Andrea Musuruane <musuruan@gmail.com> - 1.2.8-1
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
