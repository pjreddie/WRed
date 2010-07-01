// Author: Joe Redmon
// pipeline.js
/* This mainly deals with animating the pipeline and is not close to being finished,
since I think you're more interested in the other aspects, I'm going to leave out comments
until it is further along...*/


//*******EXT Stuff***********
Ext.onReady(function () {

    var conn = new Ext.data.Connection();

    function drawBox(ctx, _x, _y, _width, _height, _color) {
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

    function clearBox(ctx, _x, _y, _width, _height) {
        var width = _width;
        var height = _height;
        var x = _x - width / 2;
        var y = _y - height / 2;
        ctx.clearRect(x, y, width, height);
    }

    function connect(ctx, from, to) {
        ctx.beginPath();
        ctx.strokeStyle = 'rgb(0,0,0)';
        ctx.moveTo(from.x, from.y)
        ctx.bezierCurveTo(to.x, from.y, from.x, to.y, to.x, to.y);
        ctx.stroke();
    }

    function PlusBox(x, y, width, height) {
        this.deselect = function () {
            this.selected = false;
        };
        this.x = x;
        this.y = y;
        this.chart = function () {

        }
        this.width = width;
        this.height = height;
        this.selected = false;
        this.connected_boxes = [];
        this.draw = function (ctx) {
            clearBox(ctx, this.x, this.y, this.width, this.height);
            drawBox(ctx, this.x, this.y, this.width, this.height, 'rgb(255,0,0)');
            if (this.selected) {
                this.highlight(ctx);
            }
        };
        this.highlight = function (ctx) {
            drawBox(ctx, this.x, this.y, this.width + 4, this.height + 4, 'rgb(0,0,0)');
        };
    }

    function MinusBox(x, y, width, height) {
        this.deselect = function () {
            this.selected = false;
        };
        this.chart = function () {}
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.selected = false;
        this.connected_boxes = [];
        this.draw = function (ctx) {
            clearBox(ctx, this.x, this.y, this.width, this.height);
            drawBox(ctx, this.x, this.y, this.width, this.height, 'rgb(0,255,0)');
            if (this.selected) {
                this.highlight(ctx);
            }
        };
        this.highlight = function (ctx) {
            drawBox(ctx, this.x, this.y, this.width + 4, this.height + 4, 'rgb(0,0,0)');
        };
    }

    function TextBox(file) {
        this.deselect = function () {
            this.selected = false;
        };
        this.file = file;
        this.text = file.data['File Name'];
        this.width = 0;
        this.chart = function () {
            conn.request({
                url: '../json/' + this.file.data['id'] + '/',
                method: 'GET',
                params: {},
                success: function (responseObject) {
                    var json_response = Ext.decode(responseObject.responseText);
                    creloadData(json_response.data);
                }, failure: function () {
                    Ext.Msg.alert('Error', 'Failed JSON request');
                }
            });
        }
        this.update = function (ctx) {
            var size = ctx.measureText(this.text);
            this.width = size.width;
        };
        this.selected = false;
        this.draw = function (ctx, x, y, width, height) {
            this.x = x;
            this.y = y;
            this.width = width;
            this.height = height;
            clearBox(ctx, this.x, this.y, this.width, this.height);
            drawBox(ctx, x, y, width, height, 'rgb(100,100,255)');
            ctx.fillText(this.text, x - width / 2, y + height / 2);
            if (this.selected) this.highlight(ctx);
        };
        this.highlight = function (ctx) {
            drawBox(ctx, this.x, this.y, this.width + 4, this.height + 4, 'rgb(0,0,0)');
        };
    }

    function FileBox(x, y) {
        this.files = [];
        this.x = x;
        this.y = y;
        this.get_equation = function(){
            var eq = 'concat_data(' + this.files[0].file.data['id'];
            for(var i = 1; i < this.files.length; ++i){
                eq += ', ' + this.files[i].file.data['id'];
            }
            eq += ')'
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
            var ids;
            conn.request({
                url: '../json/evaluate/',
                method: 'GET',
                params: {'equation': this.get_equation(),}, success: function (responseObject) {
                    var json_response = Ext.decode(responseObject.responseText);
                    console.log(json_response.data);
                    creloadData(json_response.data);
                }, failure: function () {
                    Ext.Msg.alert('Error', 'Failed JSON request');
                }
            });
            }
        };
        this.width = 30;
        this.height = 30;
        this.tbwidth = 2;
        this.tbheight = 12;
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
                    this.tbwidth = Math.max(this.tbwidth, this.files[i].width + 4);
                }
                this.height = this.tbheight * this.files.length + 4 * (this.files.length + 1);
                this.width = this.tbwidth + 10;
            }
        };
        this.draw = function (ctx) {
            this.update(ctx);
            var cury = this.y - this.height / 2 + this.tbheight / 2 + 4;
            clearBox(ctx, this.x, this.y, this.width, this.height);
            drawBox(ctx, this.x, this.y, this.width, this.height, 'rgb(0,0,255)');
            for (var i = 0; i < this.files.length; ++i) {
                this.files[i].draw(ctx, this.x, cury, this.tbwidth, this.tbheight);
                cury += this.tbheight + 4;
            }
            if (this.selected) this.highlight(ctx);
        };
        this.highlight = function (ctx) {
            drawBox(ctx, this.x, this.y, this.width + 4, this.height + 4, 'rgb(0,0,0)');
        };
    }






    var maxvals = [];
    var minvals = []; /*Handles rendering of ArrayGrid to show range of parameters in data files*/

    function vrange(val, meta, record, rI, cI, store) {
        var range = maxvals[cI] - minvals[cI];
        var spl = val.split(',');
        var low = parseFloat(spl[0]);
        var high = parseFloat(spl[1]);
        var roffset = 0;
        var loffset = 0;
        if (range != 0) {
            loffset = ((low - minvals[cI]) / range) * 100 - 1;
            roffset = ((maxvals[cI] - high) / range) * 100 - 1;
        }
        var ret = high + low;
        return '<div style="border: 1px red solid;"><div style = "border:1px black solid;background-color:black;height:1.5ex;margin-right:' + roffset + '%; margin-left:' + loffset + '%;"></div></div>';
    }
    var dataArray = [];
    var store = new Ext.data.ArrayStore();
    gridColumns = [];
    var msg = function (title, msg) {
        Ext.Msg.show({
            title: title,
            msg: msg,
            minWidth: 200,
            modal: true,
            icon: Ext.Msg.INFO,
            buttons: Ext.Msg.OK
        });
    };

    /*FormPanel to enable file uploads. Sends POST request to server w/ file information*/

    var fp = new Ext.FormPanel({
        fileUpload: true,
        width: 294,
        frame: true,
        title: 'Upload file',
        autoHeight: true,
        bodyStyle: 'padding: 10px 10px 0 10px;',
        labelWidth: 50,
        defaults: {
            anchor: '95%',
            allowBlank: false,
            msgTarget: 'side',
        }, items: [{
            xtype: 'fileuploadfield',
            id: 'form-file',
            emptyText: 'Select a file...',
            fieldLabel: 'File',
            name: 'file',
            buttonText: 'Browse...',
        }],
        buttons: [{
            text: 'Upload',
            icon: 'http://famfamfam.com/lab/icons/silk/icons/page_white_add.png',
            handler: function () {
                if (fp.getForm().isValid()) {
                    fp.getForm().submit({
                        url: '../forms/upload/',
                        waitMsg: 'Uploading your file...',
                        success: function (fp, o) {}
                    });
                }
            }
        }, '-', {
            text: 'Cancel',
            icon: 'http://famfamfam.com/lab/icons/silk/icons/cancel.png',
            handler: function () {
                fp.getForm().reset();
            }
        }]
    });

    var rowRightClicked = 0; //variable to store index of row that is right clicked
    /*GridPanel that displays the data*/
    var grid = new Ext.grid.GridPanel({
        split: true,
        region: 'west',
        collapsible: true,
        width: 300,
        height: 500,
        minSize: 100,
        maxSize: 500,
        tbar: [fp, '-'],
        bbar: [],
        ds: store,
        columns: gridColumns,
        stripeRows: true,
        title: 'Available files',
/*bbar: new Ext.PagingToolbar({
            pageSize: 25,
            store: store,
            displayInfo: true,
            displayMsg: 'Displaying topics {0} - {1} of {2}',
            emptyMsg: "No topics to display",
        })*/

    });
    grid.on('rowdblclick', function (grid, rowIndex, e) {
        window.location = '../' + (store.getAt(rowIndex).get('id'));
    });

    /*Menu that shows up on right click to delete a file from the database*/
    var rowMenu = new Ext.menu.Menu({
        id: 'rowMenu',
        items: [{
            text: 'Delete',
            handler: deleteRow,
            icon: 'http://famfamfam.com/lab/icons/silk/icons/delete.png',
        }],
    }); /*Sends a POST request to server to delete a file*/

    function deleteRow() {

        conn.request({
            url: '../forms/delete/',
            method: 'POST',
            params: {
                'md5': store.getAt(rowRightClicked).get('md5')
            }, success: function (responseObject) {}, failure: function () {}
        });
    }
    grid.on('rowcontextmenu', function (grid, rowIndex, e) {
        rowRightClicked = rowIndex;
        rowMenu.showAt(e.getXY());
        e.stopEvent();
    });


