%define		hordeapp kronolith
#
%include	/usr/lib/rpm/macros.php
Summary:	Kronolith - calendar for Horde
Summary(pl.UTF-8):	Kronolith - kalendarz dla Horde
Name:		horde-%{hordeapp}
Version:	2.3
Release:	0.1
License:	LGPL
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/kronolith/%{hordeapp}-h3-%{version}.tar.gz
# Source0-md5:	81500ac468942a64a8faa03063f26d10
Source1:	%{hordeapp}.conf
URL:		http://www.horde.org/kronolith/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	horde >= 3.0
Requires:	php(xml)
Requires:	php-common >= 3:4.1.0
Requires:	webapps
Obsoletes:	%{hordeapp}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{hordeapp}
%define		_webapps	/etc/webapps
%define		_webapp		horde-%{hordeapp}
%define		_sysconfdir	%{_webapps}/%{_webapp}

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

%description -l pl.UTF-8
Kronolith to kalendarz będący aplikacją dla Horde. Dostarcza stabilny
system kalendarza o dużych możliwościach dla każdego użytkownika Horde
wraz ze zintegrowanymi możliwościami współpracy/planowania.
Intensywnie wykorzystuje szkielet Horde w celu integracji z innymi
aplikacjami.

Jak na razie Kronolith implementuje solidny, samodzielny system
kalendarza, pozwalający na powtarzanie zdarzeń, zdarzenia codzienne,
własne pola, słowa kluczowe, współdzielone kalendarze, obsługę
iCalendar, generowanie informacji o wolnym i zajętym czasie oraz
zarządzanie wieloma użytkownikami poprzez uwierzytelnianie Horde. API
kalendarza używane przez Kronolith jest abstrakcyjne, tak że może
działać z dowolnym backendem, ale aktualnie dostarczane są biblioteki
backendów SQL (jako abstrakcja do obsługi większości baz, w tym MySQL,
PostgreSQL, Oracle i MS SQL poprzez PEAR DB), MCAL i Kolab.

%prep
%setup -q -n %{hordeapp}-h3-%{version}

for i in config/*.dist; do
	mv $i config/$(basename $i .dist)
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/docs}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
echo '<?php ?>' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak
cp -a calendars feed js lib locale templates themes $RPM_BUILD_ROOT%{_appdir}
cp -a docs/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<EOF
IMPORTANT:
If you are installing Kronolith for the first time, you must now
create the Kronolith database tables. Look into directory
%{_docdir}/%{name}-%{version}/sql
to find out how to do this for your database.
EOF
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README docs/* scripts/*
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/calendars
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/feed
%{_appdir}/js
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
