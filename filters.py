# SJSU CS 218 Fall 2019 TEAM6
# Adapted from https://kishstats.com/python/2018/03/15/flask-amazon-s3-series.html
import os
import mimetypes
import arrow


additional_file_types = {
    '.md': 'text/markdown'
}


def datetimeformat(date_str):
    dt = arrow.get(date_str)
    return dt.humanize()


def file_type(key):
    file = os.path.splitext(key)
    file_extension = file[1]
    try:
        return mimetypes.types_map[file_extension]
    except KeyError:
        filetype = 'Unknown'
        if file[0].startswith('.') and file_extension == '':
            filetype = 'text'

        if file_extension in additional_file_types.keys():
            filetype = additional_file_types[file_extension]

        return filetype
