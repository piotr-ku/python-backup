#!/bin/env python3
# -*- coding: utf8 -*- 

"""
Usage:
python3 ./backup.py --help

Exit codes:
0   - success
55  - missing option
56  - missed configuration key
57  - duplicity command error
58  - restore path already exists
59  - restore path parent directory is not writeable
60  - invalid format for --date option, try 2022-04-12T112456 format
"""

import argparse
import dateparser
import os
import subprocess
import sys
import warnings

from dotenv import load_dotenv
from pathlib import Path

# Ignore dateparser warnings regarding pytz
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)

###
# Arguments
#
args = argparse.ArgumentParser()
args.add_argument("action", choices=['make', 'list', 'content', 'restore', 'remove_older_backups', 'cleanup'], help="action")
args.add_argument("-f", "--full", action="store_true", help="create full backup")
args.add_argument("-d", "--date", help="set backup date in 2013-04-30T15:38:59 format")
args.add_argument("-c", "--config", default=str(Path.home()) + '/.backup', help="config directory")
args.add_argument("-p", "--path", help="restore path")
args = args.parse_args()

###
# Configuration
# 

# load variables from .env directory
load_dotenv(".env")
# load missing variables from config directory
load_dotenv(str(args.config)+"/config")
# load missing variables
load_dotenv(".env.default")

# required configuration
required = (
    'BACKUP_DESTINATION',
    'BACKUP_SOURCE',
    'BACKUP_KEEP',
    'AWS_ACCESS_KEY_ID',
    'AWS_SECRET_ACCESS_KEY',
    'PASSPHRASE',
    'DUPLICITY',
    'DUPLICITY_PARAMS',
    'DUPLICITY_VERBOSE',
)

# checking required configuration
for key in required:
    if not key in os.environ:
        print("Missed configuration key:", key)
        sys.exit(56)

# checking required options 
if args.action == "restore" and args.path == None:
    print("--path argument is required for restore action")
    sys.exit(55)

# parse date 
if args.date:
    try:
        args.date = dateparser.parse(args.date).strftime("%Y-%m-%dT%H%M%S")
    except:
        print("Invalid format for --date option, try 2022-04-12T112456 format")
        sys.exit(60)

class Action:
    """
        The class contains all provided actions
    """
    def run(self, command) -> object:
        """
            Run OS command
        """
        # debug mode
        if "DEBUG" in os.environ:
            command.insert(0, "echo")
        
        # run command
        try:
            return subprocess.run(command)
        except Exception as e:
            print(e)
            sys.exit(57)


    def make(self) -> None:
        """
            Make a backup
        """
        # run the hook file if it exists
        if os.path.isfile(str(args.config)+"/hook"):
            subprocess.run(["/bin/sh", str(args.config)+"/hook"])
        
        # create command
        command = [
            os.environ["DUPLICITY"],
            "--verb", os.environ["DUPLICITY_VERBOSE"],
            "--exclude-filelist", str(args.config)+"/include",
            "--exclude", "**",
            os.environ["BACKUP_SOURCE"], 
            os.environ["BACKUP_DESTINATION"],
        ]
        
        # add duplicity arguments
        if os.environ["DUPLICITY_PARAMS"]:
            command = command[0:3] + os.environ["DUPLICITY_PARAMS"].split(" ") + command[3:]
        
        # add full backup mode 
        if args.full:
            command.insert(1, "full")
        
        # run command
        self.run(command)

        # remove old backups and signatures
        if args.full:
            self.remove_older_backups()
            self.cleanup()

    def remove_older_backups(self) -> None:
        """
            Remove old backups from backup destination
        """
        # create command for removing old backups
        command = [
            os.environ["DUPLICITY"],
            "remove-older-than", os.environ["BACKUP_KEEP"], "--force",
            "--verb", "0",
            os.environ["BACKUP_DESTINATION"],
        ]

        # add duplicity arguments
        if os.environ["DUPLICITY_PARAMS"]:
            command = command[0:6] + os.environ["DUPLICITY_PARAMS"].split(" ") + command[6:]
        
        # run command
        self.run(command)

    def cleanup(self) -> None:
        """
            Remove old signatures from backup destination
        """
        # create command for cleanup
        command = [
            os.environ["DUPLICITY"],
            "cleanup", "--force", "--extra-clean",
            "--verb", "0",
            os.environ["BACKUP_DESTINATION"],
        ]

        # add duplicity arguments
        if os.environ["DUPLICITY_PARAMS"]:
            command = command[0:6] + os.environ["DUPLICITY_PARAMS"].split(" ") + command[6:]
        
        # run command
        self.run(command)

    def list(self) -> None:
        """
            Show list of created backups
        """
        # create command for backup list
        command = [
            os.environ["DUPLICITY"],
            "collection-status",
            "--verb", "0",
            os.environ["BACKUP_DESTINATION"],
        ]

        # add duplicity arguments
        if os.environ["DUPLICITY_PARAMS"]:
            command = command[0:4] + os.environ["DUPLICITY_PARAMS"].split(" ") + command[4:]
        
        # run command
        self.run(command)

    def content(self) -> None:
        """
            Show files in the backup
        """
        # create command for backup list
        command = [
            os.environ["DUPLICITY"],
            "list-current-files",
            "--verb", "0",
            os.environ["BACKUP_DESTINATION"],
        ]

        # add duplicity arguments
        if os.environ["DUPLICITY_PARAMS"]:
            command = command[0:4] + os.environ["DUPLICITY_PARAMS"].split(" ") + command[4:]
        
        # add date 
        if args.date:
            command.insert(2, '--time')
            command.insert(3, args.date)

        # run command
        self.run(command)

    def restore(self) -> None:
        """
            Restore backup
        """
        # check if the path already exists
        if os.path.exists(args.path):
            print(f"{args.path} already exists!")
            sys.exit(58)

        # check if parent directory is writeable
        if not os.access(os.path.dirname(args.path), os.W_OK):
            print(f"{os.path.dirname(args.path)} is not writeable!")
            sys.exit(59)

        # create command for backup list
        command = [
            os.environ["DUPLICITY"],
            "--verb", "0",
            os.environ["BACKUP_DESTINATION"],
            args.path,
        ]

        # add duplicity arguments
        if os.environ["DUPLICITY_PARAMS"]:
            command = command[0:3] + os.environ["DUPLICITY_PARAMS"].split(" ") + command[3:]
        
        # add date 
        if args.date:
            command.insert(3, '--time')
            command.insert(4, args.date)

        # run command
        self.run(command)

# run the action
getattr(Action(), args.action)()