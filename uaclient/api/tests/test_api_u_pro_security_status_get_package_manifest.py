import mock

from uaclient import apt
from uaclient.api.u.security.package_manifest.v1 import _package_manifest

M_PATH = "uaclient.api.u.security.package_manifest.v1"


@mock.patch("uaclient.snap.system.subp")
@mock.patch(M_PATH + ".apt.get_installed_packages")
class TestPackageInstalledV1:
    def test_snap_packages_added(
        self, installed_apt_pkgs, sys_subp, FakeConfig
    ):
        installed_apt_pkgs.return_value = []
        sys_subp.return_value = (
            "Name  Version Rev Tracking Publisher Notes\n"
            "helloworld 6.0.16 126 latest/stable dev1 -\n"
            "bare 1.0 5 latest/stable canonical** base\n"
            "canonical-livepatch 10.2.3 146 latest/stable canonical** -\n"
        ), ""
        result = _package_manifest(FakeConfig())
        assert (
            "snap:helloworld\tlatest/stable\t126\n"
            + "snap:bare\tlatest/stable\t5\n"
            + "snap:canonical-livepatch\tlatest/stable\t146\n"
            == result.manifest_data
        )

    def test_apt_packages_added(
        self, installed_apt_pkgs, sys_subp, FakeConfig
    ):
        sys_subp.return_value = "", ""
        apt_pkgs = [
            apt.InstalledAptPackages(
                name="one", arch="all", version="4:1.0.2"
            ),
            apt.InstalledAptPackages(
                name="two", arch="amd64", version="0.1.1"
            ),
        ]
        installed_apt_pkgs.return_value = apt_pkgs
        result = _package_manifest(FakeConfig())
        assert "one\t4:1.0.2\ntwo:amd64\t0.1.1\n" == result.manifest_data

    def test_apt_snap_packages_added(
        self, installed_apt_pkgs, sys_subp, FakeConfig
    ):
        apt_pkgs = [
            apt.InstalledAptPackages(
                name="one", arch="all", version="4:1.0.2"
            ),
            apt.InstalledAptPackages(
                name="two", arch="amd64", version="0.1.1"
            ),
        ]
        sys_subp.return_value = (
            "Name  Version Rev Tracking Publisher Notes\n"
            "helloworld 6.0.16 126 latest/stable dev1 -\n"
            "bare 1.0 5 latest/stable canonical** base\n"
            "canonical-livepatch 10.2.3 146 latest/stable canonical** -\n"
        ), ""
        installed_apt_pkgs.return_value = apt_pkgs
        result = _package_manifest(FakeConfig())
        assert (
            "one\t4:1.0.2\ntwo:amd64\t0.1.1\n"
            + "snap:helloworld\tlatest/stable\t126\n"
            + "snap:bare\tlatest/stable\t5\n"
            + "snap:canonical-livepatch\tlatest/stable\t146\n"
            == result.manifest_data
        )
