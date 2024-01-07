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
