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
This module performs the operation related to TFTP core Expoerter.
"""
from ..common.utils import get_device_profile_dn
ucsc_base_dn = get_device_profile_dn(name="default")


def core_exporter_enable(handle,
                         hostname,
                         path,
                         port,
                         descr=None,
                         **kwargs):
    """
    This method configures UCS Central tftp core exporter.

    Args:
        handle (UcscHandle)
        hostname (string): IP or Hostname of server.
        path (string): Absolute path where core files are to be stored.
        port (string): Port number of tftp exporter
        descr (string): Basic description about configuration.
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        SysdebugAutoCoreFileExportTarget: ManagedObject

    Example:
        mo = core_exporter_enable(handle,hostname="10.65.180.18",
                port="69", path="/root/tftp")
    """

    from ucscsdk.mometa.sysdebug.SysdebugAutoCoreFileExportTarget import\
        SysdebugAutoCoreFileExportTarget

    mo = SysdebugAutoCoreFileExportTarget(
        parent_mo_or_dn=ucsc_base_dn,
        descr=descr,
        hostname=hostname,
        admin_state="enabled",
        path=path, port=port)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def core_exporter_disable(handle):
    """
    This method disables UCS Central tftp core exporter.

    Args:
        handle (UcscHandle)

    Returns:
        SysdebugAutoCoreFileExportTarget: ManagedObject

    Example:
        core_exporter_disable(handle)
    """

    from ucscsdk.mometa.sysdebug.SysdebugAutoCoreFileExportTarget import\
        SysdebugAutoCoreFileExportTarget

    mo = SysdebugAutoCoreFileExportTarget(
        parent_mo_or_dn=ucsc_base_dn,
        admin_state="disabled")

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo
