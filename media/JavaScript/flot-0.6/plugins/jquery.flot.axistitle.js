/**
 * Flot plugin for axis titles
 */

(function($) {
  function init(plot) {
    function foo(plot, canvas) {
      console.log(plot);
      var axes = plot.getAxes();
      console.log(axes);
      for (var axis in axes)
        console.log(axes[axis]);
    }
    
    plot.hooks.draw.push(foo);
  }
  
  var options = {
    series: {
      bars: { test: null }
    },
    xaxis: {
      axistitle: null
    },
    x2axis: {
      axistitle: null
    },
    yaxis: {
      axistitle: null
    },
    y2axis: {
      axistitle: null
    }
  };
  
  $.plot.plugins.push({
    init: init,
    options: options,
    name: "axisTitles",
    version: "0.1"
  });
})(jQuery);
