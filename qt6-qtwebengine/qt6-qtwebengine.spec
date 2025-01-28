%global commit0 edd09e1ec4df080deee3977e010b39e3ed140471
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 2

%global qt_module qtwebengine

# package-notes causes FTBFS (#2043178)
%undefine _package_note_file

%global use_system_libwebp 1
%global use_system_jsoncpp 1
%global use_system_libicu 1

%if 0%{?fedora} && 0%{?fedora} >= 39
# Bundled python-six is too old to work with Python 3.12+
%global use_system_py_six 1
%endif

%global use_system_re2 0

# spellchecking dictionary directory
%global _qtwebengine_dictionaries_dir %{_qt6_datadir}/qtwebengine_dictionaries

# exclude plugins
%global __provides_exclude ^lib.*plugin\\.so.*$
# and designer plugins
%global __provides_exclude_from ^%{_qt6_plugindir}/.*\\.so$

#global examples 1

Summary: Qt6 - QtWebEngine components
Name:    qt6-qtwebengine
Version: 6.9.0
Release: 0.%{bumpver}.git%{shortcommit0}%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://qt-project.org/doc/qt-5.0/qtdoc/licensing.html
# The other licenses are from Chromium and the code it bundles
License: (LGPLv2 with exceptions or GPLv3 with exceptions) and BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
URL:     http://www.qt.io
# cleaned tarball with patent-encumbered codecs removed from the bundled FFmpeg
# ./qtwebengine-release.sh
# ./clean_qtwebengine.sh 6.4.1
Source0: qtwebengine-everywhere-src-%{version_no_tilde}-clean.tar.xz

# cleanup scripts used above
Source2: clean_qtwebengine.sh
Source3: clean_ffmpeg.sh
Source4: get_free_ffmpeg_source_files.py
# macros
Source10: macros.qt6-qtwebengine

# pulseaudio headers
Source20: https://src.fedoraproject.org/lookaside/pkgs/qt6-qtwebengine/pulseaudio-12.2-headers.tar.gz/sha512/a5a9bcbb16030b3bc83cc0cc8f5e7f90e0723d3e83258a5c77eacb32eaa267118a73fa7814fbcc99a24e4907916a2b371ebb6dedc4f45541c3acf6c834fd35be/pulseaudio-12.2-headers.tar.gz

Patch2:  qtwebengine-link-pipewire.patch

## Upstream patches:

## Upstreamable patches:
Patch110: qtwebengine-webrtc-system-openh264.patch
Patch111: qtwebengine-blink-system-openh264.patch
Patch112: qtwebengine-media-system-openh264.patch

# handled by qt6-srpm-macros, which defines %%qt6_qtwebengine_arches
# FIXME use/update qt6_qtwebengine_arches
# 32-bit arches not supported (https://bugreports.qt.io/browse/QTBUG-102143)
ExclusiveArch: aarch64 x86_64

BuildRequires: cmake
BuildRequires: qt6-srpm-macros
BuildRequires: qt6-qtbase-devel
BuildRequires: qt6-qtbase-private-devel
# TODO: check of = is really needed or if >= would be good enough -- rex
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel
BuildRequires: qt6-qtlocation-devel
BuildRequires: qt6-qtsensors-devel
BuildRequires: qt6-qtsvg-devel
BuildRequires: qt6-qttools-static
BuildRequires: qt6-qtquickcontrols2-devel
BuildRequires: qt6-qtwebchannel-devel
BuildRequires: qt6-qtwebsockets-devel
# for examples?
BuildRequires: ninja-build
BuildRequires: bison
BuildRequires: flex
BuildRequires: gcc-c++
%if 0%{?rhel} && 0%{?rhel} < 10
BuildRequires: gcc-toolset-13
BuildRequires: gcc-toolset-13-libatomic-devel
%endif
# gn links statically (for now)
BuildRequires: libstdc++-static
BuildRequires: git-core
BuildRequires: gperf
BuildRequires: krb5-devel
%if 0%{?use_system_libicu}
BuildRequires: libicu-devel >= 68
%endif
BuildRequires: libatomic
BuildRequires: libjpeg-devel
BuildRequires: nodejs
%if 0%{?use_system_re2}
BuildRequires: re2-devel
%else
Provides: bundled(re2)
%endif
BuildRequires: snappy-devel
BuildConflicts: minizip-devel
Provides: bundled(minizip) = 2.8.1
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(epoxy)
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(harfbuzz)
%if 0%{?use_system_jsoncpp}
BuildRequires: pkgconfig(jsoncpp)
%endif
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(libcap)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(libevent)
BuildRequires: pkgconfig(libpci)
BuildRequires: pkgconfig(libpipewire-0.3)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libudev)
%if 0%{?use_system_libwebp}
BuildRequires: pkgconfig(libwebp) >= 0.6.0
%endif
BuildRequires: pkgconfig(libopenjp2)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(nss)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(poppler-cpp)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xscrnsaver)
BuildRequires: pkgconfig(xshmfence)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(zlib)
## https://bugreports.qt.io/browse/QTBUG-59094
## requires libxml2 built with icu support
#BuildRequires: pkgconfig(libxslt) pkgconfig(libxml-2.0)
BuildRequires: perl-interpreter
BuildRequires: %{__python3}
BuildRequires: python3-html5lib
BuildRequires: pkgconfig(vpx) >= 1.8.0
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libva)
BuildRequires: pkgconfig(openh264)

%if 0%{?fedora} && 0%{?fedora} >= 39
BuildRequires: python3-zombie-imp
%endif

# extra (non-upstream) functions needed, see
# src/3rdparty/chromium/third_party/sqlite/README.chromium for details
#BuildRequires: pkgconfig(sqlite3)

# Split subpackage
Requires: qt6-qtpdf%{?_isa} = %{version}-%{release}

## Various bundled libraries that Chromium does not support unbundling :-(
## Only the parts actually built are listed.
## Query for candidates:
## grep third_party/ build.log | sed 's!third_party/!\nthird_party/!g' | \
## grep third_party/ | sed 's!^third_party/!!g' | sed 's!/.*$!!g' | \
## sed 's/\;.*$//g' | sed 's/ .*$//g' | sort | uniq | less
## some false positives where only shim headers are generated for some reason
## some false positives with dummy placeholder dirs (swiftshader, widevine)
## some false negatives where a header-only library is bundled (e.g. x86inc)
## Spot's chromium.spec also has a list that I checked.

# Of course, Chromium itself is bundled. It cannot be unbundled because it is
# not a library, but forked (modified) application code.
Provides: bundled(chromium) = 126.0.6478.165

# Bundled in src/3rdparty/chromium/third_party:
# Check src/3rdparty/chromium/third_party/*/README.chromium for version numbers,
# except where specified otherwise.
# Note that many of those libraries are git snapshots, so version numbers are
# necessarily approximate.
# Also note that the list is probably not complete anymore due to Chromium
# adding more and more bundled stuff at every release, some of which (but not
# all) is actually built in QtWebEngine.
# src/3rdparty/chromium/third_party/angle/doc/ChoosingANGLEBranch.md points to
# http://omahaproxy.appspot.com/deps.json?version=87.0.4280.144 chromium_branch
Provides: bundled(angle)
# Google's fork of OpenSSL
# We cannot build against NSS instead because it no longer works with NSS 3.21:
# HTTPS on, ironically, Google's sites (Google, YouTube, etc.) stops working
# completely and produces only ERR_SSL_PROTOCOL_ERROR errors:
# http://kaosx.us/phpBB3/viewtopic.php?t=1235
# https://bugs.launchpad.net/ubuntu/+source/chromium-browser/+bug/1520568
# So we have to do what Chromium now defaults to (since 47): a "chimera build",
# i.e., use the BoringSSL code and the system NSS certificates.
Provides: bundled(boringssl)
Provides: bundled(brotli)
# Don't get too excited. MPEG and other legally problematic stuff is stripped
# out. See clean_qtwebengine.sh, clean_ffmpeg.sh, and
# get_free_ffmpeg_source_files.py.
# see src/3rdparty/chromium/third_party/ffmpeg/Changelog for the version number
Provides: bundled(ffmpeg) = 5.1.2
Provides: bundled(hunspell) = 1.6.0
Provides: bundled(iccjpeg)
# bundled as "khronos", headers only
Provides: bundled(khronos_headers)
# bundled as "leveldatabase"
Provides: bundled(leveldb) = 1.23
# bundled as "libjingle_xmpp"
Provides: bundled(libjingle)
# see src/3rdparty/chromium/third_party/libsrtp/CHANGES for the version number
Provides: bundled(libsrtp) = 2.4.0
# bundled as "libxml"
# see src/3rdparty/chromium/third_party/libxml/linux/include/libxml/xmlversion.h
Provides: bundled(libxml2) = 2.9.13
# see src/3rdparty/chromium/third_party/libxslt/linux/config.h for version
Provides: bundled(libxslt) = 1.1.3
Provides: bundled(libyuv) = 1819
Provides: bundled(modp_b64)
Provides: bundled(ots)
Provides: bundled(re2)
# see src/3rdparty/chromium/third_party/protobuf/CHANGES.txt for the version
Provides: bundled(protobuf) = 3.13.0.1
Provides: bundled(qcms) = 4
Provides: bundled(skia)
# bundled as "smhasher"
Provides: bundled(SMHasher) = 0-147
Provides: bundled(sqlite) = 3.39.4
Provides: bundled(usrsctp)
Provides: bundled(webrtc) = 90

%ifarch %{ix86} x86_64
# bundled by ffmpeg and libvpx:
# header (for assembly) only
Provides: bundled(x86inc)
%endif

# Bundled in src/3rdparty/chromium/base/third_party:
# Check src/3rdparty/chromium/third_party/base/*/README.chromium for version
# numbers, except where specified otherwise.
Provides: bundled(dynamic_annotations) = 4384
Provides: bundled(superfasthash) = 0
Provides: bundled(symbolize)
# bundled as "valgrind", headers only
Provides: bundled(valgrind.h)
# bundled as "xdg_mime"
Provides: bundled(xdg-mime)
# bundled as "xdg_user_dirs"
Provides: bundled(xdg-user-dirs) = 0.10

# Bundled in src/3rdparty/chromium/net/third_party:
# Check src/3rdparty/chromium/third_party/net/*/README.chromium for version
# numbers, except where specified otherwise.
Provides: bundled(mozilla_security_manager) = 1.9.2

# Bundled in src/3rdparty/chromium/url/third_party:
# Check src/3rdparty/chromium/third_party/url/*/README.chromium for version
# numbers, except where specified otherwise.
# bundled as "mozilla", file renamed and modified
Provides: bundled(nsURLParsers)

# Bundled outside of third_party, apparently not considered as such by Chromium:
Provides: bundled(mojo)
# see src/3rdparty/chromium/v8/include/v8_version.h for the version number
Provides: bundled(v8) = 11.8.172.18
# bundled by v8 (src/3rdparty/chromium/v8/src/base/ieee754.cc)
# The version number is 5.3, the last version that upstream released, years ago:
# http://www.netlib.org/fdlibm/readme
Provides: bundled(fdlibm) = 5.3

%{?_qt6_version:Requires: qt6-qtbase%{?_isa} = %{_qt6_version}}

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
Requires: qt6-qtdeclarative-devel%{?_isa}
Requires: qt6-qtpdf-devel%{?_isa} = %{version}-%{release}
# not arch'd for now, see if can get away with avoiding multilib'ing -- rex
Requires: %{name}-devtools = %{version}-%{release}
%description devel
%{summary}.

%package devtools
Summary: WebEngine devtools_resources
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devtools
Support for remote debugging.

%if 0%{?examples}
%package examples
Summary: Example files for %{name}
%description examples
%{summary}.
%endif

