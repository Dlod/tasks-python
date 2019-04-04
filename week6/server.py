import asyncio


class Server(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport

    def data_received(self, data: bytes):
        pass


def run_server(host="127.0.0.1", port=8888):
    loop = asyncio.get_event_loop()
    corotinue = asyncio.start_server(Server, host=host, port=port, loop=loop)
    server = loop.run_until_complete(corotinue)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server()