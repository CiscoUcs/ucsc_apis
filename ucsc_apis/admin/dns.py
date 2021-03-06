# Copyright 2017 Cisco Systems, Inc.
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
This module performs the operation related to dns server management.
"""
from ucscsdk.ucscexception import UcscOperationError
from ..common.utils import get_device_profile_dn
ucsc_base_dn = get_device_profile_dn(name="default")


def dns_server_add(handle, name, descr=None, **kwargs):
    """
    Adds a dns server

    Args:
        handle (UcscHandle)
        descr (string): description
        name (string): IP Address of dns server
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommDnsProvider: Managed object

    Example:
        mo = dns_server_add(handle, name="8.8.8.8", descr="dns_google")
    """

    from ucscsdk.mometa.comm.CommDnsProvider import CommDnsProvider

    mo = CommDnsProvider(
        parent_mo_or_dn=ucsc_base_dn + "/dns-svc",
        name=name,
        descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def dns_server_get(handle, name):
    """
    Gets the dns entry

    Args:
        handle (UcscHandle)
        name (string): IP address of the dns server

    Returns:
        CommDnsProvider: Managed object OR None

    Example:
        bool_var = dns_server_get(handle, "10.10.10.10")
    """

    dn = ucsc_base_dn + "/dns-svc/dns-" + name
    return handle.query_dn(dn)


def dns_server_exists(handle, name, **kwargs):
    """
    Checks if the dns entry already exists

    Args:
        handle (UcscHandle)
        name (string): IP address of the dns server
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        bool_var = dns_server_exists(handle, "10.10.10.10")
    """

    mo = dns_server_get(handle, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def dns_server_remove(handle, name):
    """
    Removes a dns server

    Args:
        handle (UcscHandle)
        name (string): IP Address of the dns server

    Returns:
        None

    Raises:
        UcscOperationError: If CommDnsProvider is not present

    Example:
        dns_server_remove(handle, "10.10.10.10")
    """

    mo = dns_server_get(handle, name)
    if not mo:
        raise UcscOperationError("dns_server_remove",
                                 "dns server '%s' not found" % name)

    handle.remove_mo(mo)
    handle.commit()


def dns_set_domain_name(handle, domain, **kwargs):
    """
    Sets the Ucs Central domain name for dns

    Args:
        handle (UcscHandle)
        domain (string): Domain name
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommDns : Managed Object

    Raises:
        UcscOperationError: If CommDns is not present

    Example:
        dns_set_domain_name(handle, domain="cisco.com")
    """

    dn = ucsc_base_dn + "/dns-svc"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcscOperationError("dns_set_domain_name",
                                 "dns MO doesn't exist")
    mo.domain = domain

    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo
