#!/usr/bin/env python3
"""
Take and read nodes with sup
"""
from datetime import datetime, timedelta
import os
from string import printable
import sys

import yaml
from dateutil.parser import parse

from . import config


def print_yaml(obj):
    """
    Method to pretty print a python object into yaml format but withwhitespace.
    """
    multi_string = yaml.dump(obj, default_flow_style=False)
    lines = []
    for i, line in enumerate(multi_string.split('\n')):

        try:
            char = line[0]
        except IndexError:
            char = ""

        if char == ' ':
            pass
        elif char in printable and i > 0:
            lines.append('\n\n\n\n')

        lines.append(line)
    return lines

def get_fileloc(date):
    """
    Returns the file location.
    """
    return os.path.join(config.ARCHIVE_DIR, get_filename(date))

def open_file(date, filepath=None, verbose=False):
    """
    Opens the sup file for a given date.
    """
    file_loc = get_fileloc(date) if not filepath else filepath

    if os.path.exists(file_loc):
        if verbose:
            print('Using text editor "%s"' % config.TEXTEDITOR)

        os.system('"%s" %s' % (config.TEXTEDITOR, file_loc))
    else:
        print("No 'Sup?' file found for %s" % date.date())

def write_file(loc, header, verbose=False):
    """
    Write an empty sup file from the template.
    """
    if not os.path.exists(loc):
        with open(loc, 'wb') as stream:
            stream.write(bytes(config.TEMPLATE % header), encoding='utf-8')
    else:
        print('Not writing %s. File already exists.')

def create_file(date, new=False, i=None, custom_title=None, verbose=False):
    """
    Creates a sup file for a given date.
    """
    loc = get_fileloc(date)

    if custom_title:
        loc = loc.replace('.yml', '_%s.yml' % custom_title)
        header = '%s %s' % (date_str(date), custom_title)
        write_file(loc, header)

    if new:
        i = 2
        pattern = '_%d.yml'
        next_file = loc.replace('.yml', pattern % i)
        while os.path.exists(next_file):
            i += 1
            next_file = loc.replace('.yml', pattern % i)
        write_file(next_file, date_str(date))
        return next_file
    elif i:
        loc = loc.replace('.yml', pattern % i)

    if not os.path.exists(loc):
        with open(loc, 'wb') as stream:
            stream.write(bytes(config.TEMPLATE % date_str(date), encoding='utf-8'))

    return loc

def date_str(date):
    """
    Return the date in sup date format.
    """
    return date.strftime('%Y-%m-%d')

def get_filename(date):
    """
    Returns the filename for a given date.
    """
    return config.FILENAME % date_str(date)

def print_sup(today, verbose=False):
    """
    Create a printer friendly sup file with extra whitespace for notes.
    """
    fileloc = get_fileloc(today)

    with open(fileloc, 'rb') as stream:
        today_dict = yaml.safe_load(stream)
        lines = print_yaml(today_dict)

    # write the file out with more carriage returns
    textloc = fileloc.replace('.yml', '.txt')

    with open(textloc, 'w') as text_file:
        text_file.write('\n'.join(lines))

    os.system('%s %s' % (config.PRINT_CMD, textloc))

def create_review_file(today):
    """
    Create a review sup file of the previous week's work.
    """
    review_file = create_file(today, custom_title='review')

    with open(review_file, 'a') as stream:
        for i in range(6, 0, -1):
            previous = today - timedelta(days=i)
            prev_loc = get_fileloc(previous)

            if os.path.exists(prev_loc):
                with open(prev_loc, 'rb') as prev_stream:
                    for line in prev_stream:
                        stream.write(bytes(line), encoding='utf-8')

        return review_file

def ignore_done_dict(obj):
    """
    Returns a version of the input dict without any items with value like 'done'
    """
    if not isinstance(obj, dict): return obj

    new_dict = {}
    for key, val in obj.items():
        #print('Dict item: %s=%s' % (key, val))
        try:
            if val.lower() == 'done':
                #print('ignoring')
                continue
            else:
                new_dict[key] = val
        except AttributeError:
            val = ignore_done_dict(val)
            val = ignore_done_list(val)
            if val:
                new_dict[key] = val

    return new_dict

def ignore_done_list(obj):
    """Ignores done, and iterates through lists in values."""
    if not isinstance(obj, list): return obj

    new_list = []
    for val in obj:
        #print('list item: %s' % val)
        val = ignore_done_dict(val)
        val = ignore_done_list(val)

        if val: new_list.append(val)

    return new_list

def ignore_done(obj):
    """
    Uses ignore_done_list and ignore_done_dict to walk through a complex
    dictionary object and sweep out any done values.
    """
    obj = ignore_done_dict(obj)
    obj = ignore_done_list(obj)
    return obj

def create_update(previous_date, today, verbose=False):
    """
    Interprets yesterday's yaml, and removes any done items, the rest are
    ported to today's yaml.
    """
    previous_loc = get_fileloc(previous_date)
    today_loc = get_fileloc(today)

    with open(previous_loc, 'rb') as stream:
        prev_list = yaml.safe_load(stream)

    today_list = []
    for item in prev_list:
        if not isinstance(item, dict):
            today_list.append(item)
        else:
            today_dict = ignore_done(item)
            if today_dict:
                today_list.append(today_dict)

    with open(today_loc, 'wb') as stream:
        stream.write(bytes(config.TEMPLATE % date_str(today), encoding='utf-8'))
        lines = '\n'.join(print_yaml(today_list))

        while '\n\n\n' in lines:
            lines = lines.replace('\n\n\n', '\n\n')

        stream.write(bytes(lines, encoding='utf-8'))

    return today_loc

def parse_date_from_filename(filename):
    """
    Return the date of a given filename pattern of FILENAME = 'sup_%s.yml'
    """
    pattern = 'sup_%Y-%m-%d.yml'
    try:
        dt = datetime.strptime(filename, pattern)
    except ValueError:
        pass
    else:
        return dt

def find_last_date():
    """
    Return the date of the most recent sup file in the sup dir.
    """
    return max([parse_date_from_filename(f)
                for f in os.listdir(config.ARCHIVE_DIR)
                if parse_date_from_filename(f)])
