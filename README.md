----create_instance.py----
Subnet = 'subnet'
#example
Subnet = '10.5.5.0/24
--------------------------
vpcCidr = 'net'
#example'
--------------------------
name = 'name owner'
#example
name = 'tsoy'
--------------------------
instanceName = 'number instance'
#example
instanceName = '1'
--------------------------
diskSize = size Gb
#example
diskSize = 25
--------------------------
ImageId = 'ami id'
#example
ImageId = 'ami-7c1bfd1b'
--------------------------

---------1-instance-status------
Enter IP: write public IP address instance
#example
Enter IP: 10.10.10.10
--------------------------------
Enter DNS: write public DNS
#example
Enter DNS: a.tsoy.example.com
--------------------------------

-------2-create-ami-------------
Enter Instance name: write Instance name
#example
Enter Instance name: tsoy-1-instance
--------------------------------

----3-create-ami-delete-instance---
Enter Instance name: write Instance name
#example
Enter Instance name: tsoy-1-instance
-----------------------------------

------4-clean-older-ami---------
#autmate clean
uncommit name, day, commit raw_input name, day
name = 'Tag name ami'
day = 'day before delete'
#example
name = tsoy-1-instance-2018-05-31
day = 7
#manual clean
Enter Tag name Images: 'Tag name ami'
Enter date before delete: 'day before delete'
#example
Enter Tag name Images:  tsoy-1-instance-2018-05-31
Enter date before delete: 7
-----------------------------------

------instance-statusl-all---------
just run programm
