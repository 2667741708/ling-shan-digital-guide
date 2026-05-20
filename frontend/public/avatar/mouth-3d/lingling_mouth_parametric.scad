// LingTour AI parametric lip reference.
// OpenSCAD is useful for reproducible CAD-like blocking, while Blender shape
// keys are the recommended route for web lip-sync morph targets.
$fn = 64;

module lip_pose(width = 44, opening = 12, lip = 6) {
  difference() {
    scale([width / 2 + lip, lip * 0.55, opening / 2 + lip])
      sphere(r = 1);
    translate([0, -lip, 0])
      scale([max(width, 1) / 2, lip * 1.2, max(opening, 1) / 2])
        sphere(r = 1);
  }
}

lip_pose(width = 46, opening = 17, lip = 6.5);
