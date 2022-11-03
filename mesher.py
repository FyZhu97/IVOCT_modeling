# This is a sample Python script.
import os
from tkinter.messagebox import *

import gmsh
import numpy as np
import toml
import vtk
from vmtk.vmtksurfacereader import vmtkSurfaceReader
from vmtk.vmtksurfaceremeshing import vmtkSurfaceRemeshing
from vmtk.vmtksurfaceviewer import vmtkSurfaceViewer
from vmtk.vmtksurfacewriter import vmtkSurfaceWriter
from vtk.util.numpy_support import numpy_to_vtk


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def data_actor(source_data, sequenceName):
    numOfSlices = int(len(source_data) / 100)
    # 新建 vtkPoints 实例
    points = vtk.vtkPoints()
    # 导入点数据
    points.SetData(numpy_to_vtk(source_data))
    # 新建 vtkPolyData 实例
    polydata = vtk.vtkPolyData()
    # 设置点坐标
    polydata.SetPoints(points)

    polys = vtk.vtkCellArray()

    for i in range(0, numOfSlices):
        for j in range(0, 99):
            if i != numOfSlices - 1:
                polys.InsertNextCell(3, [i * 100 + j, i * 100 + j + 1, (i + 1) * 100 + j])
            if i != 0:
                polys.InsertNextCell(3, [i * 100 + j, i * 100 + j + 1, (i - 1) * 100 + j + 1])
        if i != numOfSlices - 1:
            polys.InsertNextCell(3, [i * 100 + 99, i * 100, (i + 1) * 100 + 99])
        if i != 0:
            polys.InsertNextCell(3, [i * 100 + 99, i * 100, (i - 1) * 100])

    polydata.SetPolys(polys)
    dataFilter = vtk.vtkWindowedSincPolyDataFilter()
    dataFilter.SetInputData(polydata)
    dataFilter.SetNumberOfIterations(50)
    dataFilter.Update()

    cleaner = vtk.vtkCleanPolyData()
    cleaner.SetInputConnection(dataFilter.GetOutputPort())
    cleaner.Update()
    # mapper 实例
    mapper = vtk.vtkPolyDataMapper()
    # 关联 filter 输出
    mapper.SetInputConnection(cleaner.GetOutputPort())
    # 存模型
    if not os.path.exists("./mesh/" + sequenceName):
        os.makedirs("./mesh/" + sequenceName)
    writer = vtk.vtkSTLWriter()
    writer.SetFileName("./mesh/" + sequenceName + "/vtk_surface.stl")
    writer.SetInputConnection(cleaner.GetOutputPort())
    writer.Write()
    # actor 实例
    actor = vtk.vtkActor()
    # 关联 mapper
    actor.SetMapper(mapper)

    actor.GetProperty().SetColor(1, 1, 1)
    return actor


def vmtk_mesher(sequenceName):
    reader = vmtkSurfaceReader()
    reader.InputFileName = "./mesh/" + sequenceName + "/vtk_surface.stl"
    reader.ReadSTLSurfaceFile()
    surface = reader.Surface

    remesher = vmtkSurfaceRemeshing()
    remesher.Surface = surface
    remesher.TargetEdgeLength = 20
    remesher.ElementSizeMode = "edgelength"
    # remesher.CellEntityIdsArrayName = 'CellEntityIds'
    remesher.TargetEdgeLength = 40
    remesher.MaxEdgeLength = 1E16
    remesher.MinEdgeLength = 0
    remesher.TargetEdgeLengthFactor = 1
    remesher.TargetEdgeLengthArrayName = ''
    remesher.TriangleSplitFactor = 5.0
    # remesher.TargetArea = 50
    remesher.Execute()
    surface = remesher.Surface

    # viewer = vmtkSurfaceViewer()
    # viewer.Surface = surface
    # viewer.Execute()

    writer = vmtkSurfaceWriter()
    writer.Surface = surface
    writer.OutputFileName = "./mesh/" + sequenceName + "/vtk_surface_remesh.stl"
    writer.Format = "stl"
    writer.Execute()
    return surface
    # cent_calculator = vmtkCenterlines()
    # cent_calculator.SeedSelectorName = "profileidlist"
    # cent_calculator.SourceIds = [1]
    # cent_calculator.TargetIds = [0]
    # cent_calculator.Surface = surface
    # cent_calculator.Execute()
    # centerline = cent_calculator.Centerlines
    #
    # writer = vmtkSurfaceWriter()
    # writer.Surface = centerline
    # writer.OutputFileName = "./mesh/" + sequenceName + "/centerlines.vtk"
    # writer.Format = "vtk"
    # writer.Execute()




def show_actor(actor):
    # render
    render = vtk.vtkRenderer()
    render.SetBackground(0, 0, 0)

    # Renderer Window
    window = vtk.vtkRenderWindow()
    window.AddRenderer(render)
    window.SetSize(1200, 1200)

    # System Event
    win_render = vtk.vtkRenderWindowInteractor()
    win_render.SetRenderWindow(window)

    # Style
    win_render.SetInteractorStyle(vtk.vtkInteractorStyleMultiTouchCamera())

    # Insert Actor
    render.AddActor(actor)
    win_render.Initialize()
    win_render.Start()


def mesh_writer(polydata):
    polymesh = vtk.vtkUnstructuredGrid()
    polymesh.ShallowCopy(polydata)
    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName("183511.vtu")
    writer.SetInputData(polymesh)
    writer.Write()


def gmsh_mesher():
    gmsh.initialize()
    gmsh.algorithm = 1

def generateModel():
    config = toml.load("./config.toml")
    sequenceName = config["segmentation"]["sequence_name"]
    data_path = "./result/pointClouds/" + sequenceName + "/pointCloud.txt"
    if not os.path.exists(data_path):
        showinfo(title="error", message="point cloud does not exist")
    source_data = np.loadtxt(data_path)
    data_actor(source_data, sequenceName)
    surface = vmtk_mesher(sequenceName)
    viewer = vmtkSurfaceViewer()
    viewer.Surface = surface
    viewer.Execute()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    config = toml.load("./config.toml")
    sequenceName = config["segmentation"]["sequence_name"]
    source_data = np.loadtxt("./result/pointClouds/" + sequenceName + "/pointCloud.txt")
    actor = data_actor(source_data, sequenceName)
    # show_actor(actor)
    vmtk_mesher(sequenceName)
    gmsh_mesher()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
