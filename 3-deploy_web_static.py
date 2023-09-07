#!/usr/bin/python3
"""
Script Name: 3-deploy_web_static.py
Usage:       fab -f 3-deploy_web_static.py deploy
Description: This Fabric script creates and deploys
             a web_static archive to web servers.
             It packages the web_static directory,
             distributes it to the servers, and
             updates the symbolic link.
Author:      Alexander Udeogaranya
"""

from datetime import datetime
from fabric.api import env, local, put, run
import os.path

env.hosts = ['100.25.19.204', '54.157.159.85']


def do_pack():
    """
    Create a tar gzipped archive of the web_static directory.

    Returns:
        str: The path to the created archive on success, None on failure.
    """
    dt = datetime.utcnow()
    file_name = f"web_static_{dt:%Y%m%d%H%M%S}.tgz"
    target_dir = "versions"

    if not os.path.exists(target_dir):
        local("mkdir -p {}".format(target_dir))

    result = local("tar -czvf {}/{} web_static".format(target_dir, file_name))

    if result.failed:
        return None
    else:
        return os.path.join(target_dir, file_name)


def do_deploy(archive_path):
    """
    Distribute an archive to a web server and update the symbolic link.

    Args:
        archive_path (str): The path to the archive to be deployed.

    Returns:
        bool: True on success, False on failure.
    """
    if not os.path.exists(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = file_name.split('.')[0]
    tmp_archive = "/tmp/{}".format(file_name)
    releases_dir = "/data/web_static/releases/{}".format(name)

    if put(archive_path, tmp_archive).failed:
        return False

    commands = [
        "rm -rf {}/".format(releases_dir),
        "mkdir -p {}/".format(releases_dir),
        "tar -xzf {} -C {}/".format(tmp_archive, releases_dir),
        "rm {}".format(tmp_archive),
        "mv {}/web_static/* {}/".format(releases_dir, releases_dir),
        "rm -rf {}/web_static".format(releases_dir),
        "rm -rf /data/web_static/current",
        "ln -s {} /data/web_static/current".format(releases_dir)
    ]

    for cmd in commands:
        if run(cmd).failed:
            return False

    return True


def deploy():
    """
    Create and distribute an archive to a web server
    and update the symbolic link.

    Returns:
        bool: True on successful deployment, False on failure.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
