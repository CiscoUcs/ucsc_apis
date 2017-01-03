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
This module performs the operation related to snmp server, user and traps.
"""
ucsc_base_dn = "org-root/deviceprofile-default"


def snmp_enable(handle, community=None, sys_contact=None, sys_location=None,
                descr=None, **kwargs):
    """
    Enables SNMP.

    Args:
        handle (UcscHandle)
        community (string): community
        sys_contact (string): sys_contact
        sys_location (string): sys_location
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSnmp: Managed object

    Raises:
        ValueError: If CommSnmp Mo is not present

    Example:
        mo = snmp_enable(handle,
                    community="username",
                    sys_contact="user contact",
                    sys_location="user location",
                    descr="SNMP Service")

    """

    from ucscsdk.mometa.comm.CommSnmp import CommSnmpConsts

    dn = ucsc_base_dn + "/snmp-svc"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("snmp config '%s' does not exist" % dn)

    mo.admin_state = CommSnmpConsts.ADMIN_STATE_ENABLED

    if community is not None:
        mo.community = community
    if sys_contact is not None:
        mo.sys_contact = sys_contact
    if sys_location is not None:
        mo.sys_location = sys_location
    if descr is not None:
        mo.descr = descr

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def snmp_disable(handle):
    """
    Disables SNMP.

    Args:
        handle (UcscHandle)

    Returns:
        CommSnmp: Managed Object

    Raises:
        ValueError: If CommSnmp Mo is not present

    Example:
        snmp_disable(handle)
    """

    from ucscsdk.mometa.comm.CommSnmp import CommSnmpConsts

    dn = ucsc_base_dn + "/snmp-svc"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("snmp config '%s' does not exist" % dn)

    mo.admin_state = CommSnmpConsts.ADMIN_STATE_DISABLED
    handle.set_mo(mo)
    handle.commit()
    return mo


def snmp_trap_add(handle, hostname, community, port="162", version="v2c",
                  notification_type="traps", v3_privilege="noauth", **kwargs):
    """
    Adds snmp trap.

    Args:
        handle (UcscHandle)
        hostname (string): ip address
        community (string): community
        port (number): port
        version (string): "v1", "v2c", "v3"
        notification_type (string): "informs", "traps"
            Required only for version "v2c" and "v3"
        v3_privilege (string): "auth", "noauth", "priv"
            Required only for version "v3"
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSnmpTrap: Managed Object

    Example:
        snmp_trap_add(handle, hostname="10.10.10.10",
                      community="username", port="162",
                      version="v2c",
                      notification_type="informs")

    """

    from ucscsdk.mometa.comm.CommSnmpTrap import CommSnmpTrap
    mo = CommSnmpTrap(
        parent_mo_or_dn=ucsc_base_dn + "/snmp-svc",
        hostname=hostname,
        community=community,
        port=port,
        version=version,
        notification_type=notification_type,
        v3_privilege=v3_privilege)

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def snmp_trap_exists(handle, hostname, **kwargs):
    """
    checks if snmp trap exists

    Args:
        handle (UcscHandle)
        hostname (string): ip address
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        snmp_trap_exists(handle, hostname="10.10.10.10",
                      community="username", port="162",
                      version="v2c",
                      notification_type="informs")

    """

    dn = ucsc_base_dn + "/snmp-svc/snmp-trap" + hostname
    mo = handle.query_dn(dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def snmp_trap_modify(handle, hostname, **kwargs):
    """
    Modifies snmp trap.

    Args:
        handle (UcscHandle)
        hostname (string): ip address
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        CommSnmpTrap: Managed Object

    Raises:
        ValueError: If CommSnmpTrap Mo is not present

    Example:
        snmp_trap_modify(handle, hostname="10.10.10.10",
                          community="username", port="162",
                          version="v3",
                          notification_type="traps",
                          v3_privilege="noauth")

    """

    dn = ucsc_base_dn + "/snmp-svc/snmp-trap" + hostname
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("snmp trap MO is not available")

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def snmp_trap_remove(handle, hostname):
    """
    Modifies snmp trap.

    Args:
        handle (UcscHandle)
        hostname (string): ip address

    Returns:
        None

    Raises:
        ValueError: If CommSnmpTrap Mo is not present

    Example:
        snmp_trap_remove(handle, hostname="10.10.10.10")

    """

    dn = ucsc_base_dn + "/snmp-svc/snmp-trap" + hostname
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("snmp trap MO is not available")

    handle.remove_mo(mo)
    handle.commit()


def snmp_user_add(handle, name, pwd, privpwd, auth="md5",
                  use_aes="no", descr="", **kwargs):
    """
    Adds snmp user.

    Args:
        handle (UcscHandle)
        name (string): snmp username
        descr (string): description
        pwd (string): password
        privpwd (string): privacy password
        auth (string): "md5", "sha"
        use_aes (string): "yes", "no"
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSnmpUser: Managed Object

    Example:
        snmp_user_add(handle, name="snmpuser", descr="", pwd="password",
                    privpwd="password", auth="sha")

    """

    from ucscsdk.mometa.comm.CommSnmpUser import CommSnmpUser

    mo = CommSnmpUser(
        parent_mo_or_dn=ucsc_base_dn + "/snmp-svc",
        name=name,
        descr=descr,
        pwd=pwd,
        privpwd=privpwd,
        auth=auth,
        use_aes=use_aes)

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def snmp_user_exists(handle, name, **kwargs):
    """
    checks if snmp user exists.

    Args:
        handle (UcscHandle)
        name (string): snmp username
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        snmp_user_exists(handle, name="snmpuser", descr="",
                    auth="sha")

    """

    dn = ucsc_base_dn + "/snmp-svc/snmpv3-user-" + name
    mo = handle.query_dn(dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def snmp_user_modify(handle, name, **kwargs):
    """
    Modifies snmp user.

    Args:
        handle (UcscHandle)
        name (string): snmp username
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        CommSnmpUser: Managed Object

    Raises:
        ValueError: If CommSnmpUser Mo is not present

    Example:
        snmp_user_modify(handle, name="snmpuser", descr="",
                          pwd="password", privpwd="password",
                          auth="md5", use_aes="no")

    """

    dn = ucsc_base_dn + "/snmp-svc/snmpv3-user-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("snmp user MO is not available")

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def snmp_user_remove(handle, name):
    """
    removes snmp user.

    Args:
        handle (UcscHandle)
        name (string): snmp username

    Returns:
        None

    Raises:
        ValueError: If CommSnmpUser Mo is not present

    Example:
        snmp_user_remove(handle, name="snmpuser")

    """

    dn = ucsc_base_dn + "/snmp-svc/snmpv3-user-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("snmp user MO is not available")

    handle.remove_mo(mo)
    handle.commit()
