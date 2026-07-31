%define major 8
%define libname %mklibname unbound
%define devname %mklibname unbound -d

Name:		unbound
Version:	1.25.2
Release:	1
Source0:	https://github.com/NLnetLabs/unbound/archive/refs/tags/release-%{version}.tar.gz
Summary:	DNS Resolver
URL:		https://github.com/NLnetLabs/unbound
License:	BSD-3-Clause
Group:		System/Libraries
BuildRequires:	autoconf automake slibtool
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(expat)
BuildRequires:	flex bison
BuildSystem:	autotools
# FIXME re-enable gost when it is ported to OpenSSL 4.x
BuildOption:	--disable-gost

%patchlist
unbound-openssl4.patch

%description
Unbound is a validating, recursive, caching DNS resolver. It is designed to be
fast and lean and incorporates modern features based on open standards.

%package -n %{libname}
Summary:	DNS resolver library
Group:		System/Libraries

%description -n %{libname}
DNS resolver library

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%files
%{_bindir}/*
%dir %{_sysconfdir}/unbound
%{_sysconfdir}/unbound/unbound.conf
%{_mandir}/man[158]/*.[158]*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*.3*
