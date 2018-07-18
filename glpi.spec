# TODO
# - patch for tinymce
# - specs phpcas
# - %s#%{_sysconfdir}#%{_webapps}/%{_webapp}#g
# - config for lighttpd
# - description

%define		ver	9.3
%define		relver	0

Summary:	GLPI - the Information Resource-Manager with an additional Administration Interface
Summary(fr.UTF-8):	GLPI - une application libre, destinée à la gestion de parc informatique et de helpdesk
Summary(pl.UTF-8):	GLPI - zarządca informacji z dodatkowym interfejsem administracyjnym
Name:		glpi
Version:	%{ver}.%{relver}
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	https://github.com/glpi-project/glpi/releases/download/%{version}/%{name}-%{ver}.tgz
# Source0-md5:	e6ec142ee886bab0b20468c5830160da
URL:		http://glpi-project.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	sed >= 4.0
Requires:	group(http)
Requires:	php(curl)
Requires:	php(domxml)
Requires:	php(gd)
Requires:	php(imap)
Requires:	php(json)
Requires:	php(ldap)
Requires:	php(mbstring)
Requires:	php(mysqli)
Requires:	php(openssl)
Requires:	php(session)
Requires:	php(xmlrpc)
Requires:	tinymce
Requires:	user(http)
Requires:	webapps
#Requires:	webserver(access)
#Requires:	webserver(alias)
Requires:	webserver(auth)
#Requires:	webserver(cgi)
#Requires:	webserver(indexfile)
Requires:	webserver(php)
Suggests:	php(opcache)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
GLPI is the Information Resource-Manager with an additional
Administration Interface. You can use it to build up a database with
an inventory for your company (computer, software, printers...). It
has enhanced functions to make the daily life for the administrators
easier, like a job-tracking-system with mail-notification and methods
to build a database with basic information about your
network-topology.

The principal functionalities of the application are:

1) the precise inventory of all the technical resources. All their
characteristics will be stored in a database.

2) management and the history of the maintenance actions and the bound
procedures. This application is dynamic and is directly connected to
the users who can post requests to the technicians. An interface thus
authorizes the latter with if required preventing the service of
maintenance and indexing a problem encountered with one of the
technical resources to which they have access.

%description -l fr.UTF-8
GLPI est une application libre, destinée à la gestion de parc
informatique et de helpdesk.

GLPI est composé d'un ensemble de services web écrits en PHP qui
permettent de recenser et de gérer l'intégralité des composantes
matérielles ou logicielles d'un parc informatique, et ainsi
d'optimiser le travail des techniciens grâce à une maintenance plus
cohérente.

Les fonctionnalités principales de l'application s'articulent autour
des axes suivants :

- Inventaire des ordinateurs, périphériques, réseau, imprimantes et
  consommables associés.

- Gestion des licences (acquises, à acquérir, sites, oem..) et des
  dates d'expiration.

- Affectation du matériel par zone géographique (salle, étage...).

- Gestion des informations commerciales et financières (achat,
  garantie et extension, amortissement).

- Gestion des états de matériel.

- Gestion des demandes d'intervention pour tous les types de matériel
  de l'inventaire.

- Interface utilisateur finale pour demande d'intervention.

- Gestion des entreprises, contrats, documents liés aux éléments
  d'inventaires...

- Réservation de matériel.

- Gestion d'un sytème de base de connaissances hiérarchique (FAQ) ,
  gestion d'une FAQ publique.

- Génération de rapports sur le matériel, de rapports réseau, de
  rapports sur les interventions.

Utilisée conjointement avec un logiciel d'inventaire automatique comme
OCS Inventory NG, vous disposerez d'une solution puissante
d'inventaire et gestion de parc avec mises à jour automatique des
configurations.

%description -l pl.UTF-8
GLPI to zarządca zasobów informacyjnych z dodatkowym interfejsem
administracyjnym. Można go wykorzystać do stworzenia bazy danych z
inwentarzem firmy (komputery, oprogramowanie, drukarki...). Ma
rozszerzone funkcje ułatwiające codzienne życie administratorom, takie
jak system śledzenie zadań z powiadamianiem pocztowym oraz tworzenie
bazy danych z podstawowymi informacjami o topologii sieci.

Podstawowe funkcje aplikacji obejmują:
- dokładny inwentarz zasobów technicznych; cała ich charakterystyka
  jest przechowywana w bazie danych

- zarządzanie i historia zadań administracyjnych oraz związanych z
  nimi procedur. Ta aplikacja jest dynamiczna i związana bezpośrednio z
  użytkownikami, którzy mogą wysyłać żądania do techników. Interfejs po
  zautoryzowaniu tych drugich pokazuje im zgłoszony problem wraz z
  jednym z powiązanych z nimi zasobów technicznych, do których mają
  dostęp.

%prep
%setup -q -n %{name}
rm -r ./lib/tiny_mce

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},/var/lib/%{name}}

cp -a *.php COPYING.txt $RPM_BUILD_ROOT%{_appdir}
cp -aR {ajax,css,front,inc,install,js,lib,locales,pics,plugins,scripts,sound,vendor} $RPM_BUILD_ROOT%{_appdir}
for dir in config files; do
  cp -aR ${dir} $RPM_BUILD_ROOT/var/lib/%{name}/${dir}
  ln -s /var/lib/%{name}/${dir} $RPM_BUILD_ROOT%{_appdir}/${dir}
done

#TODO patch
ln -s %{_datadir}/tinymce $RPM_BUILD_ROOT%{_appdir}/lib/tiny_mce

cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
#install lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

rm $RPM_BUILD_ROOT/var/lib/%{name}/files/_*/remove.txt

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md apirest.md
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%dir %{_appdir}
%attr(770,root,http) %dir /var/lib/%{name}
# displayed in app
%{_appdir}/COPYING.txt
%{_appdir}/*.php
%{_appdir}/ajax
%dir %{_appdir}/config
%attr(770,root,http) %dir /var/lib/%{name}/config
/var/lib/%{name}/config/.htaccess
%{_appdir}/css
%{_appdir}/files
%attr(711,root,http) %dir /var/lib/%{name}/files
/var/lib/%{name}/files/.htaccess
%attr(770,root,http) %dir /var/lib/%{name}/files/_*
%{_appdir}/front
%{_appdir}/inc
%{_appdir}/install
%{_appdir}/js
%{_appdir}/lib
%{_appdir}/locales
%{_appdir}/pics
%{_appdir}/plugins
%{_appdir}/scripts
%{_appdir}/sound
%{_appdir}/vendor
