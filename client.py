import codecs
import json
import logging
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import requests


class Transcriber(object):
    def __init__(self, api_id, api_token, lang, api_url='http://api.azreco.az/transcribe'):
        self.api_id = api_id
        self.api_token = api_token
        self.lang = lang
        self.api_url = api_url

    def transcribe(self, opts):
        """
        Upload a new audio file to azreco for transcription
        If upload suceeds then this method will return the transcription in json format
        """

        params = {'api_id':int(self.api_id),'api_token': self.api_token, 'lang':self.lang}
        try:
            files={'file':open(opts.audio, "rb")}
        except IOError as ex:
            logging.error("Problem opening audio file {}".format(opts.audio))
            raise

        lang = {"lang": opts.lang}

        request = requests.post(self.api_url, files=files, params=params)
        if request.status_code == 200:
            return request.text
        else:
            raise Exception("Transcribing failed.")

def parse_args():
    """
    Parse command line arguments
    """

    # Parse the arguments
    parser = ArgumentParser(
        description='Transcribe audio or video file through the Azreco API',
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('-a', '--audio', type=str, required=True,
                        help="Audio file to be processed")
    parser.add_argument('-o', '--output', type=str, required=False,
                        help="Output filename (will print to terminal if not specified)", default=None)
    parser.add_argument('-i', '--id', type=str, required=True,
                        help="Your transcriber API ID")
    parser.add_argument('-k', '--token', type=str, required=True,
                        help="Your transcriber API Token")
    parser.add_argument('-l', '--lang', type=str, required=True,
                        help="Code of language to use (e.g., en-US, ru-RU, tr-TR)")
    parsed = parser.parse_args()

    return parsed


def main():
    """
    Example way to use the Azreco Client to transcribe audio or video file
    """
    logging.basicConfig(level=logging.INFO)

    opts = parse_args()

    client = Transcriber(opts.id, opts.token, opts.lang)

    result = client.transcribe(opts)
    if opts.output:
        with codecs.open(opts.output, 'w', 'utf-8') as out:
            out.write(result)
        logging.info("Your transcription has been written to file {}".format(opts.output))
    else:
        logging.info("Your transcription: {}".format(result))

if __name__ == '__main__':
    main()
