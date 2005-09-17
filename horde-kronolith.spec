%define	_hordeapp kronolith
#define	_snap	2005-08-01
%define	_rc		rc1
%define	_rel	0.1
#
%include	/usr/lib/rpm/macros.php
Summary:	Kronolith - calendar for Horde
Summary(pl):	Kronolith - kalendarz dla Horde
Name:		%{_hordeapp}
Version:	2.0.4
Release:	%{?_rc:0.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	LGPL
Group:		Applications/WWW
#Source0:	ftp://ftp.horde.org/pub/kronolith/%{_hordeapp}-h3-%{version}.tar.gz
Source0:	ftp://ftp.horde.org/pub/kronolith/%{_hordeapp}-h3-%{version}-%{_rc}.tar.gz
# Source0-md5:	592cb698683e449a6182e0c0b3689543
Source1:	%{_hordeapp}.conf
URL:		http://www.horde.org/kronolith/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.226
BuildRequires:	tar >= 1:1.15.1
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
Requires:	php-xml >= 3:4.1.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_sysconfdir	/etc/horde.org
%define		_appdir		%{hordedir}/%{_hordeapp}

%description
Kronolith is the Horde calendar application. It provides a stable and
featureful individual calendar system for every Horde user, with
integrated collaboration/scheduling features. It makes extensive use
of the Horde Framework to provide integration with other applications.

Right now, Kronolith implements a solid, stand-alone calendar system,
allowing repeating events, all-day events, custom fields, keywords,
shared calendars, iCalendar support, generation of free/busy
information, and managing multiple users through Horde Authentication.
The calendar API that Kronolith uses is abstracted such that it could
work with any backend, but right now we provide SQL (abstracted to
support most databases, including MySQL, PostgreSQL, Oracle, and MSSQL
via PEAR DB), MCAL, and Kolab backend libraries.

%description -l pl
Kronolith to kalendarz b�d�cy aplikacj� dla Horde. Dostarcza stabilny
system kalendarza o du�ych mo�liwo�ciach dla ka�dego u�ytkownika Horde
wraz ze zintegrowanymi mo�liwo�ciami wsp�pracy/planowania.
Intensywnie wykorzystuje szkielet Horde w celu integracji z innymi
aplikacjami.

Jak na razie Kronolith implementuje solidny, samodzielny system
kalendarza, pozwalaj�cy na powtarzanie zdarze�, zdarzenia codzienne,
w�asne pola, s�owa kluczowe, wsp�dzielone kalendarze, obs�ug�
iCalendar, generowanie informacji o wolnym i zaj�tym czasie oraz
zarz�dzanie wieloma u�ytkownikami poprzez uwierzytelnianie Horde. API
kalendarza u�ywane przez Kronolith jest abstrakcyjne, tak �e mo�e
dzia�a� z dowolnym backendem, ale aktualnie dostarczane s� biblioteki
backend�w SQL (jako abstrakcja do obs�ugi wi�kszo�ci baz, w tym MySQL,
PostgreSQL, Oracle i MS SQL poprzez PEAR DB), MCAL i Kolab.

%prep
%setup -q -c -T -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,templates,themes}

cp -a *.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -a $i $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/$(basename $i .dist)
done
echo '<?php ?>' >		$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php
cp -p config/conf.xml	$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.xml
touch					$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php.bak

cp -pR  lib/*                   $RPM_BUILD_ROOT%{_appdir}/lib
cp -pR  locale/*                $RPM_BUILD_ROOT%{_appdir}/locale
cp -pR  templates/*             $RPM_BUILD_ROOT%{_appdir}/templates
cp -pR  themes/*                $RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{_hordeapp} $RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_docdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{_hordeapp}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{_hordeapp}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{_hordeapp}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<EOF
IMPORTANT:
If you are installing for the first time, you must now
create the Kronolith database tables. Look into directory
%{_docdir}/%{name}-%{version}/sql
to find out how to do this for your database.
EOF
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc README docs/* scripts/*
%attr(750,root,http) %dir %{_sysconfdir}/%{_hordeapp}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{_hordeapp}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{_hordeapp}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/%{_hordeapp}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
