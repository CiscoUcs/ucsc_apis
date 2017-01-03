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
ucsc_base_dn = "org-root/deviceprofile-default"


def time_zone_set(handle, timezone, **kwargs):
    """
    This method sets the timezone of the UCS Central.

    Args:
        handle (UcscHandle)
        timezone (string): time zone e.g. "Asia/Kolkata"
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommDateTime: Managed object

    Raises:
        ValueError: If CommDateTime Mo is not found

    Example:
        To Set Time Zone:
            mo = time_zone_set(handle, "Asia/Kolkata")

        To Un-Set Time Zone:
            mo = time_zone_set(handle, "")
    """

    mo = handle.query_dn(ucsc_base_dn + "/datetime-svc")
    if not mo:
        raise ValueError("timezone does not exist")

    mo.timezone = timezone
    mo.admin_state = "enabled"
    mo.port = "0"

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def ntp_server_create(handle, name, descr="", **kwargs):
    """
    Adds NTP server using IP address.

    Args:
        handle (UcscHandle)
        name (string): NTP server IP address or Name
        descr (string): Basic description about NTP server
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommNtpProvider: Managed object

    Example:
        ntp_server_create(handle, "72.163.128.140", "Default NTP")
    """

    from ucscsdk.mometa.comm.CommNtpProvider import CommNtpProvider

    mo = CommNtpProvider(
        parent_mo_or_dn=ucsc_base_dn + "/datetime-svc",
        name=name,
        descr=descr)

    if kwargs:
        mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ntp_server_exists(handle, name, **kwargs):
    """
    checks if ntp server exists.

    Args:
        handle (UcscHandle)
        name (string): NTP server IP address or Name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        ntp_server_exists(handle, "72.163.128.140", descr="Default NTP")
    """

    dn = ucsc_base_dn + "/datetime-svc/ntp-" + name
    mo = handle.query_dn(dn)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ntp_server_remove(handle, name):
    """
    Removes the NTP server.

    Args:
        handle (UcscHandle)
        name : NTP server IP address or Name

    Returns:
        None

    Raises:
        ValueError: If CommNtpProvider is not found

    Example:
        ntp_server_remove(handle, "72.163.128.140")
    """

    dn = ucsc_base_dn + "/datetime-svc/ntp-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("NTP Server not found. Nothing to remove.")

    handle.remove_mo(mo)
    handle.commit()
