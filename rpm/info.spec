#
# RPM Spec file for the WaTTS info plugin.
#
# Under any yum based distro (e.g. CentOS) install `rpmdevtools' and then run:
#  $ rpmbuild -bb pkg/rpm/info.spec
#
# Maintainer: Joshua Bachmeier <uwdkl@student.kit.edu>
#

# Disable automatic rpm python bytecompiler  *ahem* Bloat *ahem*
# See https://math-linux.com/linux/rpm/article/how-to-turn-off-avoid-brp-python-bytecompile-script-in-a-spec-file
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:           %(echo $CONFIG | jq -r .pkg.name)
Summary:        %(echo $CONFIG | jq -r .pkg.short_desc)
Vendor:         %(echo $CONFIG | jq -r .pkg.vendor)
Packager:       %(echo $CONFIG | jq -r .pkg.maintainer)
Version:    	  %(echo $CONFIG | jq -r .pkg.version)
Release:    	  1
License:    	  Apache
Source0:        %(echo $CONFIG | jq -r .archive.targz)
Requires:       tts
# TODO deps
BuildArch:	    noarch

%description
%(echo $CONFIG | jq -r .pkg.long_desc)

%prep
cd $RPM_SOURCE_DIR
curl -L %(echo $CONFIG | jq -r .archive.targz) -o %name-%version.tar.gz
tar xf %name-%version.tar.gz

%build
cd $RPM_SOURCE_DIR/%(echo $CONFIG | jq -r .archive.name)-%version
eval $(echo $CONFIG | jq -r .build.bash)

%install
cd $RPM_SOURCE_DIR/%(echo $CONFIG | jq -r .archive.name)-%version
mkdir -p "$RPM_BUILD_ROOT/var/lib/watts/plugins"
cp plugin/* "$RPM_BUILD_ROOT/var/lib/watts/plugins"

%clean
rm -rf %RPM_BUILD_ROOT

%files
/var/lib/watts/plugins/*
