cl__1 = 1;
cl = 0.1;
Point(1) = {3, 0, 0, 1};
Point(2) = {-3, 0, 0, 1};
Point(3) = {0, 0, 0, 1};
Point(4) = {0, 3, 0, 1};
Point(5) = {0, -3, 0, 1};
Point(6) = {3, 0, 3, 1};
Point(7) = {-3, 0, 3, 1};
Point(8) = {0, 3, 3, 1};
Point(9) = {0, -3, 3, 1};
Point(11) = {0.5, 0, 0, cl};
Point(12) = {-0.5, 0, 0, cl};
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
Circle(13) = {11, 3, 12};
Circle(14) = {12, 3, 11};
Line Loop(16) = {10, -6, 2, 5};
Plane Surface(16) = {16};
Line Loop(18) = {5, -9, -8, -3};
Plane Surface(18) = {18};
Line Loop(20) = {8, 11, -7, -4};
Plane Surface(20) = {20};
Line Loop(22) = {1, 6, -12, -7};
Plane Surface(22) = {22};
Line Loop(24) = {12, -10, -9, 11};
Plane Surface(24) = {24};
Line Loop(27) = {1, 2, 3, 4, -14, -13};
Plane Surface(27) = {27};
Line Loop(30) = {13, 14};
Plane Surface(30) = {30};
Surface Loop(31) = {24, 22, 27, 16, 18, 20, 30};
Volume(32) = {31};
