from functools import cmp_to_key

import boto3
client=boto3.client('ec2')
DetailsOfSnapshot=[]
totalSnapshot=0

def compareSnapshotCount(a,b):
    if a['count']==b['count']:
        return 0
    elif a['count'] > b['count']:
        return 1
    else:
        return -1

def listOfSnapshot(filterList):
    count=0
    snapshots = client.describe_snapshots(Filters=filterList)
    for i in snapshots['Snapshots']:
        #print(i['SnapshotId'])
        count=count+1
    return count
    # print("NumberOfSnapshot={0}".format(count))
def instanceName(instanceId):
    pass


def createFilterForSnapshot(volumeID):
    d={}
    volumeList=[]
    filterList=[]
    volumeList.append(volumeID)
    d['Values']=volumeList
    d['Name']='volume-id'
    filterList.append(d)
    # print(filterList)
    return filterList

def listofAllVolumes():
    instanceId=""
    totalSnapshot=0
    response = client.describe_volumes()
    for i in response['Volumes']:
        temp={}
        volumeID=i['VolumeId']
        #print("this is VolumeID:={0}".format(volumeID))
        count=listOfSnapshot(createFilterForSnapshot(volumeID))
        totalSnapshot+=count
        if i['Attachments']:
            instanceId=i['Attachments'][0]['InstanceId']
        else:
            instanceId=""
        temp['volumeID']=volumeID
        temp['instanceId']=instanceId
        temp['count']=count
        if count!=0:
            DetailsOfSnapshot.append(temp)
    print(totalSnapshot)
        # print("volumeid={0}\n InstanceId={1} \n NumberOfSnapshot={2}".format(volumeID,instanceId,count))
        # print("***********************************************")

if __name__ == "__main__":
    listofAllVolumes()
    print(DetailsOfSnapshot)
    d=sorted(DetailsOfSnapshot,key=cmp_to_key(compareSnapshotCount))

    for i in d:
        print(i)
    print(totalSnapshot)





# volume-id:{count:0,NameOfserver:name}
#print volumeId,Number of snapshot for that volumeID,List all snapshotsID
# ec2 instance attach to Volume
