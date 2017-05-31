from azure.servicebus import ServiceBusService
import base64
import glob
import re
import time

numbers = re.compile(r'(\d+)')


def numerical_sort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

service_namespace = 'image-analytics'
key_name = 'Send-Images'  # SharedAccessKeyName from Azure portal
key_value = 'Md2ebj6n1NVz3mFUvlzi1WzTcBqxQ9CuDW5hqk+TNcY='  # SharedAccessKey from Azure portal
sbs = ServiceBusService(service_namespace,
                        shared_access_key_name=key_name,
                        shared_access_key_value=key_value)

path = '/Users/msftwork/Documents/VideoAnalytics/cam806_frames/*.jpg'
frames = sorted(glob.glob(path), key=numerical_sort)
starttime=time.time()
for frame_id in range(len(frames)):
    image = open(frames[frame_id], 'rb')
    image_base64 = base64.encodestring(image.read())
    image_event = '{ "CameraId":"cam806", "FrameId":"'+str(frame_id)+'", "SeenTime":"'+ str(time.time())+'",FrameEncoded:"' + image_base64 + '" }'
    sbs.send_event('input-images-eh', image_event)
    time.sleep(1.0 - ((time.time() - starttime) % 1.0))
    print image_event