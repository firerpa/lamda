---
name: Bug report
about: Create a report to help us improve
title: "[ISSUE]"
labels: ''
assignees: ''

---

**Describe the bug**
**请详细描述 BUG**

**Generate statistics**
**生成BUG诊断日志**

```bash
https://raw.githubusercontent.com/rev1si0n/lamda/master/tools/statistics.sh

# Download statistics.sh from this link via browser
# 通过浏览器从该链接下载 statistics.sh

adb push statistics.sh /data/local/tmp
sh /data/local/tmp/statistics.sh /data/local/tmp/arm64-v8a/bin/launch.sh --logfile=/data/local/tmp/server.log

# Then upload /sdcard/statistics.txt and /data/local/tmp/server.log to this ISSUE
# 随后在此 ISSUE 中附上 /sdcard/statistics.txt 以及 /data/local/tmp/server.log
```
