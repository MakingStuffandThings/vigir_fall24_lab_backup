function [uu,vu]=convert_distor_undistor_ToolBox(ud, vd, d, Intsc)
%
%   Copyright (C) 2003 ViGIR - Vision-Guided and Intelligent Robotics Lab
%   Written by Guilherme Nelson DeSouza <desouzag@missouri.edu>
%
%   This program is free software; you can redistribute it and/or modify
%   it under the terms of the GNU General Public License as published by
%   the Free Software Foundation, meaning:
%                       keep this copyright notice,
%                       do not try to make money out of it,
%                       it's distributed WITHOUT ANY WARRANTY,
%                       yada yada yada...
%
%
%   This function converts distorted image coordinates into undistorted
%   image coordinates using the Carnan's Method to solve a polynomial
%   of degree 3.
%
%   Usage:  [uu,vu] = convert_distor_undistor_ToolBox(ud, vd, d, Intsc)
%ucture
%          where (uu,vu) and (ud,vd) are the undistorted and distorted
%                                    pixel coordinates respectively;
%                d is the vector with the distortion parameters;
%           and  Intsc are the camera intrinsic parameters
%
%

if (d(1) == 0)
   uu = ud;  libavformat    58. 76.100 / 58. 76.100
  libavdevice    58. 13.100 / 58. 13.100
  libavfilter     7.110.100 /  7.110.100
  libswscale      5.  9.100 /  5.  9.100

   vu = vd;
   return;
end;

u0 = Intsc(1,3);
v0 = Intsc(2,3);
au = Intsc(1,1);
av = Intsc(2,2);
nud = (ud - u0)/au;
nvd = (vd - v0)/av;

% "solve()" returns all the roots I need,
% but that can't be done in C or other languages
%
%disp(sprintf('Solution using "solve"'))
%disp(sprintf('======================'))

nuu=zeros(1,size(nud,1));
nvu=zeros(1,size(nud,1));

syms x y;

for j=1:size(nud,1)
   A=vpasolve(x + 2*d(3)*x*y + 3*d(4)*x^2 + d(4)*y^2 + d(1)*x*(y^2) + d(1)*x^3 + d(2)*x*(y^4) + 2*d(2)*(x^3)*(y^2) + d(2)*x^5 + d(5)*x*(y^6) + 3*d(5)*(x^3)*(y^4) + 3*d(5)*(x^5)*(y^2) + d(5)*x^7 == nud(j), ...
           y + 2*d(4)*x*y + d(3)*x^2 + 3*d(4)*y^2 + d(1)*(x^2)*y + d(1)*y^3 + d(2)*(x^4)*y + 2*d(2)*(x^2)*(y^3) + d(2)*y^5 + d(5)*(x^6)*y + 3*d(5)*(x^4)*(y^3) + 3*d(5)*(x^2)*(y^5) + d(5)*y^7 == nvd(j), x, y);
   k=find(imag(eval(A.x))==0);
   k=find(abs(A.x)==min(abs(A.x(k))));
   nuu(1,j)= A.x(k);
   k=find(imag(eval(A.y))==0);
   k=find(abs(A.y)==min(abs(A.y(k))));
   nvu(1,j)= A.y(k);
end

uu = nuu*au + u0;
vu = nvu*av + v0;

