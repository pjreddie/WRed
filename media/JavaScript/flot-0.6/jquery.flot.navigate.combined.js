/*
Flot plugin for adding panning and zooming capabilities to a plot.

The default behaviour is double click and scrollwheel up/down to zoom
in, drag to pan. The plugin defines plot.zoom({ center }),
plot.zoomOut() and plot.pan(offset) so you easily can add custom
controls. It also fires a "plotpan" and "plotzoom" event when
something happens, useful for synchronizing plots.

Example usage:

  plot = $.plot(...);
  
  // zoom default amount in on the pixel (100, 200) 
  plot.zoom({ center: { left: 10, top: 20 } });

  // zoom out again
  plot.zoomOut({ center: { left: 10, top: 20 } });

  // pan 100 pixels to the left and 20 down
  plot.pan({ left: -100, top: 20 })

  // set specific limits (null for auto)  // 0.5
  plot.axis([xmin, xmax, ymin, ymax])     // 0.5

  // Add compasss rose style navigation tool    // 0.5
  plot.addRose()                                // 0.5



Options:

  zoom: {
    interactive: false  // true if mousewheel can zoom  // 0.5
    trigger: "dblclick" // or "click" for single click
    amount: 1.5         // 2 = 200% (zoom in), 0.5 = 50% (zoom out)
  }
  
  pan: {
    interactive: false  // true if click-drag pans the region   // 0.5
  }

  xaxis, yaxis, x2axis, y2axis: {
    zoomRange: null  // or [number, number] (min range, max range)
    panRange: null   // or [number, number] (min, max)
    panzoom: true // or false to suppress zoom/pan for this axis  // 0.5
  }
  
"interactive" enables the built-in drag/click behaviour. "amount" is
the amount to zoom the viewport relative to the current range, so 1 is
100% (i.e. no change), 1.5 is 150% (zoom in), 0.7 is 70% (zoom out).

"zoomRange" is the interval in which zooming can happen, e.g. with
zoomRange: [1, 100] the zoom will never scale the axis so that the
difference between min and max is smaller than 1 or larger than 100.
You can set either of them to null to ignore.

"panRange" confines the panning to stay within a range, e.g. with
panRange: [-10, 20] panning stops at -10 in one end and at 20 in the
other. Either can be null.
*/


// First two dependencies, jquery.event.drag.js and
// jquery.mousewheel.js, we put them inline here to save people the
// effort of downloading them.

/*
jquery.event.drag.js ~ v1.5 ~ Copyright (c) 2008, Three Dub Media (http://threedubmedia.com)  
Licensed under the MIT License ~ http://threedubmedia.googlecode.com/files/MIT-LICENSE.txt
*/
(function(E){E.fn.drag=function(L,K,J){if(K){this.bind("dragstart",L)}if(J){this.bind("dragend",J)}return !L?this.trigger("drag"):this.bind("drag",K?K:L)};var A=E.event,B=A.special,F=B.drag={not:":input",distance:0,which:1,dragging:false,setup:function(J){J=E.extend({distance:F.distance,which:F.which,not:F.not},J||{});J.distance=I(J.distance);A.add(this,"mousedown",H,J);if(this.attachEvent){this.attachEvent("ondragstart",D)}},teardown:function(){A.remove(this,"mousedown",H);if(this===F.dragging){F.dragging=F.proxy=false}G(this,true);if(this.detachEvent){this.detachEvent("ondragstart",D)}}};B.dragstart=B.dragend={setup:function(){},teardown:function(){}};function H(L){var K=this,J,M=L.data||{};if(M.elem){K=L.dragTarget=M.elem;L.dragProxy=F.proxy||K;L.cursorOffsetX=M.pageX-M.left;L.cursorOffsetY=M.pageY-M.top;L.offsetX=L.pageX-L.cursorOffsetX;L.offsetY=L.pageY-L.cursorOffsetY}else{if(F.dragging||(M.which>0&&L.which!=M.which)||E(L.target).is(M.not)){return }}switch(L.type){case"mousedown":E.extend(M,E(K).offset(),{elem:K,target:L.target,pageX:L.pageX,pageY:L.pageY});A.add(document,"mousemove mouseup",H,M);G(K,false);F.dragging=null;return false;case !F.dragging&&"mousemove":if(I(L.pageX-M.pageX)+I(L.pageY-M.pageY)<M.distance){break}L.target=M.target;J=C(L,"dragstart",K);if(J!==false){F.dragging=K;F.proxy=L.dragProxy=E(J||K)[0]}case"mousemove":if(F.dragging){J=C(L,"drag",K);if(B.drop){B.drop.allowed=(J!==false);B.drop.handler(L)}if(J!==false){break}L.type="mouseup"}case"mouseup":A.remove(document,"mousemove mouseup",H);if(F.dragging){if(B.drop){B.drop.handler(L)}C(L,"dragend",K)}G(K,true);F.dragging=F.proxy=M.elem=false;break}return true}function C(M,K,L){M.type=K;var J=E.event.handle.call(L,M);return J===false?false:J||M.result}function I(J){return Math.pow(J,2)}function D(){return(F.dragging===false)}function G(K,J){if(!K){return }K.unselectable=J?"off":"on";K.onselectstart=function(){return J};if(K.style){K.style.MozUserSelect=J?"":"none"}}})(jQuery);


