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
This module contains methods required for creating MAC Pools.
"""
from ucscsdk.ucscexception import UcscOperationError


def mac_pool_create(handle, name, r_from, to, descr=None, parent_dn="org-root",
                    **kwargs):
    """
    Creates MAC Pool

    Args:
        handle (UcscHandle)
        name (string) : Mac Pool Name
        r_from (string) : Beginning MAC Address
        to (string) : Ending MAC Address
        descr (string) : description
        parent_dn (string) : Dn of the Org
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        None

    Example:
        mac_pool_create(handle, "sample_mac_pool",
                    "00:25:B5:00:00:00", "00:25:B5:00:00:03")
    """
    from ucscsdk.mometa.macpool.MacpoolPool import MacpoolPool
    from ucscsdk.mometa.macpool.MacpoolBlock import MacpoolBlock

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise UcscOperationError("mac_pool_create",
                                 "Org %s does not exist" % parent_dn)

    mo = MacpoolPool(parent_mo_or_dn=obj,
                     descr=descr,
                     name=name)

    mo.set_prop_multiple(**kwargs)

    MacpoolBlock(parent_mo_or_dn=mo,
                 to=to,
                 r_from=r_from)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def mac_pool_get(handle, name, parent_dn="org-root"):
    """
    Gets the MAC Pool
    Args:
        handle (UcscHandle)
        name (string) : Network Control Policy Name
        parent_dn (string) : Dn of the Org
    Returns:
        (True/False, MO/None)
    Example:
        mac_pool_get(handle, "sample_mac_pool")
    """
    dn = parent_dn + '/mac-pool-' + name
    return handle.query_dn(dn)


def mac_pool_exists(handle, name, descr=None,
                    r_from=None, to=None, parent_dn="org-root"):
    """
    Checks if the given MAC Pool already exists with the same params
    Note: For mac_pool exist, both "r_from" and "to" must be provided
    Args:
        handle (UcscHandle)
        name (string) : Network Control Policy Name
        r_from (string) : Beginning MAC Address
        to (string) : Ending MAC Address
        descr (string) : description
        parent_dn (string) : Dn of the Org
    Returns:
        (True/False, MO/None)
    Example:
        bool_var = mac_pool_exists(handle, "sample_mac_pool",
                        "00:25:B5:00:00:00", "00:25:B5:00:00:03")
    """
    mo = mac_pool_get(handle, name, parent_dn)
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
    return (True, mo)


def mac_pool_remove(handle, name, parent_dn="org-root"):
    """
    Removes the specified MAC Pool
    Args:
        handle (UcscHandle)
        name (string) : MAC Pool Name
        parent_dn (string) : Dn of the Org
    Returns:
        None
    Raises:
        UcscOperationError: If the MAC Pool is not found
    Example:
        mac_pool_remove(handle, "sample_mac", parent_dn="org-root")
        mac_pool_remove(handle, "demo_mac_pool", parent_dn="org-root/org-demo")
    """
    mo = mac_pool_get(handle, name, parent_dn)
    if not mo:
        raise UcscOperationError("mac_pool_remove",
                                 "MAC pool %s does not exist" % name)

    handle.remove_mo(mo)
    handle.commit()
