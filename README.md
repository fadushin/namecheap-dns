# Namecheap DNS Updater

This project provides a simple script for updating your NameCheap Dynamic IP address.

Namecheap provides links to a few tools you can use to update DNS, but I wanted something I could just run in a cron job running in a jail in my basement.

This software is meant to be lean and simple, so that mere mortals can read, understand, and possibly edit the tool to suite their purposes.  It's all of a few hundred lines of python code, so figuring out how it works should not take enormous feats of brilliance.

> Caveats:  This software is only designed to work with NameCheap Dynamic DNS.  It will likely not work with other Dynamic DNS providers and is not designed to boil the Dynamic DNS ocean.  It is designed to run on a UNIX-like system, typically from a home network that has been assigned a dynamic IP from an ISP.  You should generally only be interested in this software if you are trying to host services on your home network (HTTP, SSH, etc) that you want to expose to the internet.  Only IPv4 addresses are supported.  Error handling and reporting around failure conditions could probably better, at the expense of greater complexity in the code.  Life is about making compromises.

## Instructions for the impatient

These instructions assumes you have a UNIX-like system with Python 2.7 or later installed.  The machine you run should have internet access, presumably from your home network.  You typically should not run this software outside of the network you are attempting to register (e.g., your local internet cafe), unless you are trying to ruin someone's day.  Please don't do that.

Clone the git repo:

    shell% git clone https://github.com/fadushin/namecheap-dns.git
    shell% cd namecheap-dns

Copy the `etc/config-example.py` configuration file to `etc/config.py` and edit the file to specify the hosts, domain, and your Namecheap Dynamic DNS password.

    hosts=["@", "www"]
    domain="example.com"
    password="blahblahblahblah"

> Note.  Your Namecheap Dynamic DNS password is not the same as your Namecheap account password.  Please refer to https://www.namecheap.com/support/knowledgebase/subcategory.aspx/11/dynamic-dns for more information about using Dynamic DNS with Namecheap.

You may update multiple subdomains if you have them configured as `A` fields in your DNS records (e.g., `www.example.com`).  Note that the `host` parameter should be the subdomain _prefix_ of your domain (`www`), not the entire subdomain name (`www.example.com`).  Do not specify subdomain prefixes if you use CNAME records for your subdomains (preferred).

Run the `update.sh` script to update the hosts in your domain.

    shell$ bin/update.sh
    Updated host @ in domain example.com with ip 1.2.3.4
    Updated host www in domain example.com with ip 1.2.3.4

Once completed, this program will update your dynamically assigned IP address with Namecheap.

A data file will be written to `var/update.dat`, which contains information about the last updated IP address.  Note that subsequent runs will not update the IP, if your IP has not changed:

    shell$ bin/update.sh
    Host @ has ip 1.2.3.4.  Skipping.
    Host www has ip 1.2.3.4.  Skipping.

You can force an update using the `--force` flag, or by (re)moving the `var/update.dat` file.

## (Sys)Logging

Absent any configuration, this script will log to the standard output stream of the console.  Most messages are logged at `INFO` log level.  If a domain is updated with Namecheap, a message is logged a `WARN` log level.

For applications that run in cron, however, it might be desirable to log to `syslog`.

> Note.  Most syslog default implementations will only log messages at `WARN` or higher log level.  Consult your local `syslog` documentation for more information.

The settings for logging to `syslog` will vary from platform to platform, so you will need to consult your local Python documentation to figure out the settings that work best for your platform.

Here are settings that will work on FreeBSD, assuming you are sending log messages via UNIX domain sockets.

    # import logging.handlers
    # logger.addHandler(logging.handlers.SysLogHandler("/var/run/log"))

When configured, you should see entries in your system log, when an update has occurred:

    Jan  1 12:34:56 alfred Updated host @ in domain example.com with ip 1.2.3.4
    Jan  1 12:34:56 alfred Updated host www in domain example.com with ip 1.2.3.4

For Linux and MacOS systems, please [LMGTFY](http://lmgtfy.com/?q=macos+linux+syslog+python).  The [SysLogHandler](https://docs.python.org/2/library/logging.handlers.html#sysloghandler) documentation has more information about how to configure the `SysLogHandler` class.

## `cron` Settings

You may want to run the update script on an hourly candence, to check whether your IP address has changed, and then maybe once a day, run the command with the force flag, to ensure something gets written.

    @hourly     /someplace/namecheap-dns/bin/update.sh
    @daily      /someplace/namecheap-dns/bin/update.sh --force

Consult your local `crontab` documentation for more information about how to manage `cron` jobs.

## A Note about Security

This program uses HTTPS (HTTP over TLS) to acquire the current IP address of the network on which the command is run, as well as to update the IP address with Namecheap, if warranted.

The hosts contacted are `ipinfo.io` and `dynamicdns.park-your-domain.com`.  The user's Dynamic DNS password is sent in the HTTP URL (i.e., TCP/IP payload) to the Namecheap server.

The payload is protected via TLS, and is hence hidden from a passive observer, and the Python libraries promise to perform TLS server authentication, as well as to verify the target hostname using the procedures recommended in PKIX certification authentication.  (A reference would be nice, but pedantic.)  Use the latest version of Python (2.7 or later), to ensure the Python HTTP client libraries are performing proper TLS authentication.

If you suspect your Namecheap Dynamic DNS password has been compromised, please use the Namecheap management console to generate a new Dynamic DNS password, and reconfigure this software to use it.

## License

This software is distributed under an MIT-like open source license.

    Copyright (c) dushin.net
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
        * Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in the
          documentation and/or other materials provided with the distribution.
        * Neither the name of dushin.net nor the
          names of its contributors may be used to endorse or promote products
          derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY dushin.net ``AS IS'' AND ANY
    EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL dushin.net BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
