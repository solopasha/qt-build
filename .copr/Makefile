SHELL = /bin/bash
.PHONY: prepare srpm qt6-qtwebengine.spec
specfile = $(notdir $(spec))
pkg_ver != rpmspec --define "qt_source %nil" -q --qf "%{version}\n" --srpm $(specfile)
pkg_ver_no_tilde = $(subst ~,-,$(pkg_ver))
pkg_ver_maj_min = $(subst .$(lastword $(subst ., ,$(pkg_ver))),,$(pkg_ver))

prepare:
	dnf distro-sync --nodocs --setopt=install_weak_deps=0 --disablerepo=\* \
				--repofrompath 'qt6-test,https://download.copr.fedorainfracloud.org/results/solopasha/qt6-test/fedora-41-x86_64/' \
				--setopt='qt6-test.gpgkey=https://download.copr.fedorainfracloud.org/results/solopasha/qt6-test/pubkey.gpg' \
				qt6-srpm-macros
	dnf in --nodocs --setopt=install_weak_deps=0 rpmdevtools
ifeq ($(findstring ~,$(pkg_ver)),~)
	curl "https://master.qt.io/development_releases/qt/$(pkg_ver_maj_min)/$(pkg_ver_no_tilde)/src/submodules/md5sums.txt" -LO
else
	curl "https://master.qt.io/official_releases/qt/$(pkg_ver_maj_min)/$(pkg_ver)/submodules/md5sums.txt" -LO
endif

%spec: FORCE
	tarball="$$(spectool -s0 --lf ./$(specfile) | xargs -I ,, basename ,,)" && \
	spectool -g ./$(specfile) && \
	set -x && \
	md5exp="$$(grep "$$tarball" md5sums.txt | awk '{print $$1}')" && \
	md5real="$$(md5sum "./$$tarball" | awk '{print $$1}')" && \
	[[ -n "$$md5real" && "$$md5real" == "$$md5exp" ]] || exit 1

FORCE: ;

qt6-qtwebengine.spec:
ifeq ($(findstring ~,$(pkg_ver)),~)
	curl "https://download.qt.io/development_releases/qt/$(pkg_ver_maj_min)/$(pkg_ver_no_tilde)/src/submodules/qtwebengine-everywhere-src-$(pkg_ver_no_tilde).tar.xz" -LO
else
	curl "https://download.qt.io/official_releases/qt/$(pkg_ver_maj_min)/$(pkg_ver)/submodules/qtwebengine-everywhere-src-$(pkg_ver).tar.xz" -LO
endif
	tarball="qtwebengine-everywhere-src-$(pkg_ver_no_tilde).tar.xz" && \
	md5exp="$$(grep "$$tarball" md5sums.txt | awk '{print $$1}')" && \
	md5real="$$(md5sum "./$$tarball" | awk '{print $$1}')" && \
	[[ -n "$$md5real" && "$$md5real" == "$$md5exp" ]] || exit 1
	./clean_qtwebengine.sh $(pkg_ver_no_tilde)

srpm: prepare $(specfile)
	rpmbuild -bs --define "_sourcedir ${PWD}" --define "_specdir ${PWD}" \
		--define "_builddir ${PWD}" --define "_srcrpmdir $(outdir)" --define \
		"_rpmdir ${PWD}" --define "_disable_source_fetch 0" $(specfile)
