import time
from absl import app, flags, logging
from absl.flags import FLAGS
from PIL import Image
import cv2
import numpy as np

flags.DEFINE_string('video', './data/video/video.mp4', 'path to input video or set to 0 for webcam')
flags.DEFINE_string('output', None, 'path to output video')
flags.DEFINE_string('output_format', 'XVID', 'codec used in VideoWriter when saving video to file')

def main(_argv):
   
    vid = cv2.VideoCapture(video_path)
    out = None
    if FLAGS.output:
        # by default VideoCapture returns float instead of int
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
        out = cv2.VideoWriter(FLAGS.output, codec, fps, (width, height))
        
    counter = 0
    while True:
        return_value, frame = vid.read()
        if return_value:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #image = Image.fromarray(frame)
        else:
            print('Video has ended or failed, try a different video format!')
            break
    
        img_new = cv.Laplacian(img, cv.CV_64F)
        score = img_new.var()
        threshold = 100

        if score < threshold:
            cv2.putText(frame, "Blurry Frame!", (5, 15),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (200, 0, 0), 2)
            cv2.putText(frame, "Sharpness score = {}".format(score), (5, 20),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (200, 0, 0), 2)
        else :
            cv2.putText(frame, "Clear Frame.", (5,15),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 200, 0), 2)
            cv2.putText(frame, "Sharpness score = {}".format(score), (5, 20),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 200, 0), 2)
        
        out.write(result)
        counter += 1
      
        if cv2.waitKey(50) & 0xFF == ord('q'): break
    #cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
