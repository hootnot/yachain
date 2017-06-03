import sys
import unittest
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

class TestYachain(unittest.TestCase):

    def setUp(self):
        """setup for all tests."""
        with open("/tmp/netw.cfg", "w") as F:
            F.write(yc)
        global c
        global d
        self.PREFIX = "/yep"
        c = yachain.Config().load("/tmp/netw.cfg")
        d = yachain.Config(prefix=self.PREFIX).load("/tmp/netw.cfg")

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



if __name__ == "__main__":

    unittest.main()
