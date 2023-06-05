import json
import os
import subprocess
import socket
import re
from argparse import ArgumentParser

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('--host', type=str, default='')
    parser.add_argument('--port', type=int, default=17171)
    parser.add_argument('--n_conn', type=int, default=8)
    parser.add_argument('--frontend_dir', type=str, default='./frontend')
    parser.add_argument('--backend_dir', type=str, default='./backend')
    args, unknown = parser.parse_known_args()
    return args

def create_server(host, port, n_conn):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.settimeout(None)
    server.bind((host, port))
    server.listen(n_conn)

    return server

def http_error(client):
    client.close()
    return

def get_frontend_filenames(frontend_dir, filename):
    if filename == '':
        filename = 'index.html'
        content_type = 'text/html'
    elif filename.endswith('.css'):
        content_type = 'text/css'
    elif filename.endswith('.js'):
        content_type = 'text/javascript'

    file_path = os.path.join(frontend_dir, filename)
    with open(file_path, 'r') as f:
        content = f.read()
    
    header = 'HTTP/1.1 200 OK\n'+ 'Content-Type: '+ str(content_type)+ '\n\n'
    
    return header + content

def re_search(pattern, string, n_group):
    result = list()
    match = re.search(pattern, string , re.I|re.M)
    if match is not None:
        for i in range(n_group):
            result.append(match.group(i + 1))

    return result
        
# TODO
def handle_login(username, password, backend_dir):
    script_path = os.path.join(backend_dir, 'login.sh')
    output = subprocess.check_output(['bash', script_path, username, password]).decode().split('count(*)')[-1].strip('\n')
    
    if output != "1": return 'unauthorized'

    script_path = os.path.join(backend_dir, 'query_group.sh')
    output = subprocess.check_output(['bash', script_path, username]).decode().split('groupname')[-1].strip('\n')
    print(output)

    return output

# TODO
def handle_update_password(username, password, new_password, backend_dir):
    script_path = os.path.join(backend_dir, 'login.sh')
    output = subprocess.check_output(['bash', script_path, username, password]).decode().split('count(*)')[-1].strip('\n')
    print(username, password, new_password, output)
    if output != "1":
        return False
    
    script_path = os.path.join(backend_dir, 'update_password.sh')
    output = subprocess.check_output(['bash', script_path, username, password, new_password]).decode().strip('\n')
    
    return True

def handle_upd_time_interval(time_interval, backend_dir):
    script_path = os.path.join(backend_dir, 'update_time_interval.sh')
    output = subprocess.check_output(['bash', script_path, f'Al{time_interval}']).decode().strip('\n')
    
    return True

def handle_req(client, frontend_dir, backend_dir):
    req = client.recv(1024).decode()

    parsed_req = req.split(' ')
    method = parsed_req[0]
    
    if method == 'GET':
        filename = parsed_req[1].lstrip('/')

        if filename == '' or filename.endswith('.css') or filename.endswith('.js'):
            res = get_frontend_filenames(frontend_dir, filename).encode()
        elif filename.endswith('.ico'):
            res = 'HTTP/1.1 200 OK\n'.encode()
        else:
            http_error(client)
            return
    elif method == 'POST':
        match_result = re_search('"api_name":"([a-z_]*)"', req, 1)
        if len(match_result) != 1:
            http_error(client)
            return
        api = match_result[0]

        if api == 'login':
            match_result = re_search('"username":"(.*)","password":"(.*)"}', req, 2)
            if len(match_result) != 2:
                http_error(client)
                return
            username, password = match_result[0], match_result[1]

            group = handle_login(username, password, backend_dir)
            if group == 'teachers' or group == 'students':
                content = json.dumps({'group': group})
                res = f'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{content}\n\n'.encode()
            else:
                res = 'HTTP/1.1 401 Unauthorized\n'.encode()
                print('Wrong password')
        elif api == 'update_password':
            match_result = re_search('"username":"(.*)","password":"(.*)","new_password":"(.*)"}', req, 3)
            if len(match_result) != 3:
                http_error(client)
                return
            username, password, new_password = match_result[0], match_result[1], match_result[2]

            upd_success = handle_update_password(username, password, new_password, backend_dir)
            if upd_success:
                res = 'HTTP/1.1 200 OK\n'.encode()
            else:
                res = 'HTTP/1.1 401 Unauthorized\n'.encode()
                print('Update password error')
        elif api == 'upd_time_interval':
            match_result = re_search('"time_interval":"(.*)"}', req, 1)
            if len(match_result) != 1:
                http_error(client)
                return
            time_interval = match_result[0]

            if handle_upd_time_interval(time_interval, backend_dir):
                res = 'HTTP/1.1 200 OK\n'.encode()
            else:
                res = 'HTTP/1.1 409 Conflict\n'.encode()
        else:
            http_error(client)
            return
        
    elif method == 'OPTIONS':
        res = 'HTTP/1.1 200 OK\n'.encode()
    else:
        http_error(client)
        return
    
    client.sendall(res)
    client.close()

    return

def main(args):
    server = create_server(args.host, args.port, args.n_conn)
    print('Server listening...')

    while True:
        client, addr = server.accept()

        try:
            handle_req(client, args.frontend_dir, args.backend_dir)
        except Exception as e:
            pass
    return

if __name__ == '__main__':
    main(parse_arguments())
