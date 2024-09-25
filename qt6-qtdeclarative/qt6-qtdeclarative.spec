
%global qt_module qtdeclarative

%define _lto_cflags %{nil}

# definition borrowed from qtbase
%global multilib_archs x86_64 %{ix86} %{?mips} ppc64 ppc s390x s390 sparc64 sparcv9

%global examples 1

Summary: Qt6 - QtDeclarative component
Name:    qt6-%{qt_module}
Version: 6.8.0~rc
Release: 1%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%qt_source
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)


# header file to workaround multilib issue
# https://bugzilla.redhat.com/show_bug.cgi?id=1441343
Source5: qv4global_p-multilib.h

## upstream patches

## upstreamable patches

# filter qml provides
%global __provides_exclude_from ^%{_qt6_archdatadir}/qml/.*\\.so$

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ninja-build
BuildRequires: qt6-rpm-macros
BuildRequires: qt6-qtbase-devel >= %{version}
BuildRequires: qt6-qtbase-private-devel
BuildRequires: qt6-qtbase-static
BuildRequires: qt6-qtlanguageserver-devel >= %{version}
BuildRequires: qt6-qtshadertools-devel >= %{version}
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: python%{python3_pkgversion}
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1

%if 0%{?tests}
BuildRequires: dbus-x11
BuildRequires: mesa-dri-drivers
BuildRequires: time
BuildRequires: xorg-x11-server-Xvfb
%endif

Obsoletes:     qt6-qtquickcontrols2 < 6.2.0~beta3-1
Provides:      qt6-qtquickcontrols2 = %{version}-%{release}

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Provides:  %{name}-private-devel = %{version}-%{release}
Requires:  %{name}%{?_isa} = %{version}-%{release}
Requires:  qt6-qtbase-devel%{?_isa}
Obsoletes: qt6-qtquickcontrols2-devel < 6.2.0~beta3-1
Provides:  qt6-qtquickcontrols2-devel = %{version}-%{release}
%description devel
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires:  %{name}%{?_isa} = %{version}-%{release}
Obsoletes: qt6-qtquickcontrols2-examples < 6.2.0~beta3-1
Provides:  qt6-qtquickcontrols2-examples = %{version}-%{release}
# BuildRequires: qt6-qtdeclarative-devel >= %{version}
%description examples
%{summary}.
%endif

%prep
%autosetup -n %{sourcerootdir} -p1


%build

# HACK so calls to "python" get what we want
ln -s %{__python3} python
export PATH=`pwd`:$PATH

%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF} \
  -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF}

%cmake_build


%install
%cmake_install

%ifarch %{multilib_archs}
# multilib: qv4global_p.h
  mv %{buildroot}%{_qt6_headerdir}/QtQml/%{qt_version}/QtQml/private/qv4global_p.h \
     %{buildroot}%{_qt6_headerdir}/QtQml/%{qt_version}/QtQml/private/qv4global_p-%{__isa_bits}.h
  install -p -m644 -D %{SOURCE5} %{buildroot}%{_qt6_headerdir}/QtQml/%{qt_version}/QtQml/private/qv4global_p.h
%endif

# hardlink files to %{_bindir}, add -qt6 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt6_bindir}
for i in * ; do
  case "${i}" in
    qmlcachegen|qmlleasing|qmlformat|qmleasing|qmlimportscanner|qmllint| \
    qmlpreview|qmlscene|qmltestrunner|qmltyperegistrar|qmlplugindump| \
    qmlprofiler|qml|qmlbundle|qmlmin|qmltime)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt6
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  rm -fv "$(basename ${prl_file} .prl).la"
  sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
done
popd

%check
%if 0%{?tests}
export CTEST_OUTPUT_ON_FAILURE=1
export PATH=%{buildroot}%{_qt6_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt6_libdir}
make sub-tests-all %{?_smp_mflags}
xvfb-run -a \
dbus-launch --exit-with-session \
time \
make check -k -C tests ||:
%endif


%ldconfig_scriptlets