/* jquery.mousewheel.min.js
 * Copyright (c) 2009 Brandon Aaron (http://brandonaaron.net)
 * Dual licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
 * and GPL (http://www.opensource.org/licenses/gpl-license.php) licenses.
 * Thanks to: http://adomas.org/javascript-mouse-wheel/ for some pointers.
 * Thanks to: Mathias Bank(http://www.mathias-bank.de) for a scope bug fix.
 *
 * Version: 3.0.2
 * 
 * Requires: 1.2.2+
 */
(function(c){var a=["DOMMouseScroll","mousewheel"];c.event.special.mousewheel={setup:function(){if(this.addEventListener){for(var d=a.length;d;){this.addEventListener(a[--d],b,false)}}else{this.onmousewheel=b}},teardown:function(){if(this.removeEventListener){for(var d=a.length;d;){this.removeEventListener(a[--d],b,false)}}else{this.onmousewheel=null}}};c.fn.extend({mousewheel:function(d){return d?this.bind("mousewheel",d):this.trigger("mousewheel")},unmousewheel:function(d){return this.unbind("mousewheel",d)}});function b(f){var d=[].slice.call(arguments,1),g=0,e=true;f=c.event.fix(f||window.event);f.type="mousewheel";if(f.wheelDelta){g=f.wheelDelta/120}if(f.detail){g=-f.detail/3}d.unshift(f,g);return c.event.handle.apply(this,d)}})(jQuery);




