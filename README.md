# async_reverse_dns_lookup
Python to script to perform reverse DNS lookup asynchronously

**TODO** - ` #Script crashing on lower powered CPU's. #Still in development`


**The script works as follows** -

1> User specifies country code to scan that country's IPv4 range

2> Script takes input from `ip_location_db.csv` file. This file contains ipv4 range allocations with their respective country codes

3> Then the script converts the ip ranges to list of ip addresses

4> These ip addresses are fed to the reverse_dns_lookup function

5> Reverse DNS lookup results are stored in a CSV file
