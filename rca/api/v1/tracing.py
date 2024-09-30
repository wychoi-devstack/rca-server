from __future__ import annotations

from pathlib import PurePath
from typing import Any, List, Optional, Tuple, Union

from fastapi import APIRouter, Depends, Form, Header, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse

from config import CONF
from typing import List

import os
import schemas

# manage traces with CRUD operation and Jaeger API
router = APIRouter()

#@router.post(
#    "/tickets",
#    description="Make zendesk tickets for error traces",
#    responses={
#        200: {"model": List[str]},
#        500: {"model": schemas.common.InternalServerErrorMessage},
#    },
#    response_model=List[str],
#    status_code=status.HTTP_200_OK,
#    response_description="OK",
#    response_model_exclude_none=True
#)