%package -n qt6-qtpdf
Summary: Qt6 - QtPdf components
%description -n qt6-qtpdf
%{summary}.

%package -n qt6-qtpdf-devel
Summary: Development files for qt6-qtpdf
Requires: qt6-qtpdf%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
Requires: qt6-qtdeclarative-devel%{?_isa}
%description -n qt6-qtpdf-devel
%{summary}.

%package -n qt6-qtpdf-examples
Summary: Example files for qt6-qtpdf

%description -n qt6-qtpdf-examples
%{summary}.

%prep
%autosetup -n qtwebengine-everywhere-src-%{version_no_tilde} -p1 -a20

sed -i -e 's/symbol_level=[[:digit:]]/symbol_level=1/g' cmake/Functions.cmake

mv pulse src/3rdparty/chromium/

pushd src/3rdparty/chromium
popd

# delete all "toolprefix = " lines from build/toolchain/linux/BUILD.gn, as we
# never cross-compile in native Fedora RPMs, fixes ARM and aarch64 FTBFS
sed -i -e '/toolprefix = /d' -e 's/\${toolprefix}//g' \
  src/3rdparty/chromium/build/toolchain/linux/BUILD.gn

%if 0%{?use_system_py_six}
rm src/3rdparty/chromium/third_party/six/src/six.py
rm src/3rdparty/chromium/third_party/catapult/third_party/six/six.py
rm src/3rdparty/chromium/third_party/wpt_tools/wpt/tools/third_party/six/six.py

ln -s /usr/lib/python%{python3_version}/site-packages/six.py src/3rdparty/chromium/third_party/six/src/six.py
ln -s /usr/lib/python%{python3_version}/site-packages/six.py src/3rdparty/chromium/third_party/catapult/third_party/six/six.py
ln -s /usr/lib/python%{python3_version}/site-packages/six.py src/3rdparty/chromium/third_party/wpt_tools/wpt/tools/third_party/six/six.py
%endif

# copy the Chromium license so it is installed with the appropriate name
cp -p src/3rdparty/chromium/LICENSE LICENSE.Chromium

# consider doing this as part of the tarball creation step instead?  rdieter
# fix/workaround
# fatal error: QtWebEngineCore/qtwebenginecoreglobal.h: No such file or directory
# if [ ! -f "./include/QtWebEngineCore/qtwebenginecoreglobal.h" ]; then
# {_qt6_libexecdir}/syncqt -version {version}
# fi
#
# # abort if this doesn't get created by syncqt.pl
# test -f "./include/QtWebEngineCore/qtwebenginecoreglobal.h"


%build
%global _vpath_builddir b
%if 0%{?rhel} && 0%{?rhel} < 10
. /opt/rh/gcc-toolset-13/enable
%endif
export STRIP=strip
export NINJAFLAGS="%{__ninja_common_opts}"
export NINJA_PATH=%{__ninja}

%cmake_qt6 \
  -DCMAKE_TOOLCHAIN_FILE:STRING="%{_libdir}/cmake/Qt6/qt.toolchain.cmake" \
  -DFEATURE_qtpdf_build:BOOL=ON \
  -DFEATURE_webengine_developer_build:BOOL=OFF \
  -DFEATURE_webengine_embedded_build:BOOL=OFF \
  -DFEATURE_webengine_extensions:BOOL=ON \
  -DFEATURE_webengine_kerberos:BOOL=ON \
  -DFEATURE_webengine_native_spellchecker:BOOL=OFF \
  -DFEATURE_webengine_printing_and_pdf:BOOL=ON \
  -DFEATURE_webengine_proprietary_codecs:BOOL=ON \
  -DFEATURE_webengine_system_icu:BOOL=%{?use_system_libicu} \
  -DFEATURE_webengine_system_libevent:BOOL=ON \
  -DFEATURE_webengine_system_ffmpeg:BOOL=ON \
%if 0%{?use_system_re2}
  -DQT_FEATURE_webengine_system_re2=ON \
