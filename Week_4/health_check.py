#!/usr/bin/env python3
"""System Resouce and DNS Check.

Checks if host enviroment resources are low or DNS for localhost is
misconfigured. If true, sends email alert for each issue to specified address.
Script is intended to be called by a cronjob so provides no console output.
"""
import socket
import os
import shutil
import psutil
import emails

SENDER = "automation@example.com"
RECIPIENT = "{}@example.com".format(os.environ.get('USER'))
BODY = "Please check your system and resolve the issue as soon as possible."


def check_disk_space_under(disk, threshold):
    """Check if space on a disk is greater than threshold in percent."""
    diskusage = shutil.disk_usage(disk)
    free = diskusage.free / diskusage.total * 100
    return free < threshold


def check_cpu_usage_over(threshold):
    """Check if CPU usage is greater than threshold in percent."""
    usage = psutil.cpu_percent(1)
    return usage > threshold


def check_available_memory_under(threshold):
    """Return the memory usage in MB."""
    usage = psutil.virtual_memory().available >> 20
    return usage < threshold


def check_hostname_resolves_to(host, ip_address):
    """Check if a host resolves to a specified IP."""
    try:
        resolved_ip = socket.gethostbyname(host)
        return resolved_ip == ip_address
    except socket.error:
        return False


# Email an error if CPU usage is over 80%
if check_cpu_usage_over(80):
    subject = "Error - CPU usage is over 80%"
    emails.send(emails.generate(SENDER, RECIPIENT, subject, BODY, ""))

# Report an error if available disk space is lower than 20%
if check_disk_space_under("/", 20):
    subject = "Error - Available disk space is less than 20%"
    emails.send(emails.generate(SENDER, RECIPIENT, subject, BODY, ""))

# Report an error if available memory is less than 500MB
if check_available_memory_under(500):
    subject = "Error - Available memory is less than 500MB"
    emails.send(emails.generate(SENDER, RECIPIENT, subject, BODY, ""))

# Report an error if the hostname "localhost" cannot be resolved to "127.0.0.1"
if not check_hostname_resolves_to("localhost", "127.0.0.1"):
    subject = "Error - localhost cannot be resolved to 127.0.0.1"
    emails.send(emails.generate(SENDER, RECIPIENT, subject, BODY, ""))