%files
%license LICENSES/LGPL*
%{_qt6_libdir}/libQt6LabsAnimation.so.6*
%{_qt6_libdir}/libQt6LabsFolderListModel.so.6*
%{_qt6_libdir}/libQt6LabsQmlModels.so.6*
%{_qt6_libdir}/libQt6LabsSettings.so.6*
%{_qt6_libdir}/libQt6LabsSharedImage.so.6*
%{_qt6_libdir}/libQt6LabsWavefrontMesh.so.6*
%{_qt6_libdir}/libQt6QmlLocalStorage.so.6*
%{_qt6_libdir}/libQt6QmlNetwork.so.6*
%{_qt6_libdir}/libQt6Qml.so.6*
%{_qt6_libdir}/libQt6QmlCompiler.so.*
%{_qt6_libdir}/libQt6QmlCore.so.6*
%{_qt6_libdir}/libQt6QmlModels.so.6*
%{_qt6_libdir}/libQt6QmlWorkerScript.so.6*
%{_qt6_libdir}/libQt6Quick*.so.6*
%{_qt6_libdir}/libQt6QuickControls2.so.6*
%{_qt6_libdir}/libQt6QuickControls2Impl.so.6*
%{_qt6_libdir}/libQt6QuickDialogs2.so.6*
%{_qt6_libdir}/libQt6QuickDialogs2QuickImpl.so.6*
%{_qt6_libdir}/libQt6QuickDialogs2Utils.so.6*
%{_qt6_libdir}/libQt6QuickEffects.so.6*
%{_qt6_libdir}/libQt6QuickLayouts.so.6*
%{_qt6_libdir}/libQt6QuickWidgets.so.6*
%{_qt6_libdir}/libQt6QuickParticles.so.6*
%{_qt6_libdir}/libQt6QuickShapes.so.6*
%{_qt6_libdir}/libQt6QuickTest.so.6*
%{_qt6_libdir}/libQt6QuickTemplates2.so.6*
%{_qt6_libdir}/libQt6QmlXmlListModel.so.6*
%{_qt6_libdir}/libQt6QmlMeta.so.6*
%{_qt6_libdir}/libQt6LabsPlatform.so.6*
%{_qt6_plugindir}/qmltooling/
%{_qt6_plugindir}/qmllint/
%{_qt6_plugindir}/qmlls/
%{_qt6_archdatadir}/qml/