/*After data is retrieved from server, we have to reinitiallize the Store reconfigure the ArrayGrid
so that the new data is displayed on the page*/

    function reload_data() {
        var fieldData = dataArray[0]; //First row is the parameters of the data file (e.g. ['X', 'Y', 'Z', 'Temp'])
        maxvals = dataArray[1]; //Second row is the max values of the parameters over all files (used for rendering ranges)
        minvals = dataArray[2]; //Third row is min values of parameters
        dataArray.splice(0, 3); //The rest is the actual data
        var gridColumns = [];
        storeFields = [];
/*The first three parameters (File Name, database ID, and md5 sum) aren't renedered using the
standard renderer and the ID and md5 sum aren't displayed at all, they are only used for server
requests later, so we add them to the Store differently*/
        gridColumns.push({
            header: fieldData[0],
            width: 150,
            sortable: true,
            dataIndex: fieldData[0]
        });
        storeFields.push({
            name: fieldData[0]
        });
        gridColumns.push({
            header: fieldData[1],
            width: 150,
            hidden: true,
            sortable: true,
            dataIndex: fieldData[1]
        });
        storeFields.push({
            name: fieldData[1]
        });
        gridColumns.push({
            header: fieldData[2],
            width: 150,
            hidden: true,
            sortable: true,
            dataIndex: fieldData[2]
        });
        storeFields.push({
            name: fieldData[2]
        });
        for (var i = 3; i < fieldData.length; ++i) {
            gridColumns.push({
                header: fieldData[i],
                width: 100,
                renderer: vrange,
                sortable: true,
                dataIndex: fieldData[i]
            });
            storeFields.push({
                name: fieldData[i]
            });
        }
        store = new Ext.data.Store({
            proxy: new Ext.ux.data.PagingMemoryProxy(dataArray),
            reader: new Ext.data.ArrayReader({}, storeFields),
            remoteSort: true,
        });

        colModel = new Ext.grid.ColumnModel({
            columns: gridColumns
        });
        store.load({
            params: {
                start: 0,
                limit: 10
            }
        });
        grid.getBottomToolbar().removeAll();
        grid.getBottomToolbar().add(new Ext.PagingToolbar({
            store: store,
            pageSize: 10,
            displayInfo: false,
            displayMsg: 'Displaying topics {0} - {1} of {2}',
            emptyMsg: "No topics to display",
        }))
        grid.getBottomToolbar().doLayout();
        grid.reconfigure(store, colModel);

    }
