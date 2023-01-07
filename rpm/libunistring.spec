%bcond_with doc

Version: 0.9.10
Release: 1
Name: libunistring
Summary: GNU Unicode string library
License: GPLv2+ or LGPLv3+
URL: https://www.gnu.org/software/libunistring/
Source0: https://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.xz
BuildRequires: gcc
BuildRequires: make
BuildRequires: gperf
%{?with_doc:BuildRequires texinfo}
#Provides: bundled(gnulib)

%description
This portable C library implements Unicode string types in three flavours:
(UTF-8, UTF-16, UTF-32), together with functions for character processing
(names, classifications, properties) and functions for string processing
(iteration, formatted output, width, word breaks, line breaks, normalization,
case folding and regular expressions).

%package devel
Summary: GNU Unicode string library - development files
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for programs using libunistring.

%prep
%setup -q -n %name-%version/upstream

%build
ln -sf ../gnulib
./autogen.sh
%configure --disable-static --disable-rpath
%make_build gnulib-local lib tests %{?with_doc: doc}

%install
for dir in gnulib-local lib tests %{?with_doc: doc}; do
    %{__make} -C $dir install DESTDIR=%{?buildroot} INSTALL="%{__install} -p"
done

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.la
# Move staged docs so not picked up by %%doc in main package
%{?with_doc:mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name} __doc}

%files
%license COPYING COPYING.LIB
%doc AUTHORS NEWS README
%{_libdir}/%{name}.so.*

%files devel
%doc HACKING DEPENDENCIES THANKS ChangeLog
%if %{with doc}
%doc __doc/*
%{_infodir}/%{name}.info*
%endif
%{_libdir}/%{name}.so
%{_includedir}/unistring
%{_includedir}/*.h
