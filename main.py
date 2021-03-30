
import numpy as np
import cv2
import os
from datetime import datetime
import os
import errno
import psutil  # to check disk space
import wmi  # to get Pi temperature

try:
    os.makedirs('videos')
    os.makedirs('motion')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


def get_temperature():
    try:
        w = wmi.WMI()
        print(w.Win32_TemperatureProbe()[0].CurrentReading)
        return w.Win32_TemperatureProbe()[0].CurrentReading
    except:
        print('error getting temperature')
        return 0


def get_disk_space(dir='/'):
    hdd = psutil.disk_usage(dir)
    print("Total: ", hdd.total / (2**30))
    print("Used: ", hdd.used / (2**30))
    print("Free: ", hdd.free / (2**30))


def record_video():
    print('System Active')
    now = datetime.now()  # current date and time
    date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
    video_name = "videos/{}.avi".format(date_time)
    print(video_name)
    cap = cv2.VideoCapture(0)  # select first camera to record

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_name, fourcc, 20.0, (640, 480))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # frame = cv2.flip(frame, 0)
            #
            # write the flipped frame
            out.write(frame)
            cv2.imshow('Front camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()


record_video()
# get_disk_space('../')
