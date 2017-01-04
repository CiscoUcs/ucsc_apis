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
This module performs the operation related to role.
"""
ucsc_base_dn = "org-root/deviceprofile-default"


def role_create(handle, name, priv, descr="", **kwargs):
    """
    creates a role

    Args:
        handle (UcscHandle)
        name (string): role name
        priv (comma separated string): role privilege
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaRole: Managed Object

    Example:
        role_create(handle, name="testrole", priv="read-only")

    """

    from ucscsdk.mometa.aaa.AaaRole import AaaRole

    mo = AaaRole(parent_mo_or_dn=ucsc_base_dn,
                 name=name,
                 priv=priv,
                 descr=descr)

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def role_exists(handle, name, **kwargs):
    """
    checks if a role exists

    Args:
        handle (UcscHandle)
        name (string): role name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        role_exists(handle, name="testrole", priv="read-only")
    """

    dn = ucsc_base_dn + "/role-" + name
    mo = handle.query_dn(dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def role_modify(handle, name, **kwargs):
    """
    modifies role

    Args:
        handle (UcscHandle)
        name (string): role name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaRole: Managed Object

    Raises:
        ValueError: If AaaRole is not present

    Example:
        role_modify(handle, name="testrole", priv="read-only")
    """

    dn = ucsc_base_dn + "/role-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Role does not exist")

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def role_delete(handle, name):
    """
    deletes role

    Args:
        handle (UcscHandle)
        name (string): role name

    Returns:
        None

    Raises:
        ValueError: If AaaRole is not present

    Example:
        role_delete(handle, name="testrole")
    """

    dn = ucsc_base_dn + "/role-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("Role does not exist")

    handle.remove_mo(mo)
    handle.commit()
