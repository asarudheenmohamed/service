""" API endpoint to upload the inventory."""

import datetime
import itertools
import logging
import json
import tempfile
import os

import pandas as pd
from rest_framework import parsers
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import models as models
from .. import lib as upload


logger = logging.getLogger(__name__)


class InventoryUploadView(APIView):
    """Endpoint to upload the inventory.

    Expects a file path, downloads and parses the file and pushes into DB
    """

    # Using Multipart and not fileupload to strip away the encode parts.
    parser_classes = (parsers.MultiPartParser,)

    def post(self, request, filename):
        """Get the file and uploads the data to DB.

        params:
            data:
                1. file (string): Absolute path of the file to download
        """
        logger.info("Got a file {}".format(filename))
        file_obj = request.data['file']

        _, path = tempfile.mkstemp(suffix=".xlsx")
        with open(path, "wb+") as file_handle:
            file_handle.write(file_obj.read())

        inventory = pd.read_excel(path, skiprows=[0, 1, 2, 3])
        upload.InventoryUploadController(inventory).process()

        # do some stuff with uploaded file
        return Response(status=204)
