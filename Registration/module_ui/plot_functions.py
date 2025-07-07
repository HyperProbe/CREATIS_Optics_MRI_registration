from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QMainWindow
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QMovie

import numpy as np
import cv2, os

class MatplotlibWidget(FigureCanvas):

    def __init__(self, parent=None):
        fig = Figure()
        super().__init__(fig)
        self.setParent(parent)
        # self.ax = self.figure.add_subplot(111)  # Create axis once and reuse
        # self.ax.axis('off')
        self.cmap2 = 'hot'
        self.alpha = 0.5

        self.volume1 = None
        self.volume2 = None

        self.image1 = None
        self.image2 = None

        self.pt_MRI = None
        self.pt_Optics = None
        self.dot_artists = [None, None]  # To store plotted red dots

        #Skeleton drawing
        self.is_drawing_skeleton = False
        self.optics_mask_skeleton = None
        self.MRI_mask_skeleton = None
        self.last_point = None
        # self.pt_skeleton = []

        #event connections
        self.event_connections = {}


    def disconnect_all_events(self):
        for cid in self.event_connections.values():
            self.figure.canvas.mpl_disconnect(cid)
        self.event_connections.clear()

    def set_Images(self,image1,image2=None):

        if image1 is None and image2 is None:
            return


        self.figure.clear()
        self.ax = self.figure.add_subplot(111)  # Create axis once and reuse
        self.ax.clear()
        self.ax.axis('off')

        self.image1 = image1
        self.image2 = image2
        self.plot_image()


    def set_alpha(self,alpha):
        self.alpha = alpha
        self.plot_image()

    def clear_figure(self):
        self.figure.clear()
        # self.draw()
        self.draw_idle()

    def plot_image(self):

        if self.image1 is None:
            return

        self.figure.clear()
        self.ax = self.figure.add_subplot(111)  # Create axis once and reuse
        self.ax.clear()  # Clear previous image
        self.ax.axis('off')

        self.ax.imshow(self.image1)
        if self.image2 is not None:
            self.ax.imshow(self.image2, cmap=self.cmap2, alpha=self.alpha)
        self.ax.axis('off')
        # self.draw()  # Redraw the canvas
        self.draw_idle()


    def draw_optics_skeleton(self, img):

        if img is None:
            return

        print("In [draw_skeleton]")
        #Disconnect event before creating new ones
        self.disconnect_all_events()


        print("in [draw_skeleton]")
        #Skeleton drawing
        self.is_drawing_skeleton = False
        self.last_point = None
        self.optics_mask_skeleton = np.zeros((img.shape[0],img.shape[1]), dtype=np.uint8)
        # self.pt_skeleton = []


        self.figure.clear()
        self.ax = self.figure.add_subplot(111)  # Create axis once and reuse

        self.ax.clear()  # Clear previous image
        self.ax.axis('off')
        self.ax.imshow(img)
        # self.draw()  # Redraw the canvas


        self.draw_idle()

        def add_point(event):
            x, y = int(event.xdata), int(event.ydata)
            self.optics_mask_skeleton[y, x] = 255  # Update mask


            self.ax.plot(x, y, 'go', markersize=2)
            # self.figure.canvas.draw()

            self.draw_idle()

        def on_press(event):
            if event.button == 1 and event.inaxes == self.ax:
                self.ax.set_autoscale_on(False)
                self.last_point = (int(event.xdata), int(event.ydata))
                self.is_drawing_skeleton = True
                add_point(event)

        def on_motion(event):
            if self.is_drawing_skeleton and event.inaxes == self.ax:
                add_point(event)
                if self.last_point is not None:
                    cv2.line(self.optics_mask_skeleton, self.last_point, (int(event.xdata), int(event.ydata)), 255, 2)
                    self.last_point = (int(event.xdata), int(event.ydata))
        def on_release(event):
            if event.button == 1:
                self.last_point = None
                self.is_drawing_skeleton = False
                self.ax.relim()
                self.ax.autoscale_view()

        def on_scroll(event):
            """Zoom in or out based on mouse wheel scroll"""
            ax = self.ax
            xdata, ydata = event.xdata, event.ydata  # Mouse position in data coords

            if xdata is None or ydata is None:
                return  # Ignore scrolls outside the plot

            # Get current limits
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()

            # Calculate zoom scale
            _zoom_factor=1.2
            scale_factor = _zoom_factor if event.step > 0 else 1 / _zoom_factor

            # Compute new limits centered on the mouse position
            new_xlim = [
                xdata - (xdata - xlim[0]) * scale_factor,
                xdata + (xlim[1] - xdata) * scale_factor
            ]
            new_ylim = [
                ydata - (ydata - ylim[0]) * scale_factor,
                ydata + (ylim[1] - ydata) * scale_factor
            ]

            ax.set_xlim(new_xlim)
            ax.set_ylim(new_ylim)
            self.draw_idle()  # Refresh canvas


        cid = self.figure.canvas.mpl_connect("button_press_event", on_press)
        self.event_connections["button_press_event"] = cid

        cid = self.figure.canvas.mpl_connect("motion_notify_event", on_motion)
        self.event_connections["motion_notify_event"] = cid

        cid = self.figure.canvas.mpl_connect("button_release_event", on_release)
        self.event_connections["button_release_event"] = cid

        cid = self.figure.canvas.mpl_connect("scroll_event", on_scroll)
        self.event_connections["scroll_event"] = cid

    def draw_MRI_skeleton(self, img):

        if img is None:
            return

        print("In [draw_skeleton]")
        #Disconnect event before creating new ones
        self.disconnect_all_events()


        print("in [draw_skeleton]")
        #Skeleton drawing
        self.is_drawing_skeleton = False
        self.last_point = None
        self.MRI_mask_skeleton = np.zeros((img.shape[0],img.shape[1]), dtype=np.uint8)
        # self.pt_skeleton = []


        self.figure.clear()
        self.ax = self.figure.add_subplot(111)  # Create axis once and reuse

        self.ax.clear()  # Clear previous image
        self.ax.axis('off')
        self.ax.imshow(img)
        # self.draw()  # Redraw the canvas


        self.draw_idle()

        def add_point(event):
            x, y = int(event.xdata), int(event.ydata)
            self.MRI_mask_skeleton[y, x] = 255  # Update mask


            self.ax.plot(x, y, 'go', markersize=2)
            # self.figure.canvas.draw()

            self.draw_idle()

        def on_press(event):
            if event.button == 1 and event.inaxes == self.ax:
                self.ax.set_autoscale_on(False)
                self.last_point = (int(event.xdata), int(event.ydata))
                self.is_drawing_skeleton = True
                add_point(event)

        def on_motion(event):
            if self.is_drawing_skeleton and event.inaxes == self.ax:
                add_point(event)
                if self.last_point is not None:
                    cv2.line(self.MRI_mask_skeleton, self.last_point, (int(event.xdata), int(event.ydata)), 255, 2)
                    self.last_point = (int(event.xdata), int(event.ydata))
        def on_release(event):
            if event.button == 1:
                self.last_point = None
                self.is_drawing_skeleton = False
                self.ax.relim()
                self.ax.autoscale_view()

        def on_scroll(event):
            """Zoom in or out based on mouse wheel scroll"""
            ax = self.ax
            xdata, ydata = event.xdata, event.ydata  # Mouse position in data coords

            if xdata is None or ydata is None:
                return  # Ignore scrolls outside the plot

            # Get current limits
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()

            # Calculate zoom scale
            _zoom_factor=1.2
            scale_factor = _zoom_factor if event.step > 0 else 1 / _zoom_factor

            # Compute new limits centered on the mouse position
            new_xlim = [
                xdata - (xdata - xlim[0]) * scale_factor,
                xdata + (xlim[1] - xdata) * scale_factor
            ]
            new_ylim = [
                ydata - (ydata - ylim[0]) * scale_factor,
                ydata + (ylim[1] - ydata) * scale_factor
            ]

            ax.set_xlim(new_xlim)
            ax.set_ylim(new_ylim)
            self.draw_idle()  # Refresh canvas

        cid = self.figure.canvas.mpl_connect("button_press_event", on_press)
        self.event_connections["button_press_event"] = cid

        cid = self.figure.canvas.mpl_connect("motion_notify_event", on_motion)
        self.event_connections["motion_notify_event"] = cid

        cid = self.figure.canvas.mpl_connect("button_release_event", on_release)
        self.event_connections["button_release_event"] = cid

        cid = self.figure.canvas.mpl_connect("scroll_event", on_scroll)
        self.event_connections["scroll_event"] = cid

    def plot_two_images(self, image1, image2):

        if image1 is None and image2 is None:
            return

        #Disconnect event before creating new ones
        self.disconnect_all_events()


        self.figure.clear()
        self.ax1 = self.figure.add_subplot(121)  # Create axis once and reuse
        self.ax1.axis('off')
        self.ax1.imshow(image1)

        self.ax2 = self.figure.add_subplot(122)  # Create axis once and reuse
        self.ax2.axis('off')
        self.ax2.imshow(image2)

        # self.draw()
        self.draw_idle()

        # Initialize points

        #TODO: emit pt_MRI and pt_Optics !!!


        def onclick(event):
            if event.inaxes == self.ax1 :
                self.pt_MRI = [[int(event.xdata), int(event.ydata)]]
                if self.dot_artists[0]:
                    self.dot_artists[0].remove()  # Remove previous dot
                self.dot_artists[0] = self.ax1.plot(event.xdata, event.ydata, 'bo')[0]
                self.ax1.set_title("LEFT image ✔")
                self.ax2.set_title("Click on RIGHT image")
                self.figure.canvas.draw()

            elif event.inaxes == self.ax2:
                self.pt_Optics = [int(event.xdata), int(event.ydata)]
                if self.dot_artists[1]:
                    self.dot_artists[1].remove()  # Remove previous dot
                self.dot_artists[1] = self.ax2.plot(event.xdata, event.ydata, 'bo')[0]
                self.ax2.set_title("RIGHT image ✔")
                self.figure.canvas.draw()


        cid = self.figure.canvas.mpl_connect('button_press_event', onclick)
        self.event_connections["button_press_event"] = cid



    def plot_validation_landmarks(self, image1, image2, output_dir):
        if image1 is None and image2 is None:
            return

        #init validation points
        self.pt_MRI = []
        self.pt_Optics = []

        #Disconnect event before creating new ones
        self.disconnect_all_events()



        #Remove files if it exists
        if not os.path.exists(output_dir+"verification_landmarks"):
            os.mkdir(output_dir+"verification_landmarks")


        optics_file = output_dir+"verification_landmarks/optics.txt"
        if os.path.exists(optics_file):
            os.remove(optics_file)

        mri_file = output_dir+"verification_landmarks/mri.txt"
        if os.path.exists(mri_file):
                os.remove(mri_file)







        self.figure.clear()
        self.ax1 = self.figure.add_subplot(121)  # Create axis once and reuse
        self.ax1.axis('off')
        self.ax1.imshow(image1)

        self.ax2 = self.figure.add_subplot(122)  # Create axis once and reuse
        self.ax2.axis('off')
        self.ax2.imshow(image2)

        # self.draw()
        self.draw_idle()




        def onclick(event):
            #MRI landmarks
            if event.inaxes == self.ax1 :
                pos = (int(event.xdata), int(event.ydata))
                self.ax1.plot(pos[0], pos[1], 'ro')[0]

                self.figure.canvas.draw()

                self.pt_MRI.append(pos)
                points_mri = np.asarray(self.pt_MRI).astype(int)
                points_mri = np.unique(points_mri, axis=0)
                np.savetxt(mri_file,points_mri)





            elif event.inaxes == self.ax2:
                #Optics landmarks
                pos = (int(event.xdata), int(event.ydata))
                self.ax2.plot(pos[0], pos[1], 'bo')[0]


                self.figure.canvas.draw()

                self.pt_Optics.append(pos)
                points_optics = np.asarray(self.pt_Optics).astype(int)
                points_optics = np.unique(points_optics, axis=0)
                np.savetxt(optics_file,points_optics)


        def on_scroll(event):
            """Zoom in or out based on mouse wheel scroll"""

            #Choose correct axis
            if event.inaxes == self.ax1 :
                ax = self.ax1
            else:
                if event.inaxes == self.ax2 :
                    ax = self.ax2
                else:
                    return

            xdata, ydata = event.xdata, event.ydata  # Mouse position in data coords

            if xdata is None or ydata is None:
                return  # Ignore scrolls outside the plot

            # Get current limits
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()

            # Calculate zoom scale
            _zoom_factor=1.2
            scale_factor = _zoom_factor if event.step > 0 else 1 / _zoom_factor

            # Compute new limits centered on the mouse position
            new_xlim = [
                xdata - (xdata - xlim[0]) * scale_factor,
                xdata + (xlim[1] - xdata) * scale_factor
            ]
            new_ylim = [
                ydata - (ydata - ylim[0]) * scale_factor,
                ydata + (ylim[1] - ydata) * scale_factor
            ]

            ax.set_xlim(new_xlim)
            ax.set_ylim(new_ylim)
            self.draw_idle()  # Refresh canvas

        cid = self.figure.canvas.mpl_connect('button_press_event', onclick)
        self.event_connections["button_press_event"] = cid

        cid = self.figure.canvas.mpl_connect("scroll_event", on_scroll)
        self.event_connections["scroll_event"] = cid

