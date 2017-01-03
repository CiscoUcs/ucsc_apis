# Copyright 2015 Cisco Systems, Inc.
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
This module performs the operation related to radius configuration.
"""
ucsc_base_dn = "org-root/deviceprofile-default"


def radius_provider_create(handle, name, order="lowest-available", key="",
                           auth_port="1812", timeout="5", retries="1",
                           enc_key="", descr="", **kwargs):
    """
    Creates a radius provider

    Args:
        handle (UcscHandle)
        name (string): name
        order (string): order
        key (string): key
        auth_port (string): auth_port
        timeout (string): timeout
        retries (string): retries
        enc_key (string): enc_key
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaRadiusProvider: Managed Object

    Example:
        radius_provider_create(handle, name="test_radius_provider")
    """

    from ucscsdk.mometa.aaa.AaaRadiusProvider import AaaRadiusProvider

    mo = AaaRadiusProvider(
        parent_mo_or_dn=ucsc_base_dn + "/radius-ext",
        name=name,
        order=order,
        key=key,
        auth_port=auth_port,
        timeout=timeout,
        retries=retries,
        enc_key=enc_key,
        descr=descr)

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def radius_provider_exists(handle, name, **kwargs):
    """
    checks if radius provider exists

    Args:
        handle (UcscHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        radius_provider_exists(handle, name="test_radius_provider")
    """

    dn = ucsc_base_dn + "/radius-ext/provider-" + name
    mo = handle.query_dn(dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def radius_provider_modify(handle, name, **kwargs):
    """
    modifies a radius provider

    Args:
        handle (UcscHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaRadiusProvider: Managed Object

    Raises:
        ValueError: If AaaRadiusProvider is not present

    Example:
        radius_provider_modify(handle, name="test_radius_provider")
    """

    dn = ucsc_base_dn + "/radius-ext/provider-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Radius Provider does not exist %s" % dn)

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def radius_provider_delete(handle, name):
    """
    deletes a radius provider

    Args:
        handle (UcscHandle)
        name (string): name

    Returns:
        None

    Raises:
        ValueError: If AaaRadiusProvider is not present

    Example:
        radius_provider_delete(handle, name="test_radius_provider")
    """

    dn = ucsc_base_dn + "/radius-ext/provider-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Radius Provider does not exist")

    handle.remove_mo(mo)
    handle.commit()


def radius_provider_group_create(handle, name, descr="", **kwargs):
    """
    Creates a radius provider group

    Args:
        handle (UcscHandle)
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaProviderGroup: Managed Object

    Example:
        radius_provider_group_create(handle, name="test_radius_provider_group")
    """

    from ucscsdk.mometa.aaa.AaaProviderGroup import AaaProviderGroup

    mo = AaaProviderGroup(
        parent_mo_or_dn=ucsc_base_dn + "/radius-ext",
        name=name, descr=descr)

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def radius_provider_group_exists(handle, name, **kwargs):
    """
    checks if radius provider group exists

    Args:
        handle (UcscHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        radius_provider_group_exists(handle, name="test_radius_provider_group")
    """

    dn = ucsc_base_dn + "/radius-ext/providergroup-" + name
    mo = handle.query_dn(dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def radius_provider_group_delete(handle, name):
    """
    deletes a radius provider group

    Args:
        handle (UcscHandle)
        name (string): name

    Returns:
        None

    Raises:
        ValueError: If AaaProviderGroup is not present

    Example:
        radius_provider_group_delete(handle, name="test_radius_provider_group")
    """

    dn = ucsc_base_dn + "/radius-ext/providergroup-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Provider  Group does not exist.")

    handle.remove_mo(mo)
    handle.commit()


def radius_provider_group_add_provider(handle, group_name, name,
                                       order="lowest-available", descr="",
                                       **kwargs):
    """
    adds a provider to a radius provider group

    Args:
        handle (UcscHandle)
        group_name (string): group_name
        name (string): name
        order (string): order
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaProviderRef: Managed Object

    Raises:
        ValueError: If AaaProviderGroup  or AaaProvider is not present

    Example:
        radius_provider_group_add_provider(handle,
                                    group_name="test_radius_provider_group",
                                    name="test_radius_provider")
    """

    from ucscsdk.mometa.aaa.AaaProviderRef import AaaProviderRef

    group_dn = ucsc_base_dn + "/radius-ext/providergroup-" + group_name
    group_mo = handle.query_dn(group_dn)
    if not group_mo:
        raise ValueError("Radius Provider Group does not exist.")

    provider_dn = ucsc_base_dn + "/radius-ext/provider-" + name
    mo = handle.query_dn(provider_dn)
    if not mo:
        raise ValueError("Radius Provider does not exist.")

    mo = AaaProviderRef(parent_mo_or_dn=group_mo,
                        name=name,
                        order=order,
                        descr=descr)

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def radius_provider_group_provider_exists(handle, group_name, name, **kwargs):
    """
    checks if a provider exists under a radius provider group

    Args:
        handle (UcscHandle)
        group_name (string): group_name
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Raises:
        ValueError: If AaaProviderGroup  or AaaProvider is not present

    Example:
        radius_provider_group_provider_exists(handle,
                                    group_name="test_radius_provider_group",
                                    name="test_radius_provider")
    """

    group_dn = ucsc_base_dn + "/radius-ext/providergroup-" + group_name
    group_mo = handle.query_dn(group_dn)
    if not group_mo:
        raise ValueError("Radius Provider Group does not exist.")

    provider_dn = group_dn + "/provider-ref-" + name
    mo = handle.query_dn(provider_dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def radius_provider_group_modify_provider(handle, group_name, name, **kwargs):
    """
    modifies a provider to a radius provider group

    Args:
        handle (UcscHandle)
        group_name (string): group_name
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaProviderRef: Managed Object

    Raises:
        ValueError: If AaaProviderRef is not present

    Example:
        radius_provider_group_modify_provider(handle,
                                    group_name="test_radius_provider_group",
                                    name="test_radius_provider")
    """

    group_dn = ucsc_base_dn + "/radius-ext/providergroup-" + group_name
    provider_dn = group_dn + "/provider-ref-" + name
    mo = handle.query_dn(provider_dn)
    if not mo:
        raise ValueError("Provider not available under group.")

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def radius_provider_group_remove_provider(handle, group_name, name):
    """
    removes a provider from a radius provider group

    Args:
        handle (UcscHandle)
        group_name (string): group_name
        name (string): name

    Returns:
        None

    Raises:
        ValueError: If AaaProviderRef is not present

    Example:
        radius_provider_group_remove_provider(handle,
                                    group_name="test_radius_provider_group",
                                    name="test_radius_provider")
    """

    group_dn = ucsc_base_dn + "/radius-ext/providergroup-" + group_name
    provider_dn = group_dn + "/provider-ref-" + name
    mo = handle.query_dn(provider_dn)
    if not mo:
        raise ValueError("Provider not available under group.")

    handle.remove_mo(mo)
    handle.commit()
