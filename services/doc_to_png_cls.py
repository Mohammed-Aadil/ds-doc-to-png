import datetime
import time
from wand.color import Color
from xhtml2pdf import pisa
from os import path
from wand.image import Image
from wand.color import Color
from config import config
import mammoth
import os
import logging
logger = logging.getLogger(__name__)


class ImageConverter(object):
    """
    Utility class to convert docx, pdf and text file to images
    """
    def __init__(self, file_name, **kwargs):
        self.__file_name = file_name
        self.__file_type = file_name.split('.')[-1]
        self.response = []
        self.format = '.' + (kwargs.get('format') or 'png')
        self.default_temp_pdf_file_name = kwargs.get('default_temp_pdf_file_name') or 'temp_attachment_conversion.pdf'
        self.attachment_path = config['attachment_path']
        self.root_path = config['root_path']
        self.default_resolution = kwargs.get('default_resolution') or 150
        self.default_compression = kwargs.get('default_compression') or 99
        self.hash_code = int(time.time())

    """
    Function to return file name without extension
    """
    def get_file_name_without_type(self, file_name=None):
        name_tokens = (file_name or self.__file_name).split('.')
        return '.'.join(name_tokens[: len(name_tokens) - 1]) + str(self.hash_code)

    """
    It create PDF file from given html code 
    """
    def create_pdf_file(self, html_str):
        result_file = open(path.join(self.root_path, self.default_temp_pdf_file_name), 'w+b')
        pisa_file = pisa.CreatePDF(html_str, dest=result_file)
        result_file.close()
        return pisa_file.err

    """
    It convert docx file to png 
    """
    def __convert_docx_to_image(self, file_name=None):
        html_docx = mammoth.convert_to_html(path.join(self.attachment_path, file_name or self.__file_name))

        if not self.create_pdf_file(html_docx.value):
            return self.__convert_pdf_to_image(self.default_temp_pdf_file_name)
        else:
            raise Exception('Something goes wrong while converting docx to png.')

    """
    It convert text file to png 
    """
    def __convert_text_to_image(self, file_name=None):
        _file = open(path.join(self.attachment_path, file_name or self.__file_name), 'r')
        file_data = '<br>'.join(_file.readlines())
        _file.close()

        if not self.create_pdf_file(file_data):
            return self.__convert_pdf_to_image(self.default_temp_pdf_file_name)
        else:
            raise Exception('Something goes wrong while converting text to png.')

    def add_white_bg_layer(self, img, index):
        with Image(width=img.width, height=img.height, background=Color("white")) as bg:
            bg.composite(img, 0, 0)
            bg.compression_quality = self.default_compression
            bg.save(
                filename=path.join(
                    self.attachment_path,
                    self.get_file_name_without_type() + '-' + str(index) + self.format
                )
            )
    """
    It convert pdf file to png 
    """
    def __convert_pdf_to_image(self, file_name=None):
        file_path = path.join(self.root_path, file_name or self.__file_name)
        if self.__file_type == 'pdf':
            file_path = path.join(self.attachment_path, file_name or self.__file_name)

        with Image(
            filename=file_path,
            resolution=self.default_resolution,
            format=self.format
        ) as img:

            if len(img.sequence) == 1:
                self.add_white_bg_layer(img)
                self.response.append({
                    'path': path.join(
                        self.attachment_path,
                        self.get_file_name_without_type() + self.format
                    ),
                    'name': self.get_file_name_without_type() + self.format,
                    'url': None
                })
            else:
                for index in range(len(img.sequence)):
                    self.add_white_bg_layer(img.sequence[index], index)
                    self.response.append({
                        'path': path.join(
                            self.attachment_path,
                            self.get_file_name_without_type() + '-' + str(index) + self.format
                        ),
                        'name': self.get_file_name_without_type() + '-' + str(index) + self.format,
                        'url': None
                    })
        if self.__file_type != 'pdf':
            os.remove(file_path)
        return self.response

    """
    It decides conversion strategy based on file type
    """
    def convert(self):
        try:
            if self.__file_type == 'docx':
                return self.__convert_docx_to_image()

            elif self.__file_type == 'pdf':
                return self.__convert_pdf_to_image()

            else:
                return self.__convert_text_to_image()
        except Exception as e:
            logger.error(e)
            raise e
