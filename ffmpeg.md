### windows

1. 查看所有设备
   ```
   ffmpeg -list_devices true -f dshow -i dummy
   ```

2. 查看某一设备支持的编码格式
   ```
   ffmpeg -list_options true -f dshow -i video="Doccamera"
   ```

3. 安装流媒体服务器-> easy darwin 
   ```
   https://blog.csdn.net/weixin_40448140/article/details/113180796
   ```

4. 使用ffmpeg进行推流
   ```
   # 低延时
   ffmpeg -f dshow -i video="Webcam" -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -rtsp_transport udp -f rtsp rtsp://127.0.0.1/test
   
   # 低延时
   ffmpeg -f dshow -i video="Webcam" -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -max_delay 1000 -bufsize 500000 -rtbufsize 500000 -rtsp_transport tcp -f rtsp rtsp://127.0.0.1/test
   
   # copy
   ffmpeg -f dshow -i video="Webcam" -codec:v copy -rtsp_transport udp -f rtsp rtsp://127.0.0.1/test
   
   ```

5. ffmpeg使用gpu解码
   ```
   ffmpeg -f dshow -hwaccel cuvid -c:v h264_cuvid -i video="Webcam" -c:v h264_nvenc -rtsp_transport tcp -f rtsp rtsp://127.0.0.1/test
   
   # 命令来源： https://docs.nvidia.com/video-technologies/video-codec-sdk/12.0/pdf/Using_FFmpeg_with_NVIDIA_GPU_Hardware_Acceleration.pdf
   ffmpeg -re -y -vsync 0  -f dshow -hwaccel cuvid -c:v h264_cuvid -i video="Webcam" -c:v h264_nvenc -preset p4 -tune ll -b:v 5M -bufsize 5M -maxrate 10M -qmin 0 -g 250 -bf 3 -b_ref_mode middle -temporal-aq 1 -rc-lookahead 10 -i_qfactor 0.75 -b_qfactor 1.1  -rtsp_transport tcp -f rtsp rtsp://127.0.0.1/test
   
   # 低延时
   ffmpeg -re -y -vsync 0  -f dshow -hwaccel cuvid -c:v h264_cuvid -i video="Webcam" -c:v h264_nvenc -preset p4 -tune hq -b:v 5M -bufsize 5M -maxrate 10M -qmin 0 -g 250 -bf 3 -b_ref_mode middle -temporal-aq 1 -rc-lookahead 5 -i_qfactor 0.75 -b_qfactor 1.1  -rtsp_transport udp -f rtsp rtsp://127.0.0.1/test
   ```

6. 低延时流媒体播放器

   ```
   vlc播放至少会有1s的延迟
   EasyPlayer Pro: https://github.com/tsingsee/EasyPlayerPro-Win
   ```

7. 支持cuda的opencv
   ```
   https://github.com/cudawarped/opencv-python-cuda-wheels/releases/tag/4.6.0.20220923
   ```

8. opencv读取相机代码
   ```
   import cv2
   import time
   print("=> running")
   # 检查是否支持CUDA
   if cv2.cuda.getCudaEnabledDeviceCount():
       print("检测到支持CUDA的设备数量:", cv2.cuda.getCudaEnabledDeviceCount())
   else:
       print("未检测到支持CUDA的设备")
   
   if __name__=="__main__":
       device=0
       cv2.cuda.setDevice(device)
       url="rtsp://127.0.0.1/test"
       reader=cv2.cudacodec.createVideoReader(url)
       FPS=0
       start=time.time()
       while True:
           ret,frame=reader.nextFrame()
           end=time.time()
           frame=frame.download()
           # 将RGBA图像转换为RGB
           frame=cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB )
           # import pdb;pdb.set_trace()
           # cv2.imshow("Demo4", frame)
           # key = cv2.waitKey(1)
           # if key==ord('q'):
           #     break
           if end-start>1:
               print("=> 当前的的FPS:",FPS)
               start=end
               FPS=0
           else:
               FPS+=1
           
           # import pdb;pdb.set_trace()
   
   ```
   
   