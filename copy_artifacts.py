import os
import json
import shutil
import hashlib
import datetime
import subprocess

''' base url: https://raw.githubusercontent.com/masknetgoal634/nearcore-deploy/master/ '''

''' 
nearcore-deploy/{net}/genesis_md5sum 
''' 
def save_genesis_md5sum(dest_dir):
    local_genesis_md5sum = hashlib.md5(
        open(os.path.join(os.path.join(dest_dir, 'genesis.json')),
             'rb').read()).hexdigest()
    with open(f'{dest_dir}/genesis_md5sum', 'w') as the_file:
        the_file.write(local_genesis_md5sum)


''' 
nearcore-deploy/{net}/genesis_time
nearcore-deploy/{net}/protocol_version 
'''
def save_protocol_ver_and_time(dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    filename = f'{dest_dir}/genesis.json'
    genesis_config = json.load(open(filename))
    genesis_time = genesis_config['genesis_time']
    protocol_version = genesis_config['protocol_version']
    with open(f'{dest_dir}/genesis_time', 'w') as the_file:
        the_file.write(datetime.datetime.strptime(genesis_time, '%Y-%m-%dT%H:%M:%SZ').isoformat())
    with open(f'{dest_dir}/protocol_version', 'w') as the_file:
        the_file.write(str(protocol_version))


''' 
nearcore-deploy/{net}/latest_deploy_at 
time format YYYYMMDD_HHMMSS
'''
def save_latest_deploy_time(dest_dir):
    with open(f'{dest_dir}/latest_deploy_at', 'w') as the_file:
        time_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        the_file.write(time_now)


''' 
nearcore-deploy/{net}/latest_deploy 
'''
def get_latest_deploy_hash(nearcore_path, dest_dir):
    last_commit_hash = subprocess.Popen([f'cd {nearcore_path} && git rev-parse HEAD'], stdout=subprocess.PIPE, shell = True).communicate()[0].decode("utf-8").replace("\n", "")
    with open(f'{dest_dir}/latest_deploy', 'w') as the_file:
        the_file.write(last_commit_hash)
    return last_commit_hash


def get_current_branch(nearcore_path):
    return subprocess.Popen([f'cd {nearcore_path} && git rev-parse --abbrev-ref HEAD'], stdout=subprocess.PIPE, shell = True).communicate()[0].decode("utf-8").replace("\n", "")


'''
nearcore/Linux/{net_to_branch(net)}/{latest_deploy_version}/near
nearcore/Linux/{net_to_branch(net)}/{latest_deploy_version}/keypair-generator
nearcore/Linux/{net_to_branch(net)}/{latest_deploy_version}/genesis-csv-to-json
'''
def copy_binaries(build_dir, file_names, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for fname in file_names:
        if os.path.exists(f'{dest_dir}/{fname}'):
            os.remove(f'{dest_dir}/{fname}')
        shutil.copyfile(f'{build_dir}/{fname}', f'{dest_dir}/{fname}')


if __name__ == '__main__':
    net = 'guildnet'

    nearcore_path = 'nearcore'
    dest_dir = f'nearcore-deploy/nearcore-deploy/{net}/'

    save_protocol_ver_and_time(dest_dir)
    save_latest_deploy_time(dest_dir)
    save_genesis_md5sum(dest_dir)
    get_latest_deploy_hash(nearcore_path, dest_dir)

    build_dir = f'{nearcore_path}/target/release'
    src_files = ['near', 'keypair-generator', 'genesis-csv-to-json']
    dest_dir = f'nearcore-deploy/nearcore/Linux/{get_current_branch(nearcore_path)}/{get_latest_deploy_hash(nearcore_path,dest_dir)}/'

    copy_binaries(build_dir, src_files, dest_dir)