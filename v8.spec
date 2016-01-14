%{?scl:%scl_package v8}
%{!?scl:%global pkg_name %{name}}

# Hi Googlers! If you're looking in here for patches, nifty.
# You (and everyone else) are welcome to use any of my Chromium spec files and
# patches under the terms of the GPLv2 or later.
# You (and everyone else) are welcome to use any of my V8-specific spec files
# and patches under the terms of the BSD license.
# You (and everyone else) may NOT use my spec files or patches under any other
# terms.
# I hate to be a party-pooper here, but I really don't want to help Google
# make a proprietary browser. There are enough of those already.
# All copyrightable work in these spec files and patches is Copyright 2011
# Tom Callaway <spot@fedoraproject.org>

# For the 1.2 branch, we use 0s here
# For 1.3+, we use the three digit versions
# Hey, now there are four digits. What do they mean? Popsicle.
%global somajor 3
%global sominor 14
%global sobuild 5
%global sotiny 10
%global sover %{somajor}.%{sominor}.%{sobuild}

%ifarch i686
%global target ia32
%endif
%ifarch x86_64
%global target x64
%endif
%ifarch armv7l armv7hl
%global target arm
%endif


Name:		%{?scl_prefix}v8
Version:	%{somajor}.%{sominor}.%{sobuild}.%{sotiny}
Release:	9%{?dist}
Epoch:		1
Summary:	JavaScript Engine
Group:		System Environment/Libraries
License:	BSD
URL:		http://code.google.com/p/v8
# No tarballs, pulled from svn
# svn export http://v8.googlecode.com/svn/tags/%%{version} v8-%%{version}
# tar jcf v8-%%{version}.tar.bz2 v8-%%{version}
Source0:        v8-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:	%{ix86} x86_64 %{arm}
BuildRequires:	%{?scl_prefix}gyp, readline-devel, libicu-devel, chrpath
#backport fix for CVE-2013-2634 (RHBZ#924495)
Patch1:	    v8-3.14.5.8-CVE-2013-2634.patch
#backport fix for CVE-2013-2882 (RHBZ#991116)
Patch2:     v8-3.14.5.10-CVE-2013-2882.patch
#backport fix for CVE-2013-6640 (RHBZ#1039889)
Patch3:     v8-3.14.5.10-CVE-2013-6640.patch

#backport fix for enumeration for objects with lots of properties
#https://codereview.chromium.org/11362182
Patch4:     v8-3.14.5.10-enumeration.patch

#backport fix for CVE-2013-6650 (RHBZ#1059070)
Patch5:     v8-3.14.5.10-CVE-2013-6650.patch

#backport only applicable fix for CVE-2014-1704 (RHBZ#1077136)
#the other two patches don't affect this version of v8
Patch6:     v8-3.14.5.10-CVE-2014-1704-1.patch

# use clock_gettime() instead of gettimeofday(), which increases performance
# dramatically on virtual machines
# https://github.com/joyent/node/commit/f9ced08de30c37838756e8227bd091f80ad9cafa
# see above link or head of patch for complete rationale
Patch7:     v8-3.14.5.10-use-clock_gettime.patch

# fix corner case in x64 compare stubs
# fixes bug resulting in an incorrect result when comparing certain integers
# (e.g. 2147483647 > -2147483648 is false instead of true)
# https://code.google.com/p/v8/issues/detail?id=2416
# https://github.com/joyent/node/issues/7528
Patch8:     v8-3.14.5.10-x64-compare-stubs.patch

# backport security fix for memory corruption/stack overflow (RHBZ#1125464)
# https://groups.google.com/d/msg/nodejs/-siJEObdp10/2xcqqmTHiEMJ
# https://github.com/joyent/node/commit/530af9cb8e700e7596b3ec812bad123c9fa06356
Patch9:     v8-3.14.5.10-mem-corruption-stack-overflow.patch

