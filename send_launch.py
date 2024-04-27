import argparse
from config import ACCOUNT_SEED, DOCKER_IMAGE, PINATA_KEY, PINATA_SECRET, RECIPIENTS, REMOTE_WS
from pinata import PinataUploader
from sender import Sender


def main(docker_image):
    pinata_uploader = PinataUploader(PINATA_KEY, PINATA_SECRET)
    sender = Sender(ACCOUNT_SEED, REMOTE_WS)
    ipfs_cid = pinata_uploader.upload_docker_image(docker_image)
    for address in RECIPIENTS:
        sender.send_launch_to(address, ipfs_cid)


if __name__ == "__main__":

    # Create the parser
    parser = argparse.ArgumentParser(
        description="Upload a Docker image and send launch commands to recipients."
    )
    # Add an optional argument for the Docker image with a default value from config
    parser.add_argument(
        "--docker_image",
        type=str,
        default=DOCKER_IMAGE,
        help="Docker image to upload and send (default: %(default)s).",
    )
    # Parse the command line arguments
    args = parser.parse_args()

    # Pass the docker_image argument to the main function
    main(args.docker_image)
