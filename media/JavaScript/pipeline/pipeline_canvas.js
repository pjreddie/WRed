function draw_box(ctx, _x, _y, _width, _height, _color) {
    var width = _width;
    var height = _height;
    var x = _x - width / 2;
    var y = _y - height / 2;
    var radius = Math.min(width / 10, height / 10);
    ctx.beginPath();
    ctx.strokeStyle = _color;
    ctx.moveTo(x, y + radius);
    ctx.lineTo(x, y + height - radius);
    ctx.quadraticCurveTo(x, y + height, x + radius, y + height);
    ctx.lineTo(x + width - radius, y + height);
    ctx.quadraticCurveTo(x + width, y + height, x + width, y + height - radius);
    ctx.lineTo(x + width, y + radius);
    ctx.quadraticCurveTo(x + width, y, x + width - radius, y);
    ctx.lineTo(x + radius, y);
    ctx.quadraticCurveTo(x, y, x, y + radius);
    ctx.stroke();
}

function clear_box(ctx, _x, _y, _width, _height) {
    var width = _width;
    var height = _height;
    var x = _x - width / 2;
    var y = _y - height / 2;
    ctx.clearRect(x, y, width, height);
}

function draw_arrow(ctx, x0, y0, x1, y1) {
    ctx.beginPath();
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.moveTo(x0, y0);
    ctx.lineTo(x1, y1);
    var a = Math.atan2(y1 - y0, x1 - x0);
    ctx.save();
    ctx.translate(x1, y1);
    ctx.moveTo(0, 0);
    ctx.rotate(a + 2.6);
    ctx.lineTo(6, 0);
    ctx.restore();
    ctx.save();
    ctx.translate(x1, y1);
    ctx.moveTo(0, 0);
    ctx.rotate(a - 2.6);
    ctx.lineTo(6, 0);
    ctx.restore();
    ctx.stroke();

}

function connect(ctx, from, to) {
    ctx.beginPath();
    ctx.strokeStyle = 'rgb(0,0,0)';
    ctx.moveTo(from.x, from.y)
    ctx.bezierCurveTo(to.x, from.y, from.x, to.y, to.x, to.y);
    ctx.stroke();
}

function curve(ctx, x0, y0, x1, y1) {
    ctx.beginPath();
    ctx.strokeStyle = 'rgb(0,0,0)';
    ctx.moveTo(x0, y0)
    ctx.bezierCurveTo(x1, y0, x0, y1, x1, y1);
    ctx.stroke();
}
