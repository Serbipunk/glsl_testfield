
import numpy as np
import trimesh
import pandas as pd
from enum import Enum


# attach to logger so trimesh messages will be printed to console
trimesh.util.attach_to_log()

class MeshProperties(Enum):
    MESH_DIRECT_CONSTRUCT = 1
    MESH_CONSTRUCT_AND_PROCESS = 2
    MESH_LOAD_GLB = 3
    MESH_LOAD_STL = 4

mesh_properties = MeshProperties.MESH_LOAD_STL

if mesh_properties == MeshProperties.MESH_DIRECT_CONSTRUCT:
    # mesh objects can be created from existing faces and vertex data
    mesh = trimesh.Trimesh(vertices=[[0, 0, 0], [0, 0, 1], [0, 1, 0]],
                           faces=[[0, 1, 2]])
elif mesh_properties == MeshProperties.MESH_CONSTRUCT_AND_PROCESS:
    # by default, Trimesh will do a light processing, which will
    # remove any NaN values and merge vertices that share position
    # if you want to not do this on load, you can pass `process=False`
    mesh = trimesh.Trimesh(vertices=[[0, 0, 0], [0, 0, 1], [0, 1, 0]],
                           faces=[[0, 1, 2]],
                           process=False)
elif mesh_properties == MeshProperties.MESH_LOAD_GLB:
    # some formats represent multiple meshes with multiple instances
    # the loader tries to return the datatype which makes the most sense
    # which will for scene-like files will return a `trimesh.Scene` object.
    # if you *always* want a straight `trimesh.Trimesh` you can ask the
    # loader to "force" the result into a mesh through concatenation
    mesh = trimesh.load('/Users/milesbai/lib/trimesh/models/CesiumMilkTruck.glb', force='mesh')
elif mesh_properties == MeshProperties.MESH_LOAD_STL:
    # mesh objects can be loaded from a file name or from a buffer
    # you can pass any of the kwargs for the `Trimesh` constructor
    # to `trimesh.load`, including `process=False` if you would like
    # to preserve the original loaded data without merging vertices
    # STL files will be a soup of disconnected triangles without
    # merging vertices however and will not register as watertight
    mesh = trimesh.load('/Users/milesbai/lib/trimesh/models/featuretype.STL')

# is the current mesh watertight?
is_watertight = mesh.is_watertight

# what's the euler number for the mesh?
euler_number = mesh.euler_number

# the convex hull is another Trimesh object that is available as a property
# lets compare the volume of our mesh with the volume of its convex hull
volume_ratio = mesh.volume / mesh.convex_hull.volume

# since the mesh is watertight, it means there is a
# volumetric center of mass which we can set as the origin for our mesh
mesh.vertices -= mesh.center_mass

# what's the moment of inertia for the mesh?
mesh.moment_inertia

# if there are multiple bodies in the mesh we can split the mesh by
# connected components of face adjacency
# since this example mesh is a single watertight body we get a list of one mesh
mesh.split()

# facets are groups of coplanar adjacent faces
# set each facet to a random color
# colors are 8 bit RGBA by default (n, 4) np.uint8
for facet in mesh.facets:
    mesh.visual.face_colors[facet] = trimesh.visual.random_color()

# preview mesh in an opengl window if you installed pyglet and scipy with pip
# mesh.show()

# transform method can be passed a (4, 4) matrix and will cleanly apply the transform
mesh.apply_transform(trimesh.transformations.random_rotation_matrix())

# axis aligned bounding box is available
bounding_box_extents = mesh.bounding_box.extents

# a minimum volume oriented bounding box also available
# primitives are subclasses of Trimesh objects which automatically generate
# faces and vertices from data stored in the 'primitive' attribute
oriented_bounding_box_extents = mesh.bounding_box_oriented.primitive.extents
oriented_bounding_box_transform = mesh.bounding_box_oriented.primitive.transform

# show the mesh appended with its oriented bounding box
# the bounding box is a trimesh.primitives.Box object, which subclasses
# Trimesh and lazily evaluates to fill in vertices and faces when requested
# (press w in viewer to see triangles)

# (mesh + mesh.bounding_box_oriented).show()

# bounding spheres and bounding cylinders of meshes are also
# available, and will be the minimum volume version of each
# except in certain degenerate cases, where they will be no worse
# than a least squares fit version of the primitive.
oriented_bounding_box_volume = mesh.bounding_box_oriented.volume
bounding_cylinder_volume = mesh.bounding_cylinder.volume
bounding_sphere_volume = mesh.bounding_sphere.volume

metrics = {
    "Property": [
        "Is Watertight",
        "Euler Number",
        "Volume Ratio (Mesh/Convex Hull)",
        "Bounding Box Extents",
        "Oriented Bounding Box Extents",
        "Oriented Bounding Box Volume",
        "Bounding Cylinder Volume",
        "Bounding Sphere Volume"
    ],
    "Value": [
        is_watertight,
        euler_number,
        volume_ratio,
        "[" + ", ".join([f"{e:.4f}" for e in bounding_box_extents]) + "]",
        "[" + ", ".join([f"{e:.4f}" for e in oriented_bounding_box_extents]) + "]",
        oriented_bounding_box_volume,
        bounding_cylinder_volume,
        bounding_sphere_volume
    ]
}
pd.options.display.float_format = "{:.2f}".format
df = pd.DataFrame(metrics)
print(df)


