import boto3
import subprocess

session = boto3.Session()
ec2 = session.resource('ec2')
client = session.client('ec2')

def create_vpc(vpcCIDR, name, Subnet):
    vpc_check = client.describe_vpcs(Filters = [{'Name': 'tag:Name', 'Values': [name+'-vpc']}])
    check = vpc_check['Vpcs']
    if check:
        print 'Vpcs found, ',vpc_check['Vpcs'][0]['VpcId']
    else:
        print('No vpcs found')
        print('Create VPC')
        print
        vpc = ec2.create_vpc(CidrBlock=vpcCIDR)
        vpc.create_tags(Tags=[{'Key': 'Name', 'Value': name+'-vpc'}])
        print 'vpc id        ', vpc.id
        create_sub(Subnet,vpc.id, name)
        create_igw(vpc.id, name)
        create_table(vpc.id, name)
        create_sec_group(vpc.id, name)

def create_sub(Subnet,vpcId,name):
    subnet = ec2.create_subnet(CidrBlock = Subnet, VpcId=vpcId)
    subnet.create_tags(Tags = [{'Key': 'Name', 'Value': name+'-subnet'}])
    print 'Subnet id     ', subnet.id

def create_igw(vpcId, name):
    igw = ec2.create_internet_gateway()
    igw.attach_to_vpc(VpcId = vpcId)
    igw.create_tags(Tags = [{'Key': 'Name', 'Value': name+'-internet-gateway'}])
    print 'igw id        ', igw.id

def create_sec_group(vpcId, name):
    secure_group = ec2.create_security_group(Description=name+'-sec_group', GroupName=name+'-sec_group', VpcId=vpcId)
    secure_group.create_tags(Tags=[{'Key': 'Name', 'Value': name+'-sec_group'}])
    secure_group.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
    print 'security group id      ', secure_group.id

def create_table(vpcId, name):
    routeid = client.describe_route_tables(Filters=[{'Name':'vpc-id','Values':[vpcId]}])['RouteTables'][0]['Associations'][0]['RouteTableId']
    route_table = ec2.RouteTable(id=routeid)
    route_table.create_tags(Tags = [{'Key': 'Name', 'Value': name}])
    print 'route table id      ', route_table.id

def create_key(name):
    keyname = client.describe_key_pairs(Filters = [{'Name': 'key-name', 'Values': [name+'-key']}])['KeyPairs']
    if keyname != []:
        print 'key pair found'
    else:
        keypair = ec2.create_key_pair(KeyName = name+'-key')
        print 'key pair not found'
        print 'create key pair'
        key = keypair.key_material
        with open(name+'-key.pem', 'w') as f:
            f.write(key)
            f.close()
            subprocess.call(['chmod', '400', 'tsoy-key.pem'])

def create_instance(disksize, imageid, instype, name, imageName):
    secure_group_id = client.describe_security_groups(Filters=[{'Name': 'tag:Name', 'Values': [name+'-sec_group']}])
    secure_group_id = secure_group_id['SecurityGroups'][0]['GroupId']
    subnet_id = client.describe_subnets(Filters=[{'Name': 'tag:Name', 'Values': [name+'-subnet']}])
    subnet_id = subnet_id['Subnets'][0]['SubnetId']
    ec2.create_instances(
        BlockDeviceMappings = [{'DeviceName': '/dev/sda1', 'Ebs': {'VolumeSize': disksize}}],
        ImageId = imageid,
        InstanceType = instype,
        KeyName = name+'-key',
        MaxCount = 1,
        MinCount = 1,
        NetworkInterfaces=[{'AssociatePublicIpAddress': True, 'DeviceIndex': 0, 'Description': name+'-network-interface', 'Groups': [secure_group_id], 'SubnetId': subnet_id}],
        TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': imageName+'-instance'}]}]
    )
    instances = client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [imageName+'-instance']}])
    instance_id = instances['Reservations'][0]['Instances'][0]['InstanceId']
    available = client.get_waiter('instance_status_ok')
    available.wait(InstanceIds = [instance_id])

def main():
    Subnet = '10.5.5.0/24'
    vpcCIDR = '10.5.0.0/16'
    name = 'tsoy'
    instanceName = '2'
    diskSize = 25
    ImageName = name+'-'+instanceName
    ImageId = 'ami-7c1bfd1b'
    InstanceType = 't2.micro'
    create_vpc(vpcCIDR, name, Subnet)
    create_key(name)
    create_instance(diskSize, ImageId, InstanceType, name, ImageName)

if __name__ == '__main__':
    main()
