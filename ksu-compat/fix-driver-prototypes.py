#!/usr/bin/env python3
"""Fix incompatible function signatures in the fetched OnePlus driver sources."""

import pathlib
import re
import sys


def ensure_void_prototype(path: pathlib.Path, pattern: str, replacement: str) -> None:
    source = path.read_text()
    expression = re.compile(pattern, re.MULTILINE)
    source, count = expression.subn(replacement, source)

    if count > 1:
        raise SystemExit(f"Expected one old-style definition in {path}, found {count}")
    if count == 0 and replacement not in source:
        raise SystemExit(f"Could not find expected function definition in {path}")
    if count:
        path.write_text(source)
        print(f"Fixed strict prototype: {path}")
    else:
        print(f"Strict prototype already fixed: {path}")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: fix-driver-prototypes.py <vendor-root> <techpack-root>")

    vendor = pathlib.Path(sys.argv[1])
    techpack = pathlib.Path(sys.argv[2])
    ensure_void_prototype(
        vendor / "oplus/kernel/touchpanel/oplus_touchscreen/touchpanel_common_driver.c",
        r"^bool\s+tp_boot_mode_normal\s*\(\s*\)(?=\s*\{)",
        "bool tp_boot_mode_normal(void)",
    )
    ensure_void_prototype(
        vendor / "oplus/kernel/system/uboot_log/uboot_log.c",
        r"^int\s+ubootback_thread_fn\s*\(\s*\)(?=\s*\{)",
        "int ubootback_thread_fn(void *data)",
    )
    ensure_void_prototype(
        techpack / "display/oplus/oplus_display_panel.c",
        r"^void\s+__exit\s+oplus_display_panel_exit\s*\(\s*\)(?=\s*\{)",
        "void __exit oplus_display_panel_exit(void)",
    )


if __name__ == "__main__":
    main()
