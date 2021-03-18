%{?mingw_package_header}

Name:           mingw-zstd
Version:        1.3.6
Release:        1%{?dist}
Summary:        Cross-compiled Zstd compression library

License:        BSD and GPLv2
URL:            https://github.com/facebook/zstd
Source0:        https://github.com/facebook/zstd/archive/v%{version}.tar.gz

Patch0:         0001-Cross-dlltool.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-binutils

BuildRequires:  make

%description
Zstd, short for Zstandard, is a fast lossless compression algorithm,
targeting real-time compression scenarios at zlib-level compression ratio.

# Win32
%package -n mingw32-libzstd
Summary:        MinGW libzstd

%description -n mingw32-libzstd
MinGW compiled libzstd for the Win32 target.

%package -n mingw32-libzstd-static
Summary:        MinGW libzstd (static)
Group:          Development/Libraries
Requires:       mingw32-libzstd = %{version}-%{release}

%description -n mingw32-libzstd-static
MingW compiled static libzstd for the Win32 target.

# Win64
%package -n mingw64-libzstd
Summary:        MinGW libzstd

%description -n mingw64-libzstd
MinGW compiled libzstd for the Win64 target.

%package -n mingw64-libzstd-static
Summary:        MinGW libzstd (static)
Group:          Development/Libraries
Requires:       mingw64-libzstd = %{version}-%{release}

%description -n mingw64-libzstd-static
MingW compiled static libzstd for the Win64 target.

%{?mingw_debug_package}

%prep
%autosetup -p1 -n zstd-%{version}

# create two copies of the source folder as zstd doesn't support out of source builds
mkdir ../build_win32
mv * ../build_win32
mv ../build_win32 .
mkdir build_win64
cp -Rp build_win32/* build_win64

%build
# how not to cross-compile things...
export OS="Windows_NT"
export MOREFLAGS="-fno-pic"

pushd build_win32
make -C lib PREFIX=%{mingw32_prefix} CC=%{mingw32_cc} DLLTOOL=/usr/%{mingw32_target}/bin/dlltool
popd

pushd build_win64
make -C lib PREFIX=%{mingw64_prefix} CC=%{mingw64_cc} DLLTOOL=/usr/%{mingw64_target}/bin/dlltool
popd

%install
export OS="Windows_NT"

pushd build_win32
make -C lib install PREFIX=%{mingw32_prefix} CC=%{mingw32_cc} DLLTOOL=/usr/%{mingw32_target}/bin/dlltool DESTDIR=$RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT%{mingw32_prefix}/bin/
mv $RPM_BUILD_ROOT%{mingw32_prefix}/lib/*.dll $RPM_BUILD_ROOT%{mingw32_prefix}/bin/
cp lib/dll/libzstd.lib $RPM_BUILD_ROOT%{mingw32_prefix}/lib/libzstd.dll.a
rm $RPM_BUILD_ROOT%{mingw32_prefix}/lib/libzstd.so $RPM_BUILD_ROOT%{mingw32_prefix}/lib/libzstd.so.1
popd

pushd build_win64
make -C lib install PREFIX=%{mingw64_prefix} CC=%{mingw64_cc} DLLTOOL=/usr/%{mingw64_target}/bin/dlltool DESTDIR=$RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT%{mingw64_prefix}/bin/
mv $RPM_BUILD_ROOT%{mingw64_prefix}/lib/*.dll $RPM_BUILD_ROOT%{mingw64_prefix}/bin/
cp lib/dll/libzstd.lib $RPM_BUILD_ROOT%{mingw64_prefix}/lib/libzstd.dll.a
rm $RPM_BUILD_ROOT%{mingw64_prefix}/lib/libzstd.so $RPM_BUILD_ROOT%{mingw64_prefix}/lib/libzstd.so.1
popd

%files -n mingw32-libzstd
%{mingw32_bindir}/*.dll
%{mingw32_libdir}/*.dll.a
%{mingw32_libdir}/pkgconfig/*.pc
%{mingw32_includedir}/*.h

%files -n mingw32-libzstd-static
%{mingw32_libdir}/*.a
%exclude %{mingw32_libdir}/*.dll.a

%files -n mingw64-libzstd
%{mingw64_bindir}/*.dll
%{mingw64_libdir}/*.dll.a
%{mingw64_libdir}/pkgconfig/*.pc
%{mingw64_includedir}/*.h

%files -n mingw64-libzstd-static
%{mingw64_libdir}/*.a
%exclude %{mingw64_libdir}/*.dll.a
