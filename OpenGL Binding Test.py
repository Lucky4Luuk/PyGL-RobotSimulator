from lib.glfunctions import GL_BLEND, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, \
                        GL_MODELVIEW, GL_ONE_MINUS_SRC_ALPHA, GL_PROJECTION, GL_QUADS, GL_RENDERER, \
                        GL_SRC_ALPHA, GL_VENDOR, GL_VERSION, GL_TRIANGLES, \
                        glBegin, glClear, glBlendFunc, glClearColor, \
                        glClearDepth, glColor3f, glEnable, glEnd, glGetString, glFlush, \
                        glLoadIdentity, glMatrixMode, glOrtho, glRotatef, glVertex3f, glViewport

from lib.tk_win import TkGLWin

from tkinter import Tk, YES, BOTH

class Cube(TkGLWin):

    rot = 0
    vertices = []
    faces = []
    mode = 1

    def loadModel(self,filename):
        self.vertices = []
        self.faces = []
        file = open("models/"+str(filename))
        for line in file :
            if line.startswith("v ") :
                vdata = line.split("v ")[1].split(" ")
                x = float(vdata[0])
                y = float(vdata[1])
                z = float(vdata[2].split("\n")[0])
                self.vertices.append([x,y,z])
        file.seek(0)
        for line in file :
            if line.startswith("f ") :
                fdata = line.split("f ")[1].split(" ")
                v1 = int(fdata[0].split("//")[0])-1
                v2 = int(fdata[1].split("//")[0])-1
                v3 = int(fdata[2].split("//")[0])-1
                self.faces.append([[self.vertices[v1][0],self.vertices[v1][1],self.vertices[v1][2]],[self.vertices[v2][0],self.vertices[v2][1],self.vertices[v2][2]],[self.vertices[v3][0],self.vertices[v3][1],self.vertices[v3][2]]])
        file.close()

    def on_resize(self, event, arg=None):

        if event:
            w = event.width
            h = event.height
        else:
            if arg:
                w = arg['w']
                h = arg['h']
            else:
                raise Exception

        dx = w/h
        glViewport(0, 0, w, h)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(
            -2 * dx,
            2 * dx,
            -2,
            2,
            -2,
            2
        )

    def set_ortho_view(self):
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0, 0, 0, 0)
        glClearDepth(1)
        glMatrixMode(GL_PROJECTION)

        self.on_resize(None, arg={
            'w': self.winfo_width(),
            'h': self.winfo_height()
        })

        print('%s - %s - %s' % (
            glGetString(GL_VENDOR),
            glGetString(GL_VERSION),
            glGetString(GL_RENDERER)
        ))

    def render_scene(self):

        self.rot += .5

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(self.rot, 1, 1, 0.5)

        #Draw a simple cube or model, based on self.mode

        if self.mode == 0 :
            glBegin(GL_QUADS)
            
            glColor3f(0, 1, 0)
            glVertex3f(1, 1, -1)
            glVertex3f(-1, 1, -1)
            glVertex3f(-1, 1, 1)
            glVertex3f(1, 1, 1)

            glColor3f(1, 0.5, 0)
            glVertex3f(1, -1, 1)
            glVertex3f(-1, -1, 1)
            glVertex3f(-1, -1, -1)
            glVertex3f(1, -1, -1)

            glColor3f(1, 0, 0)
            glVertex3f(1, 1, 1)
            glVertex3f(-1, 1, 1)
            glVertex3f(-1, -1, 1)
            glVertex3f(1, -1, 1)

            glColor3f(1, 1, 0)
            glVertex3f(1, -1, -1)
            glVertex3f(-1, -1, -1)
            glVertex3f(-1, 1, -1)
            glVertex3f(1, 1, -1)

            glColor3f(0, 0, 1)
            glVertex3f(-1, 1, 1)
            glVertex3f(-1, 1, -1)
            glVertex3f(-1, -1, -1)
            glVertex3f(-1, -1, 1)

            glColor3f(1, 0, 1)
            glVertex3f(1, 1, -1)
            glVertex3f(1, 1, 1)
            glVertex3f(1, -1, 1)
            glVertex3f(1, -1, -1)
        else :
            glBegin(GL_TRIANGLES)
            for f in self.faces :
                glColor3f(1,1,1)
                glVertex3f(f[0][0],f[0][1],f[0][2])
                glVertex3f(f[1][0],f[1][1],f[1][2])
                glVertex3f(f[2][0],f[2][1],f[2][2])

        glEnd()

        glFlush()


root = Tk()

cube = Cube(root, width=800, height=600)

cube.loadModel("monkeyblender.obj")

cube.pack(fill=BOTH, expand=YES)

cube.mainloop()
