# https://lorensen.github.io/VTKExamples/site/Python/Widgets/BalloonWidget/

#!/usr/bin/env python
import vtk


def main():
    colors = vtk.vtkNamedColors()

    # Sphere
    sphereSource = vtk.vtkSphereSource()
    sphereSource.SetCenter(-4.0, 0.0, 0.0)
    sphereSource.SetRadius(4.0)

    sphereMapper = vtk.vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sphereSource.GetOutputPort())

    sphereActor = vtk.vtkActor()
    sphereActor.SetMapper(sphereMapper)
    sphereActor.GetProperty().SetColor(colors.GetColor3d("Chocolate"))

    # Regular Polygon
    regularPolygonSource = vtk.vtkRegularPolygonSource()
    regularPolygonSource.SetCenter(4.0, 0.0, 0.0)
    regularPolygonSource.SetRadius(4.0)

    regularPolygonMapper = vtk.vtkPolyDataMapper()
    regularPolygonMapper.SetInputConnection(regularPolygonSource.GetOutputPort())

    regularPolygonActor = vtk.vtkActor()
    regularPolygonActor.SetMapper(regularPolygonMapper)
    regularPolygonActor.GetProperty().SetColor(colors.GetColor3d("BurlyWood"))

    # A renderer and render window
    renderer = vtk.vtkRenderer()
    
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    # renderWindow.OffScreenRenderingOn()
    # if isinstance(renderWindow, vtk.vtkCocoaRenderWindow) :
    #    renderWindow.SetWantsBestResolution(0)
    #    renderWindow.SetOffScreenRendering(1)

    # An interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Create the widget
    balloonRep = vtk.vtkBalloonRepresentation()
    balloonRep.SetBalloonLayoutToImageRight()

    balloonWidget = vtk.vtkBalloonWidget()
    balloonWidget.SetInteractor(renderWindowInteractor)
    balloonWidget.SetRepresentation(balloonRep)
    ############
    #balloonWidget.vtkCommand('WidgetActivateEvent')
    balloonWidget.AddBalloon(sphereActor, "This is a sphere")
    balloonWidget.AddBalloon(regularPolygonActor, "This is a regular polygon")

    # Add the actors to the scene
    renderer.AddActor(sphereActor)
    renderer.AddActor(regularPolygonActor)
    renderer.SetBackground(colors.GetColor3d("Wheat"))

    # Render an image (lights and cameras are created automatically)
    renderWindow.Render()
    balloonWidget.EnabledOn()

    # Begin mouse interaction
    renderWindowInteractor.Start()
    renderWindowInteractor.Initialize()


if __name__ == '__main__':
    main()


'''
def main():
    colors = vtk.vtkNamedColors()

    # Sphere
    sphereSource = vtk.vtkSphereSource()
    sphereSource.SetCenter(-4.0, 0.0, 0.0)
    sphereSource.SetRadius(4.0)

    sphereMapper = vtk.vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sphereSource.GetOutputPort())

    sphereActor = vtk.vtkActor()
    sphereActor.SetMapper(sphereMapper)
    sphereActor.GetProperty().SetColor(0.1, 0.1, 0.1)

    # Regular Polygon
    regularPolygonSource = vtk.vtkRegularPolygonSource()
    regularPolygonSource.SetCenter(4.0, 0.0, 0.0)
    regularPolygonSource.SetRadius(4.0)

    regularPolygonMapper = vtk.vtkPolyDataMapper()
    regularPolygonMapper.SetInputConnection(regularPolygonSource.GetOutputPort())

    regularPolygonActor = vtk.vtkActor()
    regularPolygonActor.SetMapper(regularPolygonMapper)
    regularPolygonActor.GetProperty().SetColor(0.1, 0.9, 0.9)

    # A renderer and render window
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    # An interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Create the widget
    balloonRep = vtk.vtkBalloonRepresentation()
    balloonRep.SetBalloonLayoutToImageRight()

    balloonWidget = vtk.vtkBalloonWidget()
    balloonWidget.SetInteractor(renderWindowInteractor)
    balloonWidget.SetRepresentation(balloonRep)
    balloonWidget.AddBalloon(sphereActor, "This is a sphere")
    balloonWidget.AddBalloon(regularPolygonActor, "This is a regular polygon")

    # Add the actors to the scene
    renderer.AddActor(sphereActor)
    renderer.AddActor(regularPolygonActor)
    renderer.SetBackground(0.2, 0.5, 0.3)

    # Render an image (lights and cameras are created automatically)
    renderWindow.Render()
    balloonWidget.EnabledOn()

    # Begin mouse interaction
    renderWindowInteractor.Start()
    renderWindowInteractor.Initialize()
    renderWindow.Render()


if __name__ == '__main__':
    main()

    '''