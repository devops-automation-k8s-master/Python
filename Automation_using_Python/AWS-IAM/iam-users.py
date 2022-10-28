import boto3
client = boto3.client('iam')
users = client.list_users()

dir(users)
for user_details in users['Users']:
    print(user_details['UserName'])

#list all custom managed policy

# custom_managed_policy=client.list_policies(Scope='local')
#
# for policy_name in custom_managed_policy['Policies']:
#     print(policy_name[])

#Direct attached policy to user
print("please enter the username")
uname=input()

a_policy=client.list_attached_user_policies(
    UserName=uname)
print("attached user policy which is directly managed by aws\n\n")
for policy_name in a_policy['AttachedPolicies']:
    print(policy_name)

#List all groups of Users
a_group=client.list_groups_for_user(UserName=uname)

print("*****all group name**********\n\n")
for gname in a_group['Groups']:
    print("group name of this user")
    print(gname['GroupName'])
#List group policy_name which is managed by customer
    gPolicy = client.list_group_policies(GroupName=gname['GroupName'])
    print("gPolicy which is managed by customer")
    for agp in gPolicy['PolicyNames']:
        print(agp)
    print("********all group attached policy managed by aws***********\n\n")
    gpolicymaws = client.list_attached_group_policies(GroupName=gname['GroupName'])
    # print(gpolicymaws)
    for pn in gpolicymaws['AttachedPolicies']:
        print(pn['PolicyName'])
