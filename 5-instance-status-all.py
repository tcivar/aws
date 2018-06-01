import boto3

session = boto3.Session()
ec2 = session.resource('ec2')
client = session.client('ec2')

def status_instance():
    instances = client.describe_instances()
    for instance in instances['Reservations']:
        for id in instance['Instances']:
            print "Name instance            ", id['Tags'][0]['Value']
            if id['State']['Name'] == 'terminated':
                print "Status instance          ", "\033[1;30m"+id['State']['Name']+"\033[m"
            else:
                print "Status instance          ", id['State']['Name']
            print


def main():
    status_instance()

if __name__ == '__main__':
    main()