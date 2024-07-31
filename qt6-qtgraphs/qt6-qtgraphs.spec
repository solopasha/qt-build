%global        qt_module qtgraphs

Name:          qt6-qtgraphs
Version:       6.8.0~beta4
Release:       1%{?dist}

%global examples 1

%global        majmin %(echo %{version} | cut -d. -f1-2)
%global        qt_version %(echo %{version} | cut -d~ -f1)

Summary:       The Qt Graphs module enables you to visualize data in 3D
License:       BSD-3-Clause AND GFDL-1.3-no-invariants-only AND GPL-3.0-only
URL:           https://doc.qt.io/qt-6/qtgraphs-index.html
%qt_source

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: ninja-build

BuildRequires: cmake(Qt6BuildInternals)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Quick)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6QuickWidgets)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6Quick3D)
BuildRequires: qt6-qtbase-private-devel

%description
The Qt Graphs module enables you to visualize data in 3D as bar,
scatter, and surface graphs. It's especially useful for visualizing
depth maps and large quantities of rapidly changing data, such as
data received from multiple sensors. The look and feel of graphs
can be customized by using themes or by adding custom items and labels.

Qt Graphs is built on Qt 6 and Qt Quick 3D to take advantage of
hardware acceleration and Qt Quick.

%package devel
Summary:       Development Files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.

%if 0%{?examples}
%package examples
Summary:       Programming examples for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}
%endif

%prep
%autosetup -n %{sourcerootdir} -p1

%build
%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF} \
  -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF}

%cmake_build

%install
%cmake_install

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

%files
%license LICENSES/BSD-3-Clause.txt LICENSES/GFDL*.txt LICENSES/GPL-*.txt
%{_qt6_libdir}/libQt6Graphs.so.6*
%{_qt6_libdir}/libQt6GraphsWidgets.so.6*
%{_qt6_libdir}/qt6/metatypes/qt6graphs*_relwithdebinfo_metatypes.json
%{_qt6_libdir}/qt6/modules/Graphs*.json
%{_qt6_qmldir}/QtGraphs/

%files devel
%{_qt6_headerdir}/QtGraphs/
%{_qt6_headerdir}/QtGraphsWidgets/
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtGraphsTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Graphs/
%{_qt6_libdir}/cmake/Qt6GraphsWidgets/
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6Graphsplugin*.cmake
%{_qt6_libdir}/libQt6Graphs.prl
%{_qt6_libdir}/libQt6Graphs.so
%{_qt6_libdir}/libQt6GraphsWidgets.prl
%{_qt6_libdir}/libQt6GraphsWidgets.so
%{_qt6_libdir}/pkgconfig/Qt6Graphs*.pc
%{_qt6_libdir}/qt6/mkspecs/modules/qt_lib_graphs*.pri

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif

%changelog
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

* Fri Jan 26 2024 Steve Cossette <farchord@gmail.com> - 6.6.1-1
- Initital release of qtgraphs
