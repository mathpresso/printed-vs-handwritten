import subprocess
for i in range(100, 1000):
    print(i)
    subprocess.run(["python", 'classify.py', f"/home/ec2-user/printed-vs-handwritten/lines/training/handwritten/{i}.png"])

