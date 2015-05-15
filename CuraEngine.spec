#
# Conditional build:
%bcond_with	tests		# build with tests

Summary:	Engine for processing 3D models into G-code instructions for 3D printers
Name:		CuraEngine
Version:	15.04
Release:	1
License:	AGPLv3
Group:		Applications/Engineering
Source0:	https://github.com/Ultimaker/CuraEngine/archive/%{version}.tar.gz
# Source0-md5:	75d34492ca18358aa554a56afb2de440
URL:		https://github.com/Ultimaker/CuraEngine
BuildRequires:	libstdc++-devel
BuildRequires:	polyclipping-devel >= 6.1.2
%{?with_tests:BuildRequires:  python}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
%{name} is a C++ console application for 3D printing G-code
generation. It has been made as a better and faster alternative to the
old Skeinforge engine.

This is just a console application for G-code generation. For a full
graphical application look at cura with is the graphical frontend for
%{name}.

%prep
%setup -q

# bundled clipper
rm -r clipper
sed -i 's|#include <clipper/clipper.hpp>|#include <polyclipping/clipper.hpp>|' src/utils/*.h
sed -i 's|-lclipper|-lpolyclipping|g' Makefile
sed -i 's| $(BUILD_DIR)/libclipper.a||g' Makefile

# allow redefinition of CFLAGS and do not build it static
sed -i 's|CFLAGS +=|CFLAGS?=|' Makefile
sed -i 's|--static||g' Makefile

%build
CXX="%{__cxx}" \
CFLAGS="-I. -Ilibs -c %{rpmcflags} %{rpmcppflags} -std=c++11 -fomit-frame-pointer" \
	%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}/%{name}
install -p build/%{name} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/%{name}