(function ($) {
    var options = {
        xaxis: {
            zoomRange: null, // or [number, number] (min range, max range)
            panRange: null, // or [number, number] (min, max)
            panzoom: true // or false to stop zoom-pan on that axis   // 0.5
        },
        yaxis: {
            zoomRange: null, // or [number, number] (min range, max range)
            panRange: null, // or [number, number] (min, max)
            panzoom: true // or false to stop zoom-pan on that axis   // 0.5
        },
        zoom: {
            interactive: false,
            selection: false,  // 0.5
            trigger: "dblclick", // or "click" for single click
            recenter: true, // recenter on trigger  // 0.5
            amount: 1.5 // how much to zoom relative to current position, 2 = 200% (zoom in), 0.5 = 50% (zoom out)
        },
        pan: {
            interactive: false
        }
    };

    function init(plot) {
        function bindEvents(plot, eventHolder) {
            var o = plot.getOptions();
            if (o.zoom.interactive) {
                function clickHandler(e, zoomOut, wheel) {  // recenter: 0.5
                    var c = plot.offset(),
                        recenter = plot.getOptions().zoom.recenter;  // 0.5
                    
                    c.left = e.pageX - c.left;
                    c.top = e.pageY - c.top;
                    
                    if (recenter && wheel) {  // 0.5 {
                      recenter = false;       //
                      c = null;               //
                    }                         // }
                    
                    if (zoomOut)
                        plot.zoomOut({ center: c, recenter: recenter });  // recenter: 0.5
                    else
                        plot.zoom({ center: c, recenter: recenter });  // recenter: 0.5
                }
                
                eventHolder[o.zoom.trigger](clickHandler);

                eventHolder.mousewheel(function (e, delta) {
                    clickHandler(e, delta < 0, true);  // true: 0.5
                    return false;
                });
            }
            
            if (o.zoom.selection) {                                         // 0.5 {
              var placeholder = plot.getPlaceholder();                      //
              placeholder.bind("plotselected", function (event, ranges) {   //
                plot.axis([ranges.xaxis.from, ranges.xaxis.to,              //
                ranges.yaxis.from, ranges.yaxis.to]);                       //
              });                                                           //
            }                                                               // }
            
            else if (o.pan.interactive) {                                   // else if: 0.5
                var prevCursor = 'default', pageX = 0, pageY = 0;
                
                eventHolder.bind("dragstart", { distance: 10 }, function (e) {
                    if (e.which != 1)  // only accept left-click
                        return false;
                    eventHolderCursor = eventHolder.css('cursor');
                    eventHolder.css('cursor', 'move');
                    pageX = e.pageX;
                    pageY = e.pageY;
                });
                eventHolder.bind("drag", function (e) {
                    // unused at the moment, but we need it here to
                    // trigger the dragstart/dragend events
                });
                eventHolder.bind("dragend", function (e) {
                    eventHolder.css('cursor', prevCursor);
                    plot.pan({ left: pageX - e.pageX,
                               top: pageY - e.pageY });
                });
            }
        }

        plot.zoomOut = function (args) {
            if (!args)
                args = {};
            
            if (!args.amount)
                args.amount = plot.getOptions().zoom.amount

            args.amount = 1 / args.amount;
            plot.zoom(args);
        }
        
        plot.zoom = function (args) {
            if (!args)
                args = {};
            
            var axes = plot.getAxes(),
                options = plot.getOptions(),
                c = args.center,
                amount = args.amount ? args.amount : options.zoom.amount,
                w = plot.width(), h = plot.height();

            if (!c)
                c = { left: w / 2, top: h / 2 };
                
            var xf = c.left / w,
                x1 = c.left - xf * w / amount,
                x2 = c.left + (1 - xf) * w / amount,
                yf = c.top / h,
                y1 = c.top - yf * h / amount,
                y2 = c.top + (1 - yf) * h / amount;

            if (args.recenter) {              // 0.5 {
              x1 -= (w/2 - c.left) / amount;  //
              x2 -= (w/2 - c.left) / amount;  //
              y1 -= (h/2 - c.top) / amount;   //
              y2 -= (h/2 - c.top) / amount;   //
            }                                 // }

            function scaleAxis(min, max, name) {
                var axis = axes[name],
                    axisOptions = options[name];
                
                if (!axis.used || !axisOptions.panzoom)  // or: 0.5
                    return;
                    
                min = axis.c2p(min);
                max = axis.c2p(max);
                if (max < min) { // make sure min < max
                    var tmp = min
                    min = max;
                    max = tmp;
                }

                var range = max - min, zr = axisOptions.zoomRange;
                if (zr &&
                    ((zr[0] != null && range < zr[0]) ||
                     (zr[1] != null && range > zr[1])))
                    return;
            
                var pr = axisOptions.panRange;                // 0.5 {
                if (pr && (pr[0] != null && min < pr[0])) {   //
                    max += pr[0] - min;                       //
                    min = pr[0];                              //
                    if (pr[1] != null && max > pr[1]) return; //
                }                                             //
                if (pr && (pr[1] != null && max > pr[1])) {   //
                    min -= max - pr[1];                       //
                    max = pr[1];                              //
                    if (pr[0] != null && min < pr[0]) return; //
                }                                             // }
            
                axisOptions.min = min;
                axisOptions.max = max;
            }

            scaleAxis(x1, x2, 'xaxis');
            scaleAxis(x1, x2, 'x2axis');
            scaleAxis(y1, y2, 'yaxis');
            scaleAxis(y1, y2, 'y2axis');
            
            plot.setupGrid();
            plot.draw();
            
            if (!args.preventEvent)
                plot.getPlaceholder().trigger("plotzoom", [ plot, [ axes['xaxis'].min, axes['xaxis'].max, axes['yaxis'].min, axes['yaxis'].max ] ]);
        }

        plot.pan = function (args) {
            var l = +args.left, t = +args.top,
                axes = plot.getAxes(), options = plot.getOptions();

            if (isNaN(l))
                l = 0;
            if (isNaN(t))
                t = 0;

            function panAxis(delta, name) {
                var axis = axes[name],
                    axisOptions = options[name],
                    min, max;
                
                if (!axis.used)
                    return;

                min = axis.c2p(axis.p2c(axis.min) + delta),
                max = axis.c2p(axis.p2c(axis.max) + delta);

                var pr = axisOptions.panRange;
                if (pr) {
                    // check whether we hit the wall
                    if (pr[0] != null && pr[0] > min) {
                        delta = pr[0] - min;
                        min += delta;
                        max += delta;
                    }
                    
                    if (pr[1] != null && pr[1] < max) {
                        delta = pr[1] - max;
                        min += delta;
                        max += delta;
                    }
                }
                
                axisOptions.min = min;
                axisOptions.max = max;
            }

            panAxis(l, 'xaxis');
            panAxis(l, 'x2axis');
            panAxis(t, 'yaxis');
            panAxis(t, 'y2axis');
            
            plot.setupGrid();
            plot.draw();
            
            if (!args.preventEvent)
                plot.getPlaceholder().trigger("plotpan", [ plot, { left: l, top: t, preventEvent: true } ]);
        }
        
        // 0.5 {
        plot.axis = function (limits) {
            if (!limits)
                limits = [null, null, null, null];
            var options = plot.getOptions(),
                xmin = limits[0], xmax = limits[1],
                ymin = limits[2], ymax = limits[3];
            options['xaxis'].min = xmin ? xmin : options['xaxis'].datamin;
            options['xaxis'].max = xmax ? xmax : options['xaxis'].datamax;
            options['yaxis'].min = ymin ? ymin : options['yaxis'].datamin;
            options['yaxis'].max = ymax ? ymax : options['yaxis'].datamax;
            plot.clearSelection();
            plot.setupGrid();
            plot.draw();
        }
        // }
        
        // Self {
        plot.getAxesScales = function() {
            var axes = plot.getAxes();
            return [ axes['xaxis'].datamin, axes['xaxis'].datamax, axes['yaxis'].datamin, axes['yaxis'].datamax ];
        }
        // }
        
        
        // 0.5 {
        // Navigation rose using image map
        plot.addRose = function () {
            var placeholder = plot.getPlaceholder(),
                mapid = placeholder.attr('id')+'_rose',
                img = $('<img class="flotrose" src="/media/JavaScript/flot-0.6/rose.png" alt="navigator"' +
                    ' usemap="#'+mapid+'"'+
                    ' style="border:0px;position:absolute;cursor:pointer;right:1em;top:1em;z-index:2;" />'),
                map = $('\
<map name="@">\n\
  <area id="@_right" alt="right" hrf="#right"   \n\
    shape="poly" coords="80,40, 54,30, 44,40, 54,50" />\n\
  <area id="@_left"  alt="left"  hrf="#left"    \n\
    shape="poly" coords=" 0,40, 26,30, 36,40, 26,50" />\n\
  <area id="@_up"    alt="up"    hrf="#up"      \n\
    shape="poly" coords="40, 0, 30,26, 40,36, 50,26" />\n\
  <area id="@_down"  alt="down"  hrf="#down"    \n\
    shape="poly" coords="40,80, 30,54, 40,44, 50,54" />\n\
  <area id="@_in"    alt="in"    hrf="#zoomin"  \n\
    shape="poly" coords="52,65, 55,58, 60,54, 70,54, 75,58, 78,65" />\n\
  <area id="@_out"   alt="out"   hrf="#zoomout" \n\
    shape="poly" coords="52,67, 55,74, 60,78, 70,78, 75,74, 78,67" />\n\
  <area id="@_reset" alt="reset" hrf="#reset"   \n\
    shape="poly" coords="52,13, 55, 5, 60, 1, 70, 1, 75, 5, 78,13, 75,21 70,25, 60,25, 55, 21" />\n\
  <area id="@_other" alt="other" hrf="#" shape="default" />\n\
</map>'.replace(/@/g,mapid));

            img.appendTo(placeholder);
            map.appendTo(placeholder);
            function none(E) { return false; }
            function addControl(op, fn) {
                var area = $('#' + mapid + '_' + op);
                area.mousehold(50, fn).click(none).dblclick(none).mousewheel(none);
                //area.click(fn).dblclick(none).mousewheel(none);
                area.click(fn);
            }
            addControl('left',  function() { plot.pan({ left: -25 }); });
            addControl('right', function() { plot.pan({ left:  25 }); });
            addControl('up',    function() { plot.pan({ top:  -25 }); });
            addControl('down',  function() { plot.pan({ top:   25 }); });
            addControl('in',    function() { plot.zoom({ amount: 1.25 }); });
            addControl('out',   function() { plot.zoomOut({ amount: 1.25 }); });
            $('#'+mapid+'_reset').mousedown(function () { 
                 plot.axis();
              }).click(none).dblclick(none).mousewheel(none);
            $('#'+mapid+'_other').click(none).dblclick(none).mousewheel(none);

            return plot;
        }
        // }
        
        
        plot.hooks.bindEvents.push(bindEvents);
    }
    
    $.plot.plugins.push({
        init: init,
        options: options,
        name: 'navigate',
        version: '1.1'
    });
})(jQuery);
