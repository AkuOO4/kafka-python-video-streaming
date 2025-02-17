import time
import sys
import cv2

from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'my-topic'


def emit_video(path_to_video):
    print('start emitting')

    video = cv2.VideoCapture("D:/designs/video/v21.mp4")

    while video.isOpened():
        success, frame = video.read()
        if not success:
            break

        # png might be too large to emit
        data = cv2.imencode('.jpeg', frame)[1].tobytes()

        future = producer.send(topic, data)
        try:
            future.get(timeout=10)
        except KafkaError as e:
            print(e)
            break

        print('.', end='', flush=True)

        # to reduce CPU usage
        time.sleep(0.2)
    print()

    video.release()

    print('done')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You need to specify a path to video file.')
        sys.exit(1)
    emit_video(sys.argv[1])
