from adjust_kubeconfig import get_server_public_ip

if __name__ == '__main__':
    env_name = 'release-6-1-0-k3s-8'
    url = f"https://{env_name}.k3s-dev.myones.net"
    print(get_server_public_ip(url))  #
