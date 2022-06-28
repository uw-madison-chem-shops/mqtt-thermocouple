$fn = 50;
inch = 25.4;
thickness = 0.05*inch;
height = 0.4*inch;

module roundedRect(size, radius)
{
        x = size[0];
        y = size[1];
        z = size[2];

        linear_extrude(height=z)
        hull()
        {
                // place 4 circles in the corners, with the given radius
                translate([(-x/2)+radius, (-y/2)+radius, 0])
                circle(r=radius);

                translate([(x/2)-radius, (-y/2)+radius, 0])
                circle(r=radius);

                translate([(-x/2) + radius, (y/2)-radius, 0])
                circle(r=radius);

                translate([(x/2)-radius, (y/2)-radius, 0])
                circle(r=radius);
        }

}

difference()
{
roundedRect([2.6*inch+thickness, 
             3.6*inch+thickness, 
             height], 
             0.3*inch, center=false);
union() {
roundedRect([2.6*inch-thickness, 
             3.6*inch-thickness, 
             height],
             0.3*inch, center=false);
translate([0,0,height-thickness])
roundedRect([2.6*inch, 
             3.6*inch, 
             height],
             0.3*inch, center=false);
}
}