class LoadingOverlay(QWidget):
    """A semi-transparent overlay with a centered loading animation"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Widget)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # Allows interaction with main window
        self.setStyleSheet("background-color: rgba(0, 0, 0, 150);")  # Semi-transparent background

        # Create QLabel for the GIF
        self.loading_label = QLabel(self)
        self.loading_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Enable transparency
        self.loading_label.setStyleSheet("background: transparent;")  # Ensure QLabel itself is transparent
        self.loading_movie = QMovie("../data/loading-image.gif")  # Ensure "loading.gif" is in the project folder
        self.loading_label.setMovie(self.loading_movie)

        # Center the GIF in the overlay
        layout = QHBoxLayout(self)
        layout.addWidget(self.loading_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        # self.hide()  # Initially hidden

        self.resize(self.parent().size())  # Ensure the overlay covers the entire window
        self.loading_movie.start()
        self.show()

    def closeEvent(self, event):
        """méthode exécutée lors de la fermeture de la fenêtre
        """
        self.loading_movie.stop() # arrête l'animation
        self.loading_label.clear() # efface le contenu du QLabel
        self.hide()




#############################################################################
class ThrobberWindow(QLabel):

    def __init__(self, parent=None):
    # def __init__(self, parent: QMainWindow = None):
        super(ThrobberWindow, self).__init__(parent)

        # image gif animée du throbber
        imagif = "../data/loading-image.gif"

        # configure la fenêtre
        self.setWindowTitle(" ") # supprime le titre de la fenêtre
        s = 160
        self.resize(s, s) # met une fenêtre carrée

        self.setFixedSize(self.width(), self.height()) # pas de redimenssionnement
        self.setStyleSheet("background: transparent;") # met un fond jaune
        # le contenu du QLabel sera au milieu (hor. et vert.)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # met seulement un cadre autour de la fenêtre du throbber
        # NB: mais on peut encore la déplacer à la souris!
        # newflags = Qt.Dialog
        # newflags |= Qt.CustomizeWindowHint  # permet la personnalisation
        # newflags &= ~Qt.WindowCloseButtonHint  # pas de case de fermeture
        # newflags &= ~Qt.WindowSystemMenuHint  # pas de menu de fenêtre
        # newflags &= ~Qt.WindowContextHelpButtonHint # pas de case "?"
        # self.setWindowFlags(newflags)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Widget | Qt.WindowStaysOnTopHint)

        # crée un movie avec le throbber sous forme d'image "gif" animée
        self.movie = QMovie(imagif)
        self.movie.setScaledSize(QSize(60, 60)) # fixe dimension 60x60

        self.setMovie(self.movie) # affecte le movie au QLabel
        self.movie.start() # lance l'animation du throbber

    #========================================================================
    def closeEvent(self, event):
        """méthode exécutée lors de la fermeture de la fenêtre
        """
        self.movie.stop() # arrête l'animation
        self.clear() # efface le contenu du QLabel
