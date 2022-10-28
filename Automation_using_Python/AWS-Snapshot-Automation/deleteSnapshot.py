from functools import cmp_to_key
import boto3
import datetime
client=boto3.client('ec2')

snapshotCountByVolumeId={}
response=client.describe_volumes(Filters=[{'Name':'tag:snapshot_enable','Values':['yes']}])
volumesDetails=[]


# This below function is used for comparing snapshot count for two different volumeIDs
def compareSnapshotCount(a,b):
    if a['nofDays']==b['nofDays']:
        return 0
    elif a['nofDays'] > b['nofDays']:
        return 1
    else:
        return -1

def noOfDaysCalculator(date):
    today=datetime.date.today()


def deleteSnapshot(snList,retentionDays):
    if( int(retentionDays)< len(snList)):
        for i in range(int(retentionDays),len(snList)):
            print("Below are the snapshots Going to delete:\n snapshot=Id{0}\tDays={1}\n".format(snList[i]['sId'],snList[i]['nofDays']))

            #response = client.delete_snapshot(SnapshotId=snList[i]['sId'],DryRun=False)
    else:
        print("not goint to delete, this is inbound")
        for i in snList:
            print(i['sId'])


def snapshotListsOfDelete(volumeId,retentionDays):
    searchSnapshot={}
    searchSnapshot['Name']='volume-id'
    l=[]
    m=[]
    l.append(volumeId)
    searchSnapshot['Values']=l
    m.append(searchSnapshot)
    snapshot=client.describe_snapshots(Filters=m,OwnerIds=['205008539362'])
    fl=[]
    fd={}

    for i in snapshot['Snapshots']:
        fd={}
        fd['sId']=i['SnapshotId']
        fd['nofDays']=(datetime.date.today() -i['StartTime'].date()).days
        fl.append(fd)
        print(i['VolumeId'])
        print((datetime.date.today() -i['StartTime'].date()).days)
    fl=output=sorted(fl,key=cmp_to_key(compareSnapshotCount))
    deleteSnapshot(fl,retentionDays)

def snapshotCountByVolumeIdRetrieve():
    snapshot=client.describe_snapshots(OwnerIds=['205008539362'])
    for i in snapshot['Snapshots']:
        snapshotCountByVolumeId[i['VolumeId']]=snapshotCountByVolumeId.get(i['VolumeId'],0)+1

for elem in response['Volumes']:
    volumeData={}
    volumeId=elem['VolumeId']
    print(elem['VolumeId'])
    for i in elem['Tags']:
        #print(i)
         if i['Key']=='retention_days':
            retentionDays=i['Value']
            print(i['Value'])
            snapshotListsOfDelete(volumeId,retentionDays)
            break