/*Retrieve data in json format via a GET request to the server. This is used
anytime there is new data, and initially to populate the table.*/

    function update() {
        conn.request({
            url: '../all/json/',
            method: 'GET',
            params: {}, success: function (responseObject) {
                dataArray = Ext.decode(responseObject.responseText); //decodes the response
                reload_data(); //resets the store and grids
            }, failure: function () {}
        });
    }
    update();

/*Sets up the stomp connection, subscribes to the 'all' channel, and updates 
whenever any message comes through (whenever files are added, removed, or changed)*/
    stomp = new STOMPClient();
    stomp.onopen = function () {};
    stomp.onclose = function (c) {
        //alert('Lost Connection, Code: ' + c);
    };
    stomp.onerror = function (error) {
        alert("Error: " + error);
    };
    stomp.onerrorframe = function (frame) {
        alert("Error: " + frame.body);
    };
    stomp.onconnectedframe = function () {
        stomp.subscribe("/updates/files/all");
    };
    stomp.onmessageframe = function (frame) {
        update();
    };
    stomp.connect('localhost', 61613);





    var plMenu = new Ext.menu.Menu({
        id: 'plMenu',
        items: [{
            text: 'Connect',
            handler: connector,
            id: 'connect',
            icon: 'http://famfamfam.com/lab/icons/silk/icons/connect.png',
        }, {
            text: 'Disconnect',
            handler: disconnector,
            id: 'disconnect',
            icon: 'http://famfamfam.com/lab/icons/silk/icons/disconnect.png',
        }],
    });

    function connected() {
        var count = 0;
        for (var i = 0; i < boxes.length && count < 3; ++i) {
            if (boxes[i].selected) {
                if (count === 0) from = boxes[i];
                else if (count == 1) to = boxes[i];
                ++count;
            }
        }
        if (count != 2) {
            return false;
        }
        else {
            var connected = false;
            for (var j = 0; j < from.connected_boxes.length; ++j) {
                if (from.connected_boxes[j] == to) connected = true;
            }
            for (var j = 0; j < to.connected_boxes.length; ++j) {
                if (to.connected_boxes[j] == from) connected = true;
            }
            return connected;
        }
        return false;
    }


    function disconnected() {
        var count = 0;
        for (var i = 0; i < boxes.length && count < 3; ++i) {
            if (boxes[i].selected) {
                if (count === 0) from = boxes[i];
                else if (count == 1) to = boxes[i];
                ++count;
            }
        }
        if (count != 2) {
            return false;
        } else {
            var connected = false;
            for (var j = 0; j < from.connected_boxes.length; ++j) {
                if (from.connected_boxes[j] == to) connected = true;
            }
            for (var j = 0; j < to.connected_boxes.length; ++j) {
                if (to.connected_boxes[j] == from) connected = true;
            }
            return !connected;
        }
        return false;
    }

    function disconnector() {
        if (connected()) {
            for (var j = 0; j < from.connected_boxes.length; ++j) {
                if (from.connected_boxes[j] == to) from.connected_boxes.splice(j, 1);
            }
            for (var j = 0; j < to.connected_boxes.length; ++j) {
                if (to.connected_boxes[j] == from) to.connected_boxes.splice(j, 1);
            }
        }
    }

    function connector() {
        if (disconnected()) {
            from.connected_boxes.push(to);
        }
    }
    var canvasContainer = new Ext.BoxComponent({
        el: 'myCanvas',
        id: 'canvasContainer',
    });
    var toolbar = new Ext.Toolbar();
    toolbar.add({
        text: 'Add',
        id: 'plus',
        icon: 'http://famfamfam.com/lab/icons/silk/icons/add.png',
        enableToggle: true,
        toggleGroup: 'toggle',
        toggleHandler: onItemToggle,
        pressed: false,
    }, {
        text: 'Subtract',
        id: 'minus',
        icon: 'http://famfamfam.com/lab/icons/silk/icons/delete.png',
        enableToggle: true,
        toggleGroup: 'toggle',
        toggleHandler: onItemToggle,
        pressed: false,
    }, {
        text: 'File',
        id: 'file',
        icon: 'http://famfamfam.com/lab/icons/silk/icons/page.png',
        enableToggle: true,
        toggleGroup: 'toggle',
        toggleHandler: onItemToggle,
        pressed: false,
    }, {
        text: 'Pointer',
        id: 'pointer',
        icon: 'http://famfamfam.com/lab/icons/silk/icons/cursor.png',
        enableToggle: true,
        toggleGroup: 'toggle',
        toggleHandler: onItemToggle,
        pressed: true,
    });

    var pipelinePanel = new Ext.Panel({
        tbar: toolbar,
        region: 'center',
        title: 'Pipeline',
        autoWidth: true,
        autoHeight: true,
        id: 'pipeline',
        items: [canvasContainer],
    });

    function onItemToggle(button, state) {
        if (state) selected = button.id;
    }
    var mousedownc = [];
    var mousemovec = [];
    var selected = 'pointer';
    var selectedFiles;
    var selectedBox = [];
    //******Drawing Stuff*********
    var boxes = [];
    var canvas = Ext.get('myCanvas');
    var ctx = canvas.dom.getContext('2d');
    ctx.globalAlpha = 1.0;
    ctx.globalCompositeOperation = 'source-over';

    function redraw(e) {
        var coords = imgCoords(e);
        ctx.clearRect(0, 0, 500, 500);

        for (var i = 0; i < boxes.length; ++i) {
            //boxes[i].draw(ctx);
            for (var j = 0; j < boxes[i].connected_boxes.length; ++j) {
                connect(ctx, boxes[i], boxes[i].connected_boxes[j]);
            }
        }
        for (var i = 0; i < boxes.length; ++i) {
            boxes[i].draw(ctx);
        }
        switch (selected) {
        case 'file':
            var fb = new FileBox(coords[0], coords[1]);
            for (var i = 0; i < selectedFiles.length; ++i) {
                fb.files.push(new TextBox(selectedFiles[i]));
            }
            fb.draw(ctx);

            break;
        case 'plus':
            new PlusBox(coords[0], coords[1], 30, 30).draw(ctx);
            break;
        case 'minus':
            new MinusBox(coords[0], coords[1], 30, 30).draw(ctx);
            break;
        case 'pointer':
            break;
        default:
            alert('default');
            break;
        }
    }

    function moveSelected(e) {
        var coords = imgCoords(e);
        for (var i = 0; i < boxes.length; ++i) {
            if (boxes[i].selected) {
                boxes[i].x += coords[0] - mousemovec[0];
                boxes[i].y += coords[1] - mousemovec[1];
            }
        }
        mousemovec = coords;
    }

    function imgCoords(e) {
        var toReturn = [e.getXY()[0], e.getXY()[1]];
        toReturn[0] -= canvasContainer.getPosition()[0];
        toReturn[1] -= canvasContainer.getPosition()[1];
        return toReturn;
    }
    var from, to;

    function mouseUp(e) {
        canvas.un('mousemove', moveSelected);
        if (e.button === 0) {
            var coords = imgCoords(e);
            switch (selected) {
            case 'plus':
                boxes.push(new PlusBox(coords[0], coords[1], 30, 30));
                break;
            case 'minus':
                boxes.push(new MinusBox(coords[0], coords[1], 30, 30));
                break;
            case 'file':
                var fb = new FileBox(coords[0], coords[1]);
                for (var i = 0; i < selectedFiles.length; ++i) {
                    fb.files.push(new TextBox(selectedFiles[i]));
                }
                boxes.push(fb);
                break;
            case 'pointer':
                if (!e.ctrlKey && coords[0] == mousedownc[0] && coords[1] == mousedownc[1]) {
                    for (var i = 0; i < boxes.length; ++i) {
                        boxes[i].selected = false;
                        if (boxes[i].x - boxes[i].width / 2 <= coords[0] && boxes[i].x + boxes[i].width / 2 >= coords[0] && boxes[i].y - boxes[i].height / 2 <= coords[1] && boxes[i].y + boxes[i].height / 2 >= coords[1]) {
                            boxes[i].selected = true;
                        }
                    }
                }
                break;
            default:
            }
            cstores = [];
            for (var i = 0; i < boxes.length; ++i) {
                if (boxes[i].selected) {
                    boxes[i].chart();
                }
            }
        } else if (e.button == 2 || e.button == 1) {
            if (connected()) {
                plMenu.items.get('connect').disable();
                plMenu.items.get('disconnect').enable();
            } else if (disconnected()) {
                plMenu.items.get('connect').enable();
                plMenu.items.get('disconnect').disable();
            } else {
                plMenu.items.get('disconnect').disable();
                plMenu.items.get('connect').disable();
            }
            plMenu.showAt(e.getXY());
            e.stopEvent();
        }
        redraw(e);
    }

    function mouseDown(e) {
        if (e.button === 0) {
            var newS = false;
            var noneS = true;
            var coords = imgCoords(e);
            mousedownc = coords;
            mousemovec = coords;
            switch (selected) {
            case 'plus':
                break;
            case 'minus':
                break;
            case 'pointer':
                canvas.on('mousemove', moveSelected);
                for (var i = 0; i < boxes.length; ++i) {
                    if (boxes[i].x - boxes[i].width / 2 <= coords[0] && boxes[i].x + boxes[i].width / 2 >= coords[0] && boxes[i].y - boxes[i].height / 2 <= coords[1] && boxes[i].y + boxes[i].height / 2 >= coords[1]) {
                        if (boxes[i].selected === false) {
                            newS = true;
                            boxes[i].selected = true;
                        }
                        else if (boxes[i].files) {
                            for (var j = 0; j < boxes[i].files.length; ++j) {
                                if (!e.ctrlKey) boxes[i].files[j].deselect();
                                if (boxes[i].files[j].x - boxes[i].files[j].width / 2 <= coords[0] && boxes[i].files[j].x + boxes[i].files[j].width / 2 >= coords[0] && boxes[i].files[j].y - boxes[i].files[j].height / 2 <= coords[1] && boxes[i].files[j].y + boxes[i].files[j].height / 2 >= coords[1]) {
                                    boxes[i].files[j].selected = true;
                                }
                            }
                        }
                        else if (e.ctrlKey) boxes[i].deselect();
                        noneS = false;
                    }
                }
                if (((!e.ctrlKey) && newS) || noneS) {
                    for (var i = 0; i < boxes.length; ++i) {
                        boxes[i].deselect();
                        if (boxes[i].x - boxes[i].width / 2 <= coords[0] && boxes[i].x + boxes[i].width / 2 >= coords[0] && boxes[i].y - boxes[i].height / 2 <= coords[1] && boxes[i].y + boxes[i].height / 2 >= coords[1]) {
                            boxes[i].selected = true;
                        }
                    }
                }
                break;
            default:
            }
        } else if (e.button == 2 || e.button == 1) {
            e.stopEvent();
        }
        redraw(e);
    }

    function rightClick(e) {
        e.stopEvent();
    }

    function keyUp(e) {
        if (e.getKey() == 8 || e.getKey() == 46) {
            for (var i = 0; i < boxes.length; ++i) {
                if (boxes[i].selected) {
                    var temp = boxes[i];
                    boxes.splice(i, 1);
                    for (var j = 0; j < boxes.length; ++j) {
                        for (var k = 0; k < boxes[j].connected_boxes.length; ++k) {
                            if (boxes[j].connected_boxes[k] == temp) {
                                boxes[j].connected_boxes.splice(k, 1);
                                --k;
                            }
                        }
                    }--i;
                }
            }
            redraw(e);
        } else if (e.getKey() == 67 && e.ctrlKey) {
            connector();
            e.stopEvent();
        } else if (e.getKey() == 68 && e.ctrlKey) {
            disconnector();
            e.stopEvent();
        }
    }

    function mouseOver(e) {
        if (selected == 'file') {
            selectedFiles = grid.getSelectionModel().getSelections();
        }
        canvas.on('mousemove', redraw);
    }
    grid.on('mouseup', function (g, rowIndex, e) {
        selectedFiles = grid.getSelectionModel().getSelections();
        cupdate(selectedFiles);
    });
    canvas.on('contextmenu', rightClick);
    canvas.on({
        'mouseover': mouseOver
    });
    canvas.on({
        'mouseout': function () {
            canvas.un('mousemove', redraw);
        },
    });
    canvas.on({
        'mousedown': mouseDown,
        'mouseup': mouseUp
    });
    documentExt = Ext.get(document);
    documentExt.on('keyup', keyUp);
