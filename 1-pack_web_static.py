#!/usr/bin/python3
"""
Script Name: 1-pack_web_static.py
Usage:       fab -f 1-pack_web_static.py do_pack
Description: This Fabric script generates a .tgz archive from the contents
             of the web_static folder of your AirBnB Clone repository using
             the do_pack function.
Author:      Alexander Udeogaranya
Example:     fab -f 1-pack_web_static.py do_pack
"""

from fabric.api import local
from time import strftime


def do_pack():
    """
    Compresses the contents of the web_static folder into a .tgz archive.

    Returns:
        str: The path to the created archive file, or None if archiving fails.
    """

    # Generate a timestamp for the archive filename
    timestamp = strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    try:
        # Create the versions directory if it doesn't exist
        local("mkdir -p versions")

        # Compress the web_static folder into the archive
        local("tar -czvf {} web_static".format(archive_path))

        return archive_path
    except Exception as e:
        return None

