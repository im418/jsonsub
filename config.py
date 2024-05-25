import os


class Config:
    BASE_PATH = os.environ.get('BASE_PATH', 'https://sub3.persiandownloadextremespeed.shop:2096')
    PORT = int(os.environ.get('PORT', '8000'))
    SSL_KEY_FILE = os.environ.get('SSL_KEY_FILE', '')
    SSL_CERT_FILE = os.environ.get('SSL_CERT_FILE', '')
