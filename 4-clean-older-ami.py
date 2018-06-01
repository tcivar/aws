import boto3
import time
import dateutil.parser

session = boto3.Session()
ec2 = session.resource('ec2')
client = session.client('ec2')

def clean_ami(name, day):
    ami = client.describe_images(Filters=[{'Name': 'tag:Name', 'Values': [name]}])
    current_time = time.time()
    print 'Current epoch date                   ', current_time
    cutoff = current_time - (day * 86400)
    print 'Date before delete all ami           ', cutoff
    print
    for i in ami['Images']:
        ami_date = i['CreationDate']
        image_id = i['ImageId']
        images_date = dateutil.parser.parse(ami_date)
        images_date = images_date.strftime('%s')
        print 'Images  epoch date                   ', images_date
        print 'Image Id                             ', image_id
        if float(images_date) < cutoff:
            client.deregister_image(ImageId = image_id)

def main():
    #name = 'Tag-name'
    #day = 7
    name = raw_input('Enter Tag name Images: ')
    day = int(raw_input('Enter date before delete: '))
    print 'Tag name Images                      ', name
    print 'day before delete                    ', day
    clean_ami(name, day)

if __name__ == '__main__':
    main()



