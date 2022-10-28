# This Script is used for, Add/Remove access in metabase for all oncall Users(pagerduty oncall users)
from pdpyras import APISession
import json
import requests
import boto3
import base64
#Fill Metabase Url
BASE_API_LINK=''

def get_secret(secret_name):
    #secret_name = "pagerduty-token"
    region_name = "us-east-1"
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
                return get_secret_value_response['SecretString']
        else:
            return  base64.b64decode(get_secret_value_response['SecretBinary'])

def getEscalationPolicyIDs(session):
    esPolicyIDS=[]
    response = session.get("/escalation_policies?limit=100")
    for esID in response.json()['escalation_policies']:
        esPolicyIDS.append(esID['id'])
    return esPolicyIDS

def getUserEmailID(session,userID):
    response = session.get("/users/{}".format(userID))
    return response.json()['user']['email']

def getLevelOneOncallUserIDUsingEscalationPolicyID(session,escalation_policy_id):
    response = session.get("/oncalls?escalation_policy_ids[]={}".format(escalation_policy_id))
    for escalation_policy in response.json()['oncalls']:
        if escalation_policy['escalation_level'] == 1:
            uid=escalation_policy['user']['id']
            return uid
            
def login(username, password):
	session = requests.Session()
	req = session.post(BASE_API_LINK + '/api/session', json={
		'username': username,
		'password': password
	}, headers={
		'Content-Type': 'application/json'
	})
	return session

def getUserID(session,emailAddress):
  req = session.get(BASE_API_LINK + '/api/user?include_deactivated=true')
  data = req.json()
  for user_info in data:
        if user_info['email'] ==  emailAddress:
            return user_info['id']
  return -1

def getUser(session, userId):
	req = session.get(BASE_API_LINK + '/api/user/{}'.format(userId))
	return req.json()

def addUserInGroup(session, userId, groupId):
	user = getUser(session, userId)
	newGroupIds = list(set(user['group_ids'] + [groupId]))
	data = {
		'first_name': user['first_name'],
		'last_name': user['last_name'],
		'email': user['email'],
		'group_ids': newGroupIds,
		'login_attributes': user['login_attributes']
	}
	return session.put(BASE_API_LINK + '/api/user/{}'.format(userId), json=data, headers={
		'Content-Type': 'application/json'
	})

def removeUserFromGroup(session, userId, groupId):
	user = getUser(session, userId)
	newGroupIds = list(user['group_ids'])
	if groupId in newGroupIds:
		newGroupIds.remove(groupId)
	data = {
		'first_name': user['first_name'],
		'last_name': user['last_name'],
		'email': user['email'],
		'group_ids': newGroupIds,
		'login_attributes': user['login_attributes']
	}
	return session.put(BASE_API_LINK + '/api/user/{}'.format(userId), json=data, headers={
		'Content-Type': 'application/json'
	})

def lambda_handler(event, context):
    username = json.loads(get_secret('metabase-user-name'))['metabase-user-name']
    password = json.loads(get_secret('metabase-password'))['metabase-password']
    GroupId  = 4
    sessionPagerDuty = APISession(json.loads(get_secret('pagerduty-token'))['pagerduty-token'])
    sessionMetabase = login(username, password)
    esPolicyIDS=getEscalationPolicyIDs(sessionPagerDuty)
    print(esPolicyIDS)
    for espid in esPolicyIDS:
        userId = getUserID(sessionMetabase,getUserEmailID(sessionPagerDuty,getLevelOneOncallUserIDUsingEscalationPolicyID(sessionPagerDuty,espid)))
        if userId != -1:
            result = addUserInGroup(sessionnMetabase, userId, GroupId)
        else:
            result = "userNotFound"
        print(result)
