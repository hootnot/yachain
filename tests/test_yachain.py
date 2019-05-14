import sys
import unittest
import yaml
import yachain


yc = """
---
network:
  name: developers
  gitserver:
    ip: 192.168.178.101
    netmask: 255.255.255.0
    gateway: 192.168.178.1
    packages:
    - yum
    - gcc
app:
  logfile: var/log/app.log
  textrules: var/app/app.txt
  database_path: var/app/db
  database_file: /var/app/db/db.txt
  database_name: db.txt
"""

c = None
d = None
e = None


class TestYachain(unittest.TestCase):

    def setUp(self):
        """setup for all tests."""
        with open("/tmp/netw.cfg", "w") as F:
            F.write(yc)
        global c
        global d
        global e
        self.PREFIX = "/yep"
        c = yachain.Config().load("/tmp/netw.cfg")
        d = yachain.Config(prefix=self.PREFIX).load("/tmp/netw.cfg")
        e = yachain.Config(prefix=self.PREFIX, configdata=yaml.load(yc, Loader=yaml.SafeLoader))

    def test_scalar(self):
        self.assertTrue(c["network::gitserver::gateway"] == "192.168.178.1")

    def test_list(self):
        self.assertTrue(c["network::gitserver::packages"] == ['yum', 'gcc'])

    def test_add_prefix_relative_file(self):
        self.assertTrue(d["app::logfile"] == self.PREFIX + "/var/log/app.log")

    def test_relative_non_path_or_file(self):
        self.assertTrue(d["app::textrules"] == "var/app/app.txt")

    def test_relative_prefixed_path(self):
        self.assertTrue(d["app::database_path"] == self.PREFIX + "/var/app/db")

    def test_absolute_file(self):
        self.assertTrue(d["app::database_file"] == "/var/app/db/db.txt")

    def test_absolute_file_bydata(self):
        self.assertTrue(e["app::database_file"] == "/var/app/db/db.txt")

    def test_no_data_error(self):
        cfg = yachain.Config()
        with self.assertRaises(yachain.NoDataError) as err:
            cfg["app::database_file"]
        self.assertTrue(isinstance(err.exception, yachain.NoDataError))

    def test_key_error(self):
        with self.assertRaises(KeyError) as err:
            d["app::not_there"]
        self.assertTrue(isinstance(err.exception, KeyError))


if __name__ == "__main__":

    unittest.main()
