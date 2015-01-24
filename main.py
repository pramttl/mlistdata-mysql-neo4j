from subprocess import Popen, PIPE

p = Popen(['python', 'migrate_mailing_lists_people.py'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
output = p.stdout.read()
p.stdin.write(raw_input())

p = Popen(['python', 'python migrate_messages.py'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
output = p.stdout.read()
p.stdin.write(raw_input())
