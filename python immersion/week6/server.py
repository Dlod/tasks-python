import asyncio

metric = []


class Server(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport

    def data_received(self, data: bytes):
        request = data.decode().split(" ")
        method = request[0]
        req = request[1:]
        if method == "get":
            result = self._get(req)
        elif method == "put":
            result = self._put(req)
        else:
            result = 'error\nwrong command\n\n'
        self.transport.write(result.encode())

    @staticmethod
    def _get(req):
        if len(req) != 1:
            return 'error\nwrong command\n\n'
        _result = "ok\n"
        if req[0].strip() == "*":
            _result = _result + "\n".join(metric)
        else:
            for m in metric:
                if req[0].strip() in m:
                    if m in _result:
                        continue
                    _result = _result + m + "\n"
        return _result + "\n\n"

    @staticmethod
    def _put(req):
        if len(req) != 3:
            return 'error\nwrong command\n\n'
        if " ".join(req).strip() not in metric:
            metric.append(" ".join(req).strip())
        return "ok\n\n"


def run_server(host="127.0.0.1", port=8888):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(Server, host=host, port=port)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server()