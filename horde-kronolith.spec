Summary:	Kronolith - calendar for HORDE
Summary(pl):	Kronolith - kalendarz dla HORDE
Name:		kronolith
Version:	2.0.1
Release:	0.2
License:	LGPL
Vendor:		The Horde Project
Group:		Applications/Mail
Source0:	http://ftp.horde.org/pub/kronolith/%{name}-h3-%{version}.tar.gz
# Source0-md5:	c8c5b26095a82305579e838875f97b8f
Source1:	%{name}.conf
URL:		http://www.horde.org/kronolith/
PreReq:		apache
Requires(post):	grep
Requires:	horde >= 3.0
Requires:	php-xml >= 4.1.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apachedir	/etc/httpd
%define		hordedir	/usr/share/horde
%define		confdir		/etc/horde.org

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
install -d $RPM_BUILD_ROOT{%{apachedir},%{confdir}/kronolith} \
	$RPM_BUILD_ROOT%{hordedir}/kronolith/{lib,locale,templates,themes,scripts}

cp -pR	*.php			$RPM_BUILD_ROOT%{hordedir}/kronolith
cp -pR  config/*.dist           $RPM_BUILD_ROOT%{confdir}/kronolith
cp -pR  config/*.xml            $RPM_BUILD_ROOT%{confdir}/kronolith
echo "<?php ?>" > 		$RPM_BUILD_ROOT%{confdir}/kronolith/conf.php
cp -pR  lib/*                   $RPM_BUILD_ROOT%{hordedir}/kronolith/lib
cp -pR  locale/*                $RPM_BUILD_ROOT%{hordedir}/kronolith/locale
cp -pR  templates/*             $RPM_BUILD_ROOT%{hordedir}/kronolith/templates
cp -pR  themes/*                $RPM_BUILD_ROOT%{hordedir}/kronolith/themes

cp -p   config/.htaccess        $RPM_BUILD_ROOT%{confdir}/kronolith

install %{SOURCE1} 		$RPM_BUILD_ROOT%{apachedir}
ln -fs %{confdir}/%{name} 	$RPM_BUILD_ROOT%{hordedir}/%{name}/config

# bit unclean..
cd $RPM_BUILD_ROOT%{confdir}/kronolith
for i in *.dist; do cp $i `basename $i .dist`; done

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

cat <<_EOF2_
IMPORTANT:
If you are installing for the first time, you must now
create the Kronolith database tables. Look into directory
/usr/share/doc/%{name}-%{version}/scripts
to find out how to do this for your database.
_EOF2_

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
	    rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
	    /usr/sbin/apachectl restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README docs/* scripts/*
%dir %{hordedir}/%{name}
%attr(640,root,http) %{hordedir}/%{name}/*.php
%attr(750,root,http) %{hordedir}/%{name}/lib
%attr(750,root,http) %{hordedir}/%{name}/locale
%attr(750,root,http) %{hordedir}/%{name}/templates
%attr(750,root,http) %{hordedir}/%{name}/themes

%attr(750,root,http) %dir %{confdir}/%{name}
%dir %{hordedir}/%{name}/config
%attr(640,root,http) %{confdir}/%{name}/*.dist
%attr(640,root,http) %{confdir}/%{name}/.htaccess
%attr(640,root,http) %config(noreplace) %{apachedir}/%{name}.conf
%attr(660,root,http) %config(noreplace) %{confdir}/%{name}/*.php
%attr(640,root,http) %config(noreplace) %{confdir}/%{name}/*.xml
