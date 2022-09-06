from django.shortcuts import render, redirect
import ctypes
from .models import Motion_status
import time
from . import consumer


# Create your views here.
axtdll_1 = ctypes.WinDLL('./AXL.dll')
axtdll_2 = ctypes.WinDLL('./EzBasicAxl.dll')

#axtdll_1.AxmMotLoadParaAll.argtypes
#각 라이브러리 함수에 대한 파라미터와 반환값 설정
AxlOpen = axtdll_1['AxlOpen']
AxlOpen.argtypes = [ctypes.c_long]
AxlOpen.restype = ctypes.c_ulong
AxmMotLoadParaAll = axtdll_1['AxmMotLoadParaAll']
AxmMotLoadParaAll.argtypes = [ctypes.c_char_p]
AxmMotLoadParaAll.restype = ctypes.c_ulong
AxmSignalServoOn = axtdll_1['AxmSignalServoOn']
AxmSignalServoOn.argtypes = [ctypes.c_long, ctypes.c_ulong]
AxmSignalServoOn.restype = ctypes.c_ulong
AxmMoveVel = axtdll_1['AxmMoveVel']
AxmMoveVel.argtypes = [ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double]
AxmMoveVel.restype = ctypes.c_ulong
AxmMoveEStop = axtdll_1['AxmMoveEStop']
AxmMoveEStop.argtypes = [ctypes.c_long]
AxmMoveEStop.restype = ctypes.c_ulong
AxmStatusGetCmdPos = axtdll_1['AxmStatusGetCmdPos']
AxmStatusGetCmdPos.argtypes = [ctypes.c_long, ctypes.POINTER(ctypes.c_double)]
AxmStatusGetCmdPos.restype = ctypes.c_ulong
AxmStatusGetActPos = axtdll_1['AxmStatusGetActPos']
AxmStatusGetActPos.argtypes = [ctypes.c_long, ctypes.POINTER(ctypes.c_double)]
AxmStatusGetActPos.restype = ctypes.c_ulong
AxmStatusReadVel = axtdll_1['AxmStatusReadVel']
AxmStatusReadVel.argtypes = [ctypes.c_long, ctypes.POINTER(ctypes.c_double)]
AxmStatusReadVel.restype = ctypes.c_ulong
AXT_RT_SUCCESS = 0
stat = 0
AxlOpen(7)
AxmMotLoadParaAll(b'MotionDefault_1.mot')
c_cPosition = ctypes.c_double(0)
c_aPosition = ctypes.c_double(0)
c_dVel = ctypes.c_double(0)

def index(request):
    global stat
    stat = 0
    return render(request, 'ctrl/view_1.html')

def content(request):
    global selected_axis
    global velo
    global accel
    working = ''
    if stat == 0:
        selected_axis = request.POST.get('axisnum')
        velo = request.POST.get('vel')
        accel = request.POST.get('accel')
        # global selected_axis = int(selected_axis_str)
        AxmSignalServoOn(int(selected_axis), True)
        #message.submit('서보켜짐')
        working = 'servo on'
    context = {'status': working, 'axis': selected_axis, 'accel': accel}
    return render(request, 'ctrl/view_2.html', context)

def motOff(request):
    AxmSignalServoOn(int(selected_axis), False)
    return redirect('AXTctrl:index')

def movEstop():
    AxmMoveEStop(int(selected_axis))

def movVel():
    AxmMoveVel(int(selected_axis), int(velo), int(accel), int(accel))

    #consumer.ChatConsumer().submit(message)

def re_status():
    AxmStatusGetCmdPos(int(selected_axis), ctypes.byref(c_cPosition))
    AxmStatusGetActPos(int(selected_axis), ctypes.byref(c_aPosition))
    AxmStatusReadVel(int(selected_axis), ctypes.byref(c_dVel))
    cPosition = c_cPosition.value
    aPosition = c_aPosition.value
    dVel = c_dVel.value
    return cPosition, aPosition, dVel

'''
def store_status(request, text_data):
    #status = Motion_status.objects.get(id=1)
    cPosition = None
    aPosition = None
    dVel = None
    status = None
    AxmStatusGetCmdPos(int(selected_axis), ctypes.byref(cPosition))
    AxmStatusGetActPos(int(selected_axis), ctypes.byref(aPosition))
    AxmStatusReadVel(int(selected_axis), ctypes.byref(dVel))
    i = 0
    if i == 0:
        status = Motion_status(cmdPos=cPosition, actPos=aPosition, cmdVel=dVel)
        status.save()
    else:
        status.cmdPos = cPosition
        status.actPos = aPosition
        status.cmdVel = dVel
        status.save()
    text_data = Motion_status.objects.get(id=1)
    context = {'text_data': text_data}
'''