/*documentExt.on({'mousedown': function(e){if(e.button == 2){e.stopEvent();}},
         'mouseup': function(e){if(e.button == 2) e.stopEvent();}});*/

    /* Holds the flot plot */


    var ChartContainer = new Ext.Container({
        height: 500,
        valueField: 'id',
        displayField: 'name',
        autoWidth: true,

        id: 'ChartContainer',

    });
    ChartContainer.on('afterrender', cupdate);
    var ChartPanel = new Ext.Panel({
        title: 'Chart',
        region: 'east',
        valueField: 'id',
        displayField: 'name',
        split: true,
        region: 'east',
        collapsible: true,
        width: 500,
        height: 300,
        minSize: 100,
        maxSize: 500,

        id: 'ChartPanel',
        items: [ChartContainer],

    });

    var cstore = new Ext.data.ArrayStore();
    var cfieldData = [];
    var cgridColumns = [];
    var cstoreFields = [];
    var cdataArray = [];

    function cupdate(files) {
        ids = [];
        for (var i = 0; i < files.length; ++i) {
            ids.push(files[i].data['id']);
        }
        cstores = [];
        for (var i = 0; i < ids.length; ++i) {
            conn.request({
                url: '../json/' + ids[i] + '/',
                method: 'GET',
                params: {}, success: function (responseObject) {
                    var json_response = Ext.decode(responseObject.responseText);
                    creloadData(json_response.data);
                }, failure: function () {
                    Ext.Msg.alert('Error', 'Failed JSON request');
                }
            });
        }
    }

    /* Same idea as in all_files.js, when new data comes, we must re-initialize our store to update the plot */

    function creloadData(pts) {
        var cfieldData = pts[0];
        pts.splice(0, 1);
        var cgridColumns = [];
        var cstoreFields = [];
        for (var i = 0; i < cfieldData.length; ++i) {
            cgridColumns.push({
                header: cfieldData[i],
                width: 70,
                sortable: true,
                dataIndex: cfieldData[i]
            });
            cstoreFields.push({
                name: cfieldData[i]
            });
        }

        var cstore = new Ext.data.ArrayStore({
            fields: cstoreFields,
        });

        cstore.loadData(pts);
        cstores.push(cstore);
        drawChart(cstores, 'A4', 'Detector', 'ChartContainer');
    }
    var viewport = new Ext.Viewport({
        layout: 'border',
        items: [pipelinePanel, grid, ChartPanel],
    });

});

