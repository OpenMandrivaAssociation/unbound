%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Validating, recursive, and caching DNS resolver
Name:		unbound
Version:	1.0.0
Release:	%mkrel 0.1
Group:		Systen/Servers
License:	BSD
URL:		http://www.unbound.net/
Source0:	http://www.unbound.net/downloads/unbound-%{version}.tar.gz
Source1:	unbound.init
Patch0:		unbound-1.0.0_stupid_rpath.patch
Patch1:		unbound-1.0.0_preserve_cflags.patch
Patch2:		unbound-1.0.0_buffer_overflow.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	libevent-devel
BuildRequires:	libldns-devel >= 1.3.0
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
Provides:	%{name} = %{version}-%{release}

%description -n	%{develname}
A validating, recursive, and caching DNS resolver

%prep

%setup -q
%patch0
%patch1
%patch2

cp %{SOURCE1} unbound.init

rm -f ldns-src.tar.gz

%build

%configure2_5x \
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
install -d %{buildroot}%{_localstatedir}/unbound

%makeinstall_std

install -m0755 unbound.init %{buildroot}%{_initrddir}/unbound

%pre
%_pre_useradd unbound %{_localstatedir}/unbound /bin/false

%postun
%_postun_userdel unbound

%post
%_post_service unbound

%preun
%_preun_service unbound

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc/CREDITS doc/Changelog doc/FEATURES doc/LICENSE doc/README doc/README.tests
%doc doc/example.conf doc/plan doc/requirements.txt
%{_initrddir}/unbound
%attr(-,root,unbound) %dir %{_sysconfdir}/unbound
%attr(-,root,unbound) %config(noreplace) %{_sysconfdir}/unbound/*
%{_sbindir}/unbound
%{_sbindir}/unbound-checkconf
%{_sbindir}/unbound-host
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%attr(0750,unbound,unbound) %dir %{_localstatedir}/unbound

%files -n %{libname}
%doc LICENSE README
%defattr(-,root,root,-)
%{_libdir}/lib*so.*

%files -n %{develname}
%defattr(-,root,root,-)
%doc doc/html/* doc/README.svn doc/TODO 
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_libdir}/lib*.*a
%{_mandir}/man3/*

