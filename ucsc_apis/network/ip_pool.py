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
This module contains methods required for creating IP Pools.
"""
from ucscsdk.ucscexception import UcscOperationError


def ip_pool_create(handle, name, descr=None, parent_dn="org-root", **kwargs):
    """
    Creates IP Pool

    Args:
        handle (UcscHandle)
        name (string) : IP pool name
        descr (string): description
        parent_dn (string) : Dn of org
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        IppoolPool : Managed Object
    Example:
        ip_pool_create(handle, "sample_ip_pool", descr="default")
    """
    from ucscsdk.mometa.ippool.IppoolPool import IppoolPool

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise UcscOperationError("ip_pool_create",
                                 "Org %s does not exist" % parent_dn)
    mo = IppoolPool(parent_mo_or_dn=obj,
                    descr=descr,
                    name=name)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ip_block_add(handle, ip_pool_name, r_from, to, subnet, def_gw,
                 prim_dns="0.0.0.0", sec_dns="0.0.0.0",
                 scope="public", parent_dn="org-root", **kwargs):
    """
    Creates IP Pool block

    Args:
        handle (UcscHandle)
        ip_pool_name (string) : Name of the IP Pool
        r_from (string) : Beginning IP Address
        to (string) : Ending IP Address
        subnet (string) : Subnet
        def_gw (string) : default gateway
        prim_dns (string): primary DNS server
        sec_dns (string): secondary DNS server
        parent_dn (string) : Dn of org
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        IppoolBlock: Managed object
    Raises:
        UcscOperationError: If the IP Pool does not exist
    Example:
        ip_block_add(handle,ip_pool_name="test_ippool", "1.1.1.1", "1.1.1.10",
                    "255.255.255.0", "1.1.1.254", parent_dn="org-root"):
    """

    from ucscsdk.mometa.ippool.IppoolBlock import IppoolBlock

    ip_pool_dn = parent_dn + "/ip-pool-" + ip_pool_name

    obj = handle.query_dn(ip_pool_dn)
    if not obj:
        raise UcscOperationError("ip_block_add",
                                 "IP pool '%s' does not exist", ip_pool_dn)

    mo = IppoolBlock(parent_mo_or_dn=obj,
                     r_from=r_from,
                     to=to,
                     subnet=subnet,
                     def_gw=def_gw,
                     prim_dns=prim_dns,
                     sec_dns=sec_dns,
                     scope=scope)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ip_pool_get(handle, name, parent_dn="org-root"):
    """
    Gets IP Pool if already exists
    Args:
        handle (UcscHandle)
        name (string) : Network Control Policy Name
        parent_dn (string) : Dn of org
    Returns:
        IppoolPool: Managed Object OR None
    Example:
        ip_pool_get(handle, "sample_ip_pool")
    """
    dn = parent_dn + '/ip-pool-' + name
    return handle.query_dn(dn)


def ip_pool_exists(handle, name, descr=None,
                   r_from=None, to=None, subnet=None, def_gw=None,
                   prim_dns=None, sec_dns=None,
                   scope=None, parent_dn="org-root"):
    """
    Checks if the given IP Pool already exists with the same params
    Note: For ip_pool exist, both "r_from" and "to" must be provided
    Args:
        handle (UcscHandle)
        name (string) : Network Control Policy Name
        descr (string) : Description
        r_from (string) : Beginning IP Address
        to (string) : Ending IP Address
        subnet (string) : Subnet
        def_gw (string) : default gateway
        prim_dns (string): primary DNS server
        sec_dns (string): secondary DNS server
        scope (string) : public or private
        parent_dn (string) : Dn of org
    Returns:
        (True/False, MO/None)
    Example:
        ip_pool_exists(handle, "sample_ip_pool",
                       "192.168.1.1", "192.168.1.10")
    """
    mo = ip_pool_get(handle, name, parent_dn)
    if not mo:
        return (False, None)

    args = {'descr': descr}
    if not mo.check_prop_match(**args):
        return (False, None)

    if r_from and to:
        mo_1_dn = mo.dn + '/block-' + r_from + '-' + to
        mo_1 = handle.query_dn(mo_1_dn)
        if not mo_1:
            return (False, None)
        args = {
            'subnet': subnet,
            'def_gw': def_gw,
            'prim_dns': prim_dns,
            'sec_dns': sec_dns,
            'scope': scope
        }
        mo_exists = mo_1.check_prop_match(**args)
        return (mo_exists, mo if mo_exists else None)
    return(True, mo)


def ip_pool_remove(handle, name, parent_dn="org-root"):
    """
    Removes the specified IP Pool
    Args:
        handle (UcscHandle)
        name (string) : IP Pool Name
        parent_dn (string) : Dn of the Org
    Returns:
        None
    Raises:
        UcscOperationError: If the IP Pool does not exist
    Example:
        ip_pool_remove(handle, "sample_ip", parent_dn="org-root")
        ip_pool_remove(handle, "demo_ip_pool", parent_dn="org-root/org-demo")
    """
    mo = ip_pool_get(handle, name, parent_dn)
    if not mo:
        raise UcscOperationError("ip_pool_remove",
                                 "IP pool '%s' does not exist" % name)

    handle.remove_mo(mo)
    handle.commit()
