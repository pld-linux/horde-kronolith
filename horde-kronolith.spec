%include	/usr/lib/rpm/macros.php
Summary:	Kronolith - calendar for HORDE
Summary(pl):	Kronolith - kalendarz dla HORDE
Name:		kronolith
Version:	2.0.3
Release:	0.1
License:	LGPL
Vendor:		The Horde Project
Group:		Applications/Mail
Source0:	http://ftp.horde.org/pub/kronolith/%{name}-h3-%{version}.tar.gz
# Source0-md5:	a17f41f0724acec5e561cfd7300759bd
Source1:	%{name}.conf
URL:		http://www.horde.org/kronolith/
BuildRequires:	rpmbuild(macros) >= 1.177
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
Requires:	php-xml >= 4.1.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{name}
%define		_sysconfdir	/etc/horde.org
%define		_apache1dir	/etc/apache
%define		_apache2dir	/etc/httpd

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
%setup -q -n %{name}-h3-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,templates,themes}

cp -pR	*.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -p $i $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$(basename $i .dist)
done
echo "<?php ?>" > 		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php
cp -pR  config/*.xml            $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php.bak

cp -pR  lib/*                   $RPM_BUILD_ROOT%{_appdir}/lib
cp -pR  locale/*                $RPM_BUILD_ROOT%{_appdir}/locale
cp -pR  templates/*             $RPM_BUILD_ROOT%{_appdir}/templates
cp -pR  themes/*                $RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{name} 	$RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_defaultdocdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

install %{SOURCE1} 		$RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{name}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{name}/conf.php.bak
fi

# apache1
if [ -d %{_apache1dir}/conf.d ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache1dir}/conf.d/99_%{name}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi
# apache2
if [ -d %{_apache2dir}/httpd.conf ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache2dir}/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
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

%postun
if [ "$1" = "0" ]; then
	# apache1
	if [ -d %{_apache1dir}/conf.d ]; then
		rm -f %{_apache1dir}/conf.d/99_%{name}.conf
		if [ -f /var/lock/subsys/apache ]; then
			/etc/rc.d/init.d/apache restart 1>&2
		fi
	fi
	# apache2
	if [ -d %{_apache2dir}/httpd.conf ]; then
		rm -f %{_apache2dir}/httpd.conf/99_%{name}.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/etc/rc.d/init.d/httpd restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc README docs/* scripts/*
%attr(750,root,http) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{name}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{name}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{name}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/%{name}/*.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
