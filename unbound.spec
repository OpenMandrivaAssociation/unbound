%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Validating, recursive, and caching DNS resolver
Name:		unbound
Version:	1.4.3
Release:	%mkrel 2
Group:		System/Servers
License:	BSD
URL:		http://www.unbound.net/
Source0:	http://www.unbound.net/downloads/unbound-%{version}.tar.gz
Source1:	unbound.init
Source2:	unbound.mandriva.conf
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	libevent-devel
BuildRequires:	ldns-devel >= 1.4.0
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Unbound is a validating, recursive, and caching DNS resolver.

%package -n	%{libname}
Summary:	Shared library from unbound
Group:		System/Libraries

%description -n	%{libname}
A validating, recursive, and caching DNS resolver

%package -n	%{develname}
Summary:	Development files for libunbound
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
A validating, recursive, and caching DNS resolver

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
rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/lib/unbound
install -d %{buildroot}/var/run//unbound

%makeinstall_std

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

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc/CREDITS doc/Changelog doc/FEATURES doc/LICENSE doc/README doc/README.tests
%doc doc/example.conf doc/requirements.txt
%{_initrddir}/unbound
%attr(-,root,unbound) %dir %{_sysconfdir}/unbound
%attr(-,root,unbound) %config(noreplace) %{_sysconfdir}/unbound/*
%{_sbindir}/unbound
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
%defattr(-,root,root,-)
%{_libdir}/lib*so.%{major}*

%files -n %{develname}
%defattr(-,root,root,-)
%doc doc/html/* doc/README.svn doc/TODO
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_libdir}/lib*.*a
%{_mandir}/man3/*
