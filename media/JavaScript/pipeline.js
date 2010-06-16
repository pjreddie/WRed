function PlusBox(x, y, width, height){
  this.x = x;
  this.y = y;
  this.width = width;
  this.height = height;
  this.selected = false;
  this.draw = function(ctx){
    drawBox(ctx, this.x, this.y, this.width, this.height, 'rgb(255,0,0)');
    if (this.selected) this.highlight(ctx);
  }
  this.highlight = function(ctx){
    drawBox(ctx, this.x, this.y, this.width+4, this.height+4, 'rgb(0,0,0)');
  }
}

function MinusBox(x, y, width, height){
  this.x = x;
  this.y = y;
  this.width = width;
  this.height = height;
  this.selected = false;
  this.draw = function(ctx){
    drawBox(ctx, this.x, this.y, this.width, this.height, 'rgb(0,255,0)');
    if (this.selected) this.highlight(ctx);
  }
  this.highlight = function(ctx){
    drawBox(ctx, this.x, this.y, this.width+4, this.height+4, 'rgb(0,0,0)');
  }
}

function FileBox(x, y, width, height){
  this.x = x;
  this.y = y;
  this.width = width;
  this.height = height;
  this.files = [];
  this.selected = false;
  this.draw = function(ctx){
    drawBox(ctx, this.x, this.y, this.width, this.height, 'rgb(0,255,0)');
    if (this.selected) this.highlight(ctx);
  }
  this.highlight = function(ctx){
    drawBox(ctx, this.x, this.y, this.width+4, this.height+4, 'rgb(0,0,0)');
  }
}


function FileBox(x,y,width,height){
  
}

function drawBox(ctx,_x,_y,_width,_height, _color){
  var width = _width;
  var height = _height;
  var x = _x - width/2;
  var y = _y - height/2;
  var radius = Math.max(width/10, height/10);
  ctx.beginPath();
  ctx.strokeStyle = _color;
  ctx.moveTo(x,y+radius);
  ctx.lineTo(x,y+height-radius);
  ctx.quadraticCurveTo(x,y+height,x+radius,y+height);
  ctx.lineTo(x+width-radius,y+height);
  ctx.quadraticCurveTo(x+width,y+height,x+width,y+height-radius);
  ctx.lineTo(x+width,y+radius);
  ctx.quadraticCurveTo(x+width,y,x+width-radius,y);
  ctx.lineTo(x+radius,y);
  ctx.quadraticCurveTo(x,y,x,y+radius);
  ctx.stroke();
}

//*******EXT Stuff***********

