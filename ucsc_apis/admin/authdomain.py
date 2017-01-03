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
This module performs the operation related to Authentication management.
"""
ucsc_base_dn = "org-root/deviceprofile-default"


def auth_domain_create(handle, name, refresh_period="600",
                       session_timeout="7200", descr="", **kwargs):
    """
    Adds a auth domain

    Args:
        handle (UcscHandle)
        name (string): name of auth domain
        refresh_period: refresh period in seconds. Default 600.
        session_timeout: timeout in seconds. Default 7200.
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaDomain : Managed Object

    Example:
        auth_domain_create(handle, name="ciscoucscentral")
    """
    from ucscsdk.mometa.aaa.AaaDomain import AaaDomain

    mo = AaaDomain(parent_mo_or_dn=ucsc_base_dn + "/auth-realm",
                   name=name,
                   refresh_period=refresh_period,
                   session_timeout=session_timeout,
                   descr=descr)

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def auth_domain_exists(handle, name, **kwargs):
    """
    checks if auth domain exists

    Args:
        handle (UcscHandle)
        name (string): name of auth domain
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        auth_domain_exists(handle, name="ciscoucscentral")
    """

    dn = ucsc_base_dn + "/auth-realm/domain-" + name
    mo = handle.query_dn(dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def auth_domain_modify(handle, name, **kwargs):
    """
    Modifies a domain

    Args:
        handle (UcscHandle)
        name (string): name of domain
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaDomain : Managed Object

    Raises:
        ValueError: If AaaDomain is not present

    Example:
        auth_domain_modify(handle, name="ciscoucscentral", descr="modified")
    """

    dn = ucsc_base_dn + "/auth-realm/domain-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Auth Domain '%s' does not exist." % dn)

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def auth_domain_delete(handle, name):
    """
    deletes a auth domain.

    Args:
        handle (UcscHandle)
        name (string): auth domain name

    Returns:
        None

    Raises:
        ValueError: If AaaDomain is not present

    Example:
        auth_domain_delete(handle, name="ciscoucscentral")
    """

    dn = ucsc_base_dn + "/auth-realm/domain-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Auth Domain '%s' does not exist." % dn)

    handle.remove_mo(mo)
    handle.commit()


def auth_domain_realm_configure(handle, domain_name, realm="local",
                                provider_group="", name="", descr="",
                                **kwargs):
    """
    configure realm of a auth domain.

    Args:
        handle (UcscHandle)
        domain_name (string): auth domain name
        realm (string): realm ["ldap", "local", "none", "radius", "tacacs"]
        provider_group (string): provider group name
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaDomainAuth : Managed Object

    Raises:
        ValueError: If AaaDomain is not present

    Example:
        auth_domain_realm_configure(handle, domain_name="ciscoucscentral",
                                    realm="ldap")
    """

    from ucscsdk.mometa.aaa.AaaDomainAuth import AaaDomainAuth

    dn = ucsc_base_dn + "/auth-realm/domain-" + domain_name
    obj = handle.query_dn(dn)
    if not obj:
        raise ValueError("Auth Domain '%s' does not exist" % dn)

    mo = AaaDomainAuth(parent_mo_or_dn=obj, name=name, descr=descr,
                       realm=realm, provider_group=provider_group)

    if kwargs:
        mo.set_prop_multiple(kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def native_authentication_configure(handle, def_role_policy=None,
                                    def_login=None, con_login=None,
                                    descr=None, **kwargs):
    """
    configure native authentication.

    Args:
        handle (UcscHandle)
        def_role_policy (string): def_role_policy
        def_login (string): def_login
        con_login (string): con_login
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaAuthRealm : Managed Object

    Raises:
        ValueError: If AaaAuthRealm is not present

    Example:
        native_authentication_configure(handle, descr="modified")
    """

    mo = handle.query_dn(ucsc_base_dn + "/auth-realm")
    if not mo:
        raise ValueError("Native Authentication does not exist.")

    if def_role_policy:
        mo.def_role_policy = def_role_policy
    if def_login:
        mo.def_login = def_login
    if con_login:
        mo.con_login = con_login
    if descr:
        mo.descr = descr

    if kwargs:
        mo.set_prop_multiple(kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def native_authentication_default(handle, realm=None, session_timeout=None,
                                  refresh_period=None, provider_group=None,
                                  name=None, descr=None, **kwargs):
    """
    configure default native authentication.

    Args:
        handle (UcscHandle)
        realm (string): realm
        session_timeout (string): session_timeout
        refresh_period (string): refresh_period
        provider_group (string): provider_group
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaDefaultAuth : Managed Object

    Raises:
        ValueError: If AaaDefaultAuth is not present

    Example:
        native_authentication_default(handle, descr="modified")
    """

    mo = handle.query_dn(
        ucsc_base_dn + "/auth-realm/default-auth")
    if not mo:
        raise ValueError("Native Default Authentication does not exist")

    if realm:
        mo.realm = realm
    if session_timeout:
        mo.session_timeout = session_timeout
    if refresh_period:
        mo.refresh_period = refresh_period
    if provider_group:
        mo.provider_group = provider_group
    if name:
        mo.name = name
    if descr:
        mo.descr = descr

    if kwargs:
        mo.set_prop_multiple(kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def native_authentication_console(handle, realm=None, provider_group=None,
                                  name=None, descr=None, **kwargs):
    """
    configure console native authentication.

    Args:
        handle (UcscHandle)
        realm (string): realm
        provider_group (string): provider_group
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaConsoleAuth : Managed Object

    Raises:
        ValueError: If AaaConsoleAuth is not present

    Example:
        native_authentication_console(handle, descr="modified")
    """

    mo = handle.query_dn(
        ucsc_base_dn + "/auth-realm/console-auth")
    if not mo:
        raise ValueError("Native Console Authentication does not exist")

    if realm:
        mo.realm = realm
    if provider_group:
        mo.provider_group = provider_group
    if name:
        mo.name = name
    if descr:
        mo.descr = descr

    if kwargs:
        mo.set_prop_multiple(kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo
