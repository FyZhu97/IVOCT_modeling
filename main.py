# This is a sample Python script.
import vmtk
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from vmtk import vmtkscripts, vmtksurfacereader, vmtkmeshgenerator, vtkvmtk
from vmtk import pype

import vtk
from vmtk.vtkvmtkComputationalGeometryPython import vtkvmtkPolyDataCenterlines
from vtk.util.numpy_support import numpy_to_vtk
import numpy as np


def data_actor(sequenceName):
    source_data = np.loadtxt("C:\\Users\\18139\\Documents\\MATLAB\\pointCloud" + sequenceName + ".txt")
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

    # polys.InsertNextCell(100, [i for i in range(0, 100)])
    # polys.InsertNextCell(100, [i for i in range((numOfSlices - 1) * 100, numOfSlices * 100)])
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
    mesh_writer(polydata)
    # mapper 实例
    mapper = vtk.vtkPolyDataMapper()
    # 关联 filter 输出
    mapper.SetInputConnection(cleaner.GetOutputPort())
    #存模型
    writer = vtk.vtkSTLWriter()
    writer.SetFileName(sequenceName + ".stl")
    writer.SetInputConnection(dataFilter.GetOutputPort())
    writer.Write()
    # actor 实例
    actor = vtk.vtkActor()
    # 关联 mapper
    actor.SetMapper(mapper)

    actor.GetProperty().SetColor(1, 1, 1)
    return actor


def vmtk_mesher(sequenceName):
    # capper = vtkvmtkCapPolyData()
    # capper.SetInputConnection(dataFilter.GetOutputPort())
    # capper.SetDisplacement(0)
    # capper.SetInPlaneDisplacement(0)
    # capper.Update()
    #

    #
    # centerlineFilter = vtkvmtkPolyDataCenterlines()
    # centerlineFilter.SetInputData(capper.GetOutput())
    # centerlineFilter.SetSourceSeedIds(sourceSeeds)
    # centerlineFilter.SetTargetSeedIds(targetSeeds)
    # centerlineFilter.SetRadiusArrayName("MaximumInscribedSphereRadius")
    # centerlineFilter.SetCostFunction("1/R")
    # centerlineFilter.SetFlipNormals(0)
    # centerlineFilter.SetAppendEndPointsToCenterlines(1)
    # centerlineFilter.SetSimplifyVoronoi(0)
    # centerlineFilter.SetCenterlineResampling(1)
    # centerlineFilter.SetResamplingStepLength(1)
    # centerlineFilter.Update()

    reader = vmtkscripts.vmtkSurfaceReader()
    reader.InputFileName = sequenceName + ".stl"
    reader.ReadSTLSurfaceFile()
    surface = reader.Surface

    # viewer = vmtkscripts.vmtkSurfaceViewer()
    # viewer.Surface = surface
    # viewer.Execute()

    remesher = vmtkscripts.vmtkSurfaceRemeshing()
    remesher.Surface = surface
    remesher.TargetEdgeLength = 20
    remesher.ElementSizeMode = "edgelength"
    # remesher.CellEntityIdsArrayName = 'CellEntityIds'
    remesher.TargetEdgeLength = 20
    remesher.MaxEdgeLength = 1E16
    remesher.MinEdgeLength = 0
    remesher.TargetEdgeLengthFactor = 1
    remesher.TargetEdgeLengthArrayName = ''
    remesher.TriangleSplitFactor = 5.0
    # remesher.TargetArea = 50
    remesher.Execute()
    surface = remesher.Surface



    viewer = vmtkscripts.vmtkSurfaceViewer()
    viewer.Surface = surface
    viewer.Execute()

    writer = vmtkscripts.vmtkSurfaceWriter()
    writer.Surface = surface
    writer.OutputFileName = sequenceName + "_remesh.stl"
    writer.Format = "stl"
    writer.Execute()


    cent_calculator = vmtkscripts.vmtkCenterLines()
    cent_calculator.SeedSelector = 'profileidlist'
    cent_calculator.SourceIds = 1
    cent_calculator.TargetIds = 0
    cent_calculator.Execute()
    # sizingFunction = vtkvmtk.vtkvmtkPolyDataSizingFunction()
    # sizingFunction.SetInputData(surface)
    # sizingFunction.SetSizingFunctionArrayName('VolumeSizingFunction')
    # sizingFunction.SetScaleFactor(0.8)
    # sizingFunction.Update()
    # meshGenerator = vmtkscripts.vmtkMeshGenerator()
    # meshGenerator.Surface = surface
    # meshGenerator.SkipRemeshing = 1
    # meshGenerator.SkipCapping = 1
    # meshGenerator.TargetEdgeLength = 20
    # # meshGenerator.Tetrahedralize = 1
    # meshGenerator.Execute()

    # myArguments = "vmtksurfacereader -ifile 183511_sb.vtp --pipe vmtkcenterlines -seedselector profileidlist -sourceids 1 -targetids 0 "\
    #               "--pipe vmtkflowextensions -adaptivelength 1 -extensionratio 20 -normalestimationratio 1 -interactive 0 "\
    #               "--pipe vmtkmeshgenerator -ofile 183511.vtu -edgelength 1 --pipe vmtkmeshviewer" \
    #               # "--pipe vmtksurfacewriter -ofile 183511_ex.vtp "
    # myPype = pype.PypeRun(myArguments)
    # myArguments = "vmtksurfacereader -ifile 183511_ex.vtp --pipe vmtkrenderer --pipe " \
    #               "vmtksurfaceviewer -opacity 0.25 --pipe vmtksurfaceviewer -i @vmtkcenterlines.voronoidiagram -array " \
    #               "MaximumInscribedSphereRadius --pipe vmtksurfaceviewer -i @vmtkcenterlines.o "
    # myPype = pype.PypeRun(myArguments)
    # myArguments = "vmtkmeshgenerator -ifile 183511_ex.vtp -ofile 183511.vtu -edgelength 20 --pipe vmtkmeshviewer "
    # myPype = pype.PypeRun(myArguments)
    #
    #
    # surface = myPype.GetScriptObject("vmtkmeshgenerator", '0')

    # myPype.GetScriptObject('vmtkimagereader','0').Surface


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
    # numOfSlices = int(len(source_data) / 100)
    # # 新建 vtkPoints 实例
    # points = vtk.vtkPoints()
    # # 导入点数据
    # points.SetData(numpy_to_vtk(source_data))
    # 新建 vtkPolyData 实例
    polymesh = vtk.vtkUnstructuredGrid()
    # 设置点坐标
    polymesh.ShallowCopy(polydata)
    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName("183511.vtu")
    writer.SetInputData(polymesh)
    writer.Write()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sequenceName = "576781"
    actor = data_actor(sequenceName)
    show_actor(actor)
    vmtk_mesher(sequenceName)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
