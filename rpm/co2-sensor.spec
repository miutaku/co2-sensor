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
python3 setup.py install --root=%{buildroot} --optimize=1
install -D -m 644 co2-sensor.service %{buildroot}/usr/lib/systemd/system/co2-sensor.service
install -D -m 644 etc/co2-sensor/config.yml %{buildroot}/etc/co2-sensor/config.yml

%files
%license LICENSE
%doc README.md
/usr/share/co2-sensor/
/usr/lib/systemd/system/co2-sensor.service
/etc/co2-sensor/config.yml

%changelog
* Tue Jul 01 2025 Your Name <your@email.com> - 0.1.0-1
- Initial package
