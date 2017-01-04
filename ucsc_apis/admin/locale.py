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
This module performs the operation related to dns server management.
"""
ucsc_base_dn = "org-root/deviceprofile-default"


def locale_create(handle, name, descr="", **kwargs):
    """
    creates a locale

    Args:
        handle (UcscHandle)
        name (string): name of ldap provider
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaLocale : Managed Object

    Example:
        locale_create(handle, name="test_locale")
    """

    from ucscsdk.mometa.aaa.AaaLocale import AaaLocale

    mo = AaaLocale(parent_mo_or_dn=ucsc_base_dn,
                   name=name,
                   descr=descr)

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def locale_exists(handle, name, **kwargs):
    """
    checks if locale exists

    Args:
        handle (UcscHandle)
        name (string): name of ldap provider
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        locale_exists(handle, name="test_locale")
    """

    dn = ucsc_base_dn + "/locale-" + name
    mo = handle.query_dn(dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def locale_modify(handle, name, **kwargs):
    """
    modifies a locale

    Args:
        handle (UcscHandle)
        name (string): name of locale
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaLocale : Managed Object

    Raises:
        ValueError: If AaaLocale is not present

    Example:
        locale_modify(handle, name="test_locale")
    """

    dn = ucsc_base_dn + "/locale-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Locale does not exist")

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def locale_delete(handle, name):
    """
    deletes locale

    Args:
        handle (UcscHandle)
        name (string): locale name

    Returns:
        None

    Raises:
        ValueError: If AaaLocale is not present

    Example:
        locale_delete(handle, name="test_locale")
    """

    dn = ucsc_base_dn + "/locale-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Locale does not exist")

    handle.remove_mo(mo)
    handle.commit()


def locale_assign_org(handle, locale_name, name, org_dn="org-root", descr="",
                      **kwargs):
    """
    assigns a locale to org

    Args:
        handle (UcscHandle)
        locale_name(string): locale name
        name (string): name for the assignment
        org_dn (string): org_dn
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaOrg : Managed Object

    Raises:
        ValueError: If AaaLocale is not present

    Example:
        locale_assign_org(handle, name="test_locale")
    """

    from ucscsdk.mometa.aaa.AaaOrg import AaaOrg

    dn = ucsc_base_dn + "/locale-" + locale_name
    obj = handle.query_dn(dn)
    if not obj:
        raise ValueError("Locale does not exist")

    mo = AaaOrg(parent_mo_or_dn=obj, name=name, org_dn=org_dn, descr=descr)

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def locale_unassign_org(handle, locale_name, name):
    """
    unassigns a locale from org

    Args:
        handle (UcscHandle)
        locale_name(string): locale name
        name (string): name of assignment

    Returns:
        None

    Raises:
        ValueError: If AaaOrg is not present

    Example:
        locale_unassign_org(handle, locale_name="test_locale,
                            name="org_name")
    """

    locale_dn = ucsc_base_dn + "/locale-" + locale_name
    dn = locale_dn + "/org-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("No Org assigned to Locale")

    handle.remove_mo(mo)
    handle.commit()


def locale_assign_domaingroup(handle, locale_name, name,
                              domaingroup_dn="domaingroup-root", descr="",
                              **kwargs):
    """
    assigns a locale to domaingroup

    Args:
        handle (UcscHandle)
        locale_name(string): locale name
        name (string): name for the assignment
        domaingroup_dn (string): domaingroup_dn
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaOrg : Managed Object

    Raises:
        ValueError: If AaaLocale is not present

    Example:
        locale_assign_domaingroup(handle, name="test_locale")
    """

    from ucscsdk.mometa.aaa.AaaDomainGroup import AaaDomainGroup

    dn = ucsc_base_dn + "/locale-" + locale_name
    obj = handle.query_dn(dn)
    if not obj:
        raise ValueError("Locale does not exist")

    mo = AaaDomainGroup(parent_mo_or_dn=obj, name=name,
                        domaingroup_dn=domaingroup_dn, descr=descr)

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def locale_unassign_domaingroup(handle, locale_name, name):
    """
    unassigns a locale

    Args:
        handle (UcscHandle)
        locale_name(string): locale name
        name (string): name of assignment
        descr (string): descr

    Returns:
        None

    Raises:
        ValueError: If AaaOrg is not present

    Example:
        locale_unassign_domaingroup(handle, locale_name="test_locale,
                            name="domaingroup_name")
    """

    locale_dn = ucsc_base_dn + "/locale-" + locale_name
    dn = locale_dn + "/domaingroup-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("No domaingroup assigned to Locale")

    handle.remove_mo(mo)
    handle.commit()
