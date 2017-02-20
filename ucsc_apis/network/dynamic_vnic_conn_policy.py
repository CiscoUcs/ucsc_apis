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
This module contains the methods required for creating Dynamic Vnic
Connection Policy.
"""
from ucscsdk.ucscexception import UcscOperationError


def dynamic_vnic_conn_policy_create(handle, name, descr=None, dynamic_eth="54",
                                    adaptor_profile_name=None,
                                    protection="protected",
                                    parent_dn="org-root", **kwargs):
    """
    Creates Dynamic vNIC Connection Policy

    Args:
        handle (UcscHandle)
        name (string) : Dynamic vNIC connection policy name
        descr (string): description
        parent_dn (string) : Dn of org
        dynamic_eth (string) : Number of dynamic vnics
        protection (string) : Protection mode
                    ["protected", "protected-pref-a", "protected-pref-b"]
        adaptor_profile_name (string) : Adaptor policy
                    ['global-default', 'global-Linux', 'global-Solaris',
                     'global-SRIOV', 'global-usNIC', 'global-usNICOrcl',
                     'global-VMWare', 'global-VMPasThr', 'global-Windows']
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        VnicDynamicConPolicy: Managed Object

    Example:
        dynamic_vnic_conn_policy_create(handle, name="test_dynavnic",
                                        descr="testing dynavnic",
                                        dynamic_eth="32")
    """

    from ucscsdk.mometa.vnic.VnicDynamicConPolicy import VnicDynamicConPolicy

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise UcscOperationError("dynamic_vnic_conn_policy_create",
                                 "Org %s does not exist" % parent_dn)

    mo = VnicDynamicConPolicy(parent_mo_or_dn=obj,
                              name=name,
                              descr=descr,
                              dynamic_eth=dynamic_eth,
                              protection=protection,
                              adaptor_profile_name=adaptor_profile_name)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def dynamic_vnic_conn_policy_get(handle, name, parent_dn="org-root"):
    """
    Gets Dynamic vNIC Connection Policy
    Args:
        handle (UcscHandle)
        name (string) : Dynamic vNIC Connection Policy name
        parent_dn (string) : Dn of org
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    Returns:
        VnicDynamicConPolicy: Managed Object OR None
    Example:
        dynamic_vnic_conn_policy_get(handle, "test_dynavnic")
    """
    dn = parent_dn + '/dynamic-con-' + name
    return handle.query_dn(dn)


def dynamic_vnic_conn_policy_exists(handle, name, parent_dn="org-root",
                                    **kwargs):
    """
    Checks if the given Dynamic vNIC Connection Policy already exists
    Args:
        handle (UcscHandle)
        name (string) : Dynamic vNIC Connection Policy name
        parent_dn (string) : Dn of org
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    Returns:
        (True/False, MO/None)
    Example:
        found, mo = dynamic_vnic_conn_policy_exists(handle,
                                                    name="test_dynavnic",
                                                    dynamic_eth="32")
    """
    mo = dynamic_vnic_conn_policy_get(handle, name, parent_dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def dynamic_vnic_conn_policy_delete(handle, name, parent_dn="org-root"):
    """
    Deletes a Dynamic vNIC Connection Policy
    Args:
        handle (UcscHandle)
        name (string) : Dynamic vNIC Connection Policy name
        parent_dn (string) : Dn of org
    Returns:
        None
    Example:
        dynamic_vnic_conn_policy_delete(handle, "test_dynavnic")
    """
    mo = dynamic_vnic_conn_policy_get(handle, name, parent_dn)
    if not mo:
        raise UcscOperationError("dynamic_vnic_conn_policy_delete",
                                 "Dynamic vNIC Connectivity Policy "
                                 "does not exist")
    handle.remove_mo(mo)
    handle.commit()
