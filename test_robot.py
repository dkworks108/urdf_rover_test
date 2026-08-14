import os
import sys
import xml.etree.ElementTree as ET

# find urdf file
urdf_file = os.path.join(os.path.dirname(__file__), 'urdf', 'robot.urdf')

if not os.path.exists(urdf_file):
    print(f"FAIL: File not found: {urdf_file}")
    sys.exit(1)

try:
    tree = ET.parse(urdf_file)
    root = tree.getroot()
except Exception as e:
    print(f"FAIL: XML parse error: {e}")
    sys.exit(1)

# get links and joints
links = {link.attrib['name']: link for link in root.findall('link')}
joints = {joint.attrib['name']: joint for joint in root.findall('joint')}

print(f"Total links: {len(links)}")
print(f"Total joints: {len(joints)}")

all_joints_valid = True
for name, j in joints.items():
    jtype = j.attrib.get('type')
    parent = j.find('parent').attrib.get('link') if j.find('parent') is not None else None
    child = j.find('child').attrib.get('link') if j.find('child') is not None else None

    print(f" - Joint: {name} | Type: {jtype} | Parent: {parent} -> Child: {child}")

    if parent not in links or child not in links:
        print(f"   ERROR: Joint {name} links missing: parent={parent}, child={child}")
        all_joints_valid = False

# check sensor frames
required_sensors = ['camera_link', 'lidar_link', 'imu_link']
sensors_found = [s for s in required_sensors if s in links]
print(f"Sensors found ({len(sensors_found)}/{len(required_sensors)}): {sensors_found}")

# check mesh path
mesh_elem = root.find('.//mesh')
mesh_valid = False
if mesh_elem is not None:
    uri = mesh_elem.attrib.get('filename', '')
    print(f"Found mesh URI: {uri}")
    # strip package prefix if present
    rel_path = uri.replace('package://05_planetary_rover/', '')
    resolved_path = os.path.join(os.path.dirname(__file__), rel_path)
    if os.path.exists(resolved_path):
        mesh_valid = True
        print(f"Resolved mesh file exists: {resolved_path}")
    else:
        print(f"ERROR: Mesh file does not exist at {resolved_path}")

# check gazebo tags
gazebo_tags = root.findall('gazebo')
print(f"Gazebo extension tags count: {len(gazebo_tags)}")

if all_joints_valid and len(sensors_found) == 3 and mesh_valid and len(gazebo_tags) >= 6:
    print("PASS: Planetary Rover verification passed! Sensors, mesh file, and gazebo friction tags verified.")
    sys.exit(0)
else:
    print("FAIL: Verification failed!")
    sys.exit(1)
