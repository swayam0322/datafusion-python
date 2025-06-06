# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pyarrow as pa
from datafusion import SessionContext
from ffi_table_provider import MyTableProvider


def test_table_loading():
    ctx = SessionContext()
    table = MyTableProvider(3, 2, 4)
    ctx.register_table_provider("t", table)
    result = ctx.table("t").collect()

    assert len(result) == 4
    assert result[0].num_columns == 3

    result = [r.column(0) for r in result]
    expected = [
        pa.array([0, 1], type=pa.int32()),
        pa.array([2, 3, 4], type=pa.int32()),
        pa.array([4, 5, 6, 7], type=pa.int32()),
        pa.array([6, 7, 8, 9, 10], type=pa.int32()),
    ]

    assert result == expected
