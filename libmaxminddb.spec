%define major 0
%define libname %mklibname maxminddb %{major}
%define develname %mklibname maxminddb -d

Name:       libmaxminddb
Summary:    C library for the MaxMind DB file format
Version:	1.14.1
Release:	1
Group:      System/Libraries
URL:        https://maxmind.github.io/libmaxminddb
Source0:    https://github.com/maxmind/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz

# original libmaxminddb code is Apache Licence 2.0
# src/maxminddb-compat-util.h is BSD
License:        ASL 2.0 and BSD

BuildSystem:	cmake
BuildOption:	-DBUILD_SHARED_LIBS:BOOL=ON

# For tests
BuildRequires: perl(Test::More)
BuildRequires: perl(File::Temp)
BuildRequires: perl(IPC::Run3)

# IP lookup + metadata dump on the shipped GeoIP2 test DBs (the same
# shape as production GeoLite/GeoIP files). Skip the crafted DoS
# databases — those overweight error paths.
%pgo
lookup=
for d in _OMV_rpm_build/bin _OMV_rpm_build bin; do
	[ -x "$d/mmdblookup" ] && lookup="$d/mmdblookup"
done
if [ -z "$lookup" ]; then
	echo "PGO: instrumented mmdblookup missing" >&2
	find . -name mmdblookup -type f | head
	exit 1
fi
export LD_LIBRARY_PATH="$PWD/_OMV_rpm_build${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
datadir=t/maxmind-db/test-data
[ -d "$datadir" ] || { echo "PGO: test-data missing" >&2; exit 1; }
for db in \
	GeoIP2-City-Test.mmdb \
	GeoIP2-Country-Test.mmdb \
	GeoLite2-City-Test.mmdb \
	GeoLite2-Country-Test.mmdb \
	GeoLite2-ASN-Test.mmdb \
	GeoIP2-ISP-Test.mmdb \
	GeoIP2-Enterprise-Test.mmdb \
	GeoIP2-Domain-Test.mmdb \
	GeoIP2-Connection-Type-Test.mmdb \
	MaxMind-DB-test-decoder.mmdb \
	MaxMind-DB-test-ipv4-24.mmdb \
	MaxMind-DB-test-mixed-24.mmdb
do
	[ -f "$datadir/$db" ] || continue
	for ip in 81.2.69.160 81.2.69.142 89.160.20.112 216.160.83.56 \
		1.1.1.1 8.8.8.8 2001:218:85a3:0:0:8a2e:370:7334 ::1; do
		"$lookup" -v -f "$datadir/$db" --ip "$ip" >/dev/null 2>&1 || true
	done
	"$lookup" -f "$datadir/$db" --ip 81.2.69.160 --benchmark 200 >/dev/null 2>&1 || true
done

%description
This package contains libmaxminddb library.

%package -n %{libname}
Group:      System/Libraries
Summary:    C library for the MaxMind DB file format
Obsoletes:  %{_lib}maxminddb1.0 < 1.3.2-3

%description -n %{libname}
This package contains libmaxminddb library.

%package -n %{develname}
Group:      Development/C
Summary:    Libraries and header files for %{name}
Requires:   %{libname} = %{EVRD}
Provides:   %{name}-devel = %{EVRD}

%description -n %{develname}
This package contains libraries and header files needed for developing
applications that use %{name}.

%if ! %{cross_compiling}
%check
cd _OMV_rpm_build
LD_LIBRARY_PATH=$(pwd):$(pwd)/t ctest
%endif

%files -n %{libname}
%doc LICENSE
%{_libdir}/libmaxminddb.so.%{major}{,.*}

%files -n %{develname}
%doc NOTICE Changes.md
%{_bindir}/mmdblookup
%{_includedir}/maxminddb.h
%{_includedir}/maxminddb_config.h
%{_libdir}/libmaxminddb.so
%{_libdir}/pkgconfig/libmaxminddb.pc
%{_libdir}/cmake/maxminddb
%{_mandir}/man1/*
%{_mandir}/man3/*
