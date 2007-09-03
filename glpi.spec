# TODO
# - patch for ezpdf,phpcas,tinymce
# - specs ezpdf,phpcas
# - %s#%{_sysconfdir}#%{_webapps}/%{_webapp}#g
# - config for lighttpd
# - description

%define		ver	0.68.3
%define		relver	2

Summary:	GLPI - the Information Resource-Manager with an additional Administration Interface
Summary(fr.UTF-8):	GLPI - une application libre, destinée à la gestion de parc informatique et de helpdesk
Name:		glpi
Version:	%{ver}.%{relver}
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://www.glpi-project.org/IMG/gz/%{name}-%{ver}-%{relver}.tar.gz
# Source0-md5:	918dbd3cb175625a4421097bbec43cc4
URL:		http://glpi-project.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Requires:	tinymce
Requires:	phpcas
Requires:	ezpdf
Requires(triggerpostun):	sed >= 4.0
#Requires:	webserver(access)
#Requires:	webserver(alias)
Requires:	webserver(auth)
#Requires:	webserver(cgi)
#Requires:	webserver(indexfile)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
GLPI is the Information Resource-Manager with an additional Administration- Interface. You can use it to build up a database with an inventory for your company (computer, software, printers...). It has enhanced functions to make the daily life for the administrators easier, like a job-tracking-system with mail-notification and methods to build a database with basic information about your network-topology.

The principal functionalities of the application are :

1) the precise inventory of all the technical resources. All their characteristics will be stored in a database.

2) management and the history of the maintenance actions and the bound procedures. This application is dynamic and is directly connected to the users who can post requests to the technicians. An interface thus authorizes the latter with if required preventing the service of maintenance and indexing a problem encountered with one of the technical resources to which they have access.

%description -l fr.UTF-8
GLPI est une application libre, destinée à la gestion de parc informatique et de helpdesk.

GLPI est composé d’un ensemble de services web écrits en PHP qui permettent de recenser et de gérer l’intégralité des composantes matérielles ou logicielles d’un parc informatique, et ainsi d’optimiser le travail des techniciens grâce à une maintenance plus cohérente.

Les fonctionnalités principales de l’application s’articulent autour des axes suivants :

- Inventaire des ordinateurs, périphériques, réseau, imprimantes et consommables associés.

- Gestion des licences (acquises, à acquérir, sites, oem..) et des dates d’expiration.

- Affectation du matériel par zone géographique (salle, étage...).

- Gestion des informations commerciales et financières (achat, garantie et extension, amortissement).

- Gestion des états de matériel.

- Gestion des demandes d’intervention pour tous les types de matériel de l’inventaire.

- Interface utilisateur finale pour demande d’intervention.

- Gestion des entreprises, contrats, documents liés aux éléments d’inventaires...

- Réservation de matériel.

- Gestion d’un sytème de base de connaissances hiérarchique (FAQ) , gestion d’une FAQ publique.

- Génération de rapports sur le matériel, de rapports réseau, de rapports sur les interventions.

Utilisée conjointement avec un logiciel d’inventaire automatique comme OCS Inventory NG, vous disposerez d’une solution puissante d’inventaire et gestion de parc avec mises à jour automatique des configurations.

%prep
%setup -q -n %{name}
rm -rf ./lib/{tiny_mce,phpcas,ezpdf}

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -a *.{php,js} $RPM_BUILD_ROOT%{_appdir}
cp -aR {ajax,css,front,inc,install,locales,plugins,pics,lib,config,files,help} $RPM_BUILD_ROOT%{_appdir}
#TODO patch
ln -s %{_datadir}/tinymce $RPM_BUILD_ROOT%{_appdir}/lib/tiny_mce
ln -s %{_datadir}/phpcas $RPM_BUILD_ROOT%{_appdir}/lib/phpcas
ln -s %{_datadir}/ezpdf $RPM_BUILD_ROOT%{_appdir}/lib/ezpdf


install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
#install lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGELOG.txt README.txt
%lang(fr) %doc LISEZMOI.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%{_appdir}/install/*.php
%{_appdir}/install/mysql
#
%{_appdir}/config/*.php
%{_appdir}/config/.htaccess
#
%{_appdir}/*.php
%{_appdir}/*.js
%{_appdir}/ajax/*.php
%{_appdir}/inc/*.php
%{_appdir}/css/*.css
%{_appdir}/front/*.php
%{_appdir}/front/*.html
%{_appdir}/help/*.html
%{_appdir}/locales/*.php
%{_appdir}/pics/icones/*.png
%{_appdir}/pics/*.gif
%{_appdir}/pics/*.png
%{_appdir}/pics/*.ico
%{_appdir}/lib/*.php
%{_appdir}/lib/scriptaculous/*.js
%{_appdir}/lib/calendar/*.js
%{_appdir}/lib/calendar/lang/*.js
%{_appdir}/lib/calendar/aqua/*.gif
%{_appdir}/lib/calendar/aqua/*.css
%{_appdir}/lib/calendar/images/*.gif
%{_appdir}/lib/vcardclass/classes-vcard.php
%{_appdir}/lib/phpmailer/*.php
%{_appdir}/lib/phpmailer/language/*.php
#
%{_appdir}/lib/tiny_mce
%{_appdir}/lib/phpcas
%{_appdir}/lib/ezpdf
