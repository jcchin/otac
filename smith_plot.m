% Axial Flow Contra-Rotating Turbines
phi = 0.8;
e_w = 0.09; %0.0546;
beta = 72; %69

i=1;
j=1;

e = 69;
e2 = 0.017*(1+(e/90)^2)*(1+3.2*(phi/2.5));

for psi = 0.5:0.5:10
    for phi = 0.2:0.2:1.6
        beta = atand(((psi/4)+1)/phi);
        %eff(j,i) = 1/(1+  (e_w*phi^2* (1+tand(beta)^2) )/(2*psi));
        alpha = atand(psi/(4*phi));
        eff(j,i) = 1/(1+ (0.001^2*(1+tand(alpha)^2)+2*e_w*phi^2* (1+tand(beta)^2) )/(4*psi));
        j=j+1;
    end
    j=1;
    i = i+1;
end
psi = 0.5:0.5:10;
phi = 0.2:0.2:1.6;
[x,y] = meshgrid(psi, phi);
[C,h]=contour(y,x,eff,0.85:0.01:0.95);
set(gca,'FontSize',16)
clabel(C,h);  
xlabel('phi. flow coefficient  (v_x/U)');
ylabel('psi, loading coefficient (delta H/U^2) ');