# backport bugfix for x64 MathMinMax:
#   Fix x64 MathMinMax for negative untagged int32 arguments.
#   An untagged int32 has zeros in the upper half even if it is negative.
#   Using cmpq to compare such numbers will incorrectly ignore the sign.
# https://github.com/joyent/node/commit/3530fa9cd09f8db8101c4649cab03bcdf760c434
Patch10:    v8-3.14.5.10-x64-MathMinMax.patch

#we need this to get over some ugly code
Patch11:    gcc-48-fix.patch
Patch12:    v8-3.14.5.10-unused-local-typedefs.patch
Patch13:    v8-3.14.5.10-CVE-2013-6668.patch
Patch14:    v8-3.14.5.10-CVE-2013-6668-segfault.patch 
Patch15:    v8-3.14.5.10-use-upstream-test-values-regress-test-1122.patch
#This is nodejs specific patch it has not been pushed upstream by joyent
Patch16:    v8-add-api-for-aborting-on-uncaught-exception.patch
Patch17:    v8-Apply-REPLACE_INVALID_UTF8-patch.patch
Patch18:    v8-jit-code-event.patch

Obsoletes: 	nodejs010-v8, ruby193-v8, mongodb24-v8 

%{?scl:Requires: %{scl}-runtime}

%description
V8 is Google's open source JavaScript engine. V8 is written in C++ and is used
in Google Chrome, the open source browser from Google. V8 implements ECMAScript
as specified in ECMA-262, 3rd edition.

%package devel
Group:		Development/Libraries
Summary:	Development headers and libraries for v8
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:      nodejs010-v8-devel, ruby193-v8-devel, mongodb24-v8-devel

%description devel
Development headers and libraries for v8.

