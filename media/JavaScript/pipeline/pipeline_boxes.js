
var conn = new Ext.data.Connection();

var iv = 'QY'
function PlusBox(x, y, width, height) {
    this.type = 'PlusBox';
    this.id = Math.random();
    this.remove = function(){};
    this.color_connections = false;
    this.update = function(){};
    this.moveable = true;
    this.operator = function () {
        return true;
    }
    this.dataset = function () {
        return this.connected_boxes.length > 0;
    };
    this.deselect = function () {
        this.selected = false;
    };
    this.x = x;
    this.y = y;
    this.chart = function () {
        if (this.dataset()) {
            conn.request({
                url: '../json/evaluate/',
                method: 'GET',
                params: {
                    'equation': this.get_equation(),
                },
                success: function (responseObject) {
                    var json_response = Ext.decode(responseObject.responseText);
                    creloadData(json_response);
                },
                failure: function () {
                    Ext.Msg.alert('Error', 'Failed JSON request');
                }
            });
        }
    }
    this.width = width;
    this.height = height;
    this.selected = false;
    this.can_add = function () {
        return true;
    };
    this.add = function (child) {
        this.connected_boxes.push(child);
    };
    this.connected_boxes = [];
    this.get_equation = function () {
        var eq = '( '
        if (this.connected_boxes.length > 0) {
            eq += this.connected_boxes[0].get_equation() + ' .add( ';
            for (var i = 1; i < this.connected_boxes.length; ++i) {
                if (i > 1){
                    eq += ' , ';}
                eq += this.connected_boxes[i].get_equation();
            }
            eq += ' ) ';
        }
        eq += ' )';
        return eq;
    }
    this.draw = function (ctx) {
        clear_box(ctx, this.x, this.y, this.width, this.height);
        draw_box(ctx, this.x, this.y, this.width, this.height, 'rgb(0,255,0)');
        ctx.drawImage(addImg, this.x - this.width / 2, this.y - this.height / 2, this.width, this.height);
        if (this.selected) {
            this.highlight(ctx);
        }
    };
    this.highlight = function (ctx) {
        draw_box(ctx, this.x, this.y, this.width, this.height, 'rgb(0,0,0)');
    };
}

function MinusBox(x, y, width, height) {
    this.type = 'MinusBox';
    this.id = Math.random();
    this.remove = function(){};
    this.color_connections = true;
    this.update = function(){};
    this.moveable = true;
    this.independent_variable = null;
    this.deselect = function () {
        this.selected = false;
    };
    this.chart = function () {
        if (this.dataset()) {
            conn.request({
                url: '../json/evaluate/',
                method: 'GET',
                params: {
                    'equation': this.get_equation(),
                },
                success: function (responseObject) {
                    var json_response = Ext.decode(responseObject.responseText);
                    creloadData(json_response);
                },
                failure: function () {
                    Ext.Msg.alert('Error', 'Failed JSON request');
                }
            });
        }
    }
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
    this.selected = false;
    this.connected_boxes = [];
    this.can_add = function () {
        return this.connected_boxes.length < 2;
    };
    this.add = function (child) {
        this.connected_boxes.push(child);
    };
    this.operator = function () {
        return this.connected_boxes.length < 2;
    }
    this.dataset = function () {
        return this.connected_boxes.length == 2;
    };
    this.get_equation = function () {
        if (this.connected_boxes.length != 2) return '';
        else {
            if(this.independent_variable ===null) this.independent_variable = iv;
                
            return ' ' + this.connected_boxes[0].get_equation() + '.sub( ' + this.connected_boxes[1].get_equation() + ' , \'' + this.independent_variable + '\' )'
        }
    };
    this.draw = function (ctx) {
        clear_box(ctx, this.x, this.y, this.width, this.height);
        draw_box(ctx, this.x, this.y, this.width, this.height, 'rgb(255,0,0)');
        ctx.drawImage(subImg, this.x - this.width / 2, this.y - this.height / 2, this.width, this.height);
        if (this.selected) {
            this.highlight(ctx);
        }
    };
    this.highlight = function (ctx) {
        draw_box(ctx, this.x, this.y, this.width, this.height, 'rgb(0,0,0)');
    };
}

