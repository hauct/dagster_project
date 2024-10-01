# fmt: off
from dagster import Definitions, load_assets_from_modules

from .resources import database_resource
from .assets import trips, metrics, requests
from .jobs import trip_update_job, weekly_update_job, adhoc_request_job
from .sensors import adhoc_request_sensor
from .schedules import trip_update_schedule, weekly_update_schedule

trip_assets = load_assets_from_modules([trips])
metric_assets = load_assets_from_modules([metrics], group_name="metrics")
request_assets = load_assets_from_modules([requests])

all_jobs = [trip_update_job, weekly_update_job, adhoc_request_job]
all_sensors = [adhoc_request_sensor]
all_schedules = [trip_update_schedule, weekly_update_schedule]

defs = Definitions(
    assets=[*trip_assets, *metric_assets, *request_assets],
    resources={
        "database": database_resource,
    },
    jobs=all_jobs,
    schedules=all_schedules,
    sensors=all_sensors,
)
