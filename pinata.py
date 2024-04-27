import requests


class PinataUploader:
    def __init__(self, api_key, api_secret):
        """
        Initializes the PinataUploader with the necessary API credentials.

        :param api_key: Your Pinata API key.
        :param api_secret: Your Pinata API secret.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.pinata.cloud"

    def upload_json(self, content):
        """
        Uploads a JSON object to Pinata and returns the IPFS CID.

        :param content: A dictionary representing the JSON content to upload.

        :return: The CID of the pinned content, or None if the upload fails.
        """
        url = f"{self.base_url}/pinning/pinJSONToIPFS"
        headers = {
            "pinata_api_key": self.api_key,
            "pinata_secret_api_key": self.api_secret,
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, json={"pinataContent": content})

        if response.status_code == 200:
            cid = response.json().get("IpfsHash")
            print(f"Content successfully uploaded to Pinata with CID: {cid}")
            return cid
        else:
            print(f"Failed to upload content to Pinata. Status Code: {response.status_code}, {response.text}")
            return None

    def upload_docker_image(self, docker_image):
        return self.upload_json({"docker_image_link": docker_image})