function TextBox(file) {
    this.type = 'TextBox';
    this.id = Math.random();
    this.remove = function(){};
    this.color_connections = false;
    this.moveable = false;
    this.deselect = function () {
        this.selected = false;
    };
    this.file = file;
    if(this.file){ this.text = this.file['File Name'];}
    this.width = 0;
    this.height = TEXTHEIGHT;
    this.chart = function () {
        conn.request({
            url: '../json/' + this.file['id'] + '/',
            method: 'GET',
            params: {},
            success: function (responseObject) {
                var json_response = Ext.decode(responseObject.responseText);
                creloadData(json_response);
            },
            failure: function () {
                Ext.Msg.alert('Error', 'Failed JSON request');
            }
        });
    }
    this.update = function (ctx) {
        var size = ctx.measureText(this.text);
        this.width = size.width + 2 * PADDING;
    };
    this.selected = false;
    this.draw = function (ctx, x, y, width) {
        this.x = x;
        this.y = y;
        this.width = width;
        clear_box(ctx, this.x, this.y, this.width, TEXTHEIGHT + 2*PADDING);
        draw_box(ctx, x, y, width, TEXTHEIGHT + 2 * PADDING, 'rgb(100,100,255)');
        ctx.fillText(this.text, x - width / 2 + PADDING, y + TEXTHEIGHT / 2);
        if (this.selected) this.highlight(ctx);
    };
    this.highlight = function (ctx) {
        draw_box(ctx, this.x, this.y, this.width, TEXTHEIGHT + 2 * PADDING, 'rgb(0,0,0)');
    };
}

function FileBox(x, y) {
    this.type = 'FileBox';
    this.id = Math.random();
    this.remove = function(){};
    this.color_connections = false;
    this.moveable = true;
    this.operator = function () {
        return false;
    }
    this.dataset = function () {
        return true;
    };

    this.files = [];
    this.x = x;
    this.y = y;
    this.get_equation = function () {
        var eq = '( ' + this.files[0].file['id'] + ' .add( ';
        for (var i = 1; i < this.files.length; ++i) {
            if (i > 1){
                eq += ' , ';
            }
            eq +=  this.files[i].file['id'];
        }
        eq += ' ) )'
        return eq;
    };
    this.chart = function () {
        var some_selected = false;
        for (var j = 0; j < this.files.length; ++j) {
            if (this.files[j].selected) {
                some_selected = true;
                break;
            }
        }
        if (some_selected) {
            for (var j = 0; j < this.files.length; ++j) {
                if (this.files[j].selected) {
                    this.files[j].chart();
                }
            }
        } else {
            conn.request({
                url: '../json/evaluate/',
                method: 'GET',
                params: {
                    'equation': this.get_equation(),
                },
                success: function (responseObject) {
                    var json_response = Ext.decode(responseObject.responseText);
                    creloadData(json_response);
                },
                failure: function () {
                    Ext.Msg.alert('Error', 'Failed JSON request');
                }
            });
        }
    };
    this.width = 30;
    this.height = 30;
    this.tbwidth = 0;
    this.tbheight = TEXTHEIGHT;
    this.selected = false;
    this.connected_boxes = [];
    this.deselect = function () {
        this.selected = false;
        for (var i = 0; i < this.files.length; ++i) this.files[i].deselect();
    };
    this.update = function (ctx) {
        if (this.files.length != 0) {
            this.tbwidth = 0;
            for (var i = 0; i < this.files.length; ++i) {
                this.files[i].update(ctx);
                this.tbwidth = Math.max(this.tbwidth, this.files[i].width);
            }
            this.height = (TEXTHEIGHT + 3 * PADDING) * this.files.length + PADDING;
            this.width = this.tbwidth + PADDING * 2;
        }
    };
    this.draw = function (ctx) {
        this.update(ctx);
        var cury = this.y - this.height / 2 + TEXTHEIGHT / 2 + 2 * PADDING;
        clear_box(ctx, this.x, this.y, this.width, this.height);
        draw_box(ctx, this.x, this.y, this.width, this.height, 'rgb(0,0,255)');
        for (var i = 0; i < this.files.length; ++i) {
            this.files[i].draw(ctx, this.x, cury, this.tbwidth);
            cury += TEXTHEIGHT + 3 * PADDING;
        }
        if (this.selected) this.highlight(ctx);
    };
    this.highlight = function (ctx) {
        draw_box(ctx, this.x, this.y, this.width, this.height, 'rgb(0,0,0)');
    };
}

