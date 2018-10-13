#
# Conditional build:
%bcond_with	tests		# build with tests

Summary:	Engine for processing 3D models into G-code instructions for 3D printers
Summary(pl.UTF-8):	Silnik do przetwarzania modeli 3D na instrukcje G-code dla drukarek 3D
Name:		CuraEngine
Version:	2.5.0
Release:	3
Epoch:		1
License:	AGPL v3
Group:		Applications/Engineering
Source0:	https://github.com/Ultimaker/CuraEngine/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8d8de8f56fd5831b3b74e8946a26681e
Patch0:		%{name}-rpath.patch
Patch1:		%{name}-static-libstdcpp.patch
Patch2:		%{name}-system-libs.patch
URL:		https://github.com/Ultimaker/CuraEngine
BuildRequires:	cmake
BuildRequires:	libArcus-devel = %{version}
BuildRequires:	libstdc++-devel
BuildRequires:	polyclipping-devel >= 6.1.2
BuildRequires:	protobuf-devel
%{?with_tests:BuildRequires:  python}
BuildRequires:	rapidjson-devel
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
%patch0 -p1
%patch1 -p1
%patch2 -p1

# bundled libraries
rm -rf libs
%{__sed} -i 's|#include <clipper/clipper.hpp>|#include <polyclipping/clipper.hpp>|' src/utils/*.h src/*.cpp

# The -DCURA_ENGINE_VERSION does not work, so we sed-change the default value
%{__sed} -i 's/"DEV"/"%{version}"/' src/settings/settings.h

%build
mkdir build
cd build
%cmake .. \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DCURA_ENGINE_VERSION:STRING=%{version}

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
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/%{name}
