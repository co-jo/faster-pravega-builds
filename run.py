import subprocess
import os
import argparse
from tabulate import tabulate
import json
import re

from tinydb import TinyDB, Query, where
from tinydb.operations import increment

run = 0

database = 'db.json'
if os.path.exists(database):
    os. remove(database)
db = TinyDB(database)

def skipped(name, package):
    if db.search(where('name') == name and where('package') == package):
        db.update(increment('skipped'), where('name') == name and where('package') == package)
    else:
        db.insert({'package': package, 'name': name, 'skipped': 1, 'failed': 0})


def failed(name, package):
    if db.search(where('name') == name and where('package') == package):
        db.update(increment('failed'), where('name') == name and where('package') == package)
    else:
        db.insert({'package': package, 'name': name, 'skipped': 0, 'failed': 1})

def parse_package(output):
    # Line contains valid qualified package name.
    match = re.search('io.pravega(\.[a-zA-Z]+)+', output)
    if not match:
        return None
    return match.group(0)

def parse_test(output):
    match = re.search('(?<=\>\s)[a-zA-Z]*', output)
    if not match:
        return None
    return match.group(0)


def clear():
    # Clear line and advance up.
    print('\033[A\r\033[K', end = '')


def render(output, process):
    if process.poll() is not None:
        return False
    elif not output:
        return True

    package = parse_package(output)
    if not package:
        return True

    name = parse_test(output)
    if not name:
        return True
   

    status = 'SUCCESS'
    if 'FAILED' in output:
        status = 'FAILED'
        failed(name, package)
    elif 'SKIPPED' in output:
        status = 'SKIPPED'
        skipped(name, package)
    
    render_current(name, package, status)
    return True

def render_current(name, package, status):
    global run, args
    prefix = '(' + str(run) + '/' + str(args.retries) + ')'
    # Save cursor position and restore it.
    output = prefix + ' ' + package + ' • ' + name

    output += ' '
    if status == 'FAILED':
        output += '❌'
    elif status == 'SKIPPED':
        output += '⚠️'
    elif status == 'SUCCESS':
        output += '✔️'

    clear()
    print(output)
    

def render_failed():
    table = []
    headers = ['package', 'name', 'failed', 'skipped']
    for entry in db.all():
        table.append([entry['package'], entry['name'], entry['failed'], entry['skipped']])
    # Adjust cursor to after the 'current table'.
    output = tabulate(table, headers, tablefmt='fancy_grid')
    return output


parser = argparse.ArgumentParser(description="Pravega Test Runner.")
parser.add_argument("--src", default=os.getcwd() + "/pravega", help="The local Pravega project directory.")
parser.add_argument("--dst", default="/home/pravega", help="The directory to mount the project from within the image.")
parser.add_argument("--image", default="pravega", help="The name of the Pravega image to use.")
parser.add_argument("--memory", default=4, type=int, help="The amount of memory (in GB) to use.")
parser.add_argument("--cpus", default=os.cpu_count(), type=int, help="The number of cpus to use.")
parser.add_argument("--command", help="The file container the commands to run.")
parser.add_argument("--retries", default=2, type=int, help="The number of times to run the command.")

args=parser.parse_args()

def execution():
    process = subprocess.Popen([
        "docker", "run",
        "-t",
        "--mount",
        "type=bind,src={},dst={}".format(args.src, args.dst),
        "--memory", "{}g".format(args.memory),
        "--cpus", str(args.cpus),
        args.image,
        args.command
        ],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE)
    
    print('')
    while True:
        data = process.stdout.readline()
        output = data.decode('ascii').strip()
        if not render(output, process):
            process.kill()
            break
    print('')

for i in range(args.retries):
    run += 1
    execution()
    # Print results table and move cursor back.
    output = render_failed()
    print(output)
    if (i < args.retries - 1):
        print((output.count('\n') + 4) * '\033[A')

