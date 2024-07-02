#!/usr/bin/env python3

import subprocess
import yaml
import os
import sys
import atexit
import time
import re
import pathlib

# os.chdir('/Users/zhangsihao/go/src/github.com/bangwork/bang-api')

config_path = pathlib.Path('~/.onesdev').expanduser()
manifest = None
config = None


def select_env():
    envs = subprocess.getoutput("kubectl --context dev get ns --no-headers -lonesdev|awk '{print $1}'").split('\n')
    print('Env list:')
    for env in envs:
        print('  ' + env)
    env = input('Input your choice: ')
    if env not in envs:
        print('Invalid env')
        exit(127)
    config['env'] = env


def save_config():
    with config_path.open('w') as f:
        yaml.dump(config, f)


def init_kubeconfig():
    user_cert = '/tmp/onesdev_user_cert'
    user_key = '/tmp/onesdev_user_key'
    with open(user_cert, 'w') as f:
        f.write('''-----BEGIN CERTIFICATE-----
MIIBkjCCATegAwIBAgIIJNaaR/qCR+owCgYIKoZIzj0EAwIwIzEhMB8GA1UEAwwY
azNzLWNsaWVudC1jYUAxNzE4NzkyNDc4MB4XDTI0MDYxOTEwMjExOFoXDTI1MDYx
OTEwMjExOFowMDEXMBUGA1UEChMOc3lzdGVtOm1hc3RlcnMxFTATBgNVBAMTDHN5
c3RlbTphZG1pbjBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABORCSYxMbE1qZGKE
dIYAKwcUAHPJqLCSQgsC7Ii6s31LnbSZ8Dz3fmIJHtqOpCNvaKIgPTTONtScJBXF
208irhmjSDBGMA4GA1UdDwEB/wQEAwIFoDATBgNVHSUEDDAKBggrBgEFBQcDAjAf
BgNVHSMEGDAWgBRA4mN7gBwsZ2aGT3huzhCrRsQvfTAKBggqhkjOPQQDAgNJADBG
AiEAlwtophysXk8Ah3YYLRupguBjSK/63akwaoaQc7T1kQUCIQCfZ+uWbRUj+OpB
SI1ubZ/KhIXS7dQA4L3O8w95nxzIZA==
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIBeDCCAR2gAwIBAgIBADAKBggqhkjOPQQDAjAjMSEwHwYDVQQDDBhrM3MtY2xp
ZW50LWNhQDE3MTg3OTI0NzgwHhcNMjQwNjE5MTAyMTE4WhcNMzQwNjE3MTAyMTE4
WjAjMSEwHwYDVQQDDBhrM3MtY2xpZW50LWNhQDE3MTg3OTI0NzgwWTATBgcqhkjO
PQIBBggqhkjOPQMBBwNCAAS1jwXWV6XoNtyXUYZSA4EiJC8LkUSPyq+qzj2zoZqH
1983rMrFT2qwoiNFjYZ1/kkTM2imQNVzJPBX+A/ZDLFEo0IwQDAOBgNVHQ8BAf8E
BAMCAqQwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUQOJje4AcLGdmhk94bs4Q
q0bEL30wCgYIKoZIzj0EAwIDSQAwRgIhAM+bQ6sX4grPUgWCTxBkIqLy/4xw8X1S
wqtVcWJJ+O02AiEA92PDAHMYKlkCfsRsZEf4AVX4ozWBdftXW4zrHlo4N4I=
-----END CERTIFICATE-----
''')
    with open(user_key, 'w') as f:
        f.write('''
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIPhAMSO7WHZvaZEOW7yupacNrOzSUty0ZMfAvrmBPfwOoAoGCCqGSM49
AwEHoUQDQgAE5EJJjExsTWpkYoR0hgArBxQAc8mosJJCCwLsiLqzfUudtJnwPPd+
Ygke2o6kI29ooiA9NM421JwkFcXbTyKuGQ==
-----END EC PRIVATE KEY-----
''')
    subprocess.run('kubectl config set-cluster dev --server=https://k3s.dev.local:6443 --insecure-skip-tls-verify=true',
                   shell=True)
    subprocess.run('kubectl config set-credentials dev --embed-certs=true --client-certificate=%s --client-key=%s' % (
    user_cert, user_key), shell=True)
    subprocess.run('kubectl config set-context dev --cluster=dev --user=dev', shell=True)
    os.unlink(user_cert)
    os.unlink(user_key)


