from collections.abc import Sequence
from typing import IO
from typing import Literal

Method = Literal["get", "post", "patch", "put", "delete"]
Readable = IO | str | bytes | bytearray
UploadFiles = dict[str, Readable] | Sequence[tuple[str, Readable]]
JSONType = str | int | float | bool | None | dict[str, "JSONType"] | list["JSONType"]