%endif
  -DFEATURE_webengine_webrtc:BOOL=ON \
  -DFEATURE_webengine_webrtc_pipewire:BOOL=ON \
  -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF} \
  -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF}

%cmake_build


%install
%cmake_install

# rpm macros
install -p -m644 -D %{SOURCE10} \
  %{buildroot}%{_rpmmacrodir}/macros.qt6-qtwebengine
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{_rpmmacrodir}/macros.qt6-qtwebengine

# .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
# explicitly omit, at least until there's a real library installed associated with it -- rex
rm -fv Qt6WebEngineCore.la
popd

mkdir -p %{buildroot}%{_qtwebengine_dictionaries_dir}

# adjust cmake dep(s) to allow for using the same Qt6 that was used to build it
# using the lesser of %%version, %%_qt6_version
%global lesser_version $(echo -e "%{version}\\n%{_qt6_version}" | sort -V | head -1)
sed -i -e "s|%{version} \${_Qt6WebEngine|%{lesser_version} \${_Qt6WebEngine|" \
  %{buildroot}%{_qt6_libdir}/cmake/Qt6WebEngine*/Qt6WebEngine*Config.cmake


%if 0%{?rhel} && 0%{?rhel} < 10
%filetriggerin -- %{_datadir}/myspell
%else
%filetriggerin -- %{_datadir}/hunspell
%endif

while read filename ; do
  case "$filename" in
    *.dic)
      bdicname=%{_qtwebengine_dictionaries_dir}/`basename -s .dic "$filename"`.bdic
      %{_qt6_libdir}/qt6/libexec/qwebengine_convert_dict "$filename" "$bdicname" &> /dev/null || :
      ;;
  esac
done

