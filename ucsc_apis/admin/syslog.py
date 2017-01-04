# Copyright 2015 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This module performs the operation related to syslog.
"""
ucsc_base_dn = "org-root/deviceprofile-default"


def syslog_local_console_enable(handle, severity="emergencies", **kwargs):
    """
    This method enables system logs on local console.

    Args:
        handle (UcscHandle)
        severity (string): Level of logging.
                           ["alerts", "critical", "emergencies"]
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSyslogConsole: Managed Object

    Raises:
        ValueError: If CommSyslogConsole is not present

    Example:
        syslog_local_console_enable(handle, severity="alert")
    """

    from ucscsdk.mometa.comm.CommSyslogConsole import \
        CommSyslogConsoleConsts

    dn = ucsc_base_dn + "/syslog/console"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sys log console does not exist.")

    mo.admin_state = CommSyslogConsoleConsts.ADMIN_STATE_ENABLED
    mo.severity = severity

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_console_disable(handle):
    """
    This method disables system logs on local console.

    Args:
        handle (UcscHandle)

    Returns:
        CommSyslogConsole: Managed Object

    Raises:
        ValueError: If CommSyslogConsole is not present

    Example:
        syslog_local_console_enable(handle)
    """

    from ucscsdk.mometa.comm.CommSyslogConsole import \
        CommSyslogConsoleConsts

    dn = ucsc_base_dn + "/syslog/console"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sys log console does not exist.")

    mo.admin_state = CommSyslogConsoleConsts.ADMIN_STATE_DISABLED
    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_monitor_enable(handle, severity="emergencies", **kwargs):
    """
    This method enables logs on local monitor.

    Args:
        handle (UcscHandle)
        severity (string): Level of logging.
                        ["alerts", "critical", "debugging", "emergencies",
                        "errors", "information", "notifications", "warnings"]
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSyslogMonitor: Managed Object

    Raises:
        ValueError: If CommSyslogMonitor is not present

    Example:
        syslog_local_monitor_enable(handle, severity="alert")
    """

    from ucscsdk.mometa.comm.CommSyslogMonitor import \
        CommSyslogMonitorConsts

    dn = ucsc_base_dn + "/syslog/monitor"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sys log monitor does not exist.")

    mo.admin_state = CommSyslogMonitorConsts.ADMIN_STATE_ENABLED
    mo.severity = severity

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_monitor_disable(handle):
    """
    This method disables logs on local monitor.

    Args:
        handle (UcscHandle)

    Returns:
        CommSyslogMonitor: Managed Object

    Raises:
        ValueError: If CommSyslogMonitor is not present

    Example:
        mo = syslog_local_monitor_disable(handle)
    """

    from ucscsdk.mometa.comm.CommSyslogMonitor import \
        CommSyslogMonitorConsts

    dn = ucsc_base_dn + "/syslog/monitor"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sys log monitor does not exist.")

    mo.admin_state = CommSyslogMonitorConsts.ADMIN_STATE_DISABLED

    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_file_enable(handle, name="", severity="emergencies",
                             size="40000", **kwargs):
    """
    This method configures System Logs on local file storage.

    Args:
        handle (UcscHandle)
        name (string): Name of Log file.
        severity (string): Level of logging.
        size (string): Maximum allowed size of log file(In KBs).
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSyslogFile: Managed object

    Raises:
        ValueError: If CommSyslogFile is not present

    Example:
        syslog_local_file_enable(handle, severity="alert", size="435675",
                                name="sys_log")
    """

    from ucscsdk.mometa.comm.CommSyslogFile import CommSyslogFileConsts

    dn = ucsc_base_dn + "/syslog/file"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sys log file does not exist.")

    mo.admin_state = CommSyslogFileConsts.ADMIN_STATE_ENABLED
    mo.name = name
    mo.severity = severity
    mo.size = size

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_file_disable(handle):
    """
    This method disables System Logs on local file storage.

    Args:
        handle (UcscHandle)

    Returns:
        CommSyslogFile: Managed Object

    Raises:
        ValueError: If CommSyslogFile is not present

    Example:
        syslog_local_file_disable(handle)
    """

    from ucscsdk.mometa.comm.CommSyslogFile import CommSyslogFileConsts

    dn = ucsc_base_dn + "/syslog/file"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sys log file does not exist.")

    mo.admin_state = CommSyslogFileConsts.ADMIN_STATE_DISABLED
    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_remote_enable(handle, name, hostname="none",
                         severity="emergencies", forwarding_facility="local0",
                         **kwargs):
    """
    This method enables System Logs on remote server.

    Args:
        handle (UcscHandle)
        name (string): Remote Server ID -
                            "primary" or "secondary" or "tertiary"
        hostname (string) : Remote host IP or Name
        severity (string): Level of logging.
                        ["alerts", "critical", "debugging", "emergencies",
                        "errors", "information", "notifications", "warnings"]

        forwarding_facility (string): Forwarding mechanism local0 to local7.
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSyslogClient Object

    Raises:
        ValueError: If CommSyslogClient is not present

    Example:
        syslog_remote_enable(handle, name="primary", hostname="192.168.1.2",
                    severity="alert")
    """

    from ucscsdk.mometa.comm.CommSyslogClient import \
        CommSyslogClientConsts

    dn = ucsc_base_dn + "/syslog/client-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Remote Destination '%s' does not exist" % dn)

    mo.admin_state = CommSyslogClientConsts.ADMIN_STATE_ENABLED
    mo.forwarding_facility = forwarding_facility
    mo.hostname = hostname
    mo.severity = severity

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_remote_disable(handle, name):
    """
    This method enables System Logs on remote server.

    Args:
        handle (UcscHandle)
        name (string): Remote Server ID -
                            "primary" or "secondary" or "tertiary"

    Returns:
        CommSyslogClient: Managed Object

    Raises:
        ValueError: If CommSyslogClient is not present

    Example:
        syslog_remote_disable(handle, name="primary")
    """

    from ucscsdk.mometa.comm.CommSyslogClient import \
        CommSyslogClientConsts

    dn = ucsc_base_dn + "/syslog/client-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Remote Destination '%s' does not exist" % dn)

    mo.admin_state = CommSyslogClientConsts.ADMIN_STATE_DISABLED

    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_source(handle, faults=None, audits=None, events=None, **kwargs):
    """
    This method configures Type of System Logs.

    Args:
        handle (UcscHandle)
        faults (string) : for fault logging. ["disabled", "enabled"]
        audits (string): for audit task logging. ["disabled", "enabled"]
        events (string): for event logging. ["disabled", "enabled"]
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSyslogSource: Managed object

    Raises:
        ValueError: If CommSyslogSource is not present

    Example:
            syslog_source(handle, faults="enabled", audits="disabled",
                    events="disabled")

    """

    dn = ucsc_base_dn + "/syslog/source"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("local sources '%s' does not exist" % dn)

    if faults is not None:
        mo.faults = faults
    if audits is not None:
        mo.audits = audits
    if events is not None:
        mo.events = events

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo
