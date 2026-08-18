# SM-F956B / F956BXXS4DZG3 exploit test APK

This branch builds an exploit-only hardware validation APK for the exact Galaxy Z Fold6 target:

- model: `SM-F956B`
- kernel: `6.1.145-android14-11-33418572-abF956BXXS4DZG3`
- payload target: `q6q-F956BXXS4DZG3`

The APK build checks out `666sxrA/Root-My-Galaxy-Payloads` branch `agent/f956b-dzg3-port`, builds the 104128-byte release app payload with Android NDK r29, and bundles it under the app assets.

The launcher activity refuses to run on a model/kernel mismatch. A successful first-stage exploit test requires the payload log to contain both `exploit completed` and `done=1 root=1`.

This test APK deliberately does **not** late-load KernelSU. The KernelSU step should be added only after the exploit path is confirmed on the exact DZG3 hardware.
