import robonomicsinterface as RI
from robonomicsinterface import Account, Launch


class Sender:
    def __init__(self, seed, remote_ws):
        """
        Initializes the Sender with the necessary seed phrase and remote ws.

        :param seed: Your seed pharese.
        :param remote_ws: Your rpc address secret.
        """
        self.sender_account = Account(
            seed=seed,
            remote_ws=remote_ws,
        )

    def send_launch_to(self, address, ipfs_cid):
        launch = Launch(self.sender_account)
        print(f"Sending launch to {address=}")
        res = launch.launch(address, ipfs_cid)
        print(f"Sended launch to {address=}, {res=}")
