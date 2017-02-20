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
This module performs the operation related to user.
"""
from ucscsdk.ucscexception import UcscOperationError
from ..common.utils import get_device_profile_dn
ucsc_base_dn = get_device_profile_dn(name="default")


def user_create(handle, name, pwd, first_name=None, last_name=None, descr=None,
                clear_pwd_history="no", phone=None, email=None, expires="no",
                pwd_life_time="no-password-expire", expiration="never",
                enc_pwd=None, account_status="active",
                role="read-only", role_descr=None, **kwargs):
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
                  last_name="lastname", descr=None, clear_pwd_history="no",
                  phone="+91-1234567890", email="test@cisco.com",
                  pwd="p@ssw0rd", expires="yes",
                  pwd_life_time="no-password-expire",
                  expiration="2016-01-13T00:00:00", enc_pwd=None,
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

    user_mo.set_prop_multiple(**kwargs)

    AaaUserRole(parent_mo_or_dn=user_mo, name=role, descr=role_descr)
    handle.add_mo(user_mo, True)
    handle.commit()
    return user_mo


def user_get(handle, name):
    """
    Gets user

    Args:
        handle (UcscHandle)
        name (string): name

    Returns:
        AaaUser: Managed Object OR None

    Example:
        user_get(handle, name="test")
    """

    dn = ucsc_base_dn + "/user-" + name
    return handle.query_dn(dn)


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
                  last_name="lastname", descr=None, clear_pwd_history="no",
                  phone="+91-1234567890", email="test@cisco.com",
                  expires="yes",
                  pwd_life_time="no-password-expire",
                  expiration="2016-01-13T00:00:00", enc_pwd=None,
                  account_status="active")
    """

    mo = user_get(handle, name)
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
        UcscOperationError: If AaaUser is not present

    Example:
        user_modify(handle, name="test", first_name="firstname",
                  last_name="lastname", descr=None, clear_pwd_history="no",
                  phone="+91-1234567890", email="test@cisco.com",
                  expires="yes",
                  pwd_life_time="no-password-expire",
                  expiration="2016-01-13T00:00:00", enc_pwd=None,
                  account_status="active")
    """

    mo = user_get(handle, name)
    if not mo:
        raise UcscOperationError("user_modify",
                                 "User does not exist.")

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
        UcscOperationError: If AaaUser is not present

    Example:
        user_delete(handle, name="test")

    """

    mo = user_get(handle, name)
    if not mo:
        raise UcscOperationError("user_delete",
                                 "User does not exist.")

    handle.remove_mo(mo)
    handle.commit()


def user_role_add(handle, user_name, name, descr=None, **kwargs):
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
        UcscOperationError: If AaaUser is not present

    Example:
        user_role_add(handle, user_name="test", name="admin")
    """

    from ucscsdk.mometa.aaa.AaaUserRole import AaaUserRole

    dn = ucsc_base_dn + "/user-" + user_name
    obj = handle.query_dn(dn)
    if not obj:
        raise UcscOperationError("user_role_add",
                                 "User does not exist.")

    mo = AaaUserRole(parent_mo_or_dn=obj, name=name, descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def user_role_get(handle, user_name, name):
    """
    Gets role for the user

    Args:
        handle (UcscHandle)
        user_name (string): username
        name (string): rolename

    Returns:
        AaaUserRole: Managed object OR None

    Example:
        user_role_get(handle, user_name="test", name="admin")
    """

    user_dn = ucsc_base_dn + "/user-" + user_name
    dn = user_dn + "/role-" + name
    return handle.query_dn(dn)


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

    mo = user_role_get(handle, user_name, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def user_role_remove(handle, user_name, name):
    """
    Remove role from user

    Args:
        handle (UcscHandle)
        user_name (string): username
        name (string): rolename

    Returns:
        None

    Raises:
        UcscOperationError: If AaaUserRole is not present

    Example:
        user_role_remove(handle, user_name="test", name="admin")
    """

    mo = user_role_get(handle, user_name, name)
    if not mo:
        raise UcscOperationError("user_role_remove",
                                 "Role is not associated with user.")

    handle.remove_mo(mo)
    handle.commit()


def user_locale_add(handle, user_name, name, descr=None, **kwargs):
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
        UcscOperationError: If AaaUser is not present

    Example:
        user_locale_add(handle, user_name="test", name="testlocale")
    """

    from ucscsdk.mometa.aaa.AaaUserLocale import AaaUserLocale

    dn = ucsc_base_dn + "/user-" + user_name
    obj = handle.query_dn(dn)
    if not obj:
        raise UcscOperationError("user_locale_add",
                                 "User does not exist.")

    mo = AaaUserLocale(parent_mo_or_dn=obj, name=name, descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def user_locale_get(handle, user_name, name):
    """
    Gets locale for the user

    Args:
        handle (UcscHandle)
        user_name (string): username
        name (string): locale name

    Returns:
        AaaUserLocale: Managed Object OR None

    Example:
        user_locale_get(handle, user_name="test", name="testlocale")
    """

    user_dn = ucsc_base_dn + "/user-" + user_name
    dn = user_dn + "/locale-" + name
    return handle.query_dn(dn)


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

    mo = user_locale_get(handle, user_name, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def user_locale_remove(handle, user_name, name):
    """
    Remove locale from user

    Args:
        handle (UcscHandle)
        user_name (string): username
        name (string): locale name

    Returns:
        None

    Raises:
        UcscOperationError: If AaaUserLocale is not present

    Example:
        user_locale_remove(handle, user_name="test", name="testlocale")
    """

    mo = user_locale_get(handle, user_name, name)
    if not mo:
        raise UcscOperationError("user_locale_remove",
                                 "Locale is not associated with user.")

    handle.remove_mo(mo)
    handle.commit()


def password_strength_check(handle, descr=None, **kwargs):
    """
    Check password strength for locally authenticated user

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

    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def password_strength_uncheck(handle):
    """
    check or un-check password strength for locally authenticated user

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
    Modify password profile of locally authenticated user

    Args:
        handle (UcscHandle)
        change_interval (string): change interval
        no_change_interval (string): no change interval
        change_during_interval (string): ["disable", "enable"]
        change_count (string): change count
        history_count (string): history count
        expiration_warn_time(string): expiration warn time
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaPwdProfile: Managed Object

    Raises:
        UcscOperationError: If AaaPwdProfile is not present

    Example:
        password_profile_modify(handle, change_count="2")
    """

    dn = ucsc_base_dn + "/pwd-profile"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcscOperationError("password_profile_modify",
                                 "password profile does not exist.")

    args = {'change_interval': change_interval,
            'no_change_interval': no_change_interval,
            'change_during_interval': change_during_interval,
            'change_count': change_count,
            'history_count': history_count,
            'expiration_warn_time': expiration_warn_time,
            'descr': descr
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo
