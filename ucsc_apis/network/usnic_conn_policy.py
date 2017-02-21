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
This module contains the methods required for creating usnic Connection Policy.
"""
from ucscsdk.ucscexception import UcscOperationError


def usnic_conn_policy_create(handle, name, descr=None, usnic_count="58",
                             adaptor_profile_name="global-default",
                             parent_dn="org-root", **kwargs):
    """
    Creates usNIC Connection Policy

    Args:
        handle (UcscHandle)
        name (string) : usNIC connection policy name
        descr (string) : description
        parent_dn (string) : Dn of org
        usnic_count (string) : Number of usnics
        adaptor_profile_name (string) : Adaptor policy
                    ['global-default', 'global-Linux', 'global-Solaris',
                     'global-SRIOV', 'global-usNIC', 'global-usNICOrcl',
                     'global-VMWare', 'global-VMPasThr', 'global-Windows']
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        vnicUsnicConPolicy: Managed Object

    Example:
        usnic_conn_policy_create(handle, "samp_usnic_conn", usnic_count="32",
                                 adaptor_profile_name="global-usNIC")
    """

    from ucscsdk.mometa.vnic.VnicUsnicConPolicy import VnicUsnicConPolicy

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise UcscOperationError("usnic_conn_policy_create",
                                 "Org %s does not exist" % parent_dn)

    mo = VnicUsnicConPolicy(parent_mo_or_dn=obj,
                            name=name,
                            descr=descr,
                            usnic_count=usnic_count,
                            adaptor_profile_name=adaptor_profile_name)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def usnic_conn_policy_get(handle, name, parent_dn="org-root"):
    """
    Gets usNIC Connection Policy
    Args:
        handle (UcscHandle)
        name (string) : usNIC Connection Policy name
        parent_dn (string) : Dn of org

    Returns:
        vnicUsnicConPolicy: Managed Object OR None
    Example:
        usnic_conn_policy_get(handle, "samp_usnic_conn")
    """
    dn = parent_dn + '/usnic-con-' + name
    return handle.query_dn(dn)


def usnic_conn_policy_exists(handle, name, parent_dn="org-root", **kwargs):
    """
    Checks if the given usNIC Connection Policy already exists
    Args:
        handle (UcscHandle)
        name (string) : usNIC Connection Policy name
        parent_dn (string) : Dn of org
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    Returns:
        (True/False, MO/None)
    Example:
        found, mo = usnic_conn_policy_exists(handle, "samp_usnic_conn",
                                             usnic_count = "32")
    """
    mo = usnic_conn_policy_get(handle, name, parent_dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def usnic_conn_policy_delete(handle, name, parent_dn="org-root"):
    """
    Deletes a usNIC Connection Policy
    Args:
        handle (UcscHandle)
        name (string) : usNIC Connection Policy name
        parent_dn (string) : Dn of org
    Returns:
        None
    Example:
        usnic_conn_policy_delete(handle, "samp_usnic_conn")
    """
    mo = usnic_conn_policy_get(handle, name, parent_dn)
    if not mo:
        raise UcscOperationError("usnic_conn_policy_delete",
                                 "usNIC Connectivity Policy does not exist")
    handle.remove_mo(mo)
    handle.commit()
