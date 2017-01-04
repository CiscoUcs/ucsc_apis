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
This module performs the operation related to user.
"""
ucsc_base_dn = "org-root/deviceprofile-default"


def user_create(handle, name, pwd, first_name="", last_name="", descr="",
                clear_pwd_history="no", phone="", email="", expires="no",
                pwd_life_time="no-password-expire", expiration="never",
                enc_pwd="", account_status="active",
                role="read-only", role_descr="", **kwargs):
    """
    Creates user and assign role to it.

    Args:
        handle (UcscHandle)
        name (string): name
        first_name (string): first_name
        last_name (string): last_name
        descr (string): descr
        clear_pwd_history (string): clear_pwd_history
        phone (string): phone
        email (string): email
        pwd (string): pwd
        expires (string): expires
        pwd_life_time (string): pwd_life_time
        expiration (string): expiration
        enc_pwd (string): enc_pwd
        account_status (string): account_status
        role (string): role
        role_descr (string): role_descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaUser: Managed Object

    Example:
        user_create(handle, name="test", first_name="firstname",
                  last_name="lastname", descr="", clear_pwd_history="no",
                  phone="+91-1234567890", email="test@cisco.com",
                  pwd="p@ssw0rd", expires="yes",
                  pwd_life_time="no-password-expire",
                  expiration="2016-01-13T00:00:00", enc_pwd="",
                  account_status="active")
    """

    from ucscsdk.mometa.aaa.AaaUser import AaaUser
    from ucscsdk.mometa.aaa.AaaUserRole import AaaUserRole

    user_mo = AaaUser(parent_mo_or_dn=ucsc_base_dn,
                      name=name,
                      first_name=first_name,
                      last_name=last_name,
                      descr=descr,
                      clear_pwd_history=clear_pwd_history,
                      phone=phone,
                      email=email,
                      pwd=pwd,
                      expires=expires,
                      pwd_life_time=pwd_life_time,
                      expiration=expiration,
                      enc_pwd=enc_pwd,
                      account_status=account_status)

    if kwargs:
        user_mo.set_prop_multiple(**kwargs)

    AaaUserRole(parent_mo_or_dn=user_mo, name=role, descr=role_descr)
    handle.add_mo(user_mo, True)
    handle.commit()
    return user_mo


def user_exists(handle, name, **kwargs):
    """
    checks if user exists

    Args:
        handle (UcscHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        user_exists(handle, name="test", first_name="firstname",
                  last_name="lastname", descr="", clear_pwd_history="no",
                  phone="+91-1234567890", email="test@cisco.com",
                  expires="yes",
                  pwd_life_time="no-password-expire",
                  expiration="2016-01-13T00:00:00", enc_pwd="",
                  account_status="active")
    """

    dn = ucsc_base_dn + "/user-" + name
    mo = handle.query_dn(dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def user_modify(handle, name, **kwargs):
    """
    modifies user

    Args:
        handle (UcscHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaUser: Managed Object

    Raises:
        ValueError: If AaaUser is not present

    Example:
        user_modify(handle, name="test", first_name="firstname",
                  last_name="lastname", descr="", clear_pwd_history="no",
                  phone="+91-1234567890", email="test@cisco.com",
                  expires="yes",
                  pwd_life_time="no-password-expire",
                  expiration="2016-01-13T00:00:00", enc_pwd="",
                  account_status="active")
    """

    dn = ucsc_base_dn + "/user-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("User does not exist.")

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def user_delete(handle, name):
    """
    deletes user

    Args:
        handle (UcscHandle)
        name (string): name

    Returns:
        None

    Raises:
        ValueError: If AaaUser is not present

    Example:
        user_delete(handle, name="test")

    """

    dn = ucsc_base_dn + "/user-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("User does not exist.")

    handle.remove_mo(mo)
    handle.commit()


def user_add_role(handle, user_name, name, descr="", **kwargs):
    """
    Adds role to an user

    Args:
        handle (UcscHandle)
        user_name (string): username
        name (string): rolename
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaUserRole: Managed object

    Raises:
        ValueError: If AaaUser is not present

    Example:
        user_add_role(handle, user_name="test", name="admin")
    """

    from ucscsdk.mometa.aaa.AaaUserRole import AaaUserRole

    dn = ucsc_base_dn + "/user-" + user_name
    obj = handle.query_dn(dn)
    if not obj:
        raise ValueError("User does not exist.")

    mo = AaaUserRole(parent_mo_or_dn=obj, name=name, descr=descr)

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def user_role_exists(handle, user_name, name, **kwargs):
    """
    check if role is already added to user

    Args:
        handle (UcscHandle)
        user_name (string): username
        name (string): rolename
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        user_role_exists(handle, user_name="test", name="admin")
    """

    user_dn = ucsc_base_dn + "/user-" + user_name
    dn = user_dn + "/role-" + name
    mo = handle.query_dn(dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def user_remove_role(handle, user_name, name):
    """
    Remove role from user

    Args:
        handle (UcscHandle)
        user_name (string): username
        name (string): rolename

    Returns:
        None

    Raises:
        ValueError: If AaaUserRole is not present

    Example:
        user_remove_role(handle, user_name="test", name="admin")
    """

    user_dn = ucsc_base_dn + "/user-" + user_name
    dn = user_dn + "/role-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Role is not associated with user.")

    handle.remove_mo(mo)
    handle.commit()


def user_add_locale(handle, user_name, name, descr="", **kwargs):
    """
    Adds locale to user

    Args:
        handle (UcscHandle)
        user_name (string): username
        name (string): locale name
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaUserLocale: Managed Object

    Raises:
        ValueError: If AaaUser is not present

    Example:
        user_add_locale(handle, user_name="test", name="testlocale")
    """

    from ucscsdk.mometa.aaa.AaaUserLocale import AaaUserLocale

    dn = ucsc_base_dn + "/user-" + user_name
    obj = handle.query_dn(dn)
    if not obj:
        raise ValueError("User does not exist.")

    mo = AaaUserLocale(parent_mo_or_dn=obj, name=name, descr=descr)

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def user_locale_exists(handle, user_name, name, **kwargs):
    """
    check if locale already added to user

    Args:
        handle (UcscHandle)
        user_name (string): username
        name (string): locale name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        user_locale_exists(handle, user_name="test", name="testlocale")
    """

    user_dn = ucsc_base_dn + "/user-" + user_name
    dn = user_dn + "/locale-" + name
    mo = handle.query_dn(dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def user_remove_locale(handle, user_name, name):
    """
    Remove locale from user

    Args:
        handle (UcscHandle)
        user_name (string): username
        name (string): locale name

    Returns:
        None

    Raises:
        ValueError: If AaaUserLocale is not present

    Example:

    """

    user_dn = ucsc_base_dn + "/user-" + user_name
    dn = user_dn + "/locale-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("Locale is not associated with user.")

    handle.remove_mo(mo)
    handle.commit()


def password_strength_check(handle, descr="", **kwargs):
    """
    check pasword strength for locally authenticated user

    Args:
        handle (UcscHandle)
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaUserEp: Managed Object

    Example:
        password_strength_check(handle)
    """

    mo = handle.query_dn(ucsc_base_dn + "/pwd-profile")
    mo.pwd_strength_check = "yes"
    mo.descr = descr

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def password_strength_uncheck(handle):
    """
    check or un-check pasword strength for locally authenticated user

    Args:
        handle (UcscHandle)

    Returns:
        AaaUserEp: Managed Object

    Example:
        password_strength_uncheck(handle)
    """

    mo = handle.query_dn(ucsc_base_dn + "/pwd-profile")
    mo.pwd_strength_check = "no"
    handle.set_mo(mo)
    handle.commit()
    return mo


def password_profile_modify(handle, change_interval=None,
                            no_change_interval=None,
                            change_during_interval=None, change_count=None,
                            history_count=None, expiration_warn_time=None,
                            descr=None, **kwargs):
    """
    modfiy passpord profile of locally authenticated user

    Args:
        handle (UcscHandle)
        change_interval (number): change interval
        no_change_interval (number): no change interval
        change_during_interval (string): ["disable", "enable"]
        change_count (number): change count
        history_count (number): history count
        expiration_warn_time(number): expiration warn time
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaPwdProfile: Managed Object

    Raises:
        ValueError: If AaaPwdProfile is not present

    Example:
        password_profile_modify(handle, change_count="2")
    """

    dn = ucsc_base_dn + "/pwd-profile"
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("password profile does not exist.")

    if change_interval:
        mo.change_interval = change_interval
    if no_change_interval:
        mo.no_change_interval = no_change_interval
    if change_during_interval:
        mo.change_during_interval = change_during_interval
    if change_count:
        mo.change_count = change_count
    if history_count:
        mo.history_count = history_count
    if expiration_warn_time:
        mo.expiration_warn_time = expiration_warn_time
    if descr:
        mo.descr = descr

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo
