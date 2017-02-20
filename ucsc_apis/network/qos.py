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
This module contains methods required for configuring QoS.
"""
from ucscsdk.ucscexception import UcscOperationError


def qos_policy_add(handle, name, descr=None, prio="best-effort", burst="10240",
                   rate="line-rate", host_control="none",
                   parent_dn="org-root", **kwargs):
    """
    Creates QoS Policy

    Args:
        handle (UcscHandle)
        name (string) : QoS Policy Name
        descr (string) :
        prio (string) : Qos class
                ["best-effort", "bronze", "fc", "gold", "platinum", "silver"]
        burst (uint): Bytes of burst
        rate (string) : ["line-rate"], ["8-40000000"] in Kbps
        host_control (string) : ["full", "none"]
        parent_dn (string) :
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        EpqosDefinition: Managed object

    Raises:
        UcscOperationError: If EpqosDefinition is not present

    Example:
        mo = qos_policy_create(handle, "sample_qos", "platinum", 10240,
                                "line-rate", "full")
    """
    from ucscsdk.mometa.epqos.EpqosDefinition import EpqosDefinition
    from ucscsdk.mometa.epqos.EpqosEgress import EpqosEgress

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise UcscOperationError("qos_policy_create",
                                 "org '%s' does not exist" % parent_dn)

    mo = EpqosDefinition(parent_mo_or_dn=obj,
                         name=name,
                         descr=descr)
    mo_1 = EpqosEgress(parent_mo_or_dn=mo,
                       rate=rate,
                       host_control=host_control,
                       name="",
                       prio=prio,
                       burst=burst)

    mo_1.set_prop_multiple(**kwargs)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def qos_policy_get(handle, name, parent_dn="org-root"):
    """
    Checks if the given qos policy already exists with the same params

    Args:
        handle (UcscHandle)
        name (string) : QoS Policy Name
        parent_dn (string) :

    Returns:
        EpqosDefinition: Managed object OR None
    Example:
        qos_policy_get(handle, "sample_qos")
    """
    dn = parent_dn + '/ep-qos-' + name
    return handle.query_dn(dn)


def qos_policy_exists(handle, name, parent_dn="org-root", **kwargs):
    """
    Checks if the given qos policy already exists with the same params

    Args:
        handle (UcscHandle)
        name (string) : QoS Policy Name
        parent_dn (string) :
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        bool_var = qos_policy_exists(handle, "sample_qos", "platinum", 10240,
                                     "line-rate", "full")
    """
    mo = qos_policy_get(handle, name, parent_dn)

    if not mo:
        return (False, None)

    args = {'descr': kwargs['descr'] if 'descr' in kwargs else None}
    if not mo.check_prop_match(**args):
        return (False, None)
    kwargs.pop('descr', None)

    mo_1_dn = mo.dn + '/egress'
    mo_1 = handle.query_dn(mo_1_dn)
    if not mo_1:
        raise UcscOperationError("qos_policy_exists",
                                 "Egress QoS policy does not exist")

    if not mo_1.check_prop_match(**kwargs):
        return (False, None)

    return (True, mo)


def qos_policy_remove(handle, name, parent_dn="org-root"):
    """
    Removes the specified qos policy

    Args:
        handle (UcscHandle)
        name (string) : QoS Policy Name
        parent_dn (string) : Dn of the Org in which the policy should reside

    Returns:
        None

    Raises:
        UcscOperationError: If the policy is not found

    Example:
        qos_policy_remove(handle, "sample_qos", parent_dn="org-root")
        qos_policy_remove(handle, "demo_qos_policy",
                          parent_dn="org-root/org-demo")
    """
    mo = qos_policy_get(handle, name, parent_dn)
    if not mo:
        raise UcscOperationError("qos_policy_remove",
                                 "Qos Policy does not exist")

    handle.remove_mo(mo)
    handle.commit()