%prep
%setup -q -n %{pkg_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
#%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1

#Patch7 needs -lrt on glibc < 2.17 (RHEL <= 6)
%if (0%{?rhel} > 6 || 0%{?fedora} > 18)
%global lrt %{nil}
%else
%global lrt -lrt
%endif

%build
mkdir -p build/gyp
ln -s %{?_scl_root}/usr/bin/gyp build/gyp/gyp

export CFLAGS="${CFLAGS:-%optflags}"
export CXXFLAGS="${CXXFLAGS:-%optflags}"
export MAKE_EXTRA_FLAGS="%{lrt} -Wnounused-but-set-variable"

%ifarch armv7hl
MAKE_EXTRA_FLAGS+=hardfp=on
%endif

%if 0%{?fedora} >= 16
export ICU_LINK_FLAGS=`pkg-config --libs-only-l icu-i18n`
%else
export ICU_LINK_FLAGS=`pkg-config --libs-only-l icu`
%endif
%{?scl:scl enable %{scl} "}
make %{target}.release %{?_smp_mflags} \
      console=readline \
      library=shared \
      soname_version=%{?scl:%{scl_name}-}%{sover} \
      $MAKE_EXTRA_FLAGS \
      $ICU_LINK_FLAGS
%{?scl:"}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}

install -p include/*.h %{buildroot}%{_includedir}
install -p out/%{target}.release/lib.target/libv8.so.%{?scl:%{scl_name}-}%{sover} %{buildroot}%{_libdir}
install -p -m0755 out/%{target}.release/d8 %{buildroot}%{_bindir}
install -p -m0755 out/%{target}.release/mksnapshot %{buildroot}%{_bindir}/v8-mksnapshot
install -p -m0755 out/%{target}.release/preparser %{buildroot}%{_bindir}/v8-preparser
install -p -m0755 out/%{target}.release/process %{buildroot}%{_bindir}/v8-process
install -p -m0755 out/%{target}.release/shell %{buildroot}%{_bindir}/v8-shell
chmod -x %{buildroot}%{_includedir}/v8*.h

mkdir -p %{buildroot}%{_includedir}/v8/extensions/
install -p src/extensions/*.h %{buildroot}%{_includedir}/v8/extensions/

chmod -x %{buildroot}%{_includedir}/v8/extensions/*.h

# install Python JS minifier scripts for nodejs
install -d %{buildroot}%{?_scl_root}%{python_sitelib}
sed -i 's|/usr/bin/python2.4|/usr/bin/env python|g' tools/jsmin.py
sed -i 's|/usr/bin/python2.4|/usr/bin/env python|g' tools/js2c.py
install -p -m0744 tools/jsmin.py %{buildroot}%{?_scl_root}%{python_sitelib}/
install -p -m0744 tools/js2c.py %{buildroot}%{?_scl_root}%{python_sitelib}/
chmod -R -x %{buildroot}%{?_scl_root}%{python_sitelib}/*.py*

pushd %{buildroot}%{_libdir}
ln -sf libv8.so.%{?scl:%{scl_name}-}%{sover} libv8.so
ln -sf libv8.so.%{?scl:%{scl_name}-}%{sover} libv8.so%{?scl:.%{?scl_name}}
ln -sf libv8.so.%{?scl:%{scl_name}-}%{sover} libv8.so%{?scl:.%{?scl_name}-}%{somajor}
popd

#remove rpaths
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/d8
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/v8-shell
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/v8-process

%check 
#make %{target}.check 
%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE
%{_libdir}/*.so%{?scl:.%{scl_name}-}*
%{_libdir}/*.so%{?scl:.%{scl_name}}

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/*.so%{?scl:.%{scl_name}}
%{_bindir}/*
%{_includedir}/*.h
%dir %{_includedir}/v8/
%{_includedir}/v8/extensions/
%{?_scl_root}%{python_sitelib}/j*.py*

%changelog
* Tue Jul 21 2015 Tomas Hrcka <thrcka@redhat.com> - 1:3.14.5.10-9
- Include upstream patch: Meaningful name for builtins in JitCodeEvent API
- https://github.com/joyent/node/commit/5a60e0d904c38c2bdb04785203b1b784967c870d

* Wed Jan 07 2015 Tomas Hrcka <thrcka@redhat.com> - 1:3.14.5.10-8
- Backport Apply REPLACE_INVALID_UTF8 patch
- https://github.com/joyent/node/commit/881ac26f27f4ac9585d66c8d8a67d5b246a23d1b

* Wed Jan 07 2015 Tomas Hrcka <thrcka@redhat.com> - 1:3.14.5.10-7
- Backport api for aborting on uncaught exception
- https://github.com/joyent/node/commit/fbff7054a47551387a99244e2cf0631f30406798

* Tue Sep 30 2014 Tomas Hrcka <thrcka@redhat.com> - 1:3.14.5.10-6
- Update regress test 1122

* Tue Sep 23 2014 Tomas Hrcka <thrcka@redhat.com> - 1:3.14.5.10-5
- Add CVE-2013-6668 patch

* Wed Sep 10 2014 Tomas Hrcka <thrcka@redhat.com> - 1:3.14.5.10-4
- multiple CVE fixes
- CVE-2013-6639 CVE-2013-6640 CVE-2013-6650 
- CVE-2013-6668 CVE-2014-1704 CVE-2014-5256

* Mon Mar 24 2014 Tomas Hrcka <thrcka@redhat.com> - 1:3.14.5.10-3.6
- Remove rpaths

* Tue Nov 26 2013 Tomas Hrcka <thrcka@redhat.com> - 1:3.14.5.10-3.5
- add simlink to libv8.so
- obsoletes v8 in all other collections

* Mon Nov 25 2013 Tomas Hrcka <thrcka@redhat.com> - 1:3.14.5.10-2.4
- changed .so suffix to libv8.so.v8314-3.14.5

* Thu Oct 10 2013 Tomas Hrcka  <thrcka@redhat.com> - 1:3.14.5.10-2.3
 - fixed typo in install section

* Thu Sep 26 2013 Tomas Hrcka  <thrcka@redhat.com> - 1:3.14.5.10-2.2
 - added patch to fix gcc48 warnings

* Thu Sep 26 2013 Tomas Hrcka  <thrcka@redhat.com> - 1:3.14.5.10-2.1
 - built with gyp instead of scons
 - spec cleanup
 - moved stuff in _bindir to devel package

* Fri Aug 02 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:3.14.5.10-2
- backport fix for remote DoS or unspecified other impact via type confusion
  (RHBZ#991116; CVE-2013-2882)

* Mon Jun 24 2013 Tomas Hrcka <thrcka@redhat.com> - 1:3.14.5.10-1.1
- merged new upstream release

* Wed May 29 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:3.14.5.10-1
- new upstream release 3.14.5.10

* Thu May 09 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.14.5.8-2.3
- Fix python_sitelib placement in SCL

* Tue May 07 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.14.5.8-2.2
- Add runtime dependency on scl-runtime

* Mon May 06 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.14.5.8-2.1
- Fix ownership of include directory (#958729)

* Fri Apr 05 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.14.5.8-2
- Add support for software collections

* Fri Mar 22 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:3.14.5.8-1
- new upstream release 3.14.5.8
- backport security fix for remote DoS via crafted javascript (RHBZ#924495; CVE-2013-2632)

* Mon Mar 11 2013 Stephen Gallagher <sgallagh@redhat.com> - 1:3.14.5.7-3
- Update to v8 3.14.5.7 for Node.js 0.10.0

* Sat Jan 26 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:3.13.7.5-2
- rebuild for icu-50
- ignore new GCC 4.8 warning

* Tue Dec  4 2012 Tom Callaway <spot@fedoraproject.org> - 1:3.13.7.5-1
- update to 3.13.7.5 (needed for chromium 23)
- Resolves multiple security issues (CVE-2012-5120, CVE-2012-5128)
- d8 is now using a static libv8, resolves bz 881973)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.10.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul  6 2012 Tom Callaway <spot@fedoraproject.org> 1:3.10.8-1
- update to 3.10.8 (chromium 20)

* Tue Jun 12 2012 Tom Callaway <spot@fedoraproject.org> 1:3.9.24-1
- update to 3.9.24 (chromium 19)

* Mon Apr 23 2012 Thomas Spura <tomspur@fedoraproject.org> 1:3.7.12.6
- rebuild for icu-49

* Fri Mar 30 2012 Dennis Gilmore <dennis@ausil.us> 1:3.7.12-5
- make sure the right arm abi is used in the second call of scons

* Thu Mar 29 2012 Dennis Gilmore <dennis@ausil.us> 1:3.7.12-4
- use correct arm macros
- use the correct abis for hard and soft float

* Tue Mar 20 2012 Tom Callaway <spot@fedoraproject.org> 3.7.12-3
- merge changes from Fedora spec file, sync, add epoch

* Fri Feb 17 2012 Tom Callaway <spot@fedoraproject.org> 3.7.12-2
- add -Wno-error=strict-overflow for gcc 4.7 (hack, hack, hack)

* Mon Feb 13 2012 Tom Callaway <spot@fedoraproject.org> 3.7.12-1
- update to 3.7.12

* Thu Nov  3 2011 Tom Callaway <spot@fedoraproject.org> 3.5.10-1
- update to 3.5.10

* Mon Sep 26 2011 Tom Callaway <spot@fedoraproject.org> 3.4.14-2
- final 3.4.14 tag
- include JavaScript minifier scripts in -devel

* Fri Jun 10 2011 Tom Callaway <spot@fedoraproject.org> 3.2.10-1
- tag 3.2.10

* Thu Apr 28 2011 Tom Callaway <spot@fedoraproject.org> 3.1.8-1
- "stable" v8 match for "stable" chromium (tag 3.1.8)

* Tue Feb 22 2011 Tom Callaway <spot@fedoraproject.org> 3.1.5-1.20110222svn6902
- update to 3.1.5
- enable experimental i18n icu stuff for chromium

* Tue Jan 11 2011 Tom Callaway <spot@fedoraproject.org> 3.0.7-1.20110111svn6276
- update to 3.0.7

* Tue Dec 14 2010 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.0-2.20101209svn5957
- fix sloppy code where NULL is used

* Thu Dec  9 2010 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.0-1.20101209svn5957
- update to 3.0.0

* Fri Oct 22 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.1-1.20101022svn5692
- update to 2.5.1
- fix another fwrite with no return checking case

* Thu Oct 14 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.0-1.20101014svn5625
- update to 2.5.0

* Mon Oct  4 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.8-1.20101004svn5585
- update to 2.4.8

* Tue Sep 14 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.3-1.20100914svn5450
- update to 2.4.3

* Tue Aug 31 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.11-1.20100831svn5385
- update to svn5385

* Fri Aug 27 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.11-1.20100827svn5365
- update to 2.3.11, svn5365

* Tue Aug 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.10-1.20100824svn5332
- update to 2.3.10, svn5332

* Wed Aug 18 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.9-1.20100819svn5308
- update to 2.3.9, svn5308

* Wed Aug 11 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.7-1.20100812svn5251
- update to svn5251

* Wed Aug 11 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.7-1.20100811svn5248
- update to 2.3.7, svn5248

* Tue Aug 10 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.6-1.20100809svn5217
- update to 2.3.6, svn5217

* Fri Aug  6 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.5-1.20100806svn5198
- update to 2.3.5, svn5198

* Mon Jul 26 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.3-1.20100726svn5134
- update to 2.3.3, svn5134

* Fri Jul 16 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.0-1.20100716svn5088
- update to 2.3.0, svn5088

* Tue Jul  6 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.22-1.20100706svn5023
- update to 2.2.22, svn5023

* Fri Jul  2 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.21-1.20100702svn5010
- update to svn5010

* Wed Jun 30 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.21-1.20100630svn4993
- update to 2.2.21, svn4993
- include checkout script

* Thu Jun  3 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.14-1.20100603svn4792
- update to 2.2.14, svn4792

* Tue Jun  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.13-1.20100601svn4772
- update to 2.2.13, svn4772

* Thu May 27 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.12-1.20100527svn4747
- update to 2.2.12, svn4747

* Tue May 25 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.11-1.20100525svn4718
- update to 2.2.11, svn4718

* Thu May 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.10-1.20100520svn4684
- update to svn4684

* Mon May 17 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.10-1.20100517svn4664
- update to 2.2.10, svn4664

* Thu May 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.9-1.20100513svn4653
- update to svn4653

* Mon May 10 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.9-1.20100510svn4636
- update to 2.2.9, svn4636

* Tue May  4 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.7-1.20100504svn4581
- update to 2.2.7, svn4581

* Mon Apr 19 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.3-1.20100419svn4440
- update to 2.2.3, svn4440

* Tue Apr 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.2-1.20100413svn4397
- update to 2.2.2, svn4397

* Thu Apr  8 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-1.20100408svn4359
- update to 2.2.1, svn4359

* Mon Mar 29 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.0-1.20100329svn4309
- update to 2.2.0, svn4309

* Thu Mar 25 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.8-1.20100325svn4273
- update to 2.1.8, svn4273

* Mon Mar 22 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.5-1.20100322svn4204
- update to 2.1.5, svn4204

* Mon Mar 15 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.4-1.20100315svn4129
- update to 2.1.4, svn4129

* Wed Mar 10 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.0-1.20100310svn4088
- update to 2.1.3, svn4088

* Thu Feb 18 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.0-1.20100218svn3902
- update to 2.1.0, svn3902

* Fri Jan 22 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-1.20100122svn3681
- update to 2.0.6, svn3681

* Tue Dec 29 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.5-1.20091229svn3528
- svn3528

* Mon Dec 21 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.5-1.20091221svn3511
- update to 2.0.5, svn3511

* Wed Dec  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.3-1.20091209svn3443
- update to 2.0.3, svn3443

* Tue Nov 24 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.2-1.20091124svn3353
- update to 2.0.2, svn3353

* Wed Nov 18 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-1.20091118svn3334
- update to 2.0.0, svn3334

* Tue Oct 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.16-1.20091027svn3152
- update to 1.3.16, svn3152

* Tue Oct 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.15-1.20091013svn3058
- update to svn3058

* Thu Oct  8 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.15-1.20091008svn3036
- update to 1.3.15, svn3036

* Tue Sep 29 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.13-1.20090929svn2985
- update to svn2985
- drop unused parameter patch, figured out how to work around it with optflag mangling
- have I mentioned lately that scons is garbage?

* Mon Sep 28 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.13-1.20090928svn2980
- update to 1.3.13, svn2980

* Wed Sep 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.11-1.20090916svn2903
- update to 1.3.11, svn2903

* Wed Sep  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.9-1.20090909svn2862
- update to 1.3.9, svn2862

* Thu Aug 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.8-1.20090827svn2777
- update to 1.3.8, svn2777

* Mon Aug 24 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.6-1.20090824svn2747
- update to 1.3.6, svn2747

* Tue Aug 18 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.4-1.20090818svn2708
- update to svn2708, build and package d8

* Fri Aug 14 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.4-1.20090814svn2692
- update to 1.3.4, svn2692

* Wed Aug 12 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.3-1.20090812svn2669
- update to 1.3.3, svn2669

* Mon Aug 10 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.2-1.20090810svn2658
- update to svn2658

* Fri Aug  7 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.2-1.20090807svn2653
- update to svn2653

* Wed Aug  5 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.2-1.20090805svn2628
- update to 1.3.2, svn2628

* Mon Aug  3 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.1-1.20090803svn2607
- update to svn2607

* Fri Jul 31 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.1-1.20090731svn2602
- update to svn2602

* Thu Jul 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.1-1.20090730svn2592
- update to 1.3.1, svn 2592

* Mon Jul 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.0-1.20090727svn2543
- update to 1.3.0, svn 2543

* Fri Jul 24 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.14-1.20090724svn2534
- update to svn2534

* Mon Jul 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.14-1.20090720svn2510
- update to svn2510

* Thu Jul 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.14-1.20090716svn2488
- update to svn2488

* Wed Jul 15 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.14-1.20090715svn2477
- update to 1.2.14, svn2477

* Mon Jul 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.13-1.20090713svn2434
- update to svn2434

* Sat Jul 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.13-1.20090711svn2430
- update to 1.2.13, svn2430

* Wed Jul  8 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.12-1.20090708svn2391
- update to 1.2.12, svn2391

* Sat Jul  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.11-1.20090704svn2356
- update to 1.2.11, svn2356

* Fri Jun 26 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.9-1.20090626svn2284
- update to svn2284

* Wed Jun 24 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.9-1.20090624svn2262
- update to 1.2.9, svn2262

* Thu Jun 18 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.7-2.20090618svn2219
- fix unused-parameter patch

* Thu Jun 18 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.7-1.20090618svn2219
- update to 1.2.8, svn2219

* Mon Jun 8 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.7-2.20090608svn2123
- fix gcc44 compile for Fedora 11

* Mon Jun  8 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.7-1.20090608svn2123
- update to 1.2.7, svn2123

* Thu May 28 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.5-1.20090528svn2072
- update to newer svn checkout

* Sun Feb 22 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.1-1.20090222svn1332
- update to newer svn checkout

* Sun Sep 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.2-2.20080914svn300
- make a versioned shared library properly

* Sun Sep 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.2-1.20080914svn300
- Initial package for Fedora
