#!/usr/bin/env python3
"""Fix compatibility issues and compiler warnings in fetched OnePlus drivers."""

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


def ensure_text_replacement(path: pathlib.Path, old: str, new: str) -> None:
    source = path.read_text()
    count = source.count(old)

    if count > 1:
        raise SystemExit(f"Expected one old expression in {path}, found {count}")
    if count == 0 and new not in source:
        raise SystemExit(f"Could not find expected source text in {path}")
    if count:
        path.write_text(source.replace(old, new))
        print(f"Fixed driver warning: {path}")
    else:
        print(f"Driver warning already fixed: {path}")


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
    ensure_text_replacement(
        techpack / "camera/drivers/cam_sensor_module/cam_ois/onsemi_fw/LC898124/DownloadCmd.c",
        'TRACE("DataPM( %08x ), LengthPM( %08x ) , Parity( %08x ), DataDM( %08x ) , LengthDMA( %08x ) , LengthDMB( %08x ) \\n"\n'
        '\t, (int)ptr->DataPM , (int)ptr->LengthPM , (int)ptr->Parity , (int)ptr->DataDM , (int)ptr->LengthDMA , (int)ptr->LengthDMB );',
        'TRACE("Download lengths: PM (%08x), DMA (%08x), DMB (%08x)\\n",\n'
        '      (unsigned int)ptr->LengthPM, (unsigned int)ptr->LengthDMA,\n'
        '      (unsigned int)ptr->LengthDMB);',
    )
    ensure_text_replacement(
        techpack / "video/msm/vidc/hfi_iris2.c",
        "(u32)device->iface_q_table.align_virtual_addr",
        "(u32)(unsigned long)device->iface_q_table.align_virtual_addr",
    )
    ensure_text_replacement(
        vendor / "oplus/kernel/touchpanel/oplus_touchscreen/touchpanel_healthinfo.c",
        "tp_irq_interval_handle(monitor_data, (int)value)",
        "tp_irq_interval_handle(monitor_data, (int)(unsigned long)value)",
    )
    ensure_text_replacement(
        vendor / "oplus/kernel/system/oplus_project/qcom/oplus_project.c",
        "#define UINT2Ptr(n)        (uint32_t *)(n)\n#define Ptr2UINT32(p)    (uint32_t)(p)",
        "#define UINT2Ptr(n)        (uint32_t *)(unsigned long)(n)\n#define Ptr2UINT32(p)    (uint32_t)(unsigned long)(p)",
    )
    ensure_text_replacement(
        vendor / "oplus/kernel/system/theia/powerkey_monitor.c",
        "static const int flow_size = 16;\nstatic const int stage_brief_size = 64;\nstatic const int stage_total_size = stage_brief_size*flow_size;",
        "enum {\n    flow_size = 16,\n    stage_brief_size = 64,\n    stage_total_size = stage_brief_size * flow_size,\n};",
    )


if __name__ == "__main__":
    main()