function InputBox(input, parent) {
    this.type = 'InputBox';
    this.id = Math.random();
    this.remove = function(b){
        for(var j = 0; j < b.length; ++j){
            if(b[j].connected_boxes[0] && b[j].connected_boxes[0] == this) {
                var temp = b[j];
                b.splice(j,1);
                temp.remove(b);
                --j;
            }
        }
    };
    this.color_connections = false;
    this.moveable = false;
    this.deselect = function () {
        this.selected = false;
    };
    this.operator = function () {
        return true;
    };
    this.dataset = function () {
        return false;
    };
    this.x = 0;
    this.y = 0;
    this.width = TEXTHEIGHT + 2 * PADDING;
    this.height = TEXTHEIGHT + 2 * PADDING;
    this.selected = false;
    this.draw = function () {};
    this.connected_boxes = [input];
    this.get_equation = function () {
        return this.connected_boxes[0].get_equation();
    }
    this.chart = function(){
        this.connected_boxes[0].chart();
    }
    this.update = function (ctx, x, y) {
        this.x = x;
        this.y = y;
    };
    this.draw = function (ctx) {
        //this.parent.update(ctx)
        clear_box(ctx, this.x, this.y, this.width, this.height);
        draw_box(ctx, this.x, this.y, this.width, this.height, 'rgb(255,0,255)');
        if (this.selected) this.highlight(ctx);
    };
    this.highlight = function (ctx) {
        draw_box(ctx, this.x, this.y, this.width, this.height, 'rgb(0,0,0)');
    };
}

function OutputBox(input, parent) {
    this.type = 'OutputBox';
    this.id = Math.random();
    this.remove = function(b){
        for(var j = 0; j < b.length; ++j){
            if(b[j].outputs){
                for(var k = 0; k < b[j].outputs.length; ++k){
                    if (b[j].outputs[k] == this){
                        b[j].outputs.splice(k,1);
                    } 
                }
            }
            for (var i  = 0; i < this.connected_boxes.length; ++i){
                if(b[j] == this.connected_boxes[i]) {
                    var temp = b[j];
                    b.splice(j,1);
                    temp.remove(b);
                    --j;
                }
            }
        }
    };
    this.color_connections = false;
    this.dataset = true;
    this.operator = false;
    this.moveable = false;
    this.parent = [parent];
    var ib = new InputBox(input, parent);
    this.operator = function () {
        return false;
    };
    this.dataset = function () {
        return true;
    };
    this.chart = function () {
        conn.request({
            url: '../json/evaluate/',
            method: 'GET',
            params: {
                'equation': this.get_equation(),
            },
            success: function (responseObject) {
                var json_response = Ext.decode(responseObject.responseText);
                creloadData(json_response);
            },
            failure: function () {
                Ext.Msg.alert('Error', 'Failed JSON request');
            }
        });
    }
    this.deselect = function () {
        this.selected = false;
    };


    this.get_equation = function () {
        switch(this.parent[0].text){
            case 'Detailed Balance':
                return ' ( ' + this.connected_boxes[0].get_equation() + ' ) .detailed_balance() ';
                break;
            case 'Scalar Multiplication':
                return ' ( ' + this.connected_boxes[0].get_equation() + ' ) .scalar_mult('+ this.parent[0].scalar +') ';
                break;
        }
    }
    this.connected_boxes = [ib];
    this.width = TEXTHEIGHT + 2 * PADDING;
    this.height = TEXTHEIGHT + 2 * PADDING;
    this.selected = false;
    this.x = 0;
    this.y = 0;
    this.update = function(ctx, x, y) {
        this.x = x;
        this.y = y;
    };
    this.draw = function (ctx) {
        //this.parent.update(ctx)
        clear_box(ctx, this.x, this.y, this.width, this.height);
        draw_box(ctx, this.x, this.y, this.width, this.height, 'rgb(255,0,255)');
        draw_arrow(ctx, this.connected_boxes[0].x + 3*PADDING + TEXTHEIGHT/2, this.connected_boxes[0].y, this.x - 3*PADDING - TEXTHEIGHT/2, this.y);
        if (this.selected) this.highlight(ctx);
    };
    this.highlight = function (ctx) {
        draw_box(ctx, this.x, this.y, this.width, this.height, 'rgb(0,0,0)');
    };
}

