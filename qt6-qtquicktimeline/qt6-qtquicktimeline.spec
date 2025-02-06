%global commit0 dac57b3480fced40c799bc6066406ab187e7a171
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 4

%global qt_module qtquicktimeline

Summary: Qt6 - QuickTimeline plugin
Name:    qt6-%{qt_module}
Version: 6.9.0%{?bumpver:~%{bumpver}.git%{shortcommit0}}
Release: 1%{?dist}

License: GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
# Generated with ../.copr/Makefile
Source0: %{qt_module}-everywhere-src-%{version_no_tilde}.tar.xz
%global majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)


BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ninja-build
BuildRequires: qt6-rpm-macros
BuildRequires: qt6-qtbase-static
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel


%description
The Qt Quick Timeline plugin provides QML types to use timelines and keyframes
to animate Qt Quick user interfaces.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
Requires: qt6-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.

%prep
%autosetup -C -p1


%build
%cmake_qt6

%cmake_build


%install
%cmake_install

%ldconfig_scriptlets

%files
%{_qt6_archdatadir}/sbom/%{qt_module}-%{qt_version}.spdx
%license LICENSES/GPL*
%dir %{_qt6_qmldir}/QtQuick
%{_qt6_libdir}/libQt6QuickTimeline.so.6*
%{_qt6_libdir}/libQt6QuickTimelineBlendTrees.so.6*
%{_qt6_qmldir}/QtQuick/Timeline/

%files devel
%{_qt6_includedir}/QtQuickTimeline/
%{_qt6_includedir}/QtQuickTimelineBlendTrees/
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6QuickTimeline/
%{_qt6_libdir}/cmake/Qt6QuickTimeline/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6QuickTimelineBlendTrees/
%{_qt6_libdir}/cmake/Qt6QuickTimelineBlendTrees/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTimelineBlendTreesPrivate/
%{_qt6_libdir}/cmake/Qt6QuickTimelinePrivate/
%{_qt6_libdir}/libQt6QuickTimeline.prl
%{_qt6_libdir}/libQt6QuickTimeline.so
%{_qt6_libdir}/libQt6QuickTimeline.prl
%{_qt6_libdir}/libQt6QuickTimeline.so
%{_qt6_libdir}/libQt6QuickTimelineBlendTrees.prl
%{_qt6_libdir}/libQt6QuickTimelineBlendTrees.so
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/pkgconfig/*.pc

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

* Thu Feb 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-1
- 6.6.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.1-1
- 6.6.1

* Tue Oct 10 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-1
- 6.6.0

* Sun Oct 01 2023 Justin Zobel <justin.zobel@gmail.com> - 6.5.3-1
- new version

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 21 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-1
- 6.5.2

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-3
- Rebuild for qtbase private API version change

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-2
- Rebuild for qtbase private API version change

* Mon May 22 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-1
- 6.5.1

* Tue Apr 04 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-1
- 6.5.0

* Thu Mar 23 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-1
- 6.4.3

* Tue Jan 31 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-1
- 6.4.2

* Wed Nov 23 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.1-1
- 6.4.1

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.0-1
- 6.4.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.1-1
- 6.3.1

* Wed Apr 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.0-1
- 6.3.0

* Fri Feb 25 2022 Jan Grulich <jgrulich@redhat.com> - 6.2.3-2
- Enable s390x builds

* Mon Jan 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.2.3-1
- 6.2.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.2-1
- 6.2.2

* Fri Oct 29 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.1-1
- 6.2.1

* Thu Sep 30 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0-1
- 6.2.0

* Mon Sep 27 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc2-1
- 6.2.0 - rc2

* Sat Sep 18 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc-1
- 6.2.0 - rc

* Mon Sep 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-1
- 6.2.0 - beta4

* Thu Aug 12 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.2-1
- 6.1.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 07 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.1-1
- 6.1.1

* Thu May 06 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-1
- 6.1.0

* Mon Apr 05 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.3-1
- 6.0.3

* Thu Feb 04 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.1-1
- 6.0.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.0-1
- 6.0.0
