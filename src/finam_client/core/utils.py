from datetime import datetime
from google.protobuf.timestamp import Timestamp

def datetime_to_timestamp(date_time: datetime) -> Timestamp:
    timestamp = Timestamp()
    timestamp.FromDatetime(date_time)
    return timestamp

def timestamp_to_datetime(time_stamp: Timestamp) -> datetime:
    return time_stamp.ToDatetime()
