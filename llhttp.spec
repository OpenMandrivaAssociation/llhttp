%global so_version 9.3
%global previous_so_version 9.2
%bcond bootstrap 0

Name:		llhttp
Version:	9.3.0
Release:	1
Summary:	Port of http_parser to llparse
URL:		https://github.com/nodejs/llhttp
License:	MIT
Group:		Development/Libraries/C and C++
Source0:	%{url}/archive/refs/tags/release/v%{version}/%{name}-release-v%{version}.tar.gz
# Contains the original TypeScript sources, which we must include in the source
# RPM per packaging guidelines.
Source1:	%{url}/archive/v%{version}/llhttp-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	ninja

%if %{with bootstrap}
%if "%{_lib}" == "lib64"
BuildRequires:  libllhttp.so.%{previous_so_version}()(64bit)
%else
BuildRequires:  libllhttp.so.%{previous_so_version}
%endif
%endif

%description
This project is a port of http_parser to TypeScript. llparse is used to
generate the output C source file, which could be compiled and linked with the
embedder's program (like Node.js).

%package devel
Summary:	Development files for llhttp
Requires:	llhttp%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The llhttp-devel package contains libraries and header files for
developing applications that use llhttp.


%prep
%autosetup -n %{name}-release-v%{version}


%build
cmake -B ./build \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DBUILD_SHARED_LIBS=ON \
	-G Ninja
%ninja_build -C build


%install
%ninja_install -C build -v

%if %{with bootstrap}
cp -vp %{_libdir}/libllhttp.so.%{previous_so_version}{,.*} \
    %{buildroot}%{_libdir}
%endif


%files
%{_libdir}/libllhttp.so.%{so_version}{,.*}
%if %{with bootstrap}
%{_libdir}/libllhttp.so.%{previous_so_version}{,.*}
%endif
%license LICENSE
%doc README.md


%files devel
%{_includedir}/llhttp.h
%{_libdir}/libllhttp.so
%{_libdir}/pkgconfig/libllhttp.pc
%{_libdir}/cmake/llhttp/
