Point(1) = {3, 0, 0, 1.0};
Point(2) = {-3, 0, 0, 1.0};
Point(3) = {0, 0, 0, 1.0};
Point(4) = {0, 3, 0, 1.0};
Point(5) = {0, -3, 0, 1.0};
Point(6) = {3, 0, 3, 1.0};
Point(7) = {-3, 0, 3, 1.0};
Point(8) = {0, 3, 3, 1.0};
Point(9) = {0, -3, 3, 1.0};
Point(10) = {1, 0, 0, 1.0};
Point(11) = {-1, 0, 0, 1.0};
Line(1) = {5, 1};
Line(2) = {1, 4};
Line(3) = {4, 2};
Line(4) = {2, 5};
Line(5) = {4, 8};
Line(6) = {1, 6};
Line(7) = {5, 9};
Line(8) = {2, 7};
Line(9) = {7, 8};
Line(10) = {8, 6};
Line(11) = {7, 9};
Line(12) = {9, 6};
Delete {
  Point{10};
}
Delete {
  Point{11};
}
Point(11) = {0.5, -0, 0, 1.0};
Point(12) = {-0.5, 0, 0, 1.0};
Circle(13) = {11, 3, 12};
Circle(14) = {12, 3, 11};
Line Loop(15) = {10, -6, 2, 5};
Plane Surface(16) = {15};
Line Loop(17) = {5, -9, -8, -3};
Plane Surface(18) = {17};
Line Loop(19) = {8, 11, -7, -4};
Plane Surface(20) = {19};
Line Loop(21) = {1, 6, -12, -7};
Plane Surface(22) = {21};
Line Loop(23) = {12, -10, -9, 11};
Plane Surface(24) = {23};
Line Loop(25) = {1, 2, 3, 4};
Line Loop(26) = {13, 14};
Plane Surface(27) = {25, 26};
Plane Surface(28) = {26};
Surface Loop(29) = {22, 27, 16, 24, 18, 20, 28};
Volume(30) = {29};
Delete {
  Surface{28};
}
Delete {
  Volume{30};
}
Delete {
  Surface{28};
}
Plane Surface(30) = {26};
Delete {
  Line{9};
}
Delete {
  Line{9};
}
Delete {
  Line{9};
}
