import os
import re
import time
import uuid
import requests
import datetime

from config import CONF
from pytz import timezone
from http import HTTPStatus
from requests.auth import HTTPBasicAuth
from fastapi import APIRouter, HTTPException, Request, Response, Header, Form, status


async def post_tickets(subject, title, body) -> str:
    try:
        url = CONF.zendesk.url
        ticket_url = "%s/tickets" % url
    
        payload = {
          "ticket": {
            "comment": {
                "body": "error log for {}: {}".format(title, body)
            },
            "priority": "high",
            "subject": "ticket for trace, {}".format(subject),
            "externalID": "{}".format(subject),
            "followers": [
                { "user_name": "wychoi", "user_email": "%s" % CONF.zendesk.user_email, "action": "put" },
            ]
          }
        }
    
        headers = {
            "Content-Type": "application/json",
        }
        email_address = CONF.zendesk.admin_email
        api_token = CONF.zendesk.token
        auth = HTTPBasicAuth(f'{email_address}/token', api_token)
        
        response = requests.request(
            "POST",
            ticket_url,
            auth=auth,
            headers=headers,
            json=payload
        )
        
        print(response.text)
        return response.text

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else:
        return response.text

async def check_existance_by_trace_id(trace_id) -> bool:
    try:
        url = CONF.zendesk.url
        search_url = "%s/search" % (url)
    
        email_address = CONF.zendesk.admin_email
        api_token = CONF.zendesk.token
        auth = HTTPBasicAuth(f'{email_address}/token', api_token)
    
        params = {
           'query': 'type:ticket %s' %trace_id
        }
        response = requests.get(
            search_url,
            auth=auth,
            params=params
        )

        if (len(response.json()["results"]) > 0):
            return True

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else:
        return False

