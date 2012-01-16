
import math

from muntjac.api import Application, Window

from muntjac.addon.canvas.canvas import Canvas


class CanvasApp(Application):

    def init(self):
        self.setMainWindow(Window(self.__class__.__name__))

        canvas = Canvas()
        canvas.setWidth('400px')
        canvas.setHeight('400px')

        # Draw some shapes to the canvas
        canvas.saveContext()
        canvas.clear()
        canvas.translate(175, 175)
        canvas.scale(1.6, 1.6)
        for i in range(1, 6):
            canvas.saveContext()
            canvas.setFillStyle('rgb(%d,%d,255)' % (51 * i, 255 - (51 * i)))

            for _ in range(i * 6):
                canvas.rotate((math.pi * 2) / (i * 6))
                canvas.beginPath()
                canvas.arc(0, i * 12.5, 5, 0, math.pi * 2, True)
                canvas.fill()

            canvas.restoreContext()

        canvas.restoreContext()

        canvas.drawImage(
                'http://www.google.ru/intl/en_com/images/srpr/logo1w.png',
                10, 10)

        self.getMainWindow().addComponent(canvas)


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(CanvasApp, nogui=True, forever=True, debug=True)
