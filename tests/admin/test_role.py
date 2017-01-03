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

from ..connection.info import custom_setup, custom_teardown
from nose.tools import *
from ucsc_apis.admin.role import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_role_create():
    role_create(handle, name="test_role", priv="admin")
    found = role_exists(handle, name="test_role", priv="admin")[0]
    assert_equal(found, True)


def test_002_role_modify():
    mo = role_modify(handle, name="test_role", priv="read-only")
    assert_equal(mo.priv, "read-only")


def test_003_role_delete():
    role_delete(handle, name="test_role")
    found = role_exists(handle, name="test_role")[0]
    assert_equal(found, False)
