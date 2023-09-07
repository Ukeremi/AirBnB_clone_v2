#!/usr/bin/python3
"""
Script Name: 2-do_deploy_web_static.py
Usage:       fab -f 2-do_deploy_web_static.py
                do_deploy:archive_path=<path_to_archive>
Description: This Fabric script deploys a web_static archive to web servers.
             It uploads, uncompresses, & manages symbolic links - the archive.
Author:      Alexander Udeogaranya
Example:     fab -f 2-do_deploy_web_static.py
                do_deploy:archive_path=versions/web_static_20170315003959.tgz
"""

from fabric.api import *
from datetime import datetime
from os import path

# Define the host servers and user
env.hosts = ['100.25.46.228', '54.236.222.22']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    Deploys the web_static archive to the web servers.

    Args:
        archive_path (str): The path to the web_static archive.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    try:
        if not path.exists(archive_path):
            return False

        # Extract the filename from the archive path
        filename = archive_path.split("/")[-1]
        # Remove the file extension (.tgz) to get the timestamp
        timestamp = filename[:-4]

        # Create paths
        archive_src = "/tmp/" + filename
        archive_dst = "/data/web_static/releases/" + timestamp

        # Upload the archive
        put(archive_path, archive_src)

        # Create the destination directory
        run("sudo mkdir -p {}".format(archive_dst))

        # Extract the archive
        run("sudo tar -xzf {} -C {}".format(archive_src, archive_dst))

        # Delete the archive
        run("sudo rm {}".format(archive_src))

        # Move contents to the correct location
        run("sudo mv {}/web_static/* {}".format(archive_dst, archive_dst))

        # Remove the old symbolic link
        run("sudo rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("sudo ln -s {} /data/web_static/current".format(archive_dst))

        return True

    except Exception as e:
        return False
