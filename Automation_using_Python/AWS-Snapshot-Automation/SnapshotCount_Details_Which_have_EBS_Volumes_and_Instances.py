from functools import cmp_to_key
import boto3

# connection to aws ec2 service by using boto3
client=boto3.client('ec2')
snapshot=client.describe_snapshots(OwnerIds=['205008539362'])

#snapshotDetails:- In this dictionary key is volumeId which is attached to snapshot and value is how many snapshot contain these volumeId
snapshotDetails={}
output=[]
output2=[]
startBody='''<!DOCTYPE html>
<html>
<body>
<h2>Snapshot Details, Which have EBS Volumes and Instances</h2>
<table style="width:100%">'''
headingFirst='''
<tr>
    <th align="left">{0}</th>
    <th align="left">{1}</th>
    <th align="left">{2}</th>
    <th align="left">{3}</th>
  </tr>
'''
enterFirstHeadingRows='''
      <tr>
        <td>{0}</td>
        <td>{1}</td>
        <td>{2}</td>
        <td>{3}</td>
      </tr>
'''
startBodySecond='''
</table>
<h3>Snapshot Details, Which do not  have EBS Volume and Instance</h3>
<table style="width:100%">
'''

headingSecond='''
<tr>
    <th align="left">{0}</th>
    <th align="left">{1}</th>
  </tr>
'''
enterSecondHeadingRows='''
<tr>
  <td>{0}</td>
  <td>{1}</td>
 </tr>
'''
endHtmlFile='''
</table>
</body>
</html>
'''

# This below function is used for comparing snapshot count for two different volumeIDs
def compareSnapshotCount(a,b):
    if a['NumberOfSnapshot']==b['NumberOfSnapshot']:
        return 0
    elif a['NumberOfSnapshot'] > b['NumberOfSnapshot']:
        return 1
    else:
        return -1


#With the help of this function you can get all available volumes in your aws account in a particular region
def currentVolumeIds():
    temp=set()
    response = client.describe_volumes()
    for vid in response['Volumes']:
        temp.add(vid['VolumeId'])
    return temp

#With the help of thi s funciton, you can get instance name by using instance id
def getInstanceName(iid):
    response=client.describe_instances(InstanceIds=iid.split())
    for elem in response['Reservations']:
        for i in elem['Instances']:
            for j in i['Tags']:
                if j['Key'] == "Name":
                    return j['Value']

#In this function we are using snapshotDetails dictionary for creating information about number NumberOfSnapshot:VolumeId:InstanceId:InstanceName
def volumeDetailsBySnapshot():
    allVolumeId=set(snapshotDetails.keys())
    presentVolumeId=currentVolumeIds()
    notPresentVolumeId=allVolumeId.difference(presentVolumeId)
    response = client.describe_volumes(VolumeIds=list(presentVolumeId))
    countVolume=0
    countattach=0
    total=0
    for elem in response['Volumes']:
        temp={}
        if elem['VolumeId'] in snapshotDetails:
            for attach in elem['Attachments']:
                temp['InstanceId']=attach['InstanceId']
                temp['InstanceName']=getInstanceName(attach['InstanceId'])
                temp['NumberOfSnapshot']=snapshotDetails[elem['VolumeId']]
                temp['VolumeId']=attach['VolumeId']
                output.append(temp)
    for elem in notPresentVolumeId:
        temp={}
        temp['NumberOfSnapshot']=snapshotDetails[elem]
        temp['VolumeId']=elem
        output2.append(temp)

def retrievingInforamationAboutSnapshotAndVolumeId():
    for element in snapshot['Snapshots']:
        snapshotDetails[element['VolumeId']] = snapshotDetails.get(element['VolumeId'],0)+1
    volumeDetailsBySnapshot()

if __name__ == "__main__":
    retrievingInforamationAboutSnapshotAndVolumeId( )
    output=sorted(output,key=cmp_to_key(compareSnapshotCount),reverse=True)
    output2=sorted(output2,key=cmp_to_key(compareSnapshotCount),reverse=True)
    with open('output.html',mode='w') as f:
        f.write(startBody)
        f.write(headingFirst.format("NumberOfSnapshot","VolumeId","InstanceId","InstanceName"))
    with open('output.html',mode='a') as f:
        for i in output:
            f.write(enterFirstHeadingRows.format(i['NumberOfSnapshot'],i['VolumeId'],i['InstanceId'],i['InstanceName']))
        f.write(startBodySecond)
        f.write(headingSecond.format("NumberOfSnapshot","VolumeId"))
        for i in output2:
            f.write(enterSecondHeadingRows.format(i['NumberOfSnapshot'],i['VolumeId']))
        f.write(endHtmlFile)
