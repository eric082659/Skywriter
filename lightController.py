import signal
import skywriter
import phue

class LightConfig:
    def __init__(self,transition_time,saturation,brightness):
        self.transition_time = transition_time
        self.saturation = saturation
        self.brightness = brightness

    def setTransitionTime(self, new_time):
        self.transition_time = new_time

    def setSaturation(self, new_sat):
        self.saturation = new_sat

    def setBrightness(self, new_bri):
        self.brightness = new_bri

class ListIter:
    def __init__(self, plist):
        self.list = plist
        self.index = 0

    def current(self):
        return(self.list[self.index])
    
    def next(self):
        if (self.index == len(self.list)-1):
            self.index=0
        else:
            self.index+=1
        return(self.list[self.index])

    def prev(self):
        if (self.index == 0):
            self.index = len(self.list)-1
        else:
           self.index-=1
        return(self.list[self.index])

IP = '192.168.0.100'
b = phue.Bridge(IP)

ctrl_grp = 4 #bedroom is group 4

config = LightConfig(2, 254, 254)
hues = {
    'red':0,
    'orange':6375,
    'yellow':12750,
    'green':21845,
    'teal':32768,
    'blue':43690,
    'uv':46556,
    'purple':49151,
    'magenta':54613
}
temps = {
    'warm':500,
    'cool':153
}

hue_commands = [
    {'transitiontime':config.transition_time, 'sat':config.saturation, 'bri':config.brightness, 'hue':hues['red']},
    {'transitiontime':config.transition_time, 'sat':config.saturation, 'bri':config.brightness, 'hue':hues['orange']},
    {'transitiontime':config.transition_time, 'sat':config.saturation, 'bri':config.brightness, 'hue':hues['yellow']},
    {'transitiontime':config.transition_time, 'sat':config.saturation, 'bri':config.brightness, 'hue':hues['green']},
    {'transitiontime':config.transition_time, 'sat':config.saturation, 'bri':config.brightness, 'hue':hues['teal']},
    {'transitiontime':config.transition_time, 'sat':config.saturation, 'bri':config.brightness, 'hue':hues['blue']},
    {'transitiontime':config.transition_time, 'sat':config.saturation, 'bri':config.brightness, 'hue':hues['uv']},
    {'transitiontime':config.transition_time, 'sat':config.saturation, 'bri':config.brightness, 'hue':hues['purple']},
    {'transitiontime':config.transition_time, 'sat':config.saturation, 'bri':config.brightness, 'hue':hues['magenta']}
]

temp_commands = [
    {'transitiontime':config.transition_time, 'bri':config.brightness, 'ct':temps['warm']},
    {'transitiontime':config.transition_time, 'bri':config.brightness, 'ct':temps['cool']}
]

on_status = [True, False]

hue_iter = ListIter(hue_commands)
temp_iter = ListIter(temp_commands)
on_iter = ListIter(on_status)

@skywriter.double_tap()
def doubletap(position):
    print('Double tap!', position)
    b.set_group(ctrl_grp,'on',on_iter.next())

@skywriter.flick()
def flick(start,finish):
    print('flick captured: ', start, finish)
    if (on_iter.current() == True):
        if (finish == 'north'):
            b.set_group(ctrl_grp, hue_iter.prev())

        if (finish == 'south'):
            b.set_group(ctrl_grp, hue_iter.next())

        if (finish == 'east'):
            if(config.brightness>84):
                config.setBrightness(config.brightness-84)
            else:
                config.setBrightness(254)
            b.set_group(ctrl_grp, 'bri', config.brightness)

        if (finish == 'west'):
            b.set_group(ctrl_grp, temp_iter.next())

signal.pause()