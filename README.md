# yachain
YAML access on chained attribute names.

Suppose we have:

```yaml
network:
   name: developers
   gitserver:
      ip: 192.168.178.101
      netmask: 255.255.255.0
      gateway: 192.168.178.1
      packages:
      - yum
      - gcc
```

With *yachain* we can access this as:

```python
>>> import yachain

>>> c = yachain.Config().load("netw.cfg")
>>> print(c["network::gitserver::gateway"])
192.168.178.1
>>> print(c["network::gitserver::packages"])
['yum', 'gcc']
```

References to files / paths independent from environment
--------------------------------------------------------

References to files and paths can be used relative and absolute.
In case an attribute ends on 'path' or 'file' then the path can be
prefixed automatically when operation from a virtual environment is detected.
The works by default upper and lower case and can be overriden.

```python
# yaml config:
yc = """
---
app:
  logfile: var/log/app.log
  textrules: var/app.app.txt
  database_path: var/app/db
  database_file: /var/app/db/db.txt
  database_name: db.txt
"""

import yachain
import yaml
import sys
import os

PREFIX = "/" if not hasattr(sys, 'real_prefix') else sys.prefix
# CONFIG_FILE = os.path.join(PREFIX, "etc/app/app.cfg")
config = yachain.Config(prefix=PREFIX, configdata=yaml.load(yc))


for A in ["logfile",
          "textrules",
          "database_path",
          "database_file",
          "database_name"]:
    k = "app::{}".format(A)
    print config[k]
```

When run from a virtual environment, this will give us:

```bash
/home/user/venv/var/log/app.log
var/app.app.txt
/home/user/venv/var/app/db
/var/app/db/db.txt
db.txt
```

So, as expected, the *logfile* and *database_path* got the PREFIX.

When run from a non-virtual environment, this will give us:

```bash
/var/log/app.log
var/app.app.txt
/var/app/db
/var/app/db/db.txt
db.txt
```

So, as expected, prefixed with "/".
