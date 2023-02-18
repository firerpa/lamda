---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**Generate statistics**

```bash
wget https://raw.githubusercontent.com/rev1si0n/lamda/master/tools/statistics.sh
adb push statistics.sh /data/local/tmp
# su to root (change launch.sh to LAMDA's launch.sh path)
sh /data/local/tmp/statistics.sh /data/local/tmp/arm64-v8a/bin/launch.sh
# then attach report file /sdcard/statistics.txt
```
