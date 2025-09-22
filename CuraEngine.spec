#
# Conditional build:
%bcond_with	tests		# build with tests

Summary:	Engine for processing 3D models into G-code instructions for 3D printers
Summary(pl.UTF-8):	Silnik do przetwarzania modeli 3D na instrukcje G-code dla drukarek 3D
# keep in sync with cura, libArcus, libSavitar, python3-Uranium
Name:		CuraEngine
Version:	4.13.2
Release:	2
Epoch:		1
License:	AGPL v3
Group:		Applications/Engineering
#Source0Download: https://github.com/Ultimaker/CuraEngine/tags
Source0:	https://github.com/Ultimaker/CuraEngine/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	85b46d4282dc061345d4efda822fae19
Source1:	https://raw.githubusercontent.com/nothings/stb/master/stb_image.h
# Source1-md5:	27932e6fb3a2f26aee2fc33f2cb4e696
Patch0:		%{name}-includes.patch
Patch1:		%{name}-static-libstdcpp.patch
Patch2:		local-stb.patch
URL:		https://github.com/Ultimaker/CuraEngine
BuildRequires:	cmake >= 3.8.0
%{?with_tests:BuildRequires:  gmock-devel >= 1.8.0}
BuildRequires:	libArcus-devel = %{version}
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	polyclipping-devel >= 6.1.2
BuildRequires:	protobuf-devel >= 3.0.0
%{?with_tests:BuildRequires:  python3 >= 1:3}
BuildRequires:	rapidjson-devel
%requires_eq	libArcus
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CuraEngine is a C++ console application for 3D printing G-code
generation. It has been made as a better and faster alternative to the
old Skeinforge engine.

This is just a console application for G-code generation. For a full
graphical application look at cura with is the graphical frontend for
CuraEngine.

%description -l pl.UTF-8
CuraEngine to aplikacja konsolowa C++ do generowania intrukcji G-code
dla drukarek 3D. Powstała jako lepsza i szybsza alternatywa dla
starego silnika Skeinforge.

To jest tylko aplikacja konsolowa do generowania kodu. Pełna graficzna
aplikacja, będąca graficznym interfejsem do CuraEngine, znajduje się w
pakiecie cura.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

mkdir stb
cp -p %{SOURCE1} stb/

# bundled libraries
%{__rm} -rf libs
%{__sed} -i 's|#include <clipper/clipper.hpp>|#include <polyclipping/clipper.hpp>|' src/utils/*.h src/*.cpp

# The -DCURA_ENGINE_VERSION does not work, so we sed-change the default value
%{__sed} -i 's/"DEV"/"%{version}"/' src/settings/Settings.h

%build
mkdir build
cd build
%cmake .. \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	%{?with_tests:-DBUILD_TESTS:BOOL=ON} \
	-DCURA_ENGINE_VERSION:STRING=%{version} \
	-DSET_RPATH:BOOL=OFF \
	-DStb_INCLUDE_DIRS:STRING="$(pwd)/.." \
	-DUSE_SYSTEM_LIBS:BOOL=ON

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/%{name}
