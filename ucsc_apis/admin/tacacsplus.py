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
This module performs the operation related to dns server management.
"""
from ucscsdk.ucscexception import UcscOperationError
from ..common.utils import get_device_profile_dn
ucsc_base_dn = get_device_profile_dn(name="default")


def tacacsplus_provider_create(handle, name, order="lowest-available",
                               key=None, port="49", timeout="5", retries="1",
                               enc_key=None, descr=None, **kwargs):
    """
    Creates a tacacsplus provider

    Args:
        handle (UcscHandle)
        name (string): name of tacacsplus provider
        order (string): order
        key (string): key
        port (string): port
        timeout (string): timeout
        retries (string): retries
        enc_key (string): enc_key
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaTacacsPlusProvider: Managed Object

    Example:
        tacacsplus_provider_create(
          handle, name="test_tacac_prov", port="320", timeout="10")
    """

    from ucscsdk.mometa.aaa.AaaTacacsPlusProvider import \
        AaaTacacsPlusProvider

    mo = AaaTacacsPlusProvider(
        parent_mo_or_dn=ucsc_base_dn + "/tacacs-ext",
        name=name,
        order=order,
        key=key,
        port=port,
        timeout=timeout,
        retries=retries,
        enc_key=enc_key,
        descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def tacacsplus_provider_get(handle, name):
    """
    Gets tacacsplus provider

    Args:
        handle (UcscHandle)
        name (string): name of tacacsplus provider

    Returns:
        AaaTacacsPlusProvider: Managed Object OR None

    Example:
        tacacsplus_provider_get(handle, name="test_tacac_prov")
    """

    dn = ucsc_base_dn + "/tacacs-ext/provider-" + name
    return handle.query_dn(dn)


def tacacsplus_provider_exists(handle, name, **kwargs):
    """
    checks if a tacacsplus provider exists

    Args:
        handle (UcscHandle)
        name (string): name of tacacsplus provider
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    Returns:
        (True/False, MO/None)

    Example:
        tacacsplus_provider_exists(handle, name="test_tacac_prov", port="320")
    """

    mo = tacacsplus_provider_get(handle, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def tacacsplus_provider_modify(handle, name, **kwargs):
    """
    modifies a tacacsplus provider

    Args:
        handle (UcscHandle)
        name (string): name of tacacsplus provider
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaTacacsPlusProvider: Managed Object

    Raises:
        UcscOperationError: If AaaTacacsPlusProvider is not present

    Example:
        tacacsplus_provider_modify(handle, "test_tacac_prov", timeout="5")
    """

    mo = tacacsplus_provider_get(handle, name)
    if not mo:
        raise UcscOperationError(
                "tacacsplus_provider_modify",
                "TacacsPlus Provider '%s' does not exist" % name)

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def tacacsplus_provider_delete(handle, name):
    """
    deletes a tacacsplus provider

    Args:
        handle (UcscHandle)
        name (string): name of tacacsplus provider

    Returns:
        None

    Raises:
        UcscOperationError: If AaaTacacsPlusProvider is not present

    Example:
        tacacsplus_provider_delete(handle, name="test_tacac_prov")
    """

    mo = tacacsplus_provider_get(handle, name)
    if not mo:
        raise UcscOperationError("tacacsplus_provider_delete",
                                 "TacacsPlus Provider does not exist")

    handle.remove_mo(mo)
    handle.commit()


def tacacsplus_provider_group_create(handle, name, descr=None, **kwargs):
    """
    Creates a tacacsplus provider group

    Args:
        handle (UcscHandle)
        name (string): name of tacacsplus provider group
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaTacacsPlusProvider: Managed Object

    Example:
        tacacsplus_provider_create(handle, name="test_prov_grp")
    """

    from ucscsdk.mometa.aaa.AaaProviderGroup import AaaProviderGroup

    mo = AaaProviderGroup(
        parent_mo_or_dn=ucsc_base_dn + "/tacacs-ext",
        name=name, descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def tacacsplus_provider_group_get(handle, name):
    """
    Gets tacacsplus provider group

    Args:
        handle (UcscHandle)
        name (string): name of tacacsplus provider group

    Returns:
        AaaTacacsPlusProvider: Managed Object OR None

    Example:
        tacacsplus_provider_group_get(handle, name="test_prov_grp")
    """

    dn = ucsc_base_dn + "/tacacs-ext/providergroup-" + name
    return handle.query_dn(dn)


def tacacsplus_provider_group_exists(handle, name, **kwargs):
    """
    checks if a tacacsplus provider group exists

    Args:
        handle (UcscHandle)
        name (string): name of tacacsplus provider group
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        tacacsplus_provider_group_exists(handle, name="test_prov_grp")
    """

    mo = tacacsplus_provider_group_get(handle, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def tacacsplus_provider_group_delete(handle, name):
    """
    deletes a tacacsplus provider group

    Args:
        handle (UcscHandle)
        name (string): name of tacacsplus provider group

    Returns:
        None

    Raises:
        UcscOperationError: If AaaProviderGroup is not present

    Example:
        tacacsplus_provider_group_delete(handle, name="test_prov_grp")
    """

    mo = tacacsplus_provider_group_get(handle, name)
    if not mo:
        raise UcscOperationError("tacacsplus_provider_group_delete",
                                 "Provider  Group does not exist.")

    handle.remove_mo(mo)
    handle.commit()


def tacacsplus_provider_group_provider_add(handle, group_name, name,
                                           order="lowest-available",
                                           descr=None, **kwargs):
    """
    adds a tacacsplus provider to a tacacsplus provider  group

    Args:
        handle (UcscHandle)
        group_name (string): name of tacacsplus provider group
        order (string): order
        name (string): name of tacacsplus provider
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaProviderRef: Managed Object

    Raises:
        UcscOperationError: If AaaProviderGroup Or AaaProvider is not present

    Example:
        tacacsplus_provider_group_provider_add(handle,
                                    group_name="test_prov_grp",
                                    name="test_tacac_prov")
    """

    from ucscsdk.mometa.aaa.AaaProviderRef import AaaProviderRef

    group_dn = ucsc_base_dn + "/tacacs-ext/providergroup-" + group_name
    group_mo = handle.query_dn(group_dn)
    if not group_mo:
        raise UcscOperationError("tacacsplus_provider_group_provider_add",
                                 "TacacsPlus Provider Group does not exist.")

    provider_dn = ucsc_base_dn + "/tacacs-ext/provider-" + name
    mo = handle.query_dn(provider_dn)
    if not mo:
        raise UcscOperationError("tacacsplus_provider_group_provider_add",
                                 "TacacsPlus Provider does not exist.")

    mo = AaaProviderRef(parent_mo_or_dn=group_mo,
                        name=name,
                        order=order,
                        descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def tacacsplus_provider_group_provider_get(handle, group_name, name):
    """
    checks if a tacacsplus provider added to a tacacsplus provider  group

    Args:
        handle (UcscHandle)
        group_name (string): name of tacacsplus provider group
        name (string): name of tacacsplus provider

    Returns:
        AaaProviderRef: Managed Object OR None

    Raises:
        UcscOperationError: If AaaProviderGroup is not present

    Example:
        tacacsplus_provider_group_provider_get(handle,
                                    group_name="test_prov_grp",
                                    name="test_tacac_prov")
    """

    group_dn = ucsc_base_dn + "/tacacs-ext/providergroup-" + group_name
    group_mo = handle.query_dn(group_dn)
    if not group_mo:
        raise UcscOperationError("tacacsplus_provider_group_provider_get",
                                 "TacacsPlus Provider Group does not exist.")

    provider_dn = group_dn + "/provider-ref-" + name
    return handle.query_dn(provider_dn)


def tacacsplus_provider_group_provider_exists(handle, group_name, name,
                                              **kwargs):
    """
    checks if a tacacsplus provider added to a tacacsplus provider  group

    Args:
        handle (UcscHandle)
        group_name (string): name of tacacsplus provider group
        name (string): name of tacacsplus provider
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Raises:
        UcscOperationError: If AaaProviderGroup is not present

    Example:
        tacacsplus_provider_group_provider_exists(handle,
                                    group_name="test_prov_grp",
                                    name="test_tacac_prov")
    """

    mo = tacacsplus_provider_group_provider_get(handle, group_name, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def tacacsplus_provider_group_provider_modify(handle, group_name, name,
                                              **kwargs):
    """
    modifies a tacacsplus provider added to a tacacsplus provider  group

    Args:
        handle (UcscHandle)
        group_name (string): name of tacacsplus provider group
        name (string): name of tacacsplus provider
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaProviderRef: Managed Object

    Raises:
        UcscOperationError: If AaaProviderRef is not present

    Example:
        tacacsplus_provider_group_provider_modify(
          handle, group_name="test_prov_grp", name="test_tacac_prov",
          order="2")
    """

    mo = tacacsplus_provider_group_provider_get(handle, group_name, name)
    if not mo:
        raise UcscOperationError("tacacsplus_provider_group_provider_modify",
                                 "Provider not available under group.")

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def tacacsplus_provider_group_provider_remove(handle, group_name, name):
    """
    removes a tacacsplus provider from a tacacsplus provider  group

    Args:
        handle (UcscHandle)
        group_name (string): name of tacacsplus provider group
        name (string): name of tacacsplus provider

    Returns:
        None

    Raises:
        UcscOperationError: If AaaProviderRef is not present

    Example:
        tacacsplus_provider_group_provider_remove(handle,
                                    group_name="test_prov_grp",
                                    name="test_tacac_prov")
    """

    mo = tacacsplus_provider_group_provider_get(handle, group_name, name)
    if not mo:
        raise UcscOperationError("tacacsplus_provider_group_provider_remove",
                                 "Provider not available under group.")

    handle.remove_mo(mo)
    handle.commit()
