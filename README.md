# yachain
YAML access on chained arttribute names.

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

which will give us:

```bash
/home/user/venv/var/log/app.log
var/app.app.txt
/home/user/venv/var/app/db
/var/app/db/db.txt
db.txt
```

So, as expected, the *logfile* and *database_path* got the PREFIX
