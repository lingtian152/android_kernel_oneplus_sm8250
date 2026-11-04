/* SPDX-License-Identifier: GPL-2.0-only */
#ifndef _LINUX_MSM_DRM_NOTIFY_H
#define _LINUX_MSM_DRM_NOTIFY_H

#include <linux/notifier.h>

#define MSM_DRM_EARLY_EVENT_BLANK  0x01
#define MSM_DRM_EVENT_BLANK        0x02

enum {
    MSM_DRM_BLANK_UNBLANK = 0,
    MSM_DRM_BLANK_LP1,
    MSM_DRM_BLANK_LP2,
    MSM_DRM_BLANK_STANDBY,
    MSM_DRM_BLANK_SUSPEND,
    MSM_DRM_BLANK_POWERDOWN,
};

extern int msm_drm_notifier_register(struct notifier_block *nb);
extern int msm_drm_notifier_unregister(struct notifier_block *nb);
extern int msm_drm_notifier_call_chain(unsigned long val, void *v);

#endif /* _LINUX_MSM_DRM_NOTIFY_H */
