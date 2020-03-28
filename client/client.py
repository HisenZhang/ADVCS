'''
@Author: HisenZhang <zhangz29@rpi.edu>
@Date: 2020-03-27 15:13:50
@LastEditors: HisenZhang <zhangz29@rpi.edu>
@LastEditTime: 2020-03-27 17:27:39
@Description: client based on pygame
'''
#!/usr/bin/env python
# coding=utf-8


import pygame as pg
import sys
import time
import requests as rq

from display import *
from config import *

pg.init()

max_res = pg.display.list_modes()[0]
display_flags = pg.FULLSCREEN | pg.HWSURFACE | pg.DOUBLEBUF

screen = pg.display.set_mode((900, 600))
pg.display.set_caption('UTC Clock - OFFILNE')

time_font = pg.font.SysFont('Ubuntu', 50)
caption_font = pg.font.SysFont('Ubuntu', 60)
status_font = pg.font.SysFont('Ubuntu', 20)
UTC_caption = caption_font.render("UTC", True, WHITE)
local_caption = caption_font.render(
    time.strftime('%Z', time.localtime()),
    True,
    WHITE)

status = (False, '')  # err, msg


def time_format(t):
    time_list = t.split(' ')
    needed = [time_list[3], time_list[1], time_list[2]]
    return ' '.join(needed)


while True:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key in {pg.K_q, pg.K_ESCAPE}:
                pg.quit()
                sys.exit()
            if event.key == pg.K_f:
                if is_fullscreen:
                    pg.display.set_mode((900, 600))
                else:
                    pg.display.set_mode(max_res, display_flags)
                is_fullscreen = not is_fullscreen
            if event.key == pg.K_r:
                auth = rq.post('http://'+conf['server']['addr']+':'+str(conf['server']['port'])+'/auth/',
                               {'username': conf['credentials']['username'],
                                'token': conf['credentials']['token']})
                if auth.status_code == 200:
                    if not auth.json()['error']:
                        pg.display.set_caption(
                            'UTC Clock @ ' + conf["credentials"]["username"])
                        status = (False, "Logged in as " +
                                  conf["credentials"]["username"])
                    else:
                        status = (True, auth.json()['msg'])

    screen.fill(BLACK)

    screen.blit(UTC_caption, (100, 100))
    time_string = time_font.render(
        time_format(time.asctime(time.gmtime())),
        True,
        YELLOW)
    screen.blit(time_string, (100, 200))

    screen.blit(local_caption, (100, 350))
    local_string = time_font.render(
        time_format(time.asctime()),
        True,
        YELLOW)
    screen.blit(local_string, (100, 450))

    if status[0]:
        screen.blit(status_font.render(status[1], True, YELLOW), (100, 50))
    else:
        screen.blit(status_font.render(status[1], True, WHITE), (100, 50))

    pg.display.flip()
    # time.sleep(0.05)
