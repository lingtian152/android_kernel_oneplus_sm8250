#!/usr/bin/env python3
"""Adapt KernelSU-Next's strscpy_pad guard to the checked-out kernel version."""

import pathlib
import re
import sys


def read_kernel_version(makefile: pathlib.Path) -> tuple[int, int, int]:
    values = {}
    for name in ("VERSION", "PATCHLEVEL", "SUBLEVEL"):
        match = re.search(
            rf"(?m)^{name}\s*=\s*(\d+)\s*$", makefile.read_text()
        )
        if not match:
            raise SystemExit(f"Could not read {name} from {makefile}")
        values[name] = int(match.group(1))
    return values["VERSION"], values["PATCHLEVEL"], values["SUBLEVEL"]


def has_strscpy_pad(version: tuple[int, int, int]) -> bool:
    return version >= (4, 14, 222) and not (4, 19, 0) <= version < (4, 19, 172)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: adapt.py <KernelSU-Next directory>")

    version = read_kernel_version(pathlib.Path("Makefile"))
    header = pathlib.Path(sys.argv[1]) / "kernel/compat/kernel_compat.h"
    source = header.read_text()

    if has_strscpy_pad(version):
        print(f"Kernel {'.'.join(map(str, version))} provides strscpy_pad; no adaptation needed.")
        return

    function = re.search(
        r"static inline ssize_t __strscpy_pad\s*\([^)]*\)\s*\{(.*?)(?=\n\})",
        source,
        re.DOTALL,
    )
    if not function or "strscpy_pad(" not in function.group(1):
        if "strscpy_pad(" not in source:
            print("KernelSU-Next no longer calls strscpy_pad; no adaptation needed.")
            return
        raise SystemExit(f"Could not locate __strscpy_pad guard in {header}")

    body = function.group(1)
    call = body.index("strscpy_pad(")
    directives = list(
        re.finditer(r"(?m)^[ \t]*#if\b[^\n]*(?:\\\n[ \t]*[^\n]*)*", body)
    )
    directive = next((item for item in reversed(directives) if item.start() < call), None)
    if not directive:
        raise SystemExit(f"Could not find the preprocessor guard for strscpy_pad in {header}")

    compatible_guard = (
        "#if (LINUX_VERSION_CODE >= KERNEL_VERSION(4, 14, 222) && "
        "LINUX_VERSION_CODE < KERNEL_VERSION(4, 19, 0)) || "
        "LINUX_VERSION_CODE >= KERNEL_VERSION(4, 19, 172)"
    )
    updated_body = body[: directive.start()] + compatible_guard + body[directive.end() :]
    updated = source[: function.start(1)] + updated_body + source[function.end(1) :]
    header.write_text(updated)
    print(
        f"Adapted KernelSU-Next for kernel {'.'.join(map(str, version))}: "
        "strscpy_pad is unavailable in this kernel version."
    )


if __name__ == "__main__":
    main()
