Name: Infraero
Version: 1.0.1
Release: 1%{?dist}
Group: Yahoo! Brazil Open Hackday 2010
Summary: Infraero (Brazilian air traffic control department) webspider module
URL: https://github.com/ehrhardt/Infraero
License: Apache Software License 2.0 
Icon: Airplane_silhouette32.xpm

#Relocatable
Prefix: /etc
Prefix: /usr
Prefix: /var

Source0: Infraero.py
Source1: README.txt
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  
#Requires:       

#%%description

%prep
#%%setup -q

%build
#%%configure
#make %%{?_smp_mflags}

%install
#rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT
install Infraero.py $RPM_BUILD_ROOT/%{_libdir}/python2.7/site-packages/Infraero.py
install README.txt $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/README.txt

%clean
rm -rf $RPM_BUILD_ROOT
#rm -rf %%{buildroot}

%pre
#exit 0

%post
#/sbin/chkconfig --add ypbind

%preun
#if [ "$1" = 0 ] ; then
#/sbin/service ypbind stop > /dev/null 2>&1
#/sbin/chkconfig --del ypbind
#fi
#exit 0

%postun
#if [ "$1" -ge 1 ]; then
#/sbin/service ypbind condrestart > /dev/null 2>&1
#fi
#exit 0

%files
%defattr(-,root,root,-)
%{_libdir}/python2.7/site-packages/Infraero.py
%doc /usr/share/doc/%{name}-%{version}/README.txt

%changelog

* Fri Aug 31 2018 Danilo Bento <ehrhardt@geocities.com>

- RPM skeleton build