%files devel
%dir %{_qt6_libdir}/cmake/Qt6PacketProtocolPrivate
%dir %{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins
%dir %{_qt6_libdir}/cmake/Qt6QmlCompiler
%dir %{_qt6_libdir}/cmake/Qt6QmlCore
%dir %{_qt6_libdir}/cmake/Qt6QmlDebugPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlIntegration
%dir %{_qt6_libdir}/cmake/Qt6QmlImportScanner
%dir %{_qt6_libdir}/cmake/Qt6LabsAnimation
%dir %{_qt6_libdir}/cmake/Qt6LabsFolderListModel
%dir %{_qt6_libdir}/cmake/Qt6LabsQmlModels
%dir %{_qt6_libdir}/cmake/Qt6LabsSettings
%dir %{_qt6_libdir}/cmake/Qt6LabsSharedImage
%dir %{_qt6_libdir}/cmake/Qt6LabsWavefrontMesh
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Basic
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2BasicStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Fusion
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2FusionStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Imagine
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2ImagineStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Material
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2MaterialStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Universal
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2UniversalStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QmlLSPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlDomPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlLocalStorage
%dir %{_qt6_libdir}/cmake/Qt6QmlModels
%dir %{_qt6_libdir}/cmake/Qt6QmlNetwork
%dir %{_qt6_libdir}/cmake/Qt6QmlTools
%dir %{_qt6_libdir}/cmake/Qt6QmlToolingSettingsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlWorkerScript
%dir %{_qt6_libdir}/cmake/Qt6QmlTypeRegistrarPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickEffectsPrivate
%dir %{_qt6_libdir}/cmake/Qt6Quick
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Impl
%dir %{_qt6_libdir}/cmake/Qt6QuickControlsTestUtilsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickDialogs2
%dir %{_qt6_libdir}/cmake/Qt6QuickDialogs2QuickImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickDialogs2Utils
%dir %{_qt6_libdir}/cmake/Qt6QuickLayouts
%dir %{_qt6_libdir}/cmake/Qt6QuickParticlesPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickShapesPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickTest
%dir %{_qt6_libdir}/cmake/Qt6QuickTestUtilsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickTemplates2
%dir %{_qt6_libdir}/cmake/Qt6QmlXmlListModel
%{_bindir}/qml*
%{_qt6_bindir}/qml*
%{_qt6_libexecdir}/qmlcachegen
%{_qt6_libexecdir}/qmlimportscanner
%{_qt6_libexecdir}/qmltyperegistrar
%{_qt6_libexecdir}/qmljsrootgen
%{_qt6_libexecdir}/qmlaotstats
%{_qt6_headerdir}/Qt*/
%{_qt6_libdir}/libQt6LabsAnimation.so
%{_qt6_libdir}/libQt6LabsFolderListModel.so
%{_qt6_libdir}/libQt6LabsQmlModels.so
%{_qt6_libdir}/libQt6LabsSettings.so
%{_qt6_libdir}/libQt6LabsSharedImage.so
%{_qt6_libdir}/libQt6LabsWavefrontMesh.so
%{_qt6_libdir}/libQt6QmlLocalStorage.so
%{_qt6_libdir}/libQt6Qml.so
%{_qt6_libdir}/libQt6QmlNetwork.so
%{_qt6_libdir}/libQt6QmlCompiler.so
%{_qt6_libdir}/libQt6QmlCore.so
%{_qt6_libdir}/libQt6QmlModels.so
%{_qt6_libdir}/libQt6QmlWorkerScript.so
%{_qt6_libdir}/libQt6Quick*.so
%{_qt6_libdir}/libQt6QmlXmlListModel.so
%{_qt6_libdir}/libQt6QmlMeta.so
%{_qt6_libdir}/libQt6LabsPlatform.so
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/objects-RelWithDebInfo/QmlTypeRegistrarPrivate_resources_1/.qt/rcc/qrc_jsRootMetaTypes_init.cpp.o
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%{_qt6_archdatadir}/mkspecs/features/*.prf
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtDeclarativeTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6PacketProtocolPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/
%{_qt6_libdir}/cmake/Qt6QmlCompiler/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlCore/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlDebugPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlIntegration/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlImportScanner/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsAnimation/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsFolderListModel/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsQmlModels/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsSettings/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsSharedImage/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsWavefrontMesh/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlLSPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlDomPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlLocalStorage/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Basic/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2BasicStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Fusion/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2FusionStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Imagine/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2ImagineStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Material/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2MaterialStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Universal/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2UniversalStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlModels/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlNetwork/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlTools/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlToolingSettingsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlWorkerScript/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlTypeRegistrarPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickEffectsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6Quick/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Impl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControlsTestUtilsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickDialogs2/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickDialogs2QuickImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickDialogs2Utils/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickLayouts/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickParticlesPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickShapesPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTest/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTestUtilsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTemplates2/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlXmlListModel/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickWidgets/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsPlatform/
%{_qt6_libdir}/cmake/Qt6QmlMeta/
%{_qt6_libdir}/cmake/Qt6QuickControls2FluentWinUI3StyleImpl/
%{_qt6_libdir}/cmake/Qt6QmlAssetDownloader/
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/pkgconfig/*.pc
%{_qt6_libdir}/libQt6*.prl

%files static
%{_qt6_libdir}/libQt6QmlDom.a
%{_qt6_libdir}/libQt6QmlLS.a
%{_qt6_libdir}/libQt6QmlTypeRegistrar.a
%{_qt6_libdir}/libQt6QmlToolingSettings.a
%{_qt6_libdir}/libQt6PacketProtocol.a
%{_qt6_libdir}/libQt6QuickControlsTestUtils.a
%{_qt6_libdir}/libQt6QuickTestUtils.a
%{_qt6_libdir}/libQt6QmlDebug.a
%{_qt6_libdir}/libQt6QmlAssetDownloader.a

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif

%changelog
* Wed Sep 25 2024 Pavel Solovev <daron439@gmail.com> - 6.8.0~rc-1
- new version

* Fri Aug 30 2024 Pavel Solovev <daron439@gmail.com> - 6.8.0~beta4-1
- new version

* Wed Aug 14 2024 Pavel Solovev <daron439@gmail.com> - 6.8.0~beta3-1
- new version

* Wed Jul 31 2024 Pavel Solovev <daron439@gmail.com> - 6.8.0~beta2-1
- new version

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-2
- Do not own /usr/lib[64]/qml directory

* Mon Jul 01 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-1
- 6.7.2

* Mon Jun 10 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-4
- Move all *prl files to -devel subpacakge

* Thu Jun 06 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-3
- Backport upstream fix - dom: avoid asserts during dom construction

* Tue May 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-2
- Rebuild for updated qtbase private api tag

* Tue May 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-1
- 6.7.1

* Wed Apr 03 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-2
- Move libQt6QmlBuiltins.a to -devel subpackage

* Tue Apr 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- 6.7.0

* Tue Apr 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-3
- Backport Qt patches for crashes

* Mon Feb 19 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-2
- Examples: also install source files

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

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-4
- Rebuild for qtlanguageserver private API version change

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-3
- Rebuild for qtbase private API version change

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-2
- Rebuild for qtbase private API version change

* Mon May 22 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-1
- 6.5.1

* Mon Apr 03 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 6.5.0-2
- Enable qmlls

* Mon Apr 03 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-1
- 6.5.0

* Thu Mar 23 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-1
- 6.4.3

* Wed Mar 15 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.4.2-5
- Backport fix for crashes in V4 JIT (#2177696)

* Fri Mar 03 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-4
- Fix directory ownership

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

* Wed May 25 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.0-2
- Enable examples

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
- Obsoletes: qt6-qtquickcontrols2

* Mon Sep 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-1
- 6.2.0 - beta4

* Mon Aug 30 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta3-1
- 6.2.0 - beta3

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

* Mon Jan 11 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.0-1
- 6.0.0