def check_context():
    contexts = subprocess.getoutput("kubectl config get-contexts --no-headers|awk '{print $2}'").split('\n')
    if 'dev' not in contexts:
        init_kubeconfig()


check_context()

if os.access('okteto.yml', os.R_OK):
    with open('okteto.yml') as f:
        manifest = yaml.load(f, Loader=yaml.FullLoader)

if config_path.exists():
    with config_path.open() as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
else:
    print('config file not found, initializing...')
    config = {}
    select_env()
    save_config()

env = config['env']


def build_context_args():
    return {
        'context': 'dev',
        'namespace': env,
    }


def args_to_cli(args):
    parts = []
    for k, v in args.items():
        parts.append('--%s' % k)
        if v is not None:
            parts.append(v)
    return ' '.join(parts)


def print_menu():
    print('------------ ONES Remote Tools ------------')
    print('Current env: %s' % env)
    print('Usage: remote.py <command> [args...]')
    if manifest is None:
        print(
            'You must have okteto.yml in current directory to use dev commands. (Maybe you\'re not in project directory)')
    print('Available commands:')
    print('  env: select environment')
    if manifest is not None:
        print('  start: start remote development environment')
        print('  stop: stop remote development environment')
    print('  mysql: connect to mysql')
    print('  redis: connect to redis')
    print('------------ ONES Remote Tools ------------')


def print_banner():
    print('------------ ONES Remote Tools ------------')
    print('Current env: %s' % env)
    print('------------ ONES Remote Tools ------------')


def start_okteto(args, ide_starter):
    print_banner()
    ssh_host = manifest['name'] + '.okteto'
    for k, v in manifest['dev'].items():
        if 'workdir' in v:
            workdir = v['workdir']
            print('found workdir %s in container %s' % (workdir, k))
            break

    ssh_port = 23012
    okteto = subprocess.Popen('okteto up --remote {port} {args}'.format(port=ssh_port, args=args),
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    def exit_hook():
        if okteto is not None:
            okteto.kill()
            print('okteto killed')

    atexit.register(exit_hook)

    ide_opened = False

    sys.stdout.write('\r')
    while okteto.poll() is None:
        line = ''
        if okteto.stdout.readable():
            try:
                c = okteto.stdout.read1()
            except:
                break
            s = c.decode('utf-8')
            sys.stdout.write(s.replace('\n', '\r\n'))
            s = s.replace('\r', '')
            line += s
            if not ide_opened and line.endswith('# ') and 'root@' in line:
                ide_starter(ssh_host, ssh_port, workdir)
                ide_opened = True
            if '\n' in line:
                line = line.split('\n')[-1]
        else:
            time.sleep(0.1)


def start_vscode(ssh_host, ssh_port, workdir):
    subprocess.run(
        'open -n -a "Visual Studio Code" --args --folder-uri vscode-remote://ssh-remote+{host}:{port}{workdir}'.format(
            host=ssh_host, port=ssh_port, workdir=workdir), shell=True)


def stop_okteto(args):
    print_banner()
    subprocess.run('okteto down %s' % (args), shell=True)


def run_mysql_cli():
    print_banner()
    p = subprocess.getoutput('kubectl -n op exec deploy/{env} -it -- cat config/private.yaml'.format(env=env))
    pwd = re.search(r'mysqlRootPassword: ["\']?(.*)["\']?', p)
    if not pwd:
        print('mysqlRootPassword not found')
        exit(127)
    pwd = pwd.group(1).strip('\'"')
    subprocess.run('kubectl {args} exec -it mysql-cluster-mysql-0 -- mysql -uroot -p{password}'.format(
        args=args_to_cli(build_context_args()), password=pwd), shell=True)


def run_redis_cli():
    print_banner()
    subprocess.run(
        'kubectl {args} exec -it stable-redis-master-0 -- redis-cli'.format(args=args_to_cli(build_context_args())),
        shell=True)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_menu()
        sys.exit(1)

    command = sys.argv[1]
    if command == 'start':
        start_okteto(args_to_cli(build_context_args()), start_vscode)
    elif command == 'stop':
        stop_okteto(args_to_cli(build_context_args()))
    elif command == 'mysql':
        run_mysql_cli()
    elif command == 'redis':
        run_redis_cli()
    elif command == 'env':
        select_env()
        save_config()
    else:
        print_menu()
        sys.exit(1)
