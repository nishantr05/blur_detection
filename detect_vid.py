from imutils.video import FPS
import time
from absl import app, flags, logging
from absl.flags import FLAGS
from PIL import Image
import cv2
import numpy as np

flags.DEFINE_string('video', './video.mp4', 'path to input video or set to 0 for webcam')
flags.DEFINE_string('output', None, 'path to output video')
flags.DEFINE_string('output_format', 'mp4v', 'codec used in VideoWriter when saving video to file')

def main(_argv):
   
    vid = cv2.VideoCapture(FLAGS.video)
    out = None
    if FLAGS.output:
        # by default VideoCapture returns float instead of int
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frameps = vid.get(cv2.CAP_PROP_FPS)
        codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
        out = cv2.VideoWriter(FLAGS.output, codec, frameps, (width, height))
        
    frame_no = 0
    fps = FPS().start()
    print("Processing the video...")
    while True:
        return_value, frame = vid.read()
        if return_value:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_no += 1
        else:
            if frame_no == vid.get(cv2.CAP_PROP_FRAME_COUNT):
                print("Video processing complete")
                break
            raise ValueError("No image! Try with another video format")
    
        img_new = cv2.Laplacian(img, cv2.CV_64F)
        score = img_new.var()
        threshold = 100
        #print(fps.type)

        curr_time = float(frame_no)/frameps
        minutes = int(curr_time/60)
        seconds = curr_time%60
        
        ##Just creating test lables for size of patch
        label1, label2 = "BlurryFrame", "SharpenessScore=10" 
        labelSize1, baseLine1 = cv2.getTextSize(label1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        labelSize2, baseLine2 = cv2.getTextSize(label2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(frame, (5, 15 - labelSize1[1]),
                              (5 + labelSize1[0], 15 + baseLine1),
                              (255, 255, 255), cv2.FILLED)
        cv2.rectangle(frame, (5, 42 - labelSize2[1]),
                              (5 + labelSize2[0], 42 + baseLine2),
                              (255, 255, 255), cv2.FILLED)
        if score < threshold:
            print('Blurry frame detected at {}min {:.1f}sec '.format(minutes, seconds))
            cv2.putText(frame, "Blurry Frame!", (5, 15),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (200, 0, 0), 2)
            cv2.putText(frame, "Sharpness score = {}".format(score), (5, 20),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (200, 0, 0), 2)
        else :
            cv2.putText(frame, "Clear Frame.", (5,15),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 200, 0), 2)
            cv2.putText(frame, "Sharpness score = {}".format(score), (5, 20),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 200, 0), 2)
        
        out.write(frame)
        fps.update()

    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
