'''
@author: avalanchy (at) google mail dot com
@version: 0.1; python 2.7; pygame 1.9.2pre; SDL 1.2.14; MS Windows XP SP3
@date: 2012-04-08
@license: This document is under GNU GPL v3

README on the bottom of document.

@font: from http://www.dafont.com/coders-crux.font
      more abuot license you can find in data/coders-crux/license.txt
'''

import Ui
import pygame
from pygame.locals import *


if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()


class Menu:
    list = []
    pola = []
    #font_size = 15
    # font_path = 'data/coders_crux/coders_crux.ttf'
    font = pygame.font.SysFont("Arial", 16)  # pygame.font.Font
    destination_surface = pygame.Surface
    ilosc_pol = 0
    background_color = (0, 0, 0)  # (51, 51, 51)
    text_color = (255, 255, 255)  # (255, 255, 153)
    mark_color = (0, 200, 255)  # (153, 102, 255)
    pozycja_zaznaczenia = 0
    pozycja_wklejenia = (0,0)
    menu_width = 0
    menu_height = 0
    selected_song = ''

    class Pole:
        tekst = ''
        pole = pygame.Surface
        pole_rect = pygame.Rect
        zaznaczenie_rect = pygame.Rect

    def move_menu(self, top, left):
        self.pozycja_wklejenia = (top,left) 

    def set_colors(self, text, selection, background):
        self.background_color = background
        self.text_color =  text
        self.mark_color = selection
        
    # def set_fontsize(self,font_size):
    #    self.font_size = font_size
        
    # def set_font(self, path):
    #    self.font_path = path
        
    def get_position(self):
        return self.pozycja_zaznaczenia
    
    def init(self, song_list, dest_surface):
        self.list = song_list
        self.destination_surface = dest_surface
        self.ilosc_pol = len(self.list)
        self.stworz_strukture()        
        
    def draw(self,przesun=0):
        if przesun:
            self.pozycja_zaznaczenia += przesun 
            if self.pozycja_zaznaczenia == -1:
                self.pozycja_zaznaczenia = self.ilosc_pol - 1
            self.pozycja_zaznaczenia %= self.ilosc_pol
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.background_color)
        zaznaczenie_rect = self.pola[self.pozycja_zaznaczenia].zaznaczenie_rect
        pygame.draw.rect(menu,self.mark_color,zaznaczenie_rect)

        for i in range(self.ilosc_pol):
            menu.blit(self.pola[i].pole,self.pola[i].pole_rect)
        self.destination_surface.blit(menu,self.pozycja_wklejenia)
        return self.pozycja_zaznaczenia

    def stworz_strukture(self):
        przesuniecie = 0
        self.menu_height = 0
        # self.font = pygame.font.Font(self.font_path, self.font_size)
        for i in range(self.ilosc_pol):
            self.pola.append(self.Pole())
            self.pola[i].tekst = self.list[i]
            self.pola[i].pole = self.font.render(self.pola[i].tekst, 1, self.text_color)

            self.pola[i].pole_rect = self.pola[i].pole.get_rect()
            przesuniecie = int(16 * 0.2)

            height = self.pola[i].pole_rect.height
            self.pola[i].pole_rect.left = przesuniecie
            self.pola[i].pole_rect.top = przesuniecie+(przesuniecie*2+height)*i

            width = self.pola[i].pole_rect.width+przesuniecie*2
            height = self.pola[i].pole_rect.height+przesuniecie*2            
            left = self.pola[i].pole_rect.left-przesuniecie
            top = self.pola[i].pole_rect.top-przesuniecie

            self.pola[i].zaznaczenie_rect = (left,top ,width, height)
            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height
        x = 10
        y = 50
        mx, my = self.pozycja_wklejenia
        self.pozycja_wklejenia = (x+mx, y+my) 


if __name__ == "__main__":
    import sys
    surface = pygame.display.set_mode((854,480)) #0,6671875 and 0,(6) of HD resoultion
    surface.fill((51,51,51))
    '''First you have to make an object of a *Menu class.
    *init take 2 arguments. List of fields and destination surface.
    Then you have a 4 configuration options:
    *set_colors will set colors of menu (text, selection, background)
    *set_fontsize will set size of font.
    *set_font take a path to font you choose.
    *move_menu is quite interseting. It is only option which you can use before 
    and after *init statement. When you use it before you will move menu from 
    center of your surface. When you use it after it will set constant coordinates. 
    Uncomment every one and check what is result!
    *draw will blit menu on the surface. Be carefull better set only -1 and 1 
    arguments to move selection or nothing. This function will return actual 
    position of selection.
    *get_postion will return actual position of seletion. '''
    menu = Menu()#necessary
    #menu.set_colors((255,255,255), (0,0,255), (0,0,0))#optional
    #menu.set_fontsize(64)#optional
    #menu.set_font('data/couree.fon')#optional
    #menu.move_menu(100, 99)#optional
    menu.init(['Start','Options','Quit'], surface)#necessary
    #menu.move_menu(0, 0)#optional
    menu.draw()#necessary
    
    pygame.key.set_repeat(199,69)#(delay,interval)
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    menu.draw(-1) #here is the Menu class function
                if event.key == K_DOWN:
                    menu.draw(1) #here is the Menu class function
                if event.key == K_RETURN:
                    if menu.get_position() == 2:#here is the Menu class function
                        pygame.display.quit()
                        sys.exit()                        
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    sys.exit()
                pygame.display.update()
            elif event.type == QUIT:
                pygame.display.quit()
                sys.exit()
        pygame.time.wait(8)
        