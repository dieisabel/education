import config
from server.server import Server


def main() -> None:
    server = Server(
        ipv4=config.SERVER_IP,
        port=config.SERVER_PORT
    )
    server.start()


if __name__ == "__main__":
    main()
