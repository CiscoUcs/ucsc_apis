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
from ucsc_apis.admin.user import *
from ucsc_apis.admin.locale import *
import random
import string

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def random_string(length):
    return ''.join(random.choice(string.ascii_letters)
                   for ii in range(length + 1))


def test_001_user_create():
    user_create(handle, name="test_user",
                first_name="testuser", pwd=random_string(8))
    found = user_exists(handle, name="test_user", first_name="testuser")[0]
    assert_equal(found, True)


def test_002_user_modify():
    mo = user_modify(handle, name="test_user", last_name="test lastname")
    assert_equal(mo.last_name, "test lastname")


def test_003_user_add_role():
    user_add_role(handle, user_name="test_user", name="storage")
    found = user_role_exists(handle, user_name="test_user", name="storage")[0]
    assert_equal(found, True)


def test_004_user_remove_role():
    user_remove_role(handle, user_name="test_user", name="storage")
    found = user_role_exists(handle, user_name="test_user", name="storage")[0]
    assert_equal(found, False)


def test_005_locale_create():
    locale_create(handle, name="testlocale")
    found = locale_exists(handle, name="testlocale")[0]
    assert_equal(found, True)


def test_006_user_add_locale():
    user_add_locale(handle, user_name="test_user", name="testlocale")
    found = user_locale_exists(handle, user_name="test_user",
                               name="testlocale")[0]
    assert_equal(found, True)


def test_007_user_remove_locale():
    user_remove_locale(handle, user_name="test_user", name="testlocale")
    found = user_locale_exists(handle, user_name="test_user",
                               name="testlocale")[0]
    assert_equal(found, False)


def test_008_locale_delete():
    locale_delete(handle, name="testlocale")
    found = locale_exists(handle, name="testlocale")[0]
    assert_equal(found, False)


def test_009_password_strength_check():
    mo = password_strength_check(handle)
    assert_equal(mo.pwd_strength_check, "yes")
    mo = password_strength_uncheck(handle)
    assert_equal(mo.pwd_strength_check, "no")


def test_010_password_profile_modify():
    mo = password_profile_modify(handle, change_count="3")
    assert_equal(mo.change_count, "3")


def test_011_user_delete():
    user_delete(handle, name="test_user")
    found = user_exists(handle, name="test_user", first_name="testuser")[0]
    assert_equal(found, False)
