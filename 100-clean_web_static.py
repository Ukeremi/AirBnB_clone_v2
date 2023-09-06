#!/usr/bin/python3
"""
Script Name: 100-clean_web_static.py
Usage:       fab -f 100-clean_web_static.py do_clean:
                number=2 -i my_ssh_private_key -u ubuntu
Description: This Fabric script deletes out-of-date archives and
                keeps a specified number of recent archives.
Author:      Alexander Udeogaranya
"""

import os
from fabric.api import env, run, local

# Define the host servers and user
env.hosts = ['100.25.46.228', '54.236.222.22']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """
    Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives, etc.
    """
    number = int(number)
    if number < 1:
        number = 1

    local_archives = sorted(local("ls -1 versions").split())
    remote_archives = run("ls -1 /data/web_static/releases").split()
    remote_archives = [arch for arch in remote_archives
                       if arch.startswith("web_static_")]

    # Delete local archives
    if len(local_archives) > number:
        archives_to_delete = local_archives[:-number]
        with lcd("versions"):
            for archive in archives_to_delete:
                local("rm -f {}".format(archive))

    # Delete remote archives
    if len(remote_archives) > number:
        archives_to_delete = remote_archives[:-number]
        with cd("/data/web_static/releases"):
            for archive in archives_to_delete:
                run("rm -rf {}".format(archive))
