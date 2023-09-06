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

def upload_archive(archive_path, timestamp):
    """
    Uploads the web_static archive to the server and uncompresses it.

    Args:
        archive_path (str): The path to the web_static archive.
        timestamp (str): The timestamp for the archive.

    Returns:
        None
    """
    archive_src = '/tmp/web_static_{}.tgz'.format(timestamp)
    archive_dst = '/data/web_static/releases/web_static_{}/'.format(timestamp)
    
    put(archive_path, archive_src)
    run('sudo mkdir -p {}'.format(archive_dst))
    run('sudo tar -xzf {} -C {}'.format(archive_src, archive_dst))
    run('sudo rm {}'.format(archive_src))

def move_contents(timestamp):
    """
    Moves the contents of the web_static archive to the web_static directory.

    Args:
        timestamp (str): The timestamp for the archive.

    Returns:
        None
    """
    release_base = '/data/web_static/releases/web_static_{}/'.format(timestamp)
    src_dir = release_base + 'web_static/'
    dst_dir = release_base

    run('sudo mv {}* {}'.format(src_dir, dst_dir))
    run('sudo rm -rf {}'.format(src_dir))

def recreate_symlink(timestamp):
    """
    Recreates the symbolic link for web_static.

    Args:
        timestamp (str): The timestamp for the archive.

    Returns:
        None
    """
    current_link = '/data/web_static/current'
    new_link = '/data/web_static/releases/web_static_{}/'.format(timestamp)

    run('sudo rm -rf {}'.format(current_link))
    run('sudo ln -s {} {}'.format(new_link, current_link))

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

        timestamp = archive_path[-18:-4]

        # Upload archive
        upload_archive(archive_path, timestamp)

        # Move contents
        move_contents(timestamp)

        # Recreate symbolic link
        recreate_symlink(timestamp)

    except Exception as e:
        return False

    return True
