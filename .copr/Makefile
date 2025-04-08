.PHONY: prepare clone srpm qt6-qtwebengine.spec
specfile = $(notdir $(spec))
qt_module != sed -n 's/%global[[:space:]]\+\bqt_module\b[[:space:]]\+\(.*\)/\1/p' $(specfile)
commit != sed -n 's/%global[[:space:]]\+\bcommit0\b[[:space:]]\+\(.*\)/\1/p' $(specfile)
pkg_ver != rpmspec -q --qf "%{version}\n" --srpm $(specfile)
pkg_ver_no_tilde = $(subst ~,-,$(pkg_ver))
pkg_ver_maj_min = $(word 1,$(subst .,  ,$(lastword $(pkg_ver)))).$(word 2,$(subst .,  ,$(lastword $(pkg_ver))))
outdir ?= $(shell pwd)

prepare:
	dnf distro-sync --nodocs -y --setopt=install_weak_deps=0 --repo=qt6-test \
				--repofrompath 'qt6-test,https://download.copr.fedorainfracloud.org/results/solopasha/qt6-test/fedora-41-x86_64/devel/' \
				--setopt='qt6-test.gpgcheck=1' \
				--setopt='qt6-test.gpgkey=https://download.copr.fedorainfracloud.org/results/solopasha/qt6-test/pubkey.gpg' \
				qt6-srpm-macros
	dnf install -y --nodocs --setopt=install_weak_deps=0 rpmdevtools git-core

clone:
ifdef commit
	git clone --recursive --single-branch --branch $(pkg_ver_maj_min) https://code.qt.io/qt/$(qt_module).git $(qt_module)-everywhere-src-$(pkg_ver_no_tilde)
	git -C $(qt_module)-everywhere-src-$(pkg_ver_no_tilde) reset --hard $(commit)
	git -C $(qt_module)-everywhere-src-$(pkg_ver_no_tilde) submodule update --recursive
else
	git clone --recursive --depth 1 --shallow-submodules --branch v$(pkg_ver_no_tilde) https://code.qt.io/qt/$(qt_module).git $(qt_module)-everywhere-src-$(pkg_ver_no_tilde)
endif
ifneq ($(specfile),qt6-qtwebchannel.spec)
	find -maxdepth 2 -type d \( -name 'tests' -o -name 'examples' \) -exec rm -rf '{}' \;
endif

%spec: clone
	XZ_OPT="-T0 -e9" tar --owner 0 --group 0 --numeric-owner --exclude-vcs -cJf $(qt_module)-everywhere-src-$(pkg_ver_no_tilde).tar.xz $(qt_module)-everywhere-src-$(pkg_ver_no_tilde)

qt6-qtwebengine.spec: clone
	./clean_qtwebengine.sh $(pkg_ver_no_tilde)

srpm: prepare $(specfile)
	rpmbuild -bs --define "_sourcedir ${PWD}" --define "_specdir ${PWD}" \
		--define "_builddir ${PWD}" --define "_srcrpmdir $(outdir)" --define \
		"_rpmdir ${PWD}" --define "_disable_source_fetch 0" $(specfile)
