import boto3
import datetime

session = boto3.Session()
ec2 = session.resource('ec2')
client = session.client('ec2')

def create_ami(name, date, instId):
    response = client.create_image(Description = name+'-'+date, InstanceId = instId, Name = name+'-'+date)
    image_id = response['ImageId']
    available = client.get_waiter('image_available')
    available.wait(ImageIds = [image_id])
    create_ami_tag(name, date)

def create_ami_tag(name, date):
    ami = client.describe_images(Filters=[{'Name': 'name', 'Values': [name+'-'+date]}])
    ami_id = ami['Images'][0]['ImageId']
    print ami_id
    ec2.create_tags(Resources = [ami_id], Tags = [{'Key': 'Name', 'Value': name}])

def search_id(name):
    instances = client.describe_instances()
    for instance in instances['Reservations']:
        for id in instance['Instances']:
            if name == id['Tags'][0]['Value']:
                name = id['InstanceId']
                return name
                print
            else:
                break

def main():
    InstanceName = raw_input('Enter Instance name: ')
    InstanceId = search_id(InstanceName)
    date = datetime.date.today().strftime('%Y-%m-%d')
    create_ami(InstanceName, date, InstanceId)
    print 'Images created           ', InstanceName+'-'+date
    print 'Instance deleted         ', InstanceName

if __name__ == '__main__':
    main()