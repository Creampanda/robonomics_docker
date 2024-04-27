import requests
import traceback
import docker
import robonomicsinterface as RI
from config import IPFS_COMMAND_GATEWAY, ROBONOMICS_LISTENER_ACCOUNT, SENDERS

# Docker client setup
client = docker.from_env()

# Environment variables for configuration


def robonomics_transaction_callback(data, launch_event_id):
    sender, recipient, command_params_32_bytes = data
    if sender not in SENDERS:
        print(f"Sender {sender} is not approved. Not running launch command...")
        return
    command_params_ipfs_hash = RI.ipfs_32_bytes_to_qm_hash(command_params_32_bytes)
    print(f"Launch Event ID: {launch_event_id}")
    print(f"Sender: {sender}")
    print(f"Recipient: {recipient}")
    print(f"Command Params IPFS Hash: {command_params_ipfs_hash}")

    # Fetching the JSON data from IPFS
    url = f"{IPFS_COMMAND_GATEWAY}{command_params_ipfs_hash}"
    print(url)
    response = requests.get(url=url)
    if response.status_code == 200:
        data = response.json()
        docker_link = data["docker_image_link"]
        print("Received Docker image link:", docker_link)
        run_container_from_link(docker_link, launch_event_id)
    else:
        print(f"Failed to fetch IPFS data: Status Code {response.status_code}")


def run_container_from_link(docker_link, launch_event_id):
    print("Pulling Docker image and starting container for launch", launch_event_id)
    try:
        client.images.pull(docker_link)  # Pulling the Docker image
        output = client.containers.run(docker_link, detach=False)  # Running the container
        print("Container started successfully. Output:\n___________")
        print(output.decode("utf-8"))  # Ensure the output is in a human-readable form
        print("___________")
    except Exception as e:
        print(f"Error running container: {e}")
        traceback.print_exc()


def launch_robonomics_subscriber():
    interface = RI.Account(remote_ws="wss://kusama.rpc.robonomics.network")
    print("Robonomics subscriber starting...")
    subscriber = RI.Subscriber(
        interface, RI.SubEvent.NewLaunch, robonomics_transaction_callback, ROBONOMICS_LISTENER_ACCOUNT
    )
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping the subscriber.")


def main():
    print("Starting the subscriber...")
    launch_robonomics_subscriber()


if __name__ == "__main__":
    main()
