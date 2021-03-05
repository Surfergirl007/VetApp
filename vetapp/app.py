
from os import path
import vtk


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
            print('Neuer Actor: ', self.NewPickedActor.GetProperty())
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


DATA_TRANSFORMATIONS = {
    'dog_head.stl': ('head'),
    'dog_spine_right.stl': (None, 'mirror'),
    'dog_hind_limb.stl': ('hind_limb_right', 'hind_limb_left'),
    'dog_front_limb.stl': ('front_limb_right', 'front_limb_left'),
}

OPERATIONS = {
    'mirror': 'transformation_mirror(transform)',
    'head': 'transformation_head(transform)', 
    'hind_limb_right': 'transformation_hind_limb(transform)', 
    'hind_limb_left': 'transformation_hind_limb(transformation_mirror(transform))',
    'front_limb_right': 'transformation_front_limb(transform)',
    'front_limb_left': 'transformation_front_limb(transformation_mirror(transform))'

}
    

def transformation_head(transform):
    '''Transformation to display head in the
    correct position'''
    transform.RotateWXYZ(90, 1, 0, 0)
    transform.RotateWXYZ(-90, 0, 0, 1)
    transform.Translate(145, -120, 300)
    return transform


def transformation_hind_limb(transform):
    '''Transformation to display hind limb in the
    correct position'''
    transform.RotateWXYZ(90, 1, 0, 0)
    transform.RotateWXYZ(-90, 0, 0, 1)
    transform.Translate(419, -376, 112)
    return transform


def transformation_front_limb(transform):
    '''Transformation to display fromt limb in the
    correct position'''
    transform.RotateWXYZ(90, 1, 0, 0)
    transform.RotateWXYZ(-90, 0, 0, 1)
    # transform.RotateWXYZ(0, 0, 1, 0)
    transform.Translate(230, -180, 220)
    return transform


def transformation_mirror(transform):
    '''Transformation to mirror part'''
    transform.Scale(1, 1, -1)
    return transform


def transform_polydata(reader, trans_op=None):
    '''If transformation of the polydata is necessary, it will
    be done here. The transformation matrix is stored in the 
    according function (e.g head_transformation)'''
    
    reader = reader
    if trans_op in OPERATIONS.keys():
        transform = vtk.vtkTransform()
        op = eval(OPERATIONS.get(trans_op))
        transform = op
        
        transFilter = vtk.vtkTransformPolyDataFilter()
        transFilter.SetInputConnection(reader.GetOutputPort())
        transFilter.SetTransform(transform)
        transFilter.Update()
    return transFilter


def loadStl(fname, trans_op=None):
    """Load the given STL file, and return a vtkPolyData object for it."""
    reader = vtk.vtkSTLReader()
    reader.SetFileName(fname)
    reader.Update()

    if trans_op:
        transFilter = transform_polydata(reader, trans_op)

    polydata = reader.GetOutput()
    if trans_op:
        return polydata, transFilter
    else:
        return polydata


def load_data(ren, stl_name, transformation=None):
    ''' Load and transform the data according to the 
    DATA_TRANSFORMATIONS DICTIONARY. OPERATIONS-Functions 
    will be called and applied accordingly. Tranformations
    are found in the according transformation-functions'''
    if transformation:
        polydata, transf = loadStl(stl_name, transformation)
        ren.AddActor(polyDataToActor(polydata, transf))
    else:
        polydata = loadStl(stl_name)
        ren.AddActor(polyDataToActor(polydata))
    return ren
        

def polyDataToActor(polydata, transf=None):
    """Wrap the provided vtkPolyData object in a mapper and an actor, returning
    the actor."""

    mapper = vtk.vtkPolyDataMapper()
    if transf:
        if vtk.VTK_MAJOR_VERSION >= 6:
            # mapper.SetInput(reader.GetOutput())
            # mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(transf.GetOutputPort())
        else:
            mapper.SetInputConnection(polydata.GetProducerPort())
    else: 
        if vtk.VTK_MAJOR_VERSION >= 6:
            
            mapper.SetInputData(polydata)
            # mapper.SetInputConnection(polydata)
        else:
            mapper.SetInputConnection(polydata.GetProducerPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetDiffuseColor(0.5, 0.5, 1.0)
    actor.GetProperty().SetDiffuse(.8)
    actor.GetProperty().SetSpecular(.5)
    actor.GetProperty().SetSpecularColor(colors.GetColor3d('White'))
    actor.GetProperty().SetSpecularPower(30.0)
    return actor


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

    # Load and transform all STL-files from whole skeleton
    for k, v in DATA_TRANSFORMATIONS.items():
        if len(v) == 2:
            load_data(ren, k, v[0])
            load_data(ren, k, v[1])
        else:
            load_data(ren, k, v)

    ren.SetBackground(0.1, 0.1, 0.1)
    
    # enable user interface interactor
    iren.Initialize()
    renWin.Render()
    iren.Start()


if __name__ == "__main__":

    main()