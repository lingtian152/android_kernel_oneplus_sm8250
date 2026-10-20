# OnePlus 8T (KB2005) kernel customization

Target: OnePlus 8T / kebab / SM8250, user-reported official OxygenOS 14.
Base: `lingtian152/android_kernel_oneplus_sm8250`, branch `lingtian152-patch-1`.

## What this workflow does

- Adds SukiSU Ultra using its official integration script (`main` by default).
- Enables TCP BBR and FQ through kernel config and checks the final Kconfig.
- Builds `Image.gz` and DTBs and uploads them as CI artifacts.
- Does **not** create a boot.img or flashable AnyKernel ZIP. Do not flash the raw kernel image directly.

## Run it

Open Actions → **OnePlus 8T KB2005 kernel** → Run workflow. The default defconfig is a best-effort guess. If it does not exist, the workflow fails early and prints matching config candidates; select the actual device defconfig and rerun.

## Compatibility note

The branch Makefile reports Linux 4.19.157. Successful compilation does not establish compatibility with the exact OxygenOS 14 build, vendor modules, DTBO, or boot image. Keep a copy of the exact stock boot image and a recovery path.

SukiSU Ultra's current integration guide documents `main` as kprobe/kretprobe-based and requires `CONFIG_KPROBES=y` and `CONFIG_EXT4_FS=y`; `builtin` requires manual hook changes and is not interchangeable without reviewing this kernel's source.
