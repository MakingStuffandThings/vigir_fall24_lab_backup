function [x, y, z] = undistor_real_coords(pLeft, pRight, uLeft, vLeft, uRight, vRight)

for i=1:length(uLeft)
    A = [(pRight(1, 1) - uRight(:, i) * pRight(3, 1)), (pRight(1, 2) - uRight(:, i) * pRight(3, 2)), (pRight(1, 3) - uRight(:, i) * pRight(3, 3));
        (pRight(2, 1) - vRight(:, i) * pRight(3, 1)), (pRight(2, 2) - vRight(:, i) * pRight(3, 2)), (pRight(2, 3) - vRight(:, i) * pRight(3, 3));
        (pLeft(1, 1) - uLeft(:, i) * pLeft(3, 1)), (pLeft(1, 2) - uLeft(:, i) * pLeft(3, 2)), (pLeft(1, 3) - uLeft(:, i) * pLeft(3, 3));
        (pLeft(2, 1) - vLeft(:, i) * pLeft(3, 1)), (pLeft(2, 2) - vLeft(:, i) * pLeft(3, 2)), (pLeft(2, 3) - vLeft(:, i) * pLeft(3, 3))];
    

    B = [uRight(:, i) * pRight(3, 4) - pRight(1, 4);
        vRight(:, i) * pRight(3, 4) - pRight(2, 4);
        uLeft(:, i) * pLeft(3, 4) - pLeft(1, 4);
        vLeft(:, i) * pLeft(3, 4) - pLeft(2, 4)];

    Ap = pinv(A);
    M = Ap * B;
    
    x(i) = M(1, 1);
    y(i) = M(2, 1);
    z(i) = M(3, 1);

end
