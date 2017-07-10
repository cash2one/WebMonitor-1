#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


class FileUtils(object):
    data_dir_path = os.getcwd() + os.sep + "date"
    out_dir_path = os.getcwd() + os.sep + "out"

    @staticmethod
    def init_dir_path():
        if not os.path.exists(FileUtils.data_dir_path):
            os.mkdir(FileUtils.data_dir_path)
            print "mkdir-->" + FileUtils.data_dir_path
        if not os.path.exists(FileUtils.out_dir_path):
            os.mkdir(FileUtils.out_dir_path)
            print "mkdir-->" + FileUtils.out_dir_path

    @staticmethod
    def build_data_dir(dir_name):
        path = FileUtils.data_dir_path + os.sep + dir_name
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def build_data_file(file_name):
        path = FileUtils.data_dir_path + os.sep + file_name
        if not os.path.exists(path):
            file(path, "w").close()

    @staticmethod
    def get_data_path(file_name):
        return FileUtils.data_dir_path + os.sep + file_name

    @staticmethod
    def build_out_dir(dir_name):
        path = FileUtils.out_dir_path + os.sep + dir_name
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def build_out_file(file_name):
        path = FileUtils.out_dir_path + os.sep + file_name
        if not os.path.exists(path):
            file(path, "w").close()

    @staticmethod
    def get_out_path(file_name):
        return FileUtils.out_dir_path + os.sep + file_name

    @staticmethod
    def exists_path(path):
        return os.path.exists(path)

    @staticmethod
    def write_file(str_data, file_path):
        try:
            f = file(file_path, "w")
            f.write(str_data)
            f.close()
        except Exception, e:
            print e.message

    @staticmethod
    def write_out_file(str_data, file_name):
        FileUtils.build_out_file(file_name)
        path_ = FileUtils.get_out_path(file_name)
        FileUtils.write_file(str_data, path_)