Ext.onReady(function(){

var plMenu = new Ext.menu.Menu({
    id:'plMenu',
    items:[
        {
            text: 'Connect',
        },
    ],
});

var canvasContainer = new Ext.BoxComponent({
    el: 'myCanvas',
    id: 'canvasContainer',
});
var toolbar = new Ext.Toolbar();
toolbar.add({
        text: '++++',
        id: 'plus',
        enableToggle: true,
        toggleGroup: 'toggle',
        toggleHandler: onItemToggle,
        pressed: false
 },{
        text: '----',
        id: 'minus',
        enableToggle: true,
        toggleGroup: 'toggle',
        toggleHandler: onItemToggle,
        pressed: false
 },{
        text: 'Pointer',
        id: 'pointer',
        enableToggle: true,
        toggleGroup: 'toggle',
        toggleHandler: onItemToggle,
        pressed: true
 });

var pipelinePanel = new Ext.Panel({
    tbar: toolbar,
    renderTo: 'canvasDiv',
    title:'Pipeline',
    autoWidth:true,
    autoHeight:true,
    id: 'pipeline',
    items: [canvasContainer],
});
function onItemToggle(button, state){
  if(state) selected = button.id;
}
var mousedownc = [];
var mousemovec = [];
var mdown = false;
var selected = 'pointer';

var selectedBox = [];
//******Drawing Stuff*********
var boxes = [];
var canvas = Ext.get('myCanvas');
var ctx = canvas.dom.getContext('2d');
ctx.globalAlpha = 1.0;
ctx.globalCompositeOperation = 'source-over';

function redraw(e){
  var coords = imgCoords(e);
  ctx.clearRect(0,0, 500,500);

  switch(selected){
    case 'plus':
  for (i = 0; i < boxes.length; ++i){
     boxes[i].draw(ctx);
  }
      new PlusBox(coords[0], coords[1], 30,30).draw(ctx);
      break;
    case 'minus':
  for (i = 0; i < boxes.length; ++i){
     boxes[i].draw(ctx);
  }
      new MinusBox(coords[0], coords[1], 30,30).draw(ctx);
      break;
    case 'pointer':
  for (i = 0; i < boxes.length; ++i){
    if (mdown && boxes[i].selected){
        boxes[i].x+=coords[0] - mousemovec[0];
        boxes[i].y+=coords[1] - mousemovec[1];
    } 
    boxes[i].draw(ctx);
  }
      break;
    default:
  }
  mousemovec = coords;
}

function imgCoords(e) {
  var toReturn = [e.getXY()[0], e.getXY()[1]];
  toReturn[0] -= canvasContainer.getPosition()[0];
  toReturn[1] -= canvasContainer.getPosition()[1];
  return toReturn;
}
function mouseUp(e){
  if(e.button == 0){
  mdown = false;
  var coords = imgCoords(e);
  switch(selected){
    case 'plus':
      boxes.push(new PlusBox(coords[0],coords[1],30,30));
      break;
    case 'minus':
      boxes.push(new MinusBox(coords[0],coords[1],30,30));
      break;
    case 'pointer':
      if (!e.ctrlKey && coords[0] == mousedownc[0] && coords[1] == mousedownc[1]){
        for (i = 0; i < boxes.length; ++i){
          boxes[i].selected = false;
          if (boxes[i].x - boxes[i].width/2 <= coords[0] && boxes[i].x + boxes[i].width/2>= coords[0] && boxes[i].y - boxes[i].height/2 <= coords[1] && boxes[i].y + boxes[i].height/2>= coords[1]){
            boxes[i].selected = true;
          }
        }
      }
      break;
    default:
  }
  }else if(e.button == 2){
  var coords = imgCoords(e);
  plMenu.showAt(e.getXY());
  e.stopEvent();
  }
  redraw(e);
}

function mouseDown(e){
  if(e.button == 0){
  var newS = false;
  var noneS = true;
  mdown = true;
  var coords = imgCoords(e);
  mousedownc = coords;
  switch(selected){
    case 'plus':
      break;
    case 'minus':
      break;
    case 'pointer':
      for (i = 0; i < boxes.length; ++i){
          if (boxes[i].x - boxes[i].width/2 <= coords[0] && boxes[i].x + boxes[i].width/2>= coords[0] && boxes[i].y - boxes[i].height/2 <= coords[1] && boxes[i].y + boxes[i].height/2>= coords[1]){
            if(boxes[i].selected == false) {newS = true; boxes[i].selected = true;}
            else if(e.ctrlKey) boxes[i].selected = false;
            noneS = false;
          }
      }
      if(((!e.ctrlKey) && newS)||noneS){
      for (i = 0; i < boxes.length; ++i){
          boxes[i].selected = false;
          if (boxes[i].x - boxes[i].width/2 <= coords[0] && boxes[i].x + boxes[i].width/2>= coords[0] && boxes[i].y - boxes[i].height/2 <= coords[1] && boxes[i].y + boxes[i].height/2>= coords[1]){
            boxes[i].selected = true;
          }
      }
      }
      break;
    default:
  }
  }else if(e.button == 2){
  e.stopEvent();
  }
redraw(e);
}
function rightClick(e){
e.stopEvent();
}
canvas.on('contextmenu', rightClick);
canvas.on({'mouseover': function(){canvas.on('mousemove', redraw);},});
canvas.on({'mouseout': function(){canvas.un('mousemove', redraw);},});
canvas.on({'mousedown': mouseDown,
          'mouseup': mouseUp});

});
