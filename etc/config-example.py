##
## Example configuration file.
##
## Copy this file to etc/config.py, and edit entries below
##

##
## hosts
##
## This parameter sets the list of hosts to update for which you have A records defined.
## Use "@" for the host domain, and the name prefix for any subdomains (e.g., "www.example.com")
##
hosts=["@", "www"]

##
## domain
##
## This parameter sets the domain you have registered with Namecheap.
##
domain="example.com"

##
## password
##
## The Namecheap Dynamic DNS password used for updates.
## Note that this password is NOT the same as your Namecheap account password.
##
password="blahblahblahblah"

##
## logger
##
## The logger instance to use.
##
import logging
logger = logging.getLogger()

##
## Add a console handler for stdout, and set the log level to INFO
##
import sys
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

##
## Uncomment and edit this section to direct logs to syslog.
## You may want or need to set the SyslogHandler UNIX domain
## socket differently, depending on the flavor of UNIX (or Linux)
## you are using.  Please consult the Python documentation for
## more information about how to log to syslog.
##

# import logging.handlers
# logger.addHandler(logging.handlers.SysLogHandler("/var/run/log"))
