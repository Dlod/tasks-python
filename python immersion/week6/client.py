import socket
import time


class ClientError(Exception):
    """Общий класс исключений клиента"""
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        try:
            self.sock_connection = socket.create_connection((self.host, self.port), timeout=self.timeout)
        except socket.error as err:
            raise ClientError("error connect", err)

    def _read_answer(self):
        """Метод для чтения ответа сервера"""
        data = b""
        # читаем буфер
        while not data.endswith(b"\n\n"):
            try:
                data += self.sock_connection.recv(1024)
            except socket.error as err:
                raise ClientError("error recv data", err)

        # преобразовываем байткод в читаемый вид
        decoded_data = data.decode()

        status, payload = decoded_data.split("\n", 1)
        payload = payload.strip()  # убираем лишние переносы строк и пробелы

        # если получили ошибку - бросаем исключение ClientError
        if status == "error":
            raise ClientError(payload)

        return payload

    def put(self, metric, data, timestamp=None):
        timestamp = int(timestamp) or time.time()
        try:
            self.sock_connection.sendall(f"put {metric} {data} {timestamp}\n".encode())
        except socket.error as err:
            raise ClientError("error send data", err)
        return self._read_answer()

    def get(self, metric):
        try:
            self.sock_connection.sendall(f"get {metric}\n".encode())
        except socket.error as err:
            raise ClientError("error send data", err)
        answer = self._read_answer()
        result = {}
        if answer == "":
            return result
        for line in answer.split("\n"):
            metric, data, timestamp = line.split()
            if metric not in result.keys():
                result[metric] = []
            result[metric].append((int(timestamp), float(data)))
        return result

    def close(self):
        try:
            self.sock_connection.close()
        except socket.error as err:
            raise ClientError("error close connection", err)


if __name__ == "__main__":
    client = Client("127.0.0.1", 8888, timeout=5)
    client.put("test", 0.5, timestamp=1)
    client.put("test", 2.0, timestamp=2)
    client.put("test", 0.5, timestamp=3)
    client.put("load", 3, timestamp=4)
    client.put("load", 4, timestamp=5)
    print(client.get("load"))
    print(client.get("*"))

    client.close()
