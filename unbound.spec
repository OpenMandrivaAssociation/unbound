%define major 8
%define libname %mklibname unbound
%define devname %mklibname unbound -d

Name:		unbound
Version:	1.26.0
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
# 1.26.0 already uses ASN1_STRING_* / X509_get_key_usage for OpenSSL 4

%description
Unbound is a validating, recursive, caching DNS resolver. It is designed to be
fast and lean and incorporates modern features based on open standards.

# Resolver packet parse/cache paths are branchy; checkconf + a local
# unbound-host lookup (no external net required) is a useful profile.
%pgo
_bd="$PWD/_OMV_rpm_build"
export LD_LIBRARY_PATH="${_bd}:$PWD${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
ub=
check=
host=
for d in "$_bd" "$PWD" "$_bd/smallapp" "$PWD/smallapp"; do
	[ -x "$d/unbound" ] && ub="$d/unbound"
	[ -x "$d/unbound-checkconf" ] && check="$d/unbound-checkconf"
	[ -x "$d/unbound-host" ] && host="$d/unbound-host"
done
if [ -z "$ub" ]; then
	echo "PGO: instrumented unbound missing" >&2
	find . -name unbound -type f 2>/dev/null | head
	exit 1
fi
train=$(mktemp -d)
trap 'rm -rf "$train"' EXIT
cat > "$train/unbound.conf" <<'EOF'
server:
	verbosity: 0
	interface: 127.0.0.1
	port: 53553
	do-daemonize: no
	username: ""
	directory: ""
	pidfile: ""
	auto-trust-anchor-file: ""
	use-syslog: no
	local-zone: "localhost." static
	local-data: "localhost. 3600 IN A 127.0.0.1"
	local-data: "localhost. 3600 IN AAAA ::1"
EOF
[ -n "$check" ] && "$check" "$train/unbound.conf"
[ -n "$host" ] && "$host" -C "$train/unbound.conf" localhost >/dev/null 2>&1 || true
"$ub" -h >/dev/null 2>&1 || true

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
