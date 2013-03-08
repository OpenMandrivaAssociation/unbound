%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Validating, recursive, and caching DNS resolver
Name:		unbound
Version:	1.4.19
Release:	1
Group:		System/Servers
License:	BSD
URL:		http://www.unbound.net/
Source0:	http://www.unbound.net/downloads/unbound-%{version}.tar.gz
Source1:	unbound.init
Source2:	unbound.mandriva.conf
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(pre):	rpm-helper
Requires(postun):	rpm-helper
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	ldns-devel >= 1.6.13
BuildRequires:	libevent-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel

%description
Unbound is a validating, recursive, and caching DNS resolver.

%package -n	%{libname}
Summary:	Shared library from unbound
Group:		System/Libraries

%description -n	%{libname}
A validating, recursive, and caching DNS resolver.

%package -n	%{develname}
Summary:	Development files for libunbound
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
A validating, recursive, and caching DNS resolver.

%prep

%setup -q

cp %{SOURCE1} unbound.init

rm -f ldns-src.tar.gz

%build
%configure2_5x \
    --localstatedir=/var/lib \
    --disable-rpath \
    --with-ssl=%{_prefix} \
    --with-pthreads \
    --with-libevent=%{_prefix} \
    --with-ldns=%{_prefix}

%make
make doc

%install

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/lib/unbound
install -d %{buildroot}/var/run//unbound

%makeinstall_std

find %{buildroot} -name "*.la" -delete

install -m0755 unbound.init %{buildroot}%{_initrddir}/unbound

install -m0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/%name/

echo "# place here local modification of the configuration" > %{buildroot}/%{_sysconfdir}/%name/unbound.local.conf

perl -pi -e '$. eq 1 && print "include: /etc/unbound/unbound.mandriva.conf\n"' %{buildroot}/%{_sysconfdir}/%name/%name.conf
perl -pi -e '$. eq 1 && print "include: /etc/unbound/unbound.local.conf\n"' %{buildroot}/%{_sysconfdir}/%name/%name.conf

%pre
%_pre_useradd unbound /var/lib/unbound /bin/false

%postun
%_postun_userdel unbound

%post
%_post_service unbound

%preun
%_preun_service unbound

%files
%doc doc/CREDITS doc/Changelog doc/FEATURES doc/LICENSE doc/README doc/README.tests
%doc doc/example.conf doc/requirements.txt
%{_initrddir}/unbound
%attr(-,root,unbound) %dir %{_sysconfdir}/unbound
%attr(-,root,unbound) %config(noreplace) %{_sysconfdir}/unbound/*
%{_sbindir}/unbound
%{_sbindir}/unbound-anchor
%{_sbindir}/unbound-checkconf
%{_sbindir}/unbound-control
%{_sbindir}/unbound-control-setup
%{_sbindir}/unbound-host
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%attr(0750,unbound,unbound) %dir /var/lib/unbound
%attr(0750,unbound,unbound) %dir /var/run/unbound

%files -n %{libname}
%doc LICENSE README
%{_libdir}/lib*so.%{major}*

%files -n %{develname}
%doc doc/html/* doc/README.svn doc/TODO
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_libdir}/lib*.*a
%{_mandir}/man3/*


%changelog
* Mon Jul 16 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.4.17-1
+ Revision: 809819
- version update 1.4.17

* Mon Jan 30 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.4.15-1
+ Revision: 769943
- major version bump and 2011 policy fix
- version update 1.4.15

* Tue Dec 27 2011 Alexander Khrukin <akhrukin@mandriva.org> 1.4.14-1
+ Revision: 745541
- version update 1.4.14

* Wed Jun 01 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.10-1
+ Revision: 682259
- fix deps
- 1.4.10 (fixes CVE-2011-1922)

* Wed Dec 22 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-5mdv2011.0
+ Revision: 623883
- rebuilt against libevent 2.x

* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-4mdv2011.0
+ Revision: 615355
- the mass rebuild of 2010.1 packages

* Thu Apr 22 2010 Michael Scherer <misc@mandriva.org> 1.4.3-3mdv2010.1
+ Revision: 537762
- fix infinite loop on service unbound status

* Mon Apr 12 2010 Funda Wang <fwang@mandriva.org> 1.4.3-2mdv2010.1
+ Revision: 533630
- rebuild

* Fri Mar 19 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-1mdv2010.1
+ Revision: 525204
- 1.4.3
- drop one upstream added patch

* Fri Jan 01 2010 Michael Scherer <misc@mandriva.org> 1.4.1-1mdv2010.1
+ Revision: 484883
- new version

* Mon Nov 16 2009 Michael Scherer <misc@mandriva.org> 1.3.4-2mdv2010.1
+ Revision: 466629
- fix wrong Provides

* Tue Oct 13 2009 Oden Eriksson <oeriksson@mandriva.com> 1.3.4-1mdv2010.0
+ Revision: 457033
- 1.3.4 (fixes CVE-2009-3602)

* Sat Aug 22 2009 Oden Eriksson <oeriksson@mandriva.com> 1.3.3-1mdv2010.0
+ Revision: 419599
- 1.3.3

* Mon Jul 13 2009 Frederik Himpe <fhimpe@mandriva.org> 1.3.2-1mdv2010.0
+ Revision: 395459
- update to new version 1.3.2

* Mon Jun 22 2009 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-1mdv2010.0
+ Revision: 387980
- 1.3.0

* Thu Mar 26 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-2mdv2009.1
+ Revision: 361343
- rebuild

* Thu Mar 05 2009 Frederik Himpe <fhimpe@mandriva.org> 1.2.1-1mdv2009.1
+ Revision: 349360
- update to new version 1.2.1

* Fri Jan 23 2009 Jérôme Soyer <saispo@mandriva.org> 1.2.0-1mdv2009.1
+ Revision: 332921
- New upstream release

* Mon Dec 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-1mdv2009.1
+ Revision: 311887
- 1.1.1
- fix deps
- drop redundant patches

* Sun Sep 21 2008 Michael Scherer <misc@mandriva.org> 1.0.2-3mdv2009.0
+ Revision: 286382
- fix initscript, by declaring a pidfile location, removing chroot, and creating a directory
  with proper permission. I have also added two configfile to minimize modification on
  upstream configuration file

* Tue Sep 16 2008 Michael Scherer <misc@mandriva.org> 1.0.2-2mdv2009.0
+ Revision: 285119
- fix the initscript, the end was missing and thus, rpmlint and pcrsys were complaining

* Sun Sep 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2009.0
+ Revision: 282300
- 1.0.2

* Wed Jul 16 2008 Michael Scherer <misc@mandriva.org> 1.0.1-1mdv2009.0
+ Revision: 236606
- update to 1.0.1
- remove patch 2, already applied upstream

* Fri May 30 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-0.2mdv2009.0
+ Revision: 213460
- fix deps
- bump release
- fix a typo
- import unbound

