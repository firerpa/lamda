FRPS service docker, save yourself the trouble of building it and you'll be up and running in a single command!

Note that these port forwarders are only recommended for Linux systems, so if your docker host is not Linux, please do not use them.

> If you need to log in to the backend of frps from outside, you will also need to unblock 6119/tcp.

Execute the command
```bash
docker run -it --rm --net host -e TOKEN=mypasswod -e BIND=127.0.0.1 -e PORTS=1000-5000 rev1si0n/frps
# TOKEN is the password, also the login password for the frps backend
# BIND is the bind interface The default is 127.0.0.1, do not set it to 0.0.0.0 unless you know what you are doing
# PORTS is the range of ports allowed to bind Default is 3000-5000
```

Note that some configuration and connection information will be output in the terminal after startup, find the ``----- LAMDA CONFIG -----`` segment
Copy the line `fwd.xxxxxx=xxxx` and write it to the `/data/local/tmp/properties.local` file on the device.
You can change the `rport` field there to the port you want, this port value must be in the `PORTS` range specified at boot time, the default 0 is randomly assigned.
Reboot the device and start lamda and lamda will automatically forward its own port to the server.


You can also access the frps backend page via 127.0.0.1:6119 (if the firewall 6119 is put through, you can also access it via http://服务器IP:6119)
The backend login user is `lamda` and the password is the TOKEN you provided when you started.