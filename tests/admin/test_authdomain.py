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

from ..connection.info import custom_setup, custom_teardown
from nose.tools import *
from ucsc_apis.admin.authdomain import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_auth_domain_create():
    auth_domain_create(handle, name="test_auth_dom", refresh_period="900")
    found = auth_domain_exists(handle, name="test_auth_dom")[0]
    assert_equal(found, True)


def test_002_auth_domain_modify():
    auth_domain_modify(handle, name="test_auth_dom", session_timeout="1000")
    mo = auth_domain_realm_configure(
        handle, domain_name="test_auth_dom", realm="ldap", provider_group="")
    assert_equal(mo.realm, "ldap")


def test_003_native_auth_configure():
    native_auth_configure(
        handle, def_role_policy="assign-default-role", con_login="local")
    mo = native_auth_configure(handle, def_role_policy="no-login")
    assert_equal(mo.def_role_policy, "no-login")


def test_004_native_auth_default():
    mo = native_auth_default(handle, realm="radius")
    assert_equal(mo.realm, "radius")
    native_auth_default(handle, realm="local")


def test_005_native_auth_console():
    mo = native_auth_console(handle, realm="local")
    assert_equal(mo.realm, "local")


def test_006_auth_domain_delete():
    auth_domain_delete(handle, name="test_auth_dom")
    found = auth_domain_exists(handle, name="test_auth_dom")[0]
    assert_equal(found, False)
