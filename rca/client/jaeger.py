import os
import re
import time
import uuid
import requests
import datetime

from config import CONF
from typing import List
from pytz import timezone
from client.zendesk import check_existance_by_trace_id, post_tickets
from fastapi_utilities import repeat_every
from fastapi import APIRouter, HTTPException, Request, Response, Header, Form, status

router = APIRouter()

error_ids = []
error_titles = []
error_logs = []
error_datas = []

async def date2unix(date) -> int:
    unix = datetime.datetime.timestamp(date) * 1000
    return int(str(unix)[0:10])

async def get_error_traces_by_service(service):
    try:
        now = datetime.datetime.now(timezone('Asia/Seoul'))
        end = await date2unix(now)
        start = await date2unix((now - datetime.timedelta(hours=int(CONF.jaeger.time_range))))

        jaeger_url = CONF.jaeger.url 
        microsec = now.microsecond
        if len(str(now.microsecond)) < 6:
            microsec = int(str(now.microsecond).zfill(6))
        res = requests.get('%s/api/traces?service=%s&tags={"error":"true"}&start=%s%s&end=%s%s' % (jaeger_url, service, start, microsec, end, microsec))

        t_len = len(res.json()["data"])
        for t in range(0, t_len):
            s_len = len(res.json()["data"][t]["spans"])
            for s in range(0, s_len):
                if res.json()["data"][t]["spans"][s]["tags"][4]["key"] == "error":
                    trace_id = res.json()["data"][t]["spans"][s]["traceID"]

                    if trace_id in error_ids:
                        continue

                    error_ids.append(trace_id)
                    error_titles.append(res.json()["data"][t]["spans"][s]["tags"][3]["value"])
                    error_logs.append(res.json()["data"][t]["spans"][s]["logs"])
                    trace_data = await get_error_trace_data(trace_id)
                    error_datas.append(trace_data)


    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

#@repeat_every(seconds=60 * 60)
@repeat_every(seconds=60)
async def get_error_traces() -> List[str]:
    try:
#        services = ["cinder-cinder-api", "cinder-cinder-backup", "cinder-cinder-volume", "glance-api", "horizon-horizon", "keystone-public", "nova-nova-compute", "nova-nova-conductor", "nova-osapi-compute", "neutron-neutron-server"]
        services = ["horizon-horizon"]

        for service in services:
            await get_error_traces_by_service(service)

        for i in range(len(error_ids)):
            if await check_existance_by_trace_id(error_ids[i]):
                continue

            await post_tickets(error_ids[i], error_titles[i], error_logs[i])

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else:
        return error_datas

    
async def get_error_trace_data(trace_id) -> dict:
    try:
        jaeger_url = CONF.jaeger.url 
        data = requests.get('%s/api/traces/%s' % (jaeger_url, trace_id))

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else: 
        return data.json()
