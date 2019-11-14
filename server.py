import socket
import os


def process(request):
    global curr_dir
    global i

    req = request.split()

    if req[0] == 'help' and len(req) == 1:
        string = '{:^60}\n'.format('list of supported commands:'.upper())
        for k, v in help_box.items():
            string += '\n{:>33}'.format(k) + f' - {v}'
        return string

    elif req[0] == 'clear' and len(req) == 1:
        return '\n' * 60

    elif req[0] == 'pwd' and len(req) == 1:
        return curr_dir

    elif req[0] == 'ls' and len(req) == 1:
        return ', '.join(os.listdir(curr_dir))

    elif req[0] == 'cd' and len(req) == 2:
        directory_name = req[1]
        if os.path.isdir(os.path.join(curr_dir, directory_name)):
            curr_dir = os.path.join(curr_dir, directory_name)
            return ''
        return f'Directory <{directory_name}> does not exist'

    elif req[0] == 'mk' and len(req) == 2:
        filename = req[1]
        open(os.path.join(curr_dir, filename), 'a').close()
        return f'File <{filename}> created'

    elif req[0] == 'cat' and len(req) == 2:
        filename = req[1]
        if filename in os.listdir(curr_dir):
            with open(os.path.join(curr_dir, filename), 'r') as f:
                return f.read()
        return 'File is not exist'

    elif req[0] == 'nano' and len(req) > 2:
        filename = req[1]
        try:
            string = ''
            for i in range(2, len(req)):
                string += f'{req[i]} '
            with open(os.path.join(curr_dir, filename), 'w') as f:
                f.write(string)
            return f'File <{filename}> successfully changed!'
        except FileNotFoundError:
            return 'File not found'

    elif req[0] == 'mkdir' and len(req) == 2:
        filename = req[1]
        os.mkdir(os.path.join(curr_dir, filename))
        return f'Directory <{filename}> created'

    elif req[0] == 'rmdir' and len(req) == 2:
        directory = req[1]
        try:
            os.rmdir(os.path.join(curr_dir, directory))
            return f'Directory <{directory}> deleted'
        except FileNotFoundError:
            return 'Directory not found'

    elif req[0] == 'rm' and len(req) == 2:
        filename = req[1]
        try:
            os.remove(os.path.join(curr_dir, filename))
            return f'File <{filename}> deleted'
        except FileNotFoundError:
            return 'File not found'

    elif req[0] == 'rename' and len(req) == 3:
        filename, new_filename = req[1], req[2]
        try:
            os.rename(os.path.join(curr_dir, filename), os.path.join(curr_dir, new_filename))
            return f'File <{filename}> renamed to <{new_filename}>'
        except FileNotFoundError:
            return 'File not found'
        except FileExistsError:
            return 'A file with this name already exists'

    elif req[0] == 'toServer' and len(req) == 3:
        filename = req[1]
        size = int(req[2])
        request = b''
        while size:
            data = conn.recv(1024)
            if not data:
                break
            request += data
            size -= 1

        with open(os.path.join(curr_dir, filename), 'wb') as f:
            f.write(request)
        i += 1
        return 'The file sent to the server'

    return 'Bad request\n"help" for list of commands '


help_box = {
    'help': 'вызвать данное окно с подсказками',
    'clear': 'очистить консоль',
    'ls': 'посмотреть содержимое папки',
    'cd <directory_name>': 'перейти в директорию',
    'cd ..': 'перейти в директорию ниже',
    'mkdir <directory_name>': 'создать папку',
    'rmdir <directory_name>': 'удалить папку',
    'mk <filename>': 'создать файл',
    'nano <filename> <text>': 'записать <text> в файл',
    'rm <filename>': 'удалить файл',
    'rename <filename> <new_filename>': 'переименовать файл',
    'toServer <filename>': 'отправить файл на сервер'
}

port = 1234
sock = socket.socket()
sock.bind(('', port))
sock.listen(1)

curr_dir = os.path.join(os.getcwd(), 'docs')

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    response = process(request)
    conn.send(response.encode())
    conn.close()
