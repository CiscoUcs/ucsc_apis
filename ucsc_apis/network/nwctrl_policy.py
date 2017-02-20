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
This module contains methods required for creating network control policies.
"""
from ucscsdk.ucscexception import UcscOperationError


def nwctrl_policy_create(handle, name, descr=None, cdp="disabled",
                         mac_register_mode="only-native-vlan",
                         uplink_fail_action="link-down",
                         forge="allow", lldp_transmit="disabled",
                         lldp_receive="disabled", parent_dn="org-root",
                         **kwargs):
    """
    Creates Network Control Policy

    Args:
        handle (UcscHandle)
        name (string) : Network Control Policy Name
        cdp (string) : ["disabled", "enabled"]
        mac_register_mode (string): ["all-host-vlans", "only-native-vlan"]
        uplink_fail_action (string) : ["link-down", "warning"]
        forge (string) : ["allow", "deny"]
        lldp_transmit (string) : ["disabled", "enabled"]
        lldp_receive (string) : ["disabled", "enabled"]
        descr (string) : description
        parent_dn (string) : Org Dn or Domain_group Dn
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        NwctrlDefinition: Managed Object

    Example:
        nwctrl_policy_create(handle, "sample_nwcontrol_policy",
                             "enabled", "all-host-vlans",
                             "link-down", "allow", "disabled", "disabled")
    """
    from ucscsdk.mometa.nwctrl.NwctrlDefinition import NwctrlDefinition
    from ucscsdk.mometa.dpsec.DpsecMac import DpsecMac

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise UcscOperationError("nwctrl_policy_create",
                                 "Org %s does not exist" % parent_dn)

    mo = NwctrlDefinition(parent_mo_or_dn=obj,
                          lldp_transmit=lldp_transmit,
                          name=name,
                          lldp_receive=lldp_receive,
                          mac_register_mode=mac_register_mode,
                          cdp=cdp,
                          uplink_fail_action=uplink_fail_action,
                          descr=descr)

    mo.set_prop_multiple(**kwargs)

    DpsecMac(parent_mo_or_dn=mo,
             forge=forge,
             name="",
             descr="")

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def nwctrl_policy_get(handle, name, parent_dn="org-root"):
    """
    Checks if the given Network Control Policy already exists with the
    same params

    Args:
        handle (UcscHandle)
        name (string) : Network Control Policy Name
        parent_dn (string) : Org Dn or Domain_group Dn

    Returns:
        NwctrlDefinition: Managed Object OR None
    Example:
        nwctrl_policy_get(handle, "sample_nwcontrol_policy")
    """
    dn = parent_dn + '/nwctrl-' + name
    return handle.query_dn(dn)


def nwctrl_policy_exists(handle, name, parent_dn="org-root", **kwargs):
    """
    Checks if the given Network Control Policy already exists with the
    same params

    Args:
        handle (UcscHandle)
        name (string) : Network Control Policy Name
        parent_dn (string) : Org Dn or Domain_group Dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    Returns:
        (True/False, MO/None)
    Example:
        bool_var = nwctrl_policy_exists(handle, "sample_nwcontrol_policy",
                                        "enabled", "all-host-vlans",
                                        "link-down", "allow", "disabled",
                                        "disabled")
    """
    mo = nwctrl_policy_get(handle, name, parent_dn)
    if not mo:
        return (False, None)

    if "forge" in kwargs:
        mo_1_dn = mo.dn + "/mac-sec"
        mo_1 = handle.query_dn(mo_1_dn)
        if not mo_1:
            raise UcscOperationError("nwctrl_policy_exists",
                                     "Mac secure object does not exist")

        args = {'forge': kwargs['forge']}
        if not mo.check_prop_match(**args):
            return (False, None)

        kwargs.pop('forge', None)

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def nwctrl_policy_delete(handle, name, parent_dn="org-root"):
    """
    Deletes a Network Control Policy
    Args:
        handle (UcscHandle)
        name (string) : Network Control Policy Name
        parent_dn (string) : Org Dn or Domain_group Dn
    Returns:
        None
    Example:
        nwctrl_policy_delete(handle, "my_nw_policy")
        nwctrl_policy_delete(handle, "my_nw_policy", "org-root/org-demo")
    """

    mo = nwctrl_policy_get(handle, name, parent_dn)
    if not mo:
        raise UcscOperationError("nwctrl_policy_delete",
                                 "Network Control policy does not exist")

    handle.remove_mo(mo)
    handle.commit()
