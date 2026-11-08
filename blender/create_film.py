import bpy
import math
import argparse
import os
from mathutils import Vector

def args_after_separator():
    import sys
    values = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", type=int, default=1)
    parser.add_argument("--frames", type=int, default=300)
    parser.add_argument("--output", default="renders/chapter_01.mp4")
    return parser.parse_args(values)

def material(name, color, roughness=0.8, metallic=0.0, emission=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = (*color, 1)
    bs.inputs["Roughness"].default_value = roughness
    bs.inputs["Metallic"].default_value = metallic
    if emission:
        bs.inputs["Emission Color"].default_value = (*color, 1)
        bs.inputs["Emission Strength"].default_value = emission
    return m

def assign(obj, mat):
    obj.data.materials.append(mat)
    return obj

def ico(name, loc, scale, mat, subdivisions=2):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=1, location=loc)
    obj=bpy.context.object; obj.name=name; obj.scale=scale
    bpy.ops.object.shade_smooth()
    return assign(obj,mat)

def cylinder(name, loc, radius, depth, mat, vertices=12):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    obj=bpy.context.object; obj.name=name
    return assign(obj,mat)

def create_character(prefix, x, body_mat, accent_mat, t0, frames):
    # Stylized original explorer: oversized head, simple body, limbs and bright scarf.
    body=ico(prefix+"_body",(x,0,1.45),(0.42,0.28,0.62),body_mat)
    head=ico(prefix+"_head",(x,0,2.35),(0.48,0.43,0.48),body_mat)
    ico(prefix+"_hair",(x,0.02,2.68),(0.49,0.43,0.22),accent_mat)
    ico(prefix+"_scarf",(x,-0.02,1.95),(0.48,0.31,0.16),accent_mat)
    for side in (-1,1):
        arm=ico(prefix+"_arm_"+str(side),(x+side*0.48,0,1.55),(0.16,0.18,0.48),body_mat)
        leg=ico(prefix+"_leg_"+str(side),(x+side*0.2,0,0.62),(0.19,0.22,0.48),accent_mat)
        arm.rotation_euler[1]=side*0.15
        leg.rotation_euler[1]=side*0.08
    # Friendly eyes, no realistic human likeness.
    for side in (-1,1):
        ico(prefix+"_eye_"+str(side),(x+side*0.17,-0.405,2.4),(0.055,0.035,0.075),accent_mat,1)
    for frame, z in ((t0,0),(t0+frames//2,0.12),(t0+frames,0)):
        head.location.z=2.35+z
        body.location.z=1.45+z*0.5
        head.keyframe_insert(data_path="location",frame=frame)
        body.keyframe_insert(data_path="location",frame=frame)
    return head

def build_scene(chapter, frames):
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
    # Palette shifts gently by chapter while retaining visual continuity.
    palettes=[
      ((0.035,0.12,0.18),(0.12,0.48,0.52),(0.95,0.55,0.18)),
      ((0.08,0.16,0.28),(0.22,0.42,0.75),(0.95,0.72,0.25)),
      ((0.10,0.20,0.14),(0.25,0.55,0.28),(0.95,0.48,0.22))
    ]
    sky,land,glow=palettes[(chapter-1)%len(palettes)]
    ground=material("Moonlit moss",land)
    dark=material("Explorer teal", (0.08,0.24,0.30))
    gold=material("Sun-thread",glow,0.35,0.1,0.15)
    rock=material("Floating stone",(0.16,0.22,0.28))
    water=material("Crystal river",(0.04,0.38,0.55),0.2,0.2,0.2)
    # Ground and river ribbon.
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0,0,-0.12))
    assign(bpy.context.object,ground)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,3,-0.02))
    river=bpy.context.object; river.name="Crystal river"; river.scale=(18,1.4,0.08); assign(river,water)
    # Floating islands and towering stylized mountains.
    for i in range(9):
        x=-14+i*3.5; y=7+(i%3)*2
        ico("Floating island",(x,y,2+(i%4)*1.2),(2.1,1.5,0.7),rock)
        ico("Mountain peak",(x,y,4.1+(i%4)*1.2),(1.2,1.0,2.6),ground,1)
    # Giant glowing trees.
    for i in range(12):
        x=-16+i*2.9; y=5+(i%2)*3
        cylinder("Ancient tree trunk",(x,y,1.5),0.22,3,rock)
        ico("Luminous canopy",(x,y,3.5),(1.15,1.0,1.25),gold)
    # Two original travelers.
    create_character("Mira",-1.0,dark,gold,1,frames)
    create_character("Tavi",1.0,material("Tavi blue",(0.16,0.27,0.58)),material("Tavi amber",(0.98,0.36,0.12)),1,frames)
    # A small floating crystal landmark.
    crystal=ico("Heart crystal",(0,4,4),(0.42,0.42,0.85),gold,1)
    crystal.rotation_euler[1]=0.4
    for f in (1,frames):
        crystal.rotation_euler[2]=0.3 if f==1 else 2.0
        crystal.keyframe_insert(data_path="rotation_euler",frame=f)
    # Camera.
    bpy.ops.object.camera_add(location=(0,-15,7))
    cam=bpy.context.object; cam.name="Cinematic camera"
    target=Vector((0,3,2.0)); direction=target-cam.location
    cam.rotation_euler=direction.to_track_quat("-Z","Y").to_euler()
    cam.data.lens=42; bpy.context.scene.camera=cam
    # Soft key and rim lighting.
    bpy.ops.object.light_add(type="AREA", location=(-5,-6,11))
    key=bpy.context.object; key.data.energy=1800; key.data.shape="DISK"; key.data.size=9
    bpy.ops.object.light_add(type="AREA", location=(7,5,8))
    rim=bpy.context.object; rim.data.energy=1300; rim.data.color=(0.2,0.65,1.0); rim.data.size=7
    world=bpy.data.worlds.new("NovaWorld twilight") if not bpy.data.worlds else bpy.data.worlds[0]
    bpy.context.scene.world=world; world.use_nodes=True
    world.node_tree.nodes["Background"].inputs[0].default_value=(*sky,1)
    world.node_tree.nodes["Background"].inputs[1].default_value=0.45
    scene=bpy.context.scene
    scene.frame_start=1; scene.frame_end=frames
    scene.render.engine="BLENDER_EEVEE_NEXT"
    scene.eevee.taa_render_samples=16
    scene.render.resolution_x=1280; scene.render.resolution_y=720
    scene.render.resolution_percentage=50
    scene.render.fps=24
    scene.view_settings.view_transform="AgX"
    scene.render.image_settings.file_format="FFMPEG"
    scene.render.ffmpeg.format="MPEG4"
    scene.render.ffmpeg.codec="H264"
    scene.render.ffmpeg.constant_rate_factor="MEDIUM"
    scene.render.filepath="//chapter"
    scene.frame_set(1)

def main():
    args=args_after_separator()
    os.makedirs(os.path.dirname(args.output) or ".",exist_ok=True)
    build_scene(args.chapter,args.frames)
    scene=bpy.context.scene
    scene.render.filepath=os.path.abspath(args.output)
    bpy.ops.render.render(animation=True)

if __name__=="__main__":
    main()
