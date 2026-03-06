%define major 0
%define libname %mklibname maxminddb %{major}
%define develname %mklibname maxminddb -d

Name:       libmaxminddb
Summary:    C library for the MaxMind DB file format
Version:	1.13.3
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
Requires:   %{libname} = %{version}-%{release}
Provides:   %{name}-devel = %{version}-%{release}

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
