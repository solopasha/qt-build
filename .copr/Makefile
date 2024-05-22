.PHONY: prepare srpm qt6-qtwebengine.spec
specfile = $(notdir $(spec))
pkg_ver != rpmspec -q --qf "%{version}\n" --srpm $(specfile) | sed 's/[\^,~].*//'
pkg_ver_maj_min = $(subst .$(lastword $(subst ., ,$(pkg_ver))),,$(pkg_ver))

%spec:
	@:

qt6-qtwebengine.spec:
	curl "https://download.qt.io/official_releases/qt/$(pkg_ver_maj_min)/$(pkg_ver)/submodules/qtwebengine-everywhere-src-$(pkg_ver).tar.xz" -LO
	./clean_qtwebengine.sh $(pkg_ver)

srpm: prepare $(specfile)
	rpmbuild -bs --define "_sourcedir ${PWD}" --define "_specdir ${PWD}" \
		--define "_builddir ${PWD}" --define "_srcrpmdir $(outdir)" --define \
		"_rpmdir ${PWD}" --define "_disable_source_fetch 0" $(specfile)
