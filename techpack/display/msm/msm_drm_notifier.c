// SPDX-License-Identifier: GPL-2.0-only
/*
 * Minimal DRM notifier for OPlus display compatibility.
 */
#include <linux/module.h>
#include <linux/notifier.h>
#include <linux/msm_drm_notify.h>

static BLOCKING_NOTIFIER_HEAD(msm_drm_notifier_list);

int msm_drm_notifier_register(struct notifier_block *nb)
{
    return blocking_notifier_chain_register(&msm_drm_notifier_list, nb);
}
EXPORT_SYMBOL(msm_drm_notifier_register);

int msm_drm_notifier_unregister(struct notifier_block *nb)
{
    return blocking_notifier_chain_unregister(&msm_drm_notifier_list, nb);
}
EXPORT_SYMBOL(msm_drm_notifier_unregister);

int msm_drm_notifier_call_chain(unsigned long val, void *v)
{
    return blocking_notifier_call_chain(&msm_drm_notifier_list, val, v);
}
EXPORT_SYMBOL(msm_drm_notifier_call_chain);
