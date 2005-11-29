%define	_hordeapp kronolith
#define	_snap	2005-08-01
#define	_rc		rc1
%define	_rel	1.1
#
%include	/usr/lib/rpm/macros.php
Summary:	Kronolith - calendar for Horde
Summary(pl):	Kronolith - kalendarz dla Horde
Name:		horde-%{_hordeapp}
Version:	2.0.5
Release:	%{?_rc:0.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	LGPL
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/kronolith/%{_hordeapp}-h3-%{version}.tar.gz
# Source0-md5:	cce9751c2de5ebb5ce55cb643662fd3e
#Source0:	ftp://ftp.horde.org/pub/kronolith/%{_hordeapp}-h3-%{version}-%{_rc}.tar.gz
Source1:	%{_hordeapp}.conf
URL:		http://www.horde.org/kronolith/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.226
BuildRequires:	tar >= 1:1.15.1
Requires:	apache(mod_access)
Requires:	horde >= 3.0
Requires:	php-xml >= 3:4.1.0
Requires:	webapps
Requires:	webserver = apache
Obsoletes:	%{_hordeapp}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{_hordeapp}
%define		_webapps	/etc/webapps
%define		_webapp		horde-%{_hordeapp}
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

%description -l pl
Kronolith to kalendarz bêd±cy aplikacj± dla Horde. Dostarcza stabilny
system kalendarza o du¿ych mo¿liwo¶ciach dla ka¿dego u¿ytkownika Horde
wraz ze zintegrowanymi mo¿liwo¶ciami wspó³pracy/planowania.
Intensywnie wykorzystuje szkielet Horde w celu integracji z innymi
aplikacjami.

Jak na razie Kronolith implementuje solidny, samodzielny system
kalendarza, pozwalaj±cy na powtarzanie zdarzeñ, zdarzenia codzienne,
w³asne pola, s³owa kluczowe, wspó³dzielone kalendarze, obs³ugê
iCalendar, generowanie informacji o wolnym i zajêtym czasie oraz
zarz±dzanie wieloma u¿ytkownikami poprzez uwierzytelnianie Horde. API
kalendarza u¿ywane przez Kronolith jest abstrakcyjne, tak ¿e mo¿e
dzia³aæ z dowolnym backendem, ale aktualnie dostarczane s± biblioteki
backendów SQL (jako abstrakcja do obs³ugi wiêkszo¶ci baz, w tym MySQL,
PostgreSQL, Oracle i MS SQL poprzez PEAR DB), MCAL i Kolab.

%prep
%setup -q -c -T -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,templates,themes}

cp -a *.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -a $i $RPM_BUILD_ROOT%{_sysconfdir}/$(basename $i .dist)
done
echo '<?php ?>' >		$RPM_BUILD_ROOT%{_sysconfdir}/conf.php
cp -p config/conf.xml	$RPM_BUILD_ROOT%{_sysconfdir}/conf.xml
touch					$RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak

cp -pR  lib/*                   $RPM_BUILD_ROOT%{_appdir}/lib
cp -pR  locale/*                $RPM_BUILD_ROOT%{_appdir}/locale
cp -pR  templates/*             $RPM_BUILD_ROOT%{_appdir}/templates
cp -pR  themes/*                $RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_docdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
install %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf

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

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache >= 2.0.0
%webapp_register httpd %{_webapp}

%triggerun -- apache >= 2.0.0
%webapp_unregister httpd %{_webapp}

%triggerpostun -- horde-%{_hordeapp} < 2.0.4-1.1
for i in conf.php conf.xml keywords.php menu.php prefs.php; do
	if [ -f /etc/horde.org/%{_hordeapp}/$i.rpmsave ]; then
		mv -f %{_sysconfdir}/$i{,.rpmnew}
		mv -f /etc/horde.org/%{_hordeapp}/$i.rpmsave %{_sysconfdir}/$i
	fi
done

if [ -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave ]; then
	mv -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	cp -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave %{_sysconfdir}/apache.conf
	cp -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave %{_sysconfdir}/httpd.conf
fi

if [ -L /etc/apache/conf.d/99_horde-%{_hordeapp}.conf ]; then
	/usr/sbin/webapp register apache %{_webapp}
	rm -f /etc/apache/conf.d/99_horde-%{_hordeapp}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache reload 1>&2
	fi
fi
if [ -L /etc/httpd/httpd.conf/99_horde-%{_hordeapp}.conf ]; then
	/usr/sbin/webapp register httpd %{_webapp}
	rm -f /etc/httpd/httpd.conf/99_horde-%{_hordeapp}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README docs/* scripts/*
%attr(750,root,http) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/httpd.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
