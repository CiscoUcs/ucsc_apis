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
This module contains the methods required for creating VMQ Connection Policy.
"""
from ucscsdk.ucscexception import UcscOperationError


def vmq_conn_policy_create(handle, name, descr=None, vmq_count="64",
                           intr_count="64", parent_dn="org-root", **kwargs):
    """
    Creates VMQ Connection Policy

    Args:
        handle (UcscHandle)
        name (string) : VMQ connection policy name
        descr (string) : description
        parent_dn (string) : Dn of org
        vmq_count (string) : Number of VMQs
        intr_count (string) : Number of Interrupts
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        VnicVmqConPolicy: Managed Object

    Example:
        vmq_conn_policy_create(handle, "samp_vmq_conn", vmq_count="48",
                               intr_count="32")
    """

    from ucscsdk.mometa.vnic.VnicVmqConPolicy import VnicVmqConPolicy

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise UcscOperationError("vmq_conn_policy_create",
                                 "Org %s does not exist" % parent_dn)

    mo = VnicVmqConPolicy(parent_mo_or_dn=obj,
                          name=name,
                          descr=descr,
                          vmq_count=vmq_count,
                          intr_count=intr_count)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def vmq_conn_policy_get(handle, name, parent_dn="org-root"):
    """
    Checks if the given VMQ Connection Policy already exists
    Args:
        handle (UcscHandle)
        name (string) : VMQ Connection Policy name
        parent_dn (string) : Dn of org

    Returns:
        VnicVmqConPolicy: Managed Object OR None
    Example:
        vmq_conn_policy_get(handle, "samp_vmq_conn")
    """
    dn = parent_dn + '/vmq-con-' + name
    return handle.query_dn(dn)


def vmq_conn_policy_exists(handle, name, parent_dn="org-root", **kwargs):
    """
    Checks if the given VMQ Connection Policy already exists
    Args:
        handle (UcscHandle)
        name (string) : VMQ Connection Policy name
        parent_dn (string) : Dn of org
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    Returns:
        (True/False, MO/None)
    Example:
        found, mo = vmq_conn_policy_exists(handle, "samp_vmq_conn",
                                           intr_count="32")
    """
    mo = vmq_conn_policy_get(handle, name, parent_dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def vmq_conn_policy_delete(handle, name, parent_dn="org-root"):
    """
    Deletes a VMQ Connection Policy
    Args:
        handle (UcscHandle)
        name (string) : VMQ Connection Policy name
        parent_dn (string) : Dn of org
    Returns:
        None
    Example:
        vmq_conn_policy_delete(handle, "samp_vmq_conn")
    """
    mo = vmq_conn_policy_get(handle, name, parent_dn)
    if not mo:
        raise UcscOperationError("vmq_conn_policy_delete",
                                 "VMQ Connectivity Policy does not exist")
    handle.remove_mo(mo)
    handle.commit()
