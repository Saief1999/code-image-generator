import argparse
import json
from typing import TextIO
from base64 import b64encode
import requests

class ImageGenerator:
    def __init__(self, src:TextIO, filename:str, config:TextIO) -> None:
        self.code = self.extract_code(src)
        self.filename = filename
        self.config = self.parse_config(config)

    def extract_code(self, src:TextIO)->str:
        """Extracts code from file

        Args:
            src (TextIO): Source file

        Returns:
            str: The code encoded as Base64
        """
        code:str = b64encode("".join(src.readlines()).encode("utf-8")).decode("utf-8")
        src.close()
        return code
        
    def parse_config(self, config:TextIO) -> dict:
        """Parses the config file

        Args:
            config (TextIO): config file

        Returns:
            dict: the json object parsed as a dictionary
        """
        config_dict = json.load(config)
        config.close()
        return config_dict


    def generate_params(self)->str:
        """Generates the parameters of the request based on the config and the code

        Returns:
            str: url parameters to send with the request
        """
        return {
            "theme": self.config["colors"],
            "spacing": self.config["padding"],
            "background": self.config["background"],
            "darkMode": self.config["darkMode"],
            "language": self.config["language"],
            "code": self.code,
            "title": self.filename
        }

    def download_img(self) -> None:
        """Downloads the image

        Args:
            config (dict): parsed configuration
        """
        response = requests.get("https://ray.so/api/image",params=self.generate_params())
        if response.status_code == 200:
                with open(f"{self.filename}.png", "wb") as f:
                    f.write(response.content)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Generate images from code.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("src", help="source file path", type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument("-t", "--title", help="image title", default="undefined")
    parser.add_argument('-c', "--config", help="config file path",type=argparse.FileType('r', encoding='UTF-8'), default="config.json")

    args = parser.parse_args()
    
    generator = ImageGenerator(args.src, {args.title}, args.config)
    generator.download_img()