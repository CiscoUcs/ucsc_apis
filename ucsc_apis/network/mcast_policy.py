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
This module performs the create the multicast policer under the specified org
"""
from ucscsdk.ucscexception import UcscOperationError


def mcast_policy_create(handle, name, querier_state="disabled",
                        snooping_state="disabled",
                        querier_ip_addr="0.0.0.0",
                        descr=None, parent_dn="org-root", **kwargs):
    """
    Creates Multicast Policy

    Args:
        handle (UcscHandle)
        name (string)
        querier_state (string) : ["disabled", "enabled"]
        snooping_state (string) : ["disabled", "enabled"]
        querier_ip_addr (string) : IP address of querier
        descr (string) : description
        parent_dn (string) : Dn of org
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        FabricMulticastPolicy: Managed Object

    Example:
        mcast_policy_create(handle, "my_mcast", "disabled", "enabled")
    """
    from ucscsdk.mometa.fabric.FabricMulticastPolicy import \
        FabricMulticastPolicy

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise UcscOperationError("mcast_policy_create",
                                 "Org %s does not exist" % parent_dn)

    mcast_policy = FabricMulticastPolicy(parent_mo_or_dn=obj,
                                         querier_ip_addr=querier_ip_addr,
                                         name=name,
                                         descr=descr,
                                         querier_state=querier_state,
                                         snooping_state=snooping_state)

    mcast_policy.set_prop_multiple(**kwargs)

    handle.add_mo(mcast_policy, modify_present=True)
    handle.commit()
    return mcast_policy


def mcast_policy_get(handle, name, parent_dn="org-root"):
    """
    Gets the mcast policy

    Args:
        handle (Ucshandle)
        name (string): Name of the policy
        parent_dn (string): Dn of org

    Returns:
        FabricMulticastPolicy: Managed Object OR None

    Example:
        mcast_policy_get(handle, "demo")
    """
    dn = parent_dn + '/mc-policy-' + name
    return handle.query_dn(dn)


def mcast_policy_exists(handle, name, parent_dn="org-root", **kwargs):
    """
    Checks if the mcast policy object exists

    Args:
        handle (Ucshandle)
        name (string): Name of the policy
        parent_dn (string): Dn of org
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        bool_var = mcast_policy_exists(handle, "demo")
        bool_var = mcast_policy_exists(handle, "demo", "org-root/org-demo")
    """
    mo = mcast_policy_get(handle, name, parent_dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def mcast_policy_delete(handle, name, parent_dn="org-root"):
    """
    Deletes a Multicast Policy

    Args:
        handle (UcscHandle)
        name (string): Name of the policy
        parent_dn (string): Dn of org

    Returns:
        None

    Example:
        mcast_policy_delete(handle, "my_mcast")
        mcast_policy_delete(handle, "my_mcast", "org-root/org-demo")
    """
    mo = mcast_policy_get(handle, name, parent_dn)
    if not mo:
        raise UcscOperationError("mcast_policy_delete",
                                 "Mcast policy does not exist")

    handle.remove_mo(mo)
    handle.commit()
