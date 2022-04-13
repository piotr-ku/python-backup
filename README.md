Incremental utility tool based on [Duplicity](https://duplicity.gitlab.io).
==

## Installation

```bash
poetry install
```

## Usage 

Make incremental backup:

```bash
poetry run python backup.py make
```

Make full backup (it will automatically delete old backups):

```bash
poetry run python backup.py make --full
```

List full and incremental backups:

```bash
poetry run python backup.py list
```

Show files included into the backup:

```bash
poetry run python backup.py content [--date 2022-02-14T08:00:00]
```

Restore backup:

```bash
poetry run python backup.py restore --path ./restored-backup [--date 2022-02-14T08:00:00]
```

## Configuration

Default configuration is in the .env.default file. You can copy it into .env file or ~/.backup/config.

```bash
# Backup settings
BACKUP_KEEP=60d
BACKUP_SOURCE=/home/${USER}
BACKUP_DESTINATION=scp://localhost/backup

# Secrets
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
PASSPHRASE=

# Duplicity command settings
DUPLICITY="/usr/bin/duplicity"
DUPLICITY_PARAMS="--log-file ~/.backup/duplicity.log --asynchronous-upload --no-print-statistics --s3-european-buckets --s3-use-new-style --s3-unencrypted-connection"
DUPLICITY_VERBOSE=2
```

## Hooks

If you have a file ~/.backup/hook, it will be executed before making backup.

## Licence

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
