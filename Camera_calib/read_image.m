function table = read_image(filename)
I= imread(filename);
I = rgb2gray(I);
thresh = graythresh(I);

BW = imbinarize(I, thresh);
BW = ~BW;
CC = bwconncomp(BW, 8)

area = regionprops("table", BW, "Area");
[~, idx] = sort(area.Area, "descend");
%Will only show 4 largest shapes by area, ensure photo prioritizes objects in field and not external objects outside or on edge
BWfilt = cc2bw(CC, ObjectsToKeep=idx(2:3));
imshow(BWfilt);

stats = regionprops(BWfilt, "Centroid", "Orientation");
table = struct2table(stats, 'AsArray', true);
