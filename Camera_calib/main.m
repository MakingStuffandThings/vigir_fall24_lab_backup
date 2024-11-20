close all
system('fswebcam -r 800x600 /dev/video2 cl_items_1.jpg');
system('fswebcam -r 800x600 /dev/video0 cr_items_1.jpg');
TableLeft = read_image("cl_items_1.jpg");
disp(TableLeft);

TableRight = read_image("cr_items_1.jpg");
disp(TableRight);

load("Calib_Results_stereo.mat", "KK_left");
load("Calib_Results_stereo.mat", "kc_left");

load("Calib_Results_stereo.mat", "KK_right");
load("Calib_Results_stereo.mat", "kc_right");

[uLeft, vLeft] = convert_distor_undistor_ToolBox(TableLeft.Centroid(:, 1), TableLeft.Centroid(:,2), kc_left, KK_left);
[uRight,vRight] = convert_distor_undistor_ToolBox(TableRight.Centroid(:,1), TableRight.Centroid(:,2), kc_right, KK_right);




% uLeft = TableLeft.Centroid(:, 1);
% vLeft = TableLeft.Centroid(:,2);
% uRight = TableRight.Centroid(:,1);
% vRight = TableRight.Centroid(:,2);
% 

load("Calib_Results_left.mat", "Tc_1");
load("Calib_Results_left.mat", "Rc_1");
eLeft = [Rc_1, Tc_1];
pLeft = KK_left * eLeft;

load("Calib_Results_stereo.mat", "T");
load("Calib_Results_stereo.mat", "R");
eRight = [R, T; 0 0 0 1];
eLeft = [eLeft; 0 0 0 1];
eRightStereo = eRight * eLeft;
eRightStereo = eRightStereo(1:3, :);
pRight = KK_right * eRightStereo;

[x, y, z] = undistor_real_coords(pLeft, pRight, uLeft, vLeft, uRight, vRight);

disp(x);
disp(y);
disp(z);
