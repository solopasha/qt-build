%global commit0 df02d1e5da06cc9a2e33b89b2ef32c6afa151452
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 8

%global qt_module qtgrpc

#global examples 1

Summary: Qt6 - Support for using gRPC and Protobuf
Name:    qt6-%{qt_module}
Version: 6.9.0%{?bumpver:~%{bumpver}.git%{shortcommit0}}
Release: 1%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
# Generated with ../.copr/Makefile
Source0: %{qt_module}-everywhere-src-%{version_no_tilde}.tar.xz
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)


# filter plugin provides
%global __provides_exclude_from ^%{_qt6_plugindir}/.*\\.so$

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: qt6-qtbase-devel
BuildRequires: qt6-qtdeclarative-devel
BuildRequires: pkgconfig(grpc++)
BuildRequires: pkgconfig(libprotobuf-c)
BuildRequires: pkgconfig(protobuf)
BuildRequires: zlib-static

BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}

%description
Protocol Buffers (Protobuf) is a cross-platform data format used to
serialize structured data. gRPC provides a remote procedure call
framework based on Protobuf. Qt provides tooling and classes to
use these technologies.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
Requires: pkgconfig(grpc++)
Requires: pkgconfig(protobuf)
%description devel
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.
%endif

%prep
%autosetup -C -p1


%build
%cmake_qt6 \
    -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF} \
    -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF}

%cmake_build


%install
%cmake_install


%files
%{_qt6_archdatadir}/sbom/%{qt_module}-%{qt_version}.spdx
%license LICENSES/GPL* LICENSES/LGPL*
%{_qt6_archdatadir}/qml/QtGrpc/
%{_qt6_archdatadir}/qml/QtProtobuf/
%{_qt6_libdir}/libQt6Grpc.so.6*
%{_qt6_libdir}/libQt6GrpcQuick.so.6*
%{_qt6_libdir}/libQt6Protobuf.so.6*
%{_qt6_libdir}/libQt6ProtobufQtCoreTypes.so.6*
%{_qt6_libdir}/libQt6ProtobufQtGuiTypes.so.6*
%{_qt6_libdir}/libQt6ProtobufQuick.so.6*
%{_qt6_libdir}/libQt6ProtobufWellKnownTypes.so.6*

%files devel
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%{_qt6_headerdir}/QtGrpc/
%{_qt6_headerdir}/QtProtobufQuick/
%{_qt6_headerdir}/QtProtobuf/
%{_qt6_headerdir}/QtProtobufQtCoreTypes/
%{_qt6_headerdir}/QtProtobufQtGuiTypes/
%{_qt6_headerdir}/QtProtobufWellKnownTypes/
%{_qt6_headerdir}/QtGrpcQuick/
%{_qt6_libdir}/libQt6Grpc.so
%{_qt6_libdir}/libQt6Protobuf.so
%{_qt6_libdir}/libQt6ProtobufQtCoreTypes.so
%{_qt6_libdir}/libQt6ProtobufQtGuiTypes.so
%{_qt6_libdir}/libQt6ProtobufWellKnownTypes.so
%{_qt6_libdir}/libQt6Grpc.prl
%{_qt6_libdir}/libQt6Protobuf.prl
%{_qt6_libdir}/libQt6ProtobufWellKnownTypes.prl
%{_qt6_libdir}/libQt6ProtobufQtCoreTypes.prl
%{_qt6_libdir}/libQt6ProtobufQtGuiTypes.prl
%{_qt6_libdir}/libQt6GrpcQuick.so
%{_qt6_libdir}/libQt6GrpcQuick.prl
%{_qt6_libdir}/libQt6ProtobufQuick.prl
%{_qt6_libdir}/libQt6ProtobufQuick.so
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtGrpcTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6GrpcTools/
%{_qt6_libdir}/cmake/Qt6GrpcTools/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Grpc/
%{_qt6_libdir}/cmake/Qt6Grpc/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Protobuf/
%{_qt6_libdir}/cmake/Qt6Protobuf/*.cmake*
%dir %{_qt6_libdir}/cmake/Qt6ProtobufQtCoreTypes/
%{_qt6_libdir}/cmake/Qt6ProtobufQtCoreTypes/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6ProtobufQtGuiTypes/
%{_qt6_libdir}/cmake/Qt6ProtobufQtGuiTypes/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6ProtobufTools/
%{_qt6_libdir}/cmake/Qt6ProtobufTools/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6ProtobufWellKnownTypes/
%{_qt6_libdir}/cmake/Qt6ProtobufWellKnownTypes/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6GrpcQuick
%{_qt6_libdir}/cmake/Qt6GrpcQuick/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qt6_libdir}/cmake/Qt6ProtobufQuick/
%{_qt6_libdir}/cmake/Qt6GrpcPrivate/
%{_qt6_libdir}/cmake/Qt6GrpcQuickPrivate/
%{_qt6_libdir}/cmake/Qt6ProtobufPrivate/
%{_qt6_libdir}/cmake/Qt6ProtobufQtCoreTypesPrivate/
%{_qt6_libdir}/cmake/Qt6ProtobufQtGuiTypesPrivate/
%{_qt6_libdir}/cmake/Qt6ProtobufQuickPrivate/
%{_qt6_libdir}/cmake/Qt6ProtobufWellKnownTypesPrivate/
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/pkgconfig/*.pc
%{_qt6_libexecdir}/qtgrpcgen
%{_qt6_libexecdir}/qtprotobufgen

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif

%changelog
%{?qt_snapshot_changelog_entry}
* Tue Jan 21 2025 Pavel Solovev <daron439@gmail.com> - 6.9.0~beta2-1
- new version

* Wed Dec 18 2024 Pavel Solovev <daron439@gmail.com> - 6.9.0~beta1-1
- new version

* Sat Dec 07 2024 Pavel Solovev <daron439@gmail.com> - 6.8.1-1.1
- rebuilt

* Mon Dec 02 2024 Pavel Solovev <daron439@gmail.com> - 6.8.1-1
- new version

* Tue Oct 08 2024 Pavel Solovev <daron439@gmail.com> - 6.8.0-1
- new version

* Wed Sep 25 2024 Pavel Solovev <daron439@gmail.com> - 6.8.0~rc-1
- new version

* Fri Aug 30 2024 Pavel Solovev <daron439@gmail.com> - 6.8.0~beta4-1
- new version

* Wed Aug 14 2024 Pavel Solovev <daron439@gmail.com> - 6.8.0~beta3-1
- new version

* Wed Jul 31 2024 Pavel Solovev <daron439@gmail.com> - 6.8.0~beta2-1
- new version

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 01 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-1
- 6.7.2

* Tue May 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-1
- 6.7.1

* Tue Apr 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- 6.7.0

* Mon Feb 19 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-2
- Examples: also install source files

* Thu Feb 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-1
- 6.6.2

* Sun Feb 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 6.6.1-3
- Rebuilt for abseil-cpp-20240116.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.1-1
- Imported into Fedora based on request from Cajus Pollmeier

* Thu Jan 18 2024 Cajus Pollmeier <pollmeier@gonicus.de> - 6.6.1-1
- 6.6.1

