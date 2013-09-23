
%global qt_module qtwayland

Summary:        Qt5 - Wayland platform support and QtCompositor module
Name:           qt5-%{qt_module}
Version:        5.1.0
Release:        1.20130826git3b0b90b%{?dist}
# Full license texts are yet to be included upstream:
# https://codereview.qt-project.org/65586
License:        LGPLv2 with exceptions or GPLv3 with exceptions
Url:            http://qt-project.org/wiki/QtWayland
# git clone --no-checkout git://gitorious.org/qt/qtwayland.git
# cd qtwayland/
# git archive 3b0b90b --prefix=qtwayland/ |gzip >qtwayland.tar.gz
Source0:        qtwayland.tar.gz

BuildRequires:  qt5-qtbase-devel >= %{version}
BuildRequires:  qt5-qtbase-static >= %{version}
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(libudev)

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
%{summary}


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel%{?_isa}

%description devel
%{summary}.


%prep
%setup -q -n %{qt_module}


%build
%{_qt5_qmake} CONFIG+=wayland-compositor
(cd src/compositor; syncqt.pl -check-includes -module QtCompositor -version %{version} -outdir %{_builddir}/%{?buildsubdir})
make %{?_smp_mflags}


%install
make install INSTALL_ROOT=$RPM_BUILD_ROOT
install -pm644 src/compositor/{wayland-wayland-server-protocol.h,qwayland-server-wayland.h} \
        $RPM_BUILD_ROOT%{_qt5_headerdir}/QtCompositor/%{version}/QtCompositor/private


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig

%files
%{_qt5_plugindir}/platforms
%{_qt5_plugindir}/waylandcompositors
%{_qt5_libdir}/libQt5Compositor.so.5*
%exclude %{_qt5_libdir}/libQt5Compositor.la
%doc README


%files devel
%{_qt5_bindir}/qtwaylandscanner
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5*.so
%{_qt5_libdir}/libQt5*.prl
%{_qt5_libdir}/cmake/Qt5*/
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri


%changelog
* Wed Sep 11 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-1.20130826git3b0b90b
- Initial packaging
