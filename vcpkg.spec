#
# Conditional build:
%bcond_without	tests		# build with tests

Summary:	C++ Library Manager for Windows, Linux, and MacOS
Name:		vcpkg
Version:	2020.04
Release:	1
License:	MIT
Group:		Development/Tools
Source0:	https://github.com/microsoft/vcpkg/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	13e30379de51a284a66c311ac45b64a6
URL:		https://docs.microsoft.com/en-us/cpp/vcpkg
BuildRequires:	cmake
BuildRequires:	ninja
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Vcpkg helps you manage C and C++ libraries on Windows, Linux and
MacOS.

%prep
%setup -q

%build
CXX="%{__cxx}" \
sh -x ./bootstrap-vcpkg.sh -useSystemBinaries

%if %{with tests}
./vcpkg search zlib
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libexecdir}/%{name}}
install -p vcpkg $RPM_BUILD_ROOT%{_libexecdir}/%{name}
cp -a ports scripts triplets .vcpkg-root $RPM_BUILD_ROOT%{_libexecdir}/%{name}
ln -s --relative %{_libexecdir}/%{name}/%{name} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md LICENSE.txt
%doc %lang(zh_CN) README_zh_CN.md
%attr(755,root,root) %{_bindir}/vcpkg
%dir %{_libexecdir}/%{name}
%attr(755,root,root) %{_libexecdir}/%{name}/vcpkg
%{_libexecdir}/%{name}/.vcpkg-root
%{_libexecdir}/%{name}/ports
%{_libexecdir}/%{name}/scripts
%{_libexecdir}/%{name}/triplets
