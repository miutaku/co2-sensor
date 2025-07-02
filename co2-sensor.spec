%define _unpackaged_files_terminate_build 0
Name:           co2-sensor
Version:        0.1.0
Release:        1%{?dist}
Summary:        CO2 sensor API for Raspberry Pi using mh_z19
License:        MIT
URL:            https://github.com/yourname/co2-sensor
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3, python3-setuptools, python3-flask, python3-pip
Requires:       python3, python3-flask, python3-pip

%description
Raspberry Pi用MH-Z19 CO2センサーAPIサーバ

%prep
%setup -q

%build
python3 setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python3 setup.py install --root=$RPM_BUILD_ROOT
install -D -m 644 co2-sensor.service $RPM_BUILD_ROOT%{_unitdir}/co2-sensor.service

%files
%doc README.md
%license LICENSE
/usr/share/co2-sensor/
%{_unitdir}/co2-sensor.service

%post
/bin/systemctl daemon-reload || :

%preun
if [ $1 -eq 0 ]; then
    /bin/systemctl --no-reload disable co2-sensor.service > /dev/null 2>&1 || :
    /bin/systemctl stop co2-sensor.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload || :
