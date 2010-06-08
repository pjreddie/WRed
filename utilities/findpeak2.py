function [p]=findpeak(x,y,npeaks)

clear p

%This is a program that finds the positions and FWHMs in a set of
%data specified by x and y.  The user supplies the number of peaks and
%the program returns an array p, where the first entries are the positions of
%the peaks and the next set are the FWHMs of the corresponding peaks
%The program is adapted from a routine written by Rob Dimeo at NIST and
%relies on using a Savit-Golay filtering technique to obtain the derivative
%without losing narrow peaks.  The parameter F is the frame size for the smoothing
%and is set to 11 pts.  The order of the polynomial for making interpolations to better
%approximate the derivate is 4.  I have improved on Dimeo's program by also calculating second
%derivate information to better handle close peaks.  If peaks are too close together, there are
%still problems because the derivative may not turn over.  I have also added a refinement of going
%down both the left and right sides of the peak to determine the FWHMs because of the issue of peaks that
%are close together.
%William Ratcliff


F=11;
[b,g]=sgolay(4,F);   %original
%g=sgolay(4,F);

yd=zeros(1,length(x));
yd2=zeros(1,length(x));
for n=(F+1)/2:length(x)-(F+1)/2
    yd(n)=g(:,2)'*y(n - (F+1)/2 + 1: n + (F+1)/2 - 1)';
    yd2(n)=g(:,3)'*y(n - (F+1)/2 + 1: n + (F+1)/2 - 1)';
end


n_crossings=0;

%npeaks=3;
ny = length(yd);

value_sign = 2*(yd > 0) - 1;
indices = 0;

% Determine the number of zero crossings
%diff_sign = value_sign(2:ny)-value_sign(1:ny-1);
diff_sign=[0 diff(value_sign)];

wh_cross = abs(diff_sign)==2 & (yd2<0)
n_crossings=sum(wh_cross)

indices = ?find(wh_cross)

no_width = 0;

if n_crossings > 0
% Ok, now which ones of these are peaks?
   local_maxima = y[wh_cross]
   peak_indices  = indices[numpy.argsort(local_maxima)[::-1]]
   

   for i,idx = enumerate(peak_indices[:npeaks]):

       full_height = y[idx]
       half_height = 0.5*full_height;
      % Descend down the peak until you get lower than the half height
      elevation = full_height;
      incrementr = 0;
      while elevation > half_height
         % go down the right side of the peak
         elevation = y[idx+incrementr];
         incrementr = incrementr+1;
         no_widthr = 0;
         if (floor(indices(i))+incrementr+1 > ny)
           no_widthr = 1;
           break;
           %goto, no_width_found
        end
      end
      %now go to the left side of the peak
      % Descend down the peak until you get lower than the half height
      elevation = full_height;
      incrementl = 0;
      while elevation > half_height
         % go down the right side of the peak
         elevation = y[idx+incrementl];
         incrementl = incrementl-1;
         no_widthl = 0;
         if (floor(indices(i))+incrementl-1 < 0)
           no_widthl = 1;
           break;
           %goto, no_width_found
        end
      end

      no_width=min(no_widthl,no_widthr);
      increment=min(abs(incrementl),incrementr);



 %     no_width_found:
      if no_width
          width = 2.0*(x(ny)-xpeaks(i));
      else
         width = # oops --- restore this
     end

      if i == 1
          fwhm = width;
      else
          fwhm = [fwhm width];
      end
       %plot([(xpeaks(i)-fwhm(i)/2) (xpeaks(i)+fwhm(i)/2)],[half_height half_height]); hold on;
  end
  %hold off;

  %b=length(fwhm);
  %fwhm=fwhm(b);
  p=[xpeaks (abs(fwhm))];
  return
end








function y=fp_gaussian(x,area,center,fwhm)
sig = fwhm/2.354;
y = (area/sqrt(2.0*pi*sig^2))*exp(-0.5*((x-center)/sig).^2);
return
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
