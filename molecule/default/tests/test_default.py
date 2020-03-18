import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_sssd_conf(host):
    conf = host.file('/etc/sssd/sssd.conf')

    assert conf.exists
    assert conf.user == 'root'
    assert conf.group == 'root'

def test_sssd_conf_content(host):
    conf = host.file('/etc/sssd/sssd.conf')
    conf_content = conf.content

    expected = [
        b'config_file_version = 2',
        b'services = nss, pam, ssh, sudo',
        b'domains = domain.com',
        b'filter_groups = root',
        b'filter_users = root',
        b'reconnection_retries = 3',
        b'[domain/domain.com]'
    ]

    for line in expected:
        assert line in conf_content
