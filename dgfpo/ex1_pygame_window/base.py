# !coding=utf-8
import pygame
import sys
from input import Input

class Base(object):
    def __init__(self, screenSize=[512, 512]):
        pygame.init()

        displayFlags = pygame.DOUBLEBUF | pygame.OPENGL  # double buf 什么叫双缓冲区 ?

        # initialize buffers to perform antialiasing
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)

        # use core OpenGL profile for cross-platform compatibility
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK,
            pygame.GL_CONTEXT_PROFILE_CORE
            # disable deprecated features
        )

        # create and display the window
        self.screen = pygame.display.set_mode(screenSize, displayFlags)
        # set the text that appears in the title bar of the window
        pygame.display.set_caption("Graphics Window")

        # determine if main loop is active
        self.running = True

        self.clock = pygame.time.Clock()

        # manage user input
        self.input = Input()

    def initialize(self):
        pass

    # implement by extending class
    def update(self):
        pass

    def run(self):
        ## startup ##
        self.initialize()

        ## main loop ##
        while self.running:
            ## process input ##

            ## update ##
            self.update()

            ## render ##
            pygame.display.flip()

            ## process input ##
            self.input.update()
            if self.input.quit:
                self.running = False

            ## pause if necessary to aachieve 60 fps ##
            self.clock.tick(60)

        ## shutdown ##
        pygame.quit()
        sys.exit()
