##############################################################################
#
# Copyright (c) 2006 Lovely Systems and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Task Service Interfaces

$Id$
"""
__docformat__ = 'restructuredtext'
import zope.interface
import zope.interface.common.mapping
import zope.schema
from zope.app.container.interfaces import IContained

QUEUED = 'queued'
PROCESSING = 'processing'
CANCELLED = 'cancelled'
ERROR = 'error'
COMPLETED = 'completed'

class ITaskService(IContained):
    """A service for managing and executing long-running, remote tasks."""

    jobs = zope.schema.Object(
        title=u'Jobs',
        description=u'A mapping of all jobs by job id.',
        schema=zope.interface.common.mapping.IMapping)

    def getAvailableTasks():
        """Return a mapping of task name to the task."""

    def add(task, input):
        """Add a new job for the specified task.

        The task argument is a string specifying the task. The input are
        arguments for the task.
        """

    def cancel(jobid):
        """Cancel a particular job."""

    def getStatus(jobid):
        """Get the status of a job."""

    def getResult(jobid):
        """Get the result data structure of the job."""

    def getError(jobid):
        """Get the error of the job."""

    def processNext():
        """Process the next job in the queue."""

    def process():
        """Process all scheduled jobs.

        This call blocks the thread it is running in.
        """

    def startProcessing():
        """Start processing jobs.

        This method has to be called after every server restart.
        """

    def stopProcessing():
        """Stop processing jobs."""

    def isProcessing():
        """Check whether the jobs are being processed.

        Return a boolean representing the state.
        """


class ITask(zope.interface.Interface):
    """A task available in the task service"""

    inputSchema = zope.schema.Object(
        title=u'Input Schema',
        description=u'A schema describing the task input signature.',
        schema=zope.interface.Interface,
        required=False)

    outputSchema = zope.schema.Object(
        title=u'Output Schema',
        description=u'A schema describing the task output signature.',
        schema=zope.interface.Interface,
        required=False)

    def __call__(self, service, input):
        """Execute the task.

        The service argument is the task service object. It allows access to
        service wide data and the system as a whole.

        The input object must conform to the input schema (if specified). The
        return value must conform to the output schema.
        """


class IJob(zope.interface.Interface):
    """An internal job object."""

    id = zope.schema.Int(
        title=u'Id',
        description=u'The job id.',
        required=True)

    task = zope.schema.TextLine(
        title=u'Task',
        description=u'The task to be completed.',
        required=True)

    status = zope.schema.Choice(
        title=u'Status',
        description=u'The current status of the job.',
        values=[QUEUED, PROCESSING, CANCELLED, ERROR, COMPLETED],
        required=True)

    input = zope.schema.Object(
        title=u'Input',
        description=u'The input for the task.',
        schema=zope.interface.Interface,
        required=False)

    output = zope.schema.Object(
        title=u'Output',
        description=u'The output of the task.',
        schema=zope.interface.Interface,
        required=False,
        default=None)

    error = zope.schema.Object(
        title=u'Error',
        description=u'The error object when the task failed.',
        schema=zope.interface.Interface,
        required=False,
        default=None)

    created = zope.schema.Datetime(
        title=u'Creation Date',
        description=u'The date/time at which the job was created.',
        required=True)

    started = zope.schema.Datetime(
        title=u'Start Date',
        description=u'The date/time at which the job was started.')

    completed = zope.schema.Datetime(
        title=u'Completion Date',
        description=u'The date/time at which the job was completed.')
