import NDIlib as ndi

class NDI_Receiver():
    def __init__(self):

        self.receiver = self.inititializeReceiver()

    def inititializeReceiver(self):

        if not ndi.initialize():
            return 0

        ndi_recv_create = ndi.RecvCreateV3()
        ndi_recv_create.color_format = ndi.RECV_COLOR_FORMAT_BGRX_BGRA

        ndi_recv = ndi.recv_create_v3(ndi_recv_create)
        print("SMALL_WINDOW inside the ndi-receiver class initialize function")

        if ndi_recv is None:
            print('receive object NULL')
            return 0
        else:
            #print('receive object OK')
            return ndi_recv

    def attachSource(self, source):

        if not ndi.initialize():
            ndi.initialize()

        tempReceiver = NDI_Receiver()
        ndi.recv_connect(tempReceiver.receiver, source)
        tempFlag = False
        for i in range(100):
            t, v, a, m = ndi.recv_capture_v2(tempReceiver.receiver, 50)
            if t == ndi.FRAME_TYPE_VIDEO:
                tempFlag = True
                ndi.recv_free_video_v2(tempReceiver.receiver, v)

        if tempFlag == False:
            self.destroy(tempReceiver.receiver)
            return
        else:
            self.destroy(tempReceiver.receiver)
            ndi.recv_connect(self.receiver, source)
            return


    def destroy(self, receiver ):
        ndi.recv_destroy(receiver)
        #print('receive object destroyed')
        return 0