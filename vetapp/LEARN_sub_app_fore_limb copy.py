from os import path
# from vetapp.vetapp.sub2_app_fore_limb import create_cleaned_name
import vtk
import re

basepath = path.dirname(__file__)


# !/bin/env python

"""
Simple VTK example in Python to load an STL mesh and display with 
a manipulator.
"""
colors = vtk.vtkNamedColors()

STL_FILES =[
    'Scapula.stl', 'Humerus.stl', 'Radius.stl', 'Ulna.stl',
    'OsCarpiAccessorium.stl', 'OsCarpiIntermedioRadiale.stl',
    'OsCarpiUlnare.stl', 'OsCarpaleQuartum.stl','OsCarpaleSecundum.stl', 
    'OsCarpaleTertium.stl', 'OsCarpaleQuartum.stl', 'OsMetacarpalePrimum.stl',
    'OsMetacarpaleSecundum.stl', 'OsMetacarpaleTertium.stl', 'OsMetacarpaleQuartum.stl',
    'OsMetacarpaleQuintum.stl', 'PhalanxProximalis1.stl', 'PhalanxProximalis2.stl',
    'PhalanxProximalis3.stl', 'PhalanxProximalis4.stl', 'PhalanxProximalis5.stl',
    'PhalanxMedia2.stl', 'PhalanxMedia3.stl', 'PhalanxMedia4.stl', 'PhalanxMedia5.stl',
    'PhalanxDistalis1.stl', 'PhalanxDistalis2.stl', 'PhalanxDistalis3.stl', 
    'PhalanxDistalis4.stl', 'PhalanxDistalis5.stl',
]

class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):
    '''Class to '''
    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)

        self.LastPickedActor = None
        self.LastPickedProperty = vtk.vtkProperty()

    def leftButtonPressEvent(self, obj, event):
        clickPos = self.GetInteractor().GetEventPosition()

        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())

        # get the new
        self.NewPickedActor = picker.GetActor()
        print(self.NewPickedActor)
        for k, v in bone_objects.items():
            print(v.name)
            if self.NewPickedActor == v:
                print(k)

        # If something was selected
        if self.NewPickedActor:
            # print('Neuer Actor: ', self.NewPickedActor.GetProperty())
            # If we picked something before, reset its property
            if self.LastPickedActor:
                self.LastPickedActor.GetProperty().DeepCopy(
                    self.LastPickedProperty)

            # Save the property of the picked actor so that we can
            # restore it next time
            self.LastPickedProperty.DeepCopy(self.NewPickedActor.GetProperty())
            # Highlight the picked actor by changing its properties
            self.NewPickedActor.GetProperty().SetColor(
                colors.GetColor3d('Green'))
            self.NewPickedActor.GetProperty().SetDiffuse(1.0)
            self.NewPickedActor.GetProperty().SetSpecular(0.0)
            # self.NewPickedActor.GetProperty().EdgeVisibilityOn()

            # save the last picked actor
            self.LastPickedActor = self.NewPickedActor

        self.OnLeftButtonDown()
        return





class Bone_Object():
    def __init__(self, name) -> None:
        self.__name = name
        self.__actor = None
    
    @property
    def name(self):
        return self.__name

    @property
    def actor(self):
        return self.__actor

    def loadStl(self, name):
        filepath = path.abspath(path.join(basepath, "..", "data\\fore_limb", name))
        """Load the given STL file, and return a vtkPolyData object for it."""
        reader = vtk.vtkSTLReader()
        reader.SetFileName(filepath)
        reader.Update()

        polydata = reader.GetOutput()
        return polydata, reader

    def load_data(self, ren, balloonWidget, stl_name):
        ''' Load the data according to  
        STL_FILES List'''

        polydata, reader = self.loadStl(stl_name)
        my_bone_actor = ren.AddActor(polyDataToActor(polydata, balloonWidget, self.__name))
        # print('my_actor:', my_bone_actor, self.__name)
        self.__actor = my_bone_actor
        return ren, reader

    

def create_cleaned_name(name):
    name_list = []
    name_list = re.findall('[A-Z][^A-Z]*', name)
    name = ' '.join(name_list)
    return name[:-4]

def polyDataToActor(polydata, balloonWidget, name):
    """Wrap the provided vtkPolyData object in a mapper and an 
    actor, returning the actor."""

    mapper = vtk.vtkPolyDataMapper()
    
    if vtk.VTK_MAJOR_VERSION >= 6:
        mapper.SetInputData(polydata)
    else:
        mapper.SetInputConnection(polydata.GetProducerPort())
    bone_actor = vtk.vtkActor()
    
    bone_actor.SetMapper(mapper)

    bone_actor.GetProperty().SetDiffuseColor(0.5, 0.5, 1.0)
    bone_actor.GetProperty().SetDiffuse(.8)
    bone_actor.GetProperty().SetSpecular(.5)
    bone_actor.GetProperty().SetSpecularColor(colors.GetColor3d('White'))
    bone_actor.GetProperty().SetSpecularPower(30.0)

    clean_name = create_cleaned_name(name)
    balloonWidget.AddBalloon(bone_actor, clean_name)

    return bone_actor


######


'''#Create a mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(textSource.GetOutputPort())

actor =vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1.0, 0.0, 0.0)

#Create a renderer, render window, and interactor
renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

#Add the actor to the scene
renderer.AddActor(actor)
renderer.SetBackground(1,1,1); # Background color white

#Render and interact
renderWindow.Render()
renderWindowInteractor.Start()'''

def main():
    # Create a rendering window and renderer
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    # Create a RenderWindowInteractor to permit manipulating the camera
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    # style = vtk.vtkInteractorStyleTrackballCamera()
    style = MouseInteractorHighLightActor()
    style.SetDefaultRenderer(ren)
    iren.SetInteractorStyle(style)
    # all for text rendering
    #mapper.SetInputConnection(textSource.GetOutputPort())
    #actor_text = vtk.vtkActor()
    #actor_text.SetMapper(mapper)
    #actor_text.GetProperty().SetColor(1.0, 0.0, 0.0)
    
     # Create the widgets
    balloonRep = vtk.vtkBalloonRepresentation()
    balloonRep.SetBalloonLayoutToImageRight()

    balloonWidget = vtk.vtkBalloonWidget()
    balloonWidget.SetInteractor(iren)
    balloonWidget.SetRepresentation(balloonRep)
    
    # Load and transform all STL-files from whole skeleton
    global bone_objects 
    bone_objects = {}
    for file in STL_FILES:
        bone_objects[file] = Bone_Object(file)
        #global bone_objects
    #print(bone_objects)
    
    for name, bone_object in bone_objects.items():
        #print(bone_object)
        ren, reader = bone_object.load_data(ren, balloonWidget, name)
    #iren.Initialize()

    ren.SetBackground(0.1, 0.1, 0.1)
    #renderer.AddActor(actor_text)

   

    '''for name, bone_object in bone_objects.items():
        print('dies', bone_object.actor)
        balloonWidget.AddBalloon(bone_object.actor(name), name)'''
        # Add the actors to the scene
        #renderer.AddActor(sphereActor)
    #renderer.AddActor(regularPolygonActor)
    #renderer.SetBackground(colors.GetColor3d("Wheat"))

    # Render an image (lights and cameras are created automatically)
    #renderWindow.Render()
    #balloonWidget.EnabledOn()
    
    # enable user interface interactor
    reader.Update()
    renWin.Render()
    balloonWidget.EnabledOn()
    
    iren.Start()
    iren.Initialize()
    reader.Update()

    
    #iren.Start()


if __name__ == "__main__":

    main()