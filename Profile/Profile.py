def printUserProfile(user, db): # Requires Database and User object, will print out full profile.
    profileQueryString = '''
    SELECT *
    FROM profile
    WHERE username = ?
    '''
    jobQueryString = '''
    SELECT *
    FROM job_experience
    WHERE username = ?
    '''
    profileInformation = db.execute(profileQueryString, [user.username])
    jobInformation = db.execute(jobQueryString, [user.username])
    if len(profileInformation) < 1:
        return -1

    print_queue = []
    print_queue.append(user.firstname + ' ' + user.lastname + '\'s Profile')
    print_queue.append('Title: ' + profileInformation[0][0])
    print_queue.append('Major: ' + profileInformation[0][1])
    print_queue.append('University: ' + profileInformation[0][2])
    print_queue.append('Information and Education\n' + profileInformation[0][3] + ' ' + profileInformation[0][4])

    if len(jobInformation) > 0:
        print_queue.append('Job Experience')
        for job in jobInformation:
            print_queue.append('Title: ' + job[0])
            print_queue.append('Employer: ' + job[1])
            print_queue.append('Date Started: ' + job[2])
            print_queue.append('Date Ended: ' + job[3])
            print_queue.append("Location: " + job[4])
            print_queue.append('Job Description: \n' + job[5])

    for item in print_queue:
        print(item + '\n')

