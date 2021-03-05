from os import path, rename
# from vetapp.vetapp.sub2_app_fore_limb import create_cleaned_name
import vtk
import re

basepath = path.dirname(__file__)


# !/bin/env python


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
        # print(self.NewPickedActor)
        '''for k, v in bone_objects.items():
            print(v.name)
            if self.NewPickedActor == v:
                print(k)'''

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

class CreateScene():
    def __init__(self, name) -> None:
        self.__name = name
        self.__ren = None
        self.__renWin = None
        self.__iren = None
        self.__style = None

    @property 
    def name(self):
        return self.__name

    # Create a rendering window 
    def create_ren(self):
        self.__ren = vtk.vtkRenderer()

    @property
    def ren(self):
        return self.__ren

    # Create a renderer
    def create_ren_win(self):
        self.__renWin = vtk.vtkRenderWindow()
        self.__renWin.AddRenderer(self.__ren)
        
    
    @property
    def renWin(self):
        return self.__renWin
    

    # Create a RenderWindowInteractor to permit manipulating the camera
    def create_iren(self):
        self.__iren = vtk.vtkRenderWindowInteractor()
        self.__iren.SetRenderWindow(self.__renWin)

    @property
    def iren(self):
        return self.__iren

    # style = vtk.vtkInteractorStyleTrackballCamera()
    def create_style(self):
        self.__style = MouseInteractorHighLightActor()
        self.__style.SetDefaultRenderer(self.ren)
        self.__iren.SetInteractorStyle(self.__style)

    @property
    def stlye(self):
        return self.__style

    def create_szene(self):
        self.create_ren()
        self.create_ren_win()
        self.create_iren()
        self.create_style()
        return self.__ren, self.__renWin, self.__iren


class CreateWidgets():
    def __init__(self, name, iren) -> None:
        self.__name = name
        self.__iren = iren
        self.__balloonRep = None

    @property
    def name(self):
        return self.__name

    # Create the widgets representation
    def create_balloon_rep(self):
        self.__balloonRep = vtk.vtkBalloonRepresentation()
        self.__balloonRep.SetBalloonLayoutToImageRight()

    @property
    def balloonRep(self):
        return self.__balloonRep

    def create_balloon_widget(self):
        self.__balloonWidget = vtk.vtkBalloonWidget()
        self.__balloonWidget.SetInteractor(self.__iren)
        self.__balloonWidget.SetRepresentation(self.__balloonRep)

    @property
    def balloonWidget(self):
        return self.__balloonWidget

    def create_widgets(self):
        self.create_balloon_rep()
        self.create_balloon_widget()
        return self.__balloonWidget, self.__iren


class Bone_Object():
    def __init__(self, name) -> None:
        self.__name = name
        self.__actor = None
        self.__polydata = None
        self.__reader = None
    
    @property
    def name(self):
        return self.__name

    @property
    def actor(self):
        return self.__actor

    def create_stl_reader(self):
        self.__reader = vtk.vtkSTLReader()

    @property
    def reader(self):
        return self.__reader

    def update_reader(self, reader, filepath):
        reader.SetFileName(filepath)
        reader.Update()
        return reader

    def loadStl(self):
        filepath = path.abspath(path.join(basepath, "..", "data\\fore_limb", self.name))
        """Load the given STL file, and return a vtkPolyData object for it."""
        self.create_stl_reader()
        self.__reader = self.update_reader(self.reader, filepath)
        polydata = self.__reader.GetOutput()
        self.__polydata = polydata
        return polydata, self.__reader

    @property
    def polydata(self):
        return self.__polydata

class AddActorAndWidget():
    def __init__(self, ren, actor_dict, balloonWidget) -> None:
        self.__ren = ren
        self.__actor_dict = actor_dict
        self.__balloonWidget = balloonWidget
        print(balloonWidget)
    
    def add_actor_and_widget(self):
        for name, actor in self.__actor_dict.items():
            cleaned_name = create_cleaned_name(name)
            self.__balloonWidget.AddBalloon(actor, cleaned_name)
            self.__ren.AddActor(actor)
            print(cleaned_name)
            # print(self.__actor_dict.get('Scapula.stl'))
        print(self.__balloonWidget.GetBalloonString(self.__actor_dict.get('Scapula.stl')))
        balloonWidget = self.__balloonWidget
        print(balloonWidget.GetBalloonString(self.__actor_dict.get('Scapula.stl')))
        print(self.__ren)
        # print(self.__balloonWidget)
        return self.__ren, balloonWidget


class CreateActor():
    def __init__(self, stl_name, polydata) -> None:
        self.__stl_name = stl_name
        self.__polydata = polydata

    def polyDataToActor(self):
        """Wrap the provided vtkPolyData object in a mapper and an 
        actor, returning the actor."""
        mapper = vtk.vtkPolyDataMapper()
        
        if vtk.VTK_MAJOR_VERSION >= 6:
            mapper.SetInputData(self.__polydata)
        else:
            mapper.SetInputConnection(self.__polydata.GetProducerPort())
        self.__bone_actor = vtk.vtkActor()
        
        self.__bone_actor.SetMapper(mapper)
        self.__bone_actor.GetProperty().SetDiffuseColor(0.5, 0.5, 1.0)
        self.__bone_actor.GetProperty().SetDiffuse(.8)
        self.__bone_actor.GetProperty().SetSpecular(.5)
        self.__bone_actor.GetProperty().SetSpecularColor(colors.GetColor3d('White'))
        self.__bone_actor.GetProperty().SetSpecularPower(30.0)
        #get_user_input_name(clean_name)
        return self.__bone_actor
    

def create_cleaned_name(name):
    name_list = []
    name_list = re.findall('[A-Z][^A-Z]*', name)
    name = ' '.join(name_list)
    return name[:-4]


def widget_callback(obj, event):
    print(f'Name: {obj}')



def main():

    my_scene = CreateScene('my_scene')
    ren, renWin, iren = my_scene.create_szene()

    my_widgets = CreateWidgets('my_widgets', iren)
    balloonWidget, iren = my_widgets.create_widgets()
    
    # Load and transform all STL-files from whole skeleton
    global bone_objects 
    bone_objects = {}
    poly_actors = {}
    for file in STL_FILES:
        bone_objects[file] = Bone_Object(file)

    for name, bone_object in bone_objects.items():
        polydata, reader = bone_object.loadStl()
        poly_actors[name] = CreateActor(name, polydata).polyDataToActor()
    # print('created_actors', poly_actors)

    ren, balloonWidget = AddActorAndWidget(ren, poly_actors, balloonWidget
                                           ).add_actor_and_widget()

    print(balloonWidget.GetBalloonString(poly_actors.get('PhalanxDistalis5.stl')))
    ren.SetBackground(0.1, 0.1, 0.1)
    renWin.Render()
    balloonWidget.EnabledOn() 
    reader.Update()
    
    iren.Initialize()
    iren.Start()


if __name__ == "__main__":

    main()