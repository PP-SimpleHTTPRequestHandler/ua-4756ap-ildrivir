import json
from http.server import HTTPServer, BaseHTTPRequestHandler

from exceptions import InvalidData, UserNotFound, UserExists
from schema import PUT_REQUIRED_FIELDS, REQUIRED_FIELDS, USERS_LIST

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_response(self, status_code=200, body=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body if body else {}).encode('utf-8'))

    def _pars_body(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        return json.loads(self.rfile.read(content_length).decode('utf-8'))  # <--- Gets the data itself

    @staticmethod
    def _default_user():
        return {
            "id": 1,
            "username": "theUser",
            "firstName": "John",
            "lastName": "James",
            "email": "john@email.com",
            "password": "12345",
        }

    @staticmethod
    def _get_user(username):
        for u in USERS_LIST:
            if u["username"] == username:
                return u

        raise UserNotFound

    @staticmethod
    def _get_user_by_id(user_id):
        for u in USERS_LIST:
            if u["id"] == user_id:
                return u

        raise UserNotFound

    @staticmethod
    def _validate_data(data, fields=None):
        if fields is None:
            fields = REQUIRED_FIELDS
        if not isinstance(data, dict):
            raise InvalidData
        for k, v in fields.items():
            if k not in data or not isinstance(data[k], v):
                raise InvalidData

    def do_GET(self):
        parts = self.path.strip('/').split('/')
        try:
            if parts[0] == 'reset':
                USERS_LIST.clear()
                USERS_LIST.append(self._default_user())
                self._set_response(200)

            elif parts[0] == 'users':
                self._set_response(200, USERS_LIST)

            elif parts[0] == 'user':
                username = parts[1]
                self._set_response(200, self._get_user(username))

        except UserNotFound:
            self._set_response(400, {'error': 'User not found'})

        except Exception as e:
            self._set_response(500, {'error': f"Internal server error: {e}"})

    def do_POST(self):
        parts = self.path.strip('/').split('/')
        try:
            data = self._pars_body()

            if parts == ['user']:
                self._validate_data(data)
                if any(
                        u['id'] == data['id'] for u in USERS_LIST
                ):
                    raise UserExists

                USERS_LIST.append(data)
                self._set_response(201, data)

            elif parts == ['user', 'createWithList']:
                if not isinstance(data, list):
                    raise InvalidData

                for item in data:
                    self._validate_data(item)

                existing_ids = {u['id'] for u in USERS_LIST}

                if any(item['id'] in existing_ids for item in data):
                    raise UserExists

                USERS_LIST.extend(data)
                self._set_response(201, data)

        except (UserExists, InvalidData):
            self._set_response(400, {})

        except Exception as e:
            self._set_response(500, {'error': f"Internal server error: {e}"})

    def do_PUT(self):
        parts = self.path.strip('/').split('/')
        try:
            if parts[0] == 'user':
                user_id = int(parts[1])
                data = self._pars_body()
                self._validate_data(data, PUT_REQUIRED_FIELDS)
                user = self._get_user_by_id(user_id)
                user.update(data)
                self._set_response(200, user)

        except InvalidData:
            self._set_response(400, {"error": "not valid request data"})
        except UserNotFound:
            self._set_response(404, {"error": "User not found"})

        except Exception as e:
            self._set_response(500, {"error": f"Internal server error: {e}"})

    def do_DELETE(self):
        parts = self.path.strip('/').split('/')
        try:
            if parts[0] == 'user':
                user_id = int(parts[1])
                user = self._get_user_by_id(user_id)
                USERS_LIST.remove(user)
                self._set_response(200, {})

        except UserNotFound:
            self._set_response(404, {"error": "User not found"})


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, host='localhost', port=8000):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
