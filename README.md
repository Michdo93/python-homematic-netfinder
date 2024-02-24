# python-homematic-netfinder
Rebuilt the HomeMatic Netfinder in Python. It should be able to find the IP addresses of HomeMatic control centres.

I have only tested this with a CCU2 and a CCU3. I have not tested how it works with HomeMatic IP or HomeMatic IP Wired Access Points or with various LAN gateways.

## Pre-Installation

Because you can run the code in `Python 2.7` or `Python 3.x` you have this two pre-installation opotions:

```
python -m pip install ping3
```

or

```
python -m pip install ping3
```

The `ping3` module is used to ping whether a device could be reached under this IP at all. It only makes sense to check whether it is a HomeMatic control centre if network devices are available.

## Usage

You can use it like this:

```
from netfinder import Netfinder

netfinder = Netfinder()
print(netfinder.find_homematic_devices())
```

This means that an IP address range of 192.168.0.X is taken from your own IP address (e.g. 192.168.0.5) in order to iterate through all 255 network addresses to check whether it is a HomeMatic control centre.

Of course, if you are in a different network area, the IP range is taken from this network area.

Or you can give an `ip address` like this:

```
from netfinder import Netfinder

netfinder = Netfinder("192.168.3.1")
print(netfinder.find_homematic_devices())
```

However, you can also specify an IPv4 address from another network area. However, this only works if you can access the other network area from one network area. In this example, all network devices in the 192.168.3.X range are checked for HomeMatic control centres.

And of course you can add ports like this:


```
from netfinder import Netfinder

netfinder = Netfinder("192.168.3.1", [80, 443, 9293])
print(netfinder.find_homematic_devices())
```

A HomeMatic control centre has a minimum of ports 80 (http) and 443 (https) open. However, this means that the scan would also incorrectly identify a large number of web servers as HomeMatic control centres. The main port that must be searched for is 9293. As you can of course reconfigure ports or open additional ports, it makes sense to be able to specify additional or different ports manually.
