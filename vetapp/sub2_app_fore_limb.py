from os import path
import vtk
import re

basepath = path.dirname(__file__)


# !/bin/env python

"""
Simple VTK example in Python to load an STL mesh and display with 
a manipulator.
"""
colors = vtk.vtkNamedColors()


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


class Bone_Object():
    def __init__(self, name) -> None:
        self.__name = name
        self.__actor = None

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
        #print('LOAD STL', polydata)
        return polydata, reader

    def load_data(self, ren, balloonWidget, text_widget, text_actor, stl_name):
        ''' Load and transform the data according to the 
        DATA_TRANSFORMATIONS DICTIONARY. OPERATIONS-Functions 
        will be called and applied accordingly. Tranformations
        are found in the according transformation-functions'''

        polydata, reader = self.loadStl(stl_name)
        bone_actor = ren.AddActor(poly_data_to_actor(polydata, balloonWidget, self.__name))
        text_actor = ren.AddActor(text_to_actor(text_widget, text_actor, self.__name))
        # print('my_actor:', my_bone_actor, self.__name)
        self.__actor = bone_actor
        #my_bounds = polydata.getbounds()
        #print(my_bounds)
        return ren, reader
    
def text_to_actor(text_widget, text_actor, name):
    cleaned_name = create_cleaned_name(name)
    text_actor = vtk.vtkTextActor()
    text_actor.SetInput(cleaned_name)
    text_actor.GetTextProperty().SetColor(colors.GetColor3d('Cyan'))

    
    #text_representation.GetPositionCoordinate().SetValue(0.15, 0.15)
    #text_representation.GetPosition2Coordinate().SetValue(0.7, 0.2)
    #print(text_representation)
    return text_actor

def create_cleaned_name(name):
    name_list = []
    name_list = re.findall('[A-Z][^A-Z]*', name)
    name = ' '.join(name_list)
    cleaned_name = name[:-4]
    return cleaned_name

def poly_data_to_actor(polydata, balloonWidget, name):
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
    cleaned_name = create_cleaned_name(name)
    print(name)
    #print(balloonWidget)
    balloonWidget.AddBalloon(bone_actor, cleaned_name)
    
    
    #balloonWidget.EnabledOn()
    #print('polyActor', bone_actor)
    return bone_actor


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
    # Create selection(selected bone turns green)
    style = MouseInteractorHighLightActor()
    style.SetDefaultRenderer(ren)
    iren.SetInteractorStyle(style)
    
    # Create the widgets to display name of the objects
    # widgetman = vtk.widgetManager.setRenderer(ren)
    balloonRep = vtk.vtkBalloonRepresentation()
    balloonRep.SetBalloonLayoutToImageRight()

    balloonWidget = vtk.vtkBalloonWidget()
    balloonWidget.SetInteractor(iren)
    balloonWidget.SetRepresentation(balloonRep)
    
    # alternative Text representation (fromTExtWidget example)
    # Create the TextActor
    text_actor = vtk.vtkTextActor()
    text_widget = vtk.vtkTextWidget()
    text_representation = vtk.vtkTextRepresentation()

    # Create a dictionary with {name:bone_object} of all
    # bones in STL_FILES
    bone_objects = {}
    for file in STL_FILES:
        bone_objects[file] = Bone_Object(file)

    # Load and transform all STL-files from whole skeleton
    for name, bone_object in bone_objects.items():
        ren, reader = bone_object.load_data(ren, balloonWidget, text_widget, text_actor, name)

    ren.SetBackground(0.1, 0.1, 0.1)

    # SelectableOn/Off indicates whether the interior region of the widget can be
    # selected or not. If not, then events (such as left mouse down) allow the user
    # to "move" the widget, and no selection is possible. Otherwise the
    # SelectRegion() method is invoked.
    
    text_widget.SetRepresentation(text_representation)
    text_widget.SetInteractor(iren)
    text_widget.SetTextActor(text_actor)
    text_widget.SelectableOff()
    text_widget.On()
    reader.Update()
    renWin.Render()
    balloonWidget.EnabledOn()
    # balloonWidget.enablePicking()
    # print(balloonWidget)
    iren.Initialize()

    iren.Start()


if __name__ == "__main__":

    main()