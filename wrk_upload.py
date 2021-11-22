# -*- coding: utf-8 -*-
"""
wrk_upload
upload file to Google Drive

2021/nov  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os

# pyDrive
import pydrive.auth as gda
import pydrive.drive as gdd

# < logging >--------------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------
def upload_file(fs_fname):
    """
    upload file to Google Drive
    """
    try:
        # login to Google Drive
        l_gd_login = gda.GoogleAuth()
        assert l_gd_login

        # create drive object
        l_gd_drive = gdd.GoogleDrive(l_gd_login)
        assert l_gd_drive

    # em caso de erro,...
    except:
        # logger
        M_LOG.error("Erro na autenticação do Google Drive.")
        # quit
        return None

    # open file to upload
    with open(fs_fname) as lfh_in:
        # filename
        ls_fbase = os.path.basename(lfh_in.name)

        try:
            # create file on GDrive
            l_gd_file_drive = l_gd_drive.CreateFile({"title": ls_fbase})
            assert l_gd_file_drive
            
            # set file contents
            l_gd_file_drive.SetContentString(lfh_in.read())

        # em caso de erro,...
        except:
            # logger
            M_LOG.error("Erro na criação do arquivo.")
            # quit
            return None

        try:
            # upload file
            l_gd_file_drive.Upload()

        # em caso de erro,...
        except:
            # logger
            M_LOG.error("Erro no upload do arquivo.")
            # quit
            return None

        # change file permissions
        l_permission = l_gd_file_drive.InsertPermission({"type":  "anyone",
                                                         "value": "anyone",
                                                         "role":  "reader"})

        # return link to file
        return l_gd_file_drive["alternateLink"]

    # return
    return None
    
# < the end >--------------------------------------------------------------------------------------
