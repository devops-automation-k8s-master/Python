#Users Which is not present in any group or users which has directly attached permission
    import boto3

    client=boto3.client('iam')
    all_users_data=client.list_users()
    all_users_name=[]
    for uname in all_users_data['Users']:
        all_users_name.append(uname['UserName'])
    print(all_users_name)

    for user in all_users_name:
        all_direct_attached_policy=client.list_attached_user_policies(UserName=user)
        if len(all_direct_attached_policy['AttachedPolicies'])!=0:
            print("These all are directly attached policy of the user={0}\n".format(user))
            for policy in all_direct_attached_policy['AttachedPolicies']:
                print(policy['PolicyName'])
