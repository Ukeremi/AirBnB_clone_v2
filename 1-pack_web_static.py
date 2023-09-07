#!/usr/bin/python3
"""
Fabric script that Generates a .tgz archive
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