%files
%license LICENSE.*
%{_qt6_archdatadir}/sbom/%{qt_module}-%{version_no_git}.spdx
%{_qt6_libdir}/libQt6WebEngineCore.so.*
%{_qt6_libdir}/libQt6WebEngineQuick.so.*
%{_qt6_libdir}/libQt6WebEngineQuickDelegatesQml.so.*
%{_qt6_libdir}/libQt6WebEngineWidgets.so.*
%{_qt6_libdir}/qt6/libexec/qwebengine_convert_dict
%{_qt6_libdir}/qt6/libexec/QtWebEngineProcess
%{_qt6_libdir}/qt6/libexec/webenginedriver
%dir %{_qt6_libdir}/qt6/qml/QtWebEngine
%{_qt6_libdir}/qt6/qml/QtWebEngine/*
%dir %{_qt6_datadir}/resources/
%{_qt6_datadir}/resources/v8_context_snapshot.bin
%{_qt6_datadir}/resources/qtwebengine_resources.pak
%{_qt6_datadir}/resources/qtwebengine_resources_100p.pak
%{_qt6_datadir}/resources/qtwebengine_resources_200p.pak
%if ! 0%{?use_system_libicu}
%{_qt6_datadir}/resources/icudtl.dat
%endif
%dir %{_qtwebengine_dictionaries_dir}
%dir %{_qt6_translationdir}/qtwebengine_locales
%lang(am) %{_qt6_translationdir}/qtwebengine_locales/am.pak
%lang(ar) %{_qt6_translationdir}/qtwebengine_locales/ar.pak
%lang(bg) %{_qt6_translationdir}/qtwebengine_locales/bg.pak
%lang(bn) %{_qt6_translationdir}/qtwebengine_locales/bn.pak
%lang(ca) %{_qt6_translationdir}/qtwebengine_locales/ca.pak
%lang(cs) %{_qt6_translationdir}/qtwebengine_locales/cs.pak
%lang(da) %{_qt6_translationdir}/qtwebengine_locales/da.pak
%lang(de) %{_qt6_translationdir}/qtwebengine_locales/de.pak
%lang(el) %{_qt6_translationdir}/qtwebengine_locales/el.pak
%lang(en) %{_qt6_translationdir}/qtwebengine_locales/en-GB.pak
%lang(en) %{_qt6_translationdir}/qtwebengine_locales/en-US.pak
%lang(es) %{_qt6_translationdir}/qtwebengine_locales/es-419.pak
%lang(es) %{_qt6_translationdir}/qtwebengine_locales/es.pak
%lang(et) %{_qt6_translationdir}/qtwebengine_locales/et.pak
%lang(fa) %{_qt6_translationdir}/qtwebengine_locales/fa.pak
%lang(fi) %{_qt6_translationdir}/qtwebengine_locales/fi.pak
%lang(fil) %{_qt6_translationdir}/qtwebengine_locales/fil.pak
%lang(fr) %{_qt6_translationdir}/qtwebengine_locales/fr.pak
%lang(gu) %{_qt6_translationdir}/qtwebengine_locales/gu.pak
%lang(he) %{_qt6_translationdir}/qtwebengine_locales/he.pak
%lang(hi) %{_qt6_translationdir}/qtwebengine_locales/hi.pak
%lang(hr) %{_qt6_translationdir}/qtwebengine_locales/hr.pak
%lang(hu) %{_qt6_translationdir}/qtwebengine_locales/hu.pak
%lang(id) %{_qt6_translationdir}/qtwebengine_locales/id.pak
%lang(it) %{_qt6_translationdir}/qtwebengine_locales/it.pak
%lang(ja) %{_qt6_translationdir}/qtwebengine_locales/ja.pak
%lang(kn) %{_qt6_translationdir}/qtwebengine_locales/kn.pak
%lang(ko) %{_qt6_translationdir}/qtwebengine_locales/ko.pak
%lang(lt) %{_qt6_translationdir}/qtwebengine_locales/lt.pak
%lang(lv) %{_qt6_translationdir}/qtwebengine_locales/lv.pak
%lang(ml) %{_qt6_translationdir}/qtwebengine_locales/ml.pak
%lang(mr) %{_qt6_translationdir}/qtwebengine_locales/mr.pak
%lang(ms) %{_qt6_translationdir}/qtwebengine_locales/ms.pak
%lang(nb) %{_qt6_translationdir}/qtwebengine_locales/nb.pak
%lang(nl) %{_qt6_translationdir}/qtwebengine_locales/nl.pak
%lang(pl) %{_qt6_translationdir}/qtwebengine_locales/pl.pak
%lang(pt_BR) %{_qt6_translationdir}/qtwebengine_locales/pt-BR.pak
%lang(pt_PT) %{_qt6_translationdir}/qtwebengine_locales/pt-PT.pak
%lang(ro) %{_qt6_translationdir}/qtwebengine_locales/ro.pak
%lang(ru) %{_qt6_translationdir}/qtwebengine_locales/ru.pak
%lang(sk) %{_qt6_translationdir}/qtwebengine_locales/sk.pak
%lang(sl) %{_qt6_translationdir}/qtwebengine_locales/sl.pak
%lang(sr) %{_qt6_translationdir}/qtwebengine_locales/sr.pak
%lang(sv) %{_qt6_translationdir}/qtwebengine_locales/sv.pak
%lang(sw) %{_qt6_translationdir}/qtwebengine_locales/sw.pak
%lang(ta) %{_qt6_translationdir}/qtwebengine_locales/ta.pak
%lang(te) %{_qt6_translationdir}/qtwebengine_locales/te.pak
%lang(th) %{_qt6_translationdir}/qtwebengine_locales/th.pak
%lang(tr) %{_qt6_translationdir}/qtwebengine_locales/tr.pak
%lang(uk) %{_qt6_translationdir}/qtwebengine_locales/uk.pak
%lang(vi) %{_qt6_translationdir}/qtwebengine_locales/vi.pak
%lang(zh_CN) %{_qt6_translationdir}/qtwebengine_locales/zh-CN.pak
%lang(zh_TW) %{_qt6_translationdir}/qtwebengine_locales/zh-TW.pak

%files devel
%{_rpmmacrodir}/macros.qt6-qtwebengine
%dir %{_qt6_headerdir}/QtWebEngineCore
%{_qt6_headerdir}/QtWebEngineCore/*
%dir %{_qt6_headerdir}/QtWebEngineQuick
%{_qt6_headerdir}/QtWebEngineQuick/*
%dir %{_qt6_headerdir}/QtWebEngineWidgets
%{_qt6_headerdir}/QtWebEngineWidgets/*
%{_qt6_libdir}/qt6/libexec/gn
%{_qt6_libdir}/qt6/metatypes/qt6webengine*.json
%{_qt6_libdir}/qt6/modules/WebEngine*.json
%{_qt6_libdir}/libQt6WebEngineCore.so
%{_qt6_libdir}/libQt6WebEngineQuick.so
%{_qt6_libdir}/libQt6WebEngineQuickDelegatesQml.so
%{_qt6_libdir}/libQt6WebEngineWidgets.so
%{_qt6_libdir}/libQt6WebEngineCore.prl
%{_qt6_libdir}/libQt6WebEngineQuick.prl
%{_qt6_libdir}/libQt6WebEngineQuickDelegatesQml.prl
%{_qt6_libdir}/libQt6WebEngineWidgets.prl
%{_qt6_libdir}/cmake/Qt6/*.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtWebEngine*
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtwebengine*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Designer
%{_qt6_libdir}/cmake/Qt6Designer/Qt6QWebEngine*.cmake
%dir %{_qt6_libdir}/cmake/Qt6WebEngineQuick
%{_qt6_libdir}/cmake/Qt6WebEngineQuick/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6WebEngineWidgets
%{_qt6_libdir}/cmake/Qt6WebEngineWidgets/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6WebEngineCore
%{_qt6_libdir}/cmake/Qt6WebEngineCore/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6WebEngineCoreTools
%{_qt6_libdir}/cmake/Qt6WebEngineCoreTools/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6WebEngineQuickDelegatesQml
%{_qt6_libdir}/cmake/Qt6WebEngineQuickDelegatesQml/*.cmake
%{_qt6_libdir}/cmake/Qt6WebEngineCorePrivate/
%{_qt6_libdir}/cmake/Qt6WebEngineQuickDelegatesQmlPrivate/
%{_qt6_libdir}/cmake/Qt6WebEngineQuickPrivate/
%{_qt6_libdir}/cmake/Qt6WebEngineWidgetsPrivate/
%{_qt6_libdir}/pkgconfig/Qt6WebEngineCore.pc
%{_qt6_libdir}/pkgconfig/Qt6WebEngineQuick.pc
%{_qt6_libdir}/pkgconfig/Qt6WebEngineQuickDelegatesQml.pc
%{_qt6_libdir}/pkgconfig/Qt6WebEngineWidgets.pc
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_webengine*.pri
%{_qt6_plugindir}/designer/libqwebengineview.so

%files devtools
%{_qt6_datadir}/resources/qtwebengine_devtools_resources.pak

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/webengine*
%endif

%files -n qt6-qtpdf
%license LICENSE.*
%{_qt6_archdatadir}/sbom/qtpdf-%{version_no_git}.spdx
%{_qt6_libdir}/libQt6Pdf.so.*
%{_qt6_libdir}/libQt6PdfQuick.so.*
%{_qt6_libdir}/libQt6PdfWidgets.so.*
%dir %{_qt6_libdir}/qt6/qml/QtQuick/Pdf
%{_qt6_libdir}/qt6/qml/QtQuick/Pdf/*
%{_qt6_plugindir}/imageformats/libqpdf.so

%files -n qt6-qtpdf-devel
%dir %{_qt6_headerdir}/QtPdf
%{_qt6_headerdir}/QtPdf/*
%dir %{_qt6_headerdir}/QtPdfQuick
%{_qt6_headerdir}/QtPdfQuick/*
%dir %{_qt6_headerdir}/QtPdfWidgets
%{_qt6_headerdir}/QtPdfWidgets/*
%{_qt6_libdir}/qt6/metatypes/qt6pdf*.json
%{_qt6_libdir}/qt6/modules/Pdf*.json
%{_qt6_libdir}/libQt6Pdf.so
%{_qt6_libdir}/libQt6PdfQuick.so
%{_qt6_libdir}/libQt6PdfWidgets.so
%{_qt6_libdir}/libQt6Pdf.prl
%{_qt6_libdir}/libQt6PdfQuick.prl
%{_qt6_libdir}/libQt6PdfWidgets.prl
%{_qt6_libdir}/cmake/Qt6Gui/Qt6QPdf*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Pdf
%{_qt6_libdir}/cmake/Qt6Pdf/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6PdfQuick
%{_qt6_libdir}/cmake/Qt6PdfQuick/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6PdfWidgets
%{_qt6_libdir}/cmake/Qt6PdfWidgets/*.cmake
%{_qt6_libdir}/cmake/Qt6PdfPrivate/
%{_qt6_libdir}/cmake/Qt6PdfQuickPrivate/
%{_qt6_libdir}/cmake/Qt6PdfWidgetsPrivate/
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6Pdf*.cmake
%{_qt6_libdir}/pkgconfig/Qt6Pdf.pc
%{_qt6_libdir}/pkgconfig/Qt6PdfQuick.pc
%{_qt6_libdir}/pkgconfig/Qt6PdfWidgets.pc
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_pdf*.pri

%if 0%{?examples}
%files -n qt6-qtpdf-examples
%{_qt6_examplesdir}/pdf*
%endif

%changelog
%{?qt_snapshot_changelog_entry}
* Wed Jan 22 2025 Pavel Solovev <daron439@gmail.com> - 6.9.0~beta2-1
- new version

* Wed Dec 18 2024 Pavel Solovev <daron439@gmail.com> - 6.9.0~beta1-1
- new version

* Sat Dec 07 2024 Pavel Solovev <daron439@gmail.com> - 6.8.1-1.1
- rebuilt

* Mon Dec 02 2024 Pavel Solovev <daron439@gmail.com> - 6.8.1-1
- new version

* Wed Oct 30 2024 Pavel Solovev <daron439@gmail.com> - 6.8.0-1.1
- pick upstream commit

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

* Tue Jul 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-1
- 6.7.2

* Wed May 22 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-1
- 6.7.1

* Wed Apr 24 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-2
- Rework and enable openh264 patches

* Wed Apr 03 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- 6.7.0

* Sun Mar 3 2024 Marie Loise Nolden <loise@kde.org> - 6.6.2-3
- move qt designer plugin to -devel
- remove old doc package code (docs are in qt6-doc)

* Mon Feb 19 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-2
- Examples: also install source files

* Thu Feb 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-1
- 6.6.2

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 28 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.1-1
- 6.6.1

* Fri Oct 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-2
- Move v8_context_snapshot file to correct subpackage

* Wed Oct 11 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-1
- 6.6.0

* Sun Oct 01 2023 Justin Zobel <justin.zobel@gmail.com> - 6.5.3-1
- new version

* Tue Sep 05 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 6.5.2-2
- Separate qtpdf subpackages

* Mon Jul 24 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-1
- 6.5.2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 František Zatloukal <fzatlouk@redhat.com> - 6.5.1-3
- Python 3.12 Fixes

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 6.5.1-2
- Rebuilt for ICU 73.2

* Thu May 25 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-1
- 6.5.1

* Tue Apr 04 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-1
- 6.5.0

* Fri Mar 24 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-1
- 6.4.3

* Sun Mar 12 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.4.2-4
- Rebuild for ffmpeg 6.0

* Sat Feb 25 2023 Marek Kasik <mkasik@redhat.com> - 6.4.2-3
- Rebuild for freetype-2.13.0

* Wed Feb 15 2023 Tom Callaway <spot@fedoraproject.org> - 6.4.2-2
- rebuild for libvpx

* Mon Jan 16 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-1

- Initial package
