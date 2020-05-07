#
# Conditional build:
%bcond_without	tests		# build with tests
%bcond_with	telemetry	# sending metrics to MS

Summary:	C++ Library Manager for Windows, Linux, and MacOS
Summary(pl.UTF-8):	Zarządca bibliotek C++ dla Windows, Linuksa i MacOS-a
Name:		vcpkg
Version:	2020.04
Release:	3
License:	MIT
Group:		Development/Tools
Source0:	https://github.com/microsoft/vcpkg/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	13e30379de51a284a66c311ac45b64a6
Patch0:		%{name}-arch.patch
URL:		https://docs.microsoft.com/en-us/cpp/vcpkg
BuildRequires:	cmake >= 3.14
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	ninja
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm} aarch64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		vcpkgrootdir	%{_datadir}/%{name}

%description
Vcpkg helps you manage C and C++ libraries on Windows, Linux and
MacOS.

%description -l pl.UTF-8
Vcpkg pomaga zarządzać bibliotekami C i C++ w systemach Windows, Linux
i MacOS.

%package root
Summary:	Ports, scripts and triplets for vcpkg
Summary(pl.UTF-8):	Porty, skrypty i trójki dla vcpkg
Group:		Development/Tools
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description root
This package contains vcpkg-root:
- ports, scripts and triplets

%description root -l pl.UTF-8
Ten pakiet zawiera vcpkg-root:
- porty, skrypty i trójki

%prep
%setup -q
%patch0 -p1

%build
install -d toolsrc/build
cd toolsrc/build
%cmake .. \
	-G Ninja \
	-DBUILD_TESTING=OFF \
	-DVCPKG_DEVELOPMENT_WARNINGS=OFF \
	%{!?with_telemetry:-DVCPKG_DISABLE_METRICS=ON}

%ninja_build

cd ../..

%if %{with tests}
toolsrc/build/vcpkg search zlib
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{vcpkgrootdir}}

install -p toolsrc/build/vcpkg $RPM_BUILD_ROOT%{_bindir}
cp -a ports scripts triplets .vcpkg-root $RPM_BUILD_ROOT%{vcpkgrootdir}
ln -s --relative $RPM_BUILD_ROOT%{_bindir}/%{name} $RPM_BUILD_ROOT%{vcpkgrootdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md LICENSE.txt
%doc %lang(zh_CN) README_zh_CN.md
%attr(755,root,root) %{_bindir}/vcpkg

%files root
%defattr(644,root,root,755)
%dir %{vcpkgrootdir}
%{vcpkgrootdir}/.vcpkg-root
%{vcpkgrootdir}/ports
%{vcpkgrootdir}/scripts
%{vcpkgrootdir}/triplets
%attr(755,root,root) %{vcpkgrootdir}/vcpkg
