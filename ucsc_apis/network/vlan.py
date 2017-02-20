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
This module performs the Vlan related operation
"""
from ucscsdk.ucscexception import UcscOperationError


def vlan_create(handle, name, id, sharing="none", vlan_type="lan",
                mcast_policy_name=None, compression_type="included",
                default_net="no", pub_nw_name=None, domain_group="root",
                **kwargs):
    """
    Creates VLAN

    Args:
        handle (UcscHandle)
        name (string) : VLAN Name
        id (string): VLAN ID
        sharing (string) : Vlan sharing
                           ["community", "isolated", "none", "primary"]
        vlan_type (string) : Type of Vlan ["lan", "appliance"]
        mcast_policy_name (string) : Multicast policy name
        compression_type (string) : ["excluded", "included"]
        default_net (string) : ["false", "no", "true", "yes"]
        pub_nw_name (string) : Name of primary vlan, applicable for isolated
                               or community vlan
        domain_group (string) : Full domain group name
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        FabricVlan: Managed Object

    Example:
        vlan_create(handle, "none", "vlan-lab", "123",  "sample_mcast_policy",
                    "included")
    """
    from ucscsdk.mometa.fabric.FabricVlan import FabricVlan
    from ucscsdk.utils.ucscdomain import get_domain_group_dn

    domain_group_dn = get_domain_group_dn(handle, domain_group)

    if vlan_type != "lan" and vlan_type != "appliance":
        raise UcscOperationError("vlan_create",
                                 "Vlan Type %s does not exist" % vlan_type)
    vlan_obj_dn = domain_group_dn + "/fabric/lan" if vlan_type == "lan" else \
        domain_group_dn + "/fabric/eth-estc"
    obj = handle.query_dn(vlan_obj_dn)
    if not obj:
        raise UcscOperationError("vlan_create",
                                 "Fabric LAN cloud %s does not exist"
                                 % vlan_obj_dn)

    vlan = FabricVlan(parent_mo_or_dn=obj,
                      sharing=sharing,
                      name=name,
                      id=id,
                      mcast_policy_name=mcast_policy_name,
                      default_net=default_net,
                      pub_nw_name=pub_nw_name,
                      compression_type=compression_type)

    vlan.set_prop_multiple(**kwargs)

    handle.add_mo(vlan, modify_present=True)
    handle.commit()
    return vlan


def vlan_get(handle, name, vlan_type="lan", domain_group="root"):
    """
    Gets the VLAN
    Args:
        handle (UcscHandle)
        name (string) : VLAN Name
        vlan_type (string) : Type of Vlan ["lan", "appliance"]
        domain_group (string) : Full domain group name

    Returns:
        FabricVlan: Managed Object OR None
    Example:
        bool_var = vlan_exists(handle, "none", "vlan-lab", "123",
                        "sample_mcast_policy", "included")
    """
    from ucscsdk.utils.ucscdomain import get_domain_group_dn

    if vlan_type != "lan" and vlan_type != "appliance":
        raise UcscOperationError("vlan_get",
                                 "Vlan Type %s does not exist" % vlan_type)
    domain_group_dn = get_domain_group_dn(handle, domain_group)
    dn = (domain_group_dn + "/fabric/lan/net-" + name) if vlan_type == "lan" \
        else (domain_group_dn + "/fabric/eth-estc/net-" + name)
    return handle.query_dn(dn)


def vlan_exists(handle, name, vlan_type="lan", domain_group="root", **kwargs):
    """
    Checks if the given VLAN already exists with the same params
    Args:
        handle (UcscHandle)
        name (string) : VLAN Name
        vlan_type (string) : Type of Vlan ["lan", "appliance"]
        domain_group (string) : Full domain group name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    Returns:
        (True/False, MO/None)
    Example:
        bool_var = vlan_exists(handle, "none", "vlan-lab", "123",
                        "sample_mcast_policy", "included")
    """
    mo = vlan_get(handle, name, vlan_type, domain_group)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def vlan_delete(handle, name, vlan_type="lan", domain_group="root"):
    """
    Deletes a VLAN
    Args:
        handle (UcscHandle)
        name (string) : VLAN Name
        vlan_type (string) : Type of Vlan ["lan", "appliance"]
        domain_group (string) : Full domain group name
    Returns:
        None
    Example:
        vlan_delete(handle, "lab-vlan")
    """
    mo = vlan_get(handle, name, vlan_type, domain_group)
    if not mo:
        raise UcscOperationError("vlan_delete",
                                 "VLAN does not exist")

    handle.remove_mo(mo)
    handle.commit()
