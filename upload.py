import subprocess

with open('results.txt') as f:
    rs = f.read().split('\n')

for r in rs:
    subprocess.run(["aws", "s3", "cp", r, "s3://mathpresso-rnd"])

