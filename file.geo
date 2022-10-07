 Mesh.Algorithm = 6; //(1=MeshAdapt, 5=Delaunay, 6=Frontal, 7=bamg, 8=delquad)
 Mesh.Algorithm3D = 1; //(1=tetgen, 4=netgen, 7=MMG3D, 9=R-tree)
 Merge "./mesh/855513/vtk_surface_remesh.stl"
 Field(1) = Centerline;
 Field(1).FileName = "./mesh/855513/centerlines.vtk";
 Field(1).nbPoints = 25; //number of mesh elements in a circle


 //Close in and outlets with planar faces
 Field(1).closeVolume =1;
 //Extrude in the outward direction a vessel wall
 Field(1).extrudeWall =1;
 Field(1).nbElemLayer = 4; //number of layers
 Field(1).hLayer = 0.2;// extrusion thickness given as percent of vessel radius


 //Remesh the initial stl
 Field(1).reMesh =1;
 Field(1).run;
 Background Field = 1;