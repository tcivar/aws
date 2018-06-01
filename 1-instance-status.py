import boto3

session = boto3.Session()
ec2 = session.resource('ec2')
client = session.client('ec2')

def status_instance(IP, DNS):
    instances = client.describe_instances(Filters=[
        {
            'Name': 'network-interface.association.public-ip', 'Values': [IP]
        },
        {
            'Name': 'dns-name', 'Values': [DNS]
        }
    ]
    )
    if instances['Reservations'] == []:
        print 'instance not found'
    else:
        print 'Instance status               ', instances['Reservations'][0]['Instances'][0]['State']['Name']

def main():
    IP =  raw_input('Enter IP: ')
    DNS = raw_input('Enter DNS: ')
    print 'Instance IP                   ',IP
    print 'Instance DNS                  ',DNS
    status_instance(IP, DNS)

if __name__ == '__main__':
    main()