%global qt_module qtspeech

#global examples 1

%bcond flite 0%{?fedora}

Summary: Qt6 - Speech component
Name:    qt6-%{qt_module}
Version: 6.8.1
Release: 1%{?dist}.1

# Code can be either LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only
# See e.g. src/plugins/speechdispatcher or src/tts
# Examples are under BSD-3-Clause
License: (GPL-2.0-only OR LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0) AND BSD-3-Clause
Url:     http://www.qt.io
%qt_source
%global majmin %(echo %{version} | cut -d. -f1-2)

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: qt6-qtbase-devel >= %{version}
BuildRequires: qt6-qtmultimedia-devel >= %{version}
BuildRequires: qt6-qtdeclarative-devel >= %{version}
BuildRequires: speech-dispatcher-devel >= 0.8
%if %{with flite}
BuildRequires: flite-devel
%endif

BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}

%if %{with flite}
Recommends:    (%{name}-flite%{?_isa} = %{version}-%{release} if flite)
%endif
Recommends:    (%{name}-speechd%{?_isa} = %{version}-%{release} if speech-dispatcher)

%description
The module enables a Qt application to support accessibility features
such as text-to-speech, which is useful for end-users who are visually
challenged or cannot access the application for whatever reason. The
most common use case where text-to-speech comes in handy is when the
end-user is driving and cannot attend the incoming messages on the phone.
In such a scenario, the messaging application can read out the incoming
message. Qt Serial Port provides the basic functionality, which includes
configuring, I/O operations, getting and setting the control signals of
the RS-232 pinouts.

%if %{with flite}
%package flite
Summary: Festival Lite text-to-speech engine for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description flite
%{summary}.
%endif

%package speechd
Summary: Speech Dispatcher text-to-speech engine for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description speechd
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
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
%{_qt6_archdatadir}/sbom/%{qt_module}-%{version_no_git}.spdx
%license LICENSES/GPL* LICENSES/LGPL* LICENSES/BSD*
%{_qt6_libdir}/libQt6TextToSpeech.so.6{,.*}
%dir %{_qt6_plugindir}/texttospeech
%{_qt6_plugindir}/texttospeech/libqtexttospeech_mock.so
%dir %{_qt6_qmldir}/QtTextToSpeech
%{_qt6_qmldir}/QtTextToSpeech/*
%dir %{_qt6_libdir}/cmake/Qt6TextToSpeech

%if %{with flite}
%files flite
%{_qt6_plugindir}/texttospeech/libqtexttospeech_flite.so
%{_qt6_libdir}/cmake/Qt6TextToSpeech/Qt6QTextToSpeechFlitePlugin*.cmake
%endif

%files speechd
%{_qt6_plugindir}/texttospeech/libqtexttospeech_speechd.so
%{_qt6_libdir}/cmake/Qt6TextToSpeech/Qt6QTextToSpeechSpeechdPlugin*.cmake

%files devel
%dir %{_qt6_headerdir}/QtTextToSpeech
%{_qt6_headerdir}/QtTextToSpeech/*
%{_qt6_libdir}/libQt6TextToSpeech.so
%{_qt6_libdir}/libQt6TextToSpeech.prl
%{_qt6_libdir}/cmake/Qt6/*.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6TextToSpeech
%{_qt6_libdir}/cmake/Qt6TextToSpeech/Qt6QTextToSpeechMockPlugin*.cmake
%{_qt6_libdir}/cmake/Qt6TextToSpeech/Qt6TextToSpeech*.cmake
%{_qt6_libdir}/pkgconfig/Qt6TextToSpeech.pc
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_texttospeech*.pri
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/qt6/metatypes/*.json

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif

%changelog
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

* Wed Aug 09 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 6.5.2-3
- Separate flite and speechd subpackages

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

* Mon Feb 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-1
- Initial package