function FilterBox(x, y, text) {
    this.scalar = 1;
    this.type = 'FilterBox';
    this.id = Math.random();
    this.remove = function(b){
        for (var i  = 0; i < this.outputs.length; ++i){
            for(var j = 0; j < b.length; ++j){
                if(b[j] == this.outputs[i]) {
                    var temp = b[j]
                    b.splice(j,1);
                    temp.remove(b);
                    --j;
                }
            }
        }
    };
    this.color_connections = false;
    this.moveable = true;
    this.operator = function () {
        return true;
    };
    this.dataset = function () {
        return false;
    };
    this.x = x;
    this.y = y;
    this.text = text;
    this.outputs = [];
    this.chart = function () {};
    this.can_add = function () {
        return true;
    };
    this.add = function (input, boxes) {
        var ob = new OutputBox(input, this);
        boxes.push(ob);
        boxes.push(ob.connected_boxes[0]);
        this.outputs.push(ob);
    };
    this.width = 10;
    this.height = 2 * PADDING + TEXTHEIGHT;
    this.selected = false;
    this.connected_boxes = [];
    this.deselect = function () {
        this.selected = false;
        for (var i = 0; i < this.outputs.length; ++i) this.outputs[i].deselect();
    };
    this.update = function (ctx) {
        this.width = ctx.measureText(this.text).width + 4 * PADDING;
        this.height = TEXTHEIGHT + 4 * PADDING + (TEXTHEIGHT + 3 * PADDING) * this.outputs.length;
    };
    this.draw = function (ctx) {
        this.update(ctx);
        clear_box(ctx, this.x, this.y, this.width, this.height);
        draw_box(ctx, this.x, this.y, this.width, this.height, 'rgb(255,0,255)');
        var cury = this.y - this.height / 2 + TEXTHEIGHT / 2 + 2 * PADDING;

        draw_box(ctx, this.x, cury, this.width - 2 * PADDING, TEXTHEIGHT + 2 * PADDING, 'rgb(255,50,255)');
        ctx.fillText(this.text, this.x - (this.width) / 2 + 2 * PADDING, cury + TEXTHEIGHT / 2);
        for (var i = 0; i < this.outputs.length; ++i) {
            cury += 3 * PADDING + TEXTHEIGHT;
            this.outputs[i].update(ctx, this.x + this.width / 2 + (TEXTHEIGHT + 2 * PADDING) / 2 + PADDING, cury);
            this.outputs[i].connected_boxes[0].update(ctx, this.x - this.width / 2 - (TEXTHEIGHT + 2 * PADDING) / 2 - PADDING, cury);
        }
        if (this.selected) this.highlight(ctx);
    };
    this.highlight = function (ctx) {
        draw_box(ctx, this.x, this.y, this.width, this.height, 'rgb(0,0,0)');
    };
}


