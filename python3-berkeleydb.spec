#
# Conditional build:
%bcond_with	agpl	# generate AGPLv3 licensed package
%bcond_with	doc	# API documentation (fails with sphinx 4.5/docutils 0.18)
%bcond_without	tests	# unit tests

Summary:	Python bindings for Oracle Berkeley DB
Summary(pl.UTF-8):	Wiązania Pythona do Oracle Berkeley DB
Name:		python3-berkeleydb
Version:	18.1.5
Release:	2
%if %{with agpl}
License:	AGPL v3
%else
License:	BSD
%endif
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/berkeleydb/
Source0:	https://files.pythonhosted.org/packages/source/b/berkeleydb/berkeleydb-%{version}.tar.gz
# Source0-md5:	d7e0cf782268806d681c6648d2a48d12
URL:		https://pypi.org/project/berkeleydb/
# supported versions: 4.8, 5.3, 6.2, 18.1
BuildRequires:	db-devel >= 4.8
%if %{without agpl}
BuildRequires:	db-devel < 6
%endif
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-setuptools >= 1:49.1.2
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
Obsoletes:	python3-bsddb3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python bindings for Oracle Berkeley DB.

%description -l pl.UTF-8
Wiązania Pythona do Oracle Berkeley DB.

%package apidocs
Summary:	API documentation for Python berkeleydb module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona berkeleydb
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python berkeleydb module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona berkeleydb.

%prep
%setup -q -n berkeleydb-%{version}

%{__sed} -i -e "s,'build','build-3'," test.py

%build
export BERKELEYDB_DIR=%{_prefix}
export BERKELEYDB_LIBDIR=%{_libdir}
%if %{with agpl}
export YES_I_HAVE_THE_RIGHT_TO_USE_THIS_BERKELEY_DB_VERSION=1
%endif

%py3_build

%if %{with tests}
%{__python3} test.py
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

export BERKELEYDB_DIR=%{_prefix}
export BERKELEYDB_LIBDIR=%{_libdir}
%if %{with agpl}
export YES_I_HAVE_THE_RIGHT_TO_USE_THIS_BERKELEY_DB_VERSION=1
%endif
%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BerkeleyDB_issues.txt ChangeLog LICENSE.txt README.txt TODO.txt licenses.txt
%dir %{py3_sitedir}/berkeleydb
%{py3_sitedir}/berkeleydb/*.py
%attr(755,root,root) %{py3_sitedir}/berkeleydb/*.so
%{py3_sitedir}/berkeleydb/__pycache__
%{py3_sitedir}/berkeleydb-%{version}-py*.egg-info
# -devel?
%{py3_incdir}/berkeleydb

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/*.html
%endif
