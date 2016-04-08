// Gmsh project created on Thu Apr  7 13:33:02 2016
center = 0.6;
sides = 0.6;
h = 10;
Point(1) = {0, 0, 0, center};
Point(2) = {1, 0, 0, sides};
Point(3) = {-1, 0, 0, sides};
Point(4) = {0, 1, 0, sides};
Point(5) = {0, -1, 0, sides};
Point(6) = {1, 0, h, sides};
Point(7) = {-1, 0, h, sides};
Point(8) = {0, 1, h, sides};
Point(9) = {0, -1, h, sides};
Circle(1) = {5, 1, 3};
Circle(2) = {3, 1, 4};
Circle(3) = {4, 1, 2};
Circle(4) = {2, 1, 5};
Point(10) = {0, 0, h, center};
Circle(5) = {9, 10, 7};
Circle(6) = {7, 10, 8};
Circle(7) = {8, 10, 6};
Circle(8) = {6, 10, 9};
Line(9) = {9, 5};
Line(10) = {6, 2};
Line(11) = {8, 4};
Line(12) = {7, 3};
Line Loop(13) = {5, 6, 7, 8};
Plane Surface(14) = {13};
Line Loop(15) = {1, 2, 3, 4};
Plane Surface(16) = {15};
Line Loop(17) = {12, 2, -11, -6};
Plane Surface(18) = {17};
Delete {
  Surface{18};
}
Ruled Surface(18) = {17};
Line Loop(19) = {3, -10, -7, 11};
Ruled Surface(20) = {19};
Line Loop(21) = {10, 4, -9, -8};
Ruled Surface(22) = {21};
Line Loop(23) = {9, 1, -12, -5};
Ruled Surface(24) = {23};
Surface Loop(25) = {16, 24, 22, 20, 14, 18};
Volume(26) = {25};
