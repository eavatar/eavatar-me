#
# Check GMail every 1 minute
#
# Replace 'username@gmail.com' and 'password' with real GMail account's login ID and
# password.

last_unseen = 0

for it in ava.schedule.every(1).minute:
    check_task = ava.do('imap.check_gmail',
                        username='username@gmail.com',
                        password='password')

    messages, unseen = check_task.result()
    if unseen > 0 and unseen != last_unseen:
        last_unseen = unseen
        ava.do('user.notify',
               message="You got %d new messages." % unseen,
               title="You Got Mails from GMail")

