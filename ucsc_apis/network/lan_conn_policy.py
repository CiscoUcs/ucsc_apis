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
This module contains the methods required for creating LAN Connectivity Policy.
"""
from ucscsdk.ucscexception import UcscOperationError


def lan_conn_policy_create(handle, name, descr=None, parent_dn="org-root",
                           **kwargs):
    """
    Creates LAN Connectivity Policy

    Args:
        handle (UcscHandle)
        name (string) : LAN Connectivity Policy name
        descr (string): description
        parent_dn (string) : Dn of org
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        VnicLanConnPolicy: Managed Object
    Example:
        lan_conn_policy_create(handle, "samp_conn_pol2")
    """
    from ucscsdk.mometa.vnic.VnicLanConnPolicy import VnicLanConnPolicy

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise UcscOperationError("lan_conn_policy_create",
                                 "Org %s does not exist" % parent_dn)

    mo = VnicLanConnPolicy(parent_mo_or_dn=obj,
                           name=name,
                           descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def lan_conn_policy_get(handle, name, parent_dn="org-root"):
    """
    Gets the given LAN Connectivity Policy if exists
    Args:
        handle (UcscHandle)
        name (string) : LAN Connectivity Policy name
        parent_dn (string) : Dn of org
    Returns:
        VnicLanConnPolicy: Managed Object OR None
    Example:
        lan_conn_policy_get(handle, "samp_conn_pol2")
    """
    dn = parent_dn + '/lan-conn-pol-' + name
    return handle.query_dn(dn)


def lan_conn_policy_exists(handle, name, parent_dn="org-root", **kwargs):
    """
    Checks if the given LAN Connectivity Policy already exists
    Args:
        handle (UcscHandle)
        name (string) : LAN Connectivity Policy name
        parent_dn (string) : Dn of org
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    Returns:
        (True/False, MO/None)
    Example:
        lan_conn_policy_exists(handle, "samp_conn_pol2")
    """
    mo = lan_conn_policy_get(handle, name, parent_dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def lan_conn_policy_delete(handle, name, parent_dn="org-root"):
    """
    Deletes a LAN Connectivity Policy
    Args:
        handle (UcscHandle)
        name (string): LAN Connectivity Policy name
        parent_dn (string) : Dn of org
    Returns:
        None
    Example:
        lan_conn_policy_delete(handle, "sample-lan-conpolicy")
    """
    mo = lan_conn_policy_get(handle, name, parent_dn)
    if not mo:
        raise UcscOperationError("lan_conn_policy_delete",
                                 "LAN Connectivity Policy does not exist")
    handle.remove_mo(mo)
    handle.commit()


def lcp_vnic_add(handle, name, parent_dn, nw_ctrl_policy_name="global-default",
                 admin_host_port="ANY", admin_vcon="any",
                 stats_policy_name="global-default", admin_cdn_name=None,
                 switch_id="A", pin_to_group_name=None, mtu="1500",
                 qos_policy_name=None, adaptor_profile_name=None,
                 cdn_source="vnic-name",
                 ident_pool_name=None, order="unspecified", nw_templ_name=None,
                 addr="derived", **kwargs):
    """
    Adds vNIC to LAN Connectivity Policy

    Args:
        handle (UcscHandle)
        parent_dn (string) : Dn of LAN connectivity policy name
        name (string) : Name of vnic
        nw_ctrl_policy_name (string) : Network control policy name
        admin_host_port (string) : Admin host port placement for vnic
        admin_vcon (string) : Admin vcon for vnic
        stats_policy_name (string) : Stats policy name
        cdn_source (string) : CDN source ['vnic-name', 'user-defined']
        admin_cdn_name (string) : CDN name
        switch_id (string): Switch id
        pin_to_group_name (string) : Pinning group name
        mtu (string): MTU
        qos_policy_name (string): Qos policy name
        adaptor_profile_name (string): Adaptor profile name
        ident_pool_name (string) : Identity pool name
        order (string) : Order of the vnic
        nw_templ_name (string) : Network template name
        addr (string) : Address of the vnic
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        VnicEther: Managed Object

    Example:
        lcp_vnic_add(handle, "test_vnic", "org-root/lan-conn-pol-lcp_test_pol",
                 nw_ctrl_policy_name="test_nwpol", switch_id= "A",mtu="2240",
                 adaptor_profile_name="global-SRIOV")
    """
    from ucscsdk.mometa.vnic.VnicEther import VnicEther

    mo = handle.query_dn(parent_dn)
    if not mo:
        raise UcscOperationError("lcp_vnic_add",
                                 "LAN connectivity policy '%s' does not exist"
                                 % parent_dn)

    if cdn_source not in ['vnic-name', 'user-defined']:
        raise UcscOperationError("lcp_vnic_add",
                                 "Invalid CDN source name")

    admin_cdn_name = "" if cdn_source == "vnic-name" else admin_cdn_name

    mo_1 = VnicEther(parent_mo_or_dn=mo,
                     name=name,
                     nw_ctrl_policy_name=nw_ctrl_policy_name,
                     admin_host_port=admin_host_port,
                     admin_vcon=admin_vcon,
                     stats_policy_name=stats_policy_name,
                     admin_cdn_name=admin_cdn_name,
                     switch_id=switch_id,
                     pin_to_group_name=pin_to_group_name,
                     mtu=mtu,
                     qos_policy_name=qos_policy_name,
                     adaptor_profile_name=adaptor_profile_name,
                     ident_pool_name=ident_pool_name,
                     order=order,
                     nw_templ_name=nw_templ_name,
                     cdn_source=cdn_source,
                     addr=addr)

    mo_1.set_prop_multiple(**kwargs)

    handle.add_mo(mo_1, modify_present=True)
    handle.commit()
    return mo_1


def lcp_vnic_get(handle, name, parent_dn):
    """
    Gets the vNIC under given Lan Connectivity Policy
    Args:
        handle (UcscHandle)
        name (string) : Name of vnic
        parent_dn (string) : Dn of LAN connectivity policy name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    Returns:
        VnicEther: Managed Object OR None
    Example:
        lcp_vnic_get(handle, "test_vnic",
                 "org-root/lan-conn-pol-samp_conn_pol2")
    """
    dn = parent_dn + '/ether-' + name
    return handle.query_dn(dn)


def lcp_vnic_exists(handle, name, parent_dn, **kwargs):
    """
    Checks if the given vNIC already exists with the same params under a
    given Lan Connectivity Policy
    Args:
        handle (UcscHandle)
        name (string) : Name of vnic
        parent_dn (string) : Dn of LAN connectivity policy name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    Returns:
        (True/False, MO/None)
    Example:
        lcp_vnic_exists(handle, "test_vnic",
                        "org-root/lan-conn-pol-samp_conn_pol2",
                        mtu="2240")
    """
    mo = lcp_vnic_get(handle, name, parent_dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def lcp_vnic_delete(handle, name, parent_dn):
    """
    Remove vNIC from LAN Connectivity Policy
    Args:
        handle (UcscHandle)
        name (string) : Name of vnic
        parent_dn (string) : Dn of LAN connectivity policy name
    Returns:
        None
    Example:
        lcp_vnic_delete(handle, "sample-vnic",
                        "org-root/lan-conn-pol-samp_conn_pol")
    """
    mo = lcp_vnic_get(handle, name, parent_dn)
    if not mo:
        raise UcscOperationError("lcp_vnic_delete",
                                 "vnic does not exist")

    handle.remove_mo(mo)
    handle.commit()


def lcp_iscsi_vnic_add(handle, name, parent_dn, addr="derived",
                       admin_host_port="ANY",
                       admin_vcon="any", stats_policy_name="global-default",
                       admin_cdn_name=None, cdn_source="vnic-name",
                       switch_id="A", pin_to_group_name=None, vnic_name=None,
                       qos_policy_name=None,
                       adaptor_profile_name="global-default",
                       ident_pool_name=None, order="unspecified",
                       nw_templ_name=None, vlan_name="default",
                       **kwargs):
    """
    Adds iSCSI vNIC to LAN Connectivity Policy

    Args:
        handle (UcscHandle)
        parent_dn (string) : Dn of LAN connectivity policy name
        name (string) : Name of iscsi vnic
        admin_host_port (string) : Admin host port placement for vnic
        admin_vcon (string) : Admin vcon for vnic
        stats_policy_name (string) : Stats policy name
        cdn_source (string) : CDN source ['vnic-name', 'user-defined']
        admin_cdn_name (string) : CDN name
        switch_id (string): Switch id
        pin_to_group_name (string) : Pinning group name
        vnic_name (string): Overlay vnic name
        qos_policy_name (string): Qos policy name
        adaptor_profile_name (string): Adaptor profile name
        ident_pool_name (string) : Identity pool name
        order (string) : Order of the vnic
        nw_templ_name (string) : Network template name
        addr (string) : Address of the vnic
        vlan_name (string): Name of the vlan
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        VnicIScsiLCP : Managed Object
    Example:
        lcp_iscsi_vnic_add(handle, "test_iscsi",
                           "org-root/lan-conn-pol-samppol2",
                           nw_ctrl_policy_name="test_nwpol", switch_id= "A",
                           vnic_name="vnic1",
                           adaptor_profile_name="global-SRIOV")
    """
    from ucscsdk.mometa.vnic.VnicIScsiLCP import VnicIScsiLCP
    from ucscsdk.mometa.vnic.VnicVlan import VnicVlan

    mo = handle.query_dn(parent_dn)
    if not mo:
        raise UcscOperationError("lcp_iscsi_vnic_add",
                                 "LAN connectivity policy '%s' does not exist"
                                 % parent_dn)

    if cdn_source not in ['vnic-name', 'user-defined']:
        raise UcscOperationError("lcp_iscsi_vnic_add",
                                 "Invalid CDN source name")

    admin_cdn_name = "" if cdn_source == "vnic-name" else admin_cdn_name
    mo_1 = VnicIScsiLCP(parent_mo_or_dn=mo,
                        addr=addr,
                        admin_host_port=admin_host_port,
                        admin_vcon=admin_vcon,
                        stats_policy_name=stats_policy_name,
                        cdn_source=cdn_source,
                        admin_cdn_name=admin_cdn_name,
                        switch_id=switch_id,
                        pin_to_group_name=pin_to_group_name,
                        vnic_name=vnic_name,
                        qos_policy_name=qos_policy_name,
                        adaptor_profile_name=adaptor_profile_name,
                        ident_pool_name=ident_pool_name,
                        order=order,
                        nw_templ_name=nw_templ_name,
                        name=name)

    mo_1.set_prop_multiple(**kwargs)

    VnicVlan(parent_mo_or_dn=mo_1, name="", vlan_name=vlan_name)

    handle.add_mo(mo_1)
    handle.commit()
    return mo_1


def lcp_iscsi_vnic_get(handle, name, parent_dn):
    """
    Gets iSCSI vNIC under a given Lan Connectivity Policy
    Args:
        handle (UcscHandle)
        name (string) : Name of iscsi vnic
        parent_dn (string) : Dn of LAN connectivity policy name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    Returns:
        VnicIScsiLCP : Managed Object OR None
    Example:
        lcp_iscsi_vnic_get(handle, "test_iscsi_vnic",
                       "org-root/lan-conn-pol-samp_conn_pol2")
    """
    dn = parent_dn + '/iscsi-' + name
    return handle.query_dn(dn)


def lcp_iscsi_vnic_exists(handle, name, parent_dn, **kwargs):
    """
    Checks if the given iSCSI vNIC already exists with the same params
    under a given Lan Connectivity Policy
    Args:
        handle (UcscHandle)
        name (string) : Name of iscsi vnic
        parent_dn (string) : Dn of LAN connectivity policy name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    Returns:
        (True/False, MO/None)
    Example:
        lcp_iscsi_vnic_exists(handle, "org-root/lan-conn-pol-samp_conn_pol2",
                        "test_iscsi_vnic")
    """
    mo = lcp_iscsi_vnic_get(handle, name, parent_dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def lcp_iscsi_vnic_delete(handle, name, parent_dn):
    """
    Remove iSCSI vNIC from LAN Connectivity Policy
    Args:
        handle (UcscHandle)
        name (string) : Name of iscsi vnic
        parent_dn (string) : Dn of LAN connectivity policy name
    Returns:
        None
    Example:
        lcp_iscsi_vnic_delete(handle, "sample-vnic-iscsi",
                    "org-root/lan-conn-pol-samp_conn_pol")
    """
    mo = lcp_iscsi_vnic_get(handle, name, parent_dn)
    if not mo:
        raise UcscOperationError("lcp_iscsi_vnic_delete",
                                 "iSCSI vnic does not exist")

    handle.remove_mo(mo)
    handle.commit()