function getData(store, xChoice, yChoice) {
    var dataResults = [];
    for (var recordIndex = 0; recordIndex < store.getCount(); recordIndex++) {
        var record = store.getAt(recordIndex);

        // Calculate error bars with square roots; not included in data file as it should be
        var data = [+record.get(xChoice), +record.get(yChoice), +Math.sqrt(record.get(yChoice))]; // + to convert string to number
        dataResults.push(data);
    }

    return dataResults;
} /* Initialize Flot generation, draw the chart with error bars */

function drawChart(stores, xChoice, yChoice, chart) {

    var plotContainer = $('#' + chart);

    plotOptions = {
        series: {
            points: {
                show: true,
                radius: 3
            }
        }, selection: {
            mode: 'xy'
        }, crosshair: {
            mode: 'xy'
        }, zoom: { // plugin
            interactive: true,
            //recenter: true,
            selection: 'xy',
            //trigger: null,
            amount: 1.25,
        }, pan: { // plugin
            interactive: true,
        }, grid: {
            hoverable: true,
            clickable: true
        },
        //yaxis: { autoscaleMargin: null },
    };
    var seriesPointsOptions = {
        show: true,
        errorbars: 'y',
        yerr: {
            show: true,
            upperCap: '-',
            lowerCap: '-'
        },
    };
    var plotDataSeries = [];

    for (var i = 0; i < stores.length; ++i) {
        var seriesData = getData(stores[i], xChoice, yChoice);
        plotDataSeries.push({
            label: xChoice + ' vs. ' + yChoice + ': Series ' + (i + 1),
            data: seriesData,
            points: seriesPointsOptions,
            lines: {
                show: false
            },
        });
    }

    plot = $.plot(
    plotContainer, plotDataSeries, plotOptions); //.addRose(); // Compass rose for panning
}
