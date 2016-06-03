# trinket.tasks
# Celery tasks
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Fri Jun 03 12:03:55 2016 -0700
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: tasks.py [] allen.leis@gmail.com $

"""
Celery tasks
"""

##########################################################################
# Imports
##########################################################################

from trinket.celery import app

##########################################################################
# Tasks
##########################################################################

@app.task(ignore_result=True)
def ping():
    print("pong")


##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    pass
