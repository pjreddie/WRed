// Author: Joe Redmon
// pipeline.js
/* This mainly deals with animating the pipeline and is not close to being finished,
since I think you're more interested in the other aspects, I'm going to leave out comments
until it is further along...*/

// Constants for pipeline canvas elements
var TEXTHEIGHT = 8;
var PADDING = 4;
var addImg = new Image();
addImg.src = 'http://famfamfam.com/lab/icons/silk/icons/add.png';
var subImg = new Image();
subImg.src = 'http://famfamfam.com/lab/icons/silk/icons/delete.png';

//*******EXT Stuff***********
Ext.onReady(onReadyFunction);

function onReadyFunction() {

    // Returns simplified versions of boxes without pointers to other boxes (JSON-serialized)
    function clone_boxes() {
        var bclone = [];
        for (var i = 0; i < boxes.length; ++i) {
            var box = {};
            for (s in boxes[i]) {
                if (boxes[i][s]) {
                    if (s == 'connected_boxes' || s == 'outputs' || s == 'parent') {
                        var temp = [];
                        for (var j = 0; j < boxes[i][s].length; ++j) {
                            for (var k = 0; k < boxes.length; ++k) {
                                if (boxes[i][s][j] == boxes[k]) {
                                    temp.push(k);
                                    break;
                                }
                            }
                        }
                        box[s] = temp;
                    } else {
                        box[s] = boxes[i][s];
                    }
                }
            }
            bclone.push(box);
        }
        return bclone;
    }
    var myCanvas = new Ext.Element(document.createElement('canvas'));
    myCanvas.set({
        width: 1000,
        height: 1000,
        //style: "width: 500; height: 500;",
        id: 'myCanvas',
    });
    myCanvas.appendTo(document.body);

    var loadMask = new Ext.LoadMask(Ext.getBody(), {
        msg: 'Please wait a moment while the page loads...'
    });
    loadMask.show();


    var maxvals = [];
    var minvals = []; /*Handles rendering of ArrayGrid to show range of parameters in data files*/

    // Generates the "range graphic" in the cells of the file gridpanel
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
    var gridColumns = [];

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
        },
        items: [{
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
            }}, '-',
        {
            text: 'Cancel',
            icon: 'http://famfamfam.com/lab/icons/silk/icons/cancel.png',
            handler: function () {
                fp.getForm().reset();
            }}]
    });

    var rowRightClicked = 0; //variable to store index of row that is right clicked
    /*GridPanel that displays the data*/
    var grid = new Ext.grid.GridPanel({
        split: true,
        region: 'west',
        collapsible: true,
        enableDragDrop: true,
        ddGroup: 'dd_files',
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

    // Enables dragging/dropping from the file panel to the canvas
    var formPanelDropTarget = new Ext.dd.DropTarget(myCanvas, {
        ddGroup: 'dd_files',
        notifyEnter: function (ddSource, e, data) {
            selected = 'file';
            selectedFiles = ddSource.dragData.selections;
            //Add some flare to invite drop.
            myCanvas.highlight();
        },
        notifyOut: function (ddS, e, data) {
            selected = 'pointer';
            redraw(e);
        },
        notifyDrop: function (ddSource, e, data) {

            // Reference the record (single selection) for readability
            selected = 'pointer';
            return (true);
        }
    });

    // When you double click on a row in the file panel, navigate to view_file.php
    grid.on('rowdblclick', function (grid, rowIndex, e) {
        window.location = '../' + (store.getAt(rowIndex).get('id'));
    });

    /* Sends a POST request to server to delete a file */
    function deleteRow() {
        conn.request({
            url: '../forms/delete/',
            method: 'POST',
            params: {
                'md5': store.getAt(rowRightClicked).get('md5')
            },
            success: function (responseObject) {},
            failure: function () {}
        });
    }

    // Opens a new window to download a file from the file panel
    function download() {
        window.open('../forms/download/?id=' + store.getAt(rowRightClicked).get('id'));
    }



    /* Right click menu for file panel */
    var rowMenu = new Ext.menu.Menu({
        id: 'rowMenu',
        items: [{
            text: 'Delete',
            handler: deleteRow,
            icon: 'http://famfamfam.com/lab/icons/silk/icons/delete.png',
            },
        {
            text: 'Download',
            handler: download,
            icon: 'http://famfamfam.com/lab/icons/silk/icons/disk.png',
            }],
    });
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
        var storeFields = [];
        
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
    var toolbar = new Ext.Toolbar();

    // Save a pipeline to the database
    function save_pipeline() {
        var form = new Ext.form.FormPanel({
            baseCls: 'x-plain',
            layout: 'absolute',
            defaultType: 'textfield',

            items: [{
                x: 0,
                y: 5,
                xtype: 'label',
                text: 'Pipeline Name:'
            },
            {
                x: 60,
                y: 0,
                name: 'name',
                anchor: '100%' // anchor width by percentage
            }]
        });
        var win = new Ext.Window({
            title: 'Save Pipeline...',
            width: 300,
            height: 100,
            layout: 'fit',
            closeAction: 'hide',
            plain: true,
            items: form,
            buttons: [{
                text: 'Save',
                handler: function () {
                    console.log(clone_boxes());
                    conn.request({
                        url: '../forms/save_pipeline/',
                        method: 'POST',
                        params: {
                            'pipeline': Ext.encode(clone_boxes()),
                            'name': form.getForm().getFieldValues().name,
                        },
                        success: function (responseObject) {
                            win.hide();
                        },
                        failure: function () {
                            win.hide();
                        }
                    });
                }},
            {
                text: 'Cancel',
                handler: function () {
                    win.hide();
                }
            }]
        });
        win.show();
    }

    // Save the output of an operation to the database
    function save() {
        var form = new Ext.form.FormPanel({
            baseCls: 'x-plain',
            layout: 'absolute',
            defaultType: 'textfield',

            items: [{
                x: 0,
                y: 5,
                xtype: 'label',
                text: 'File Name:'},
            {
                x: 60,
                y: 0,
                name: 'name',
                anchor: '100%' // anchor width by percentage
                }]
        });
        var win = new Ext.Window({
            title: 'Save To Database...',
            width: 300,
            height: 100,
            layout: 'fit',
            closeAction: 'hide',
            plain: true,
            items: form,
            buttons: [{
                text: 'Save',
                handler: function () {
                    console.log(form.getForm().getFieldValues());
                    conn.request({
                        url: '../json/evaluate/save/',
                        method: 'GET',
                        params: {
                            'equation': toSave.get_equation(),
                            'file_name': form.getForm().getFieldValues().name,
                        },
                        success: function (responseObject) {
                            win.hide();
                        },
                        failure: function () {
                            win.hide();
                        }
                    });
                }},
            {
                text: 'Cancel',
                handler: function () {
                    win.hide();
                }}]
        });
        win.show();
    }
    var initDragZone = function (v) {
        v.dragZone = new Ext.dd.DragZone(Ext.getBody(), {
            getDragData: function (e) {
                // .button-draggable == class of the button you want to drag around
                if (sourceEl = e.getTarget('.button-draggable')) {
                    d = sourceEl.cloneNode(true);
                    d.id = Ext.id();
                    return v.dragData = {
                        sourceEl: sourceEl,
                        repairXY: Ext.fly(sourceEl).getXY(),
                        ddel: d
                    }
                }
            },

            onDrag: function (e) {
                // !Important: manually fix the default position of Ext-generated proxy element
                // Uncomment these line to see the Ext issue
                var proxy = Ext.DomQuery.select('*', this.getDragEl());
                proxy[2].style.position = '';
            },

            getRepairXY: function () {
                return this.dragData.repairXY;
            }
        });
    };
    var my_pipeline_menu = [];
    toolbar.add({
        text: 'Add',
        id: 'plus',
        icon: 'http://famfamfam.com/lab/icons/silk/icons/add.png',
        cls: 'button-draggable',
        listeners: {
            render: initDragZone
        }
        //enableToggle: true,
        //toggleGroup: 'toggle',
        //toggleHandler: onItemToggle,
        //pressed: false,
    }, {
        text: 'Subtract',
        id: 'minus',
        icon: 'http://famfamfam.com/lab/icons/silk/icons/delete.png',
        cls: 'button-draggable',
        listeners: {
            render: initDragZone
        }
        //enableToggle: true,
        //toggleGroup: 'toggle',
        //toggleHandler: onItemToggle,
        //pressed: false,
    },
/*{
        text: 'File',
        id: 'file',
        icon: 'http://famfamfam.com/lab/icons/silk/icons/page.png',
        enableToggle: true,
        toggleGroup: 'toggle',
        toggleHandler: onItemToggle,
        pressed: false,
    }, */
    {
        text: 'Filter',
        id: 'filter',
        icon: 'http://famfamfam.com/lab/icons/silk/icons/calculator.png',
        cls: 'button-draggable',
        listeners: {
            render: initDragZone
        }
        //enableToggle: true,
        //toggleGroup: 'toggle',
        //toggleHandler: onItemToggle,
        //pressed: false,
    },
    '->',
    {
        text: 'Save Current Pipeline',
        id: 'save_pipeline',
        icon: 'http://famfamfam.com/lab/icons/silk/icons/disk.png',
        handler: save_pipeline,

    },
    {
        text: 'Load Pipeline',
        id: 'load_pipeline',
        icon: 'http://famfamfam.com/lab/icons/silk/icons/folder_table.png',
        menu: [
            {
                text: 'Templates',
                id: 'templates',
                icon: 'http://famfamfam.com/lab/icons/silk/icons/table_gear.png',
                menu: ['-'],
            },
            {
                text: 'My Pipelines',
                id: 'my_pipelines',
                icon: 'http://famfamfam.com/lab/icons/silk/icons/table.png',
                menu: ['-'],
            }
        ],

        //enableToggle: true,
        //toggleGroup: 'toggle',
        //toggleHandler: onItemToggle,
        //pressed: false,
    },{
        text: 'Clear Pipeline',
        id: 'clear_pipeline',
        icon: 'http://famfamfam.com/lab/icons/silk/icons/bomb.png',
        handler: function(b,e){boxes = []; redraw(e);},

    }
    
/*{
        text: 'Pointer',
        id: 'pointer',
        icon: 'http://famfamfam.com/lab/icons/silk/icons/cursor.png',
        enableToggle: true,
        toggleGroup: 'toggle',
        toggleHandler: onItemToggle,
        pressed: true,
    }*/
    );
    // Make the panel droppable to the button
    var initDropZone = function (g) {
        g.dropZone = new Ext.dd.DropZone(g.body, {

            getTargetFromEvent: function (e) {
                return e.getTarget('#myCanvas');
            },

            onNodeOver: function (target, dd, e, data) {
                selected = data.sourceEl.id;
                return Ext.dd.DropZone.prototype.dropAllowed;
            },
            onNodeOut: function (target, dd, e, data) {
                selected = 'pointer';
                redraw(e);
            },
            onNodeDrop: function (target, dd, e, data) {
                // !Important: We assign the dragged element to be set to new drop position
                selected = 'pointer';
                return true;
            }

        });
    };


    var canvasContainer = new Ext.BoxComponent({
        el: 'myCanvas',
        id: 'canvasContainer',

    });
    var pipelinePanel = new Ext.Panel({
        tbar: toolbar,
        region: 'center',
        title: 'Pipeline',
        //        autoWidth: true,
        autoHeight: true,
        id: 'pipeline',
        //	layout: 'fit',
        items: [canvasContainer],
        listeners: {
            render: initDropZone
        },

    });
    pipelines = [];

    function recreate_box(b) {
        var temp;
        
        var switcher = {
            'PlusBox': PlusBox,
            'MinusBox': MinusBox,
            'TextBox': TextBox,
            'FileBox': FileBox,
            'InputBox': InputBox,
            'OutputBox': OutputBox,
            'FilterBox': FilterBox,
        };
        temp = new switcher[b.type]();

        for (var a in temp) {
            if (temp[a] && typeof(temp[a] == 'function') && a != 'files' && a != 'id' && a != 'connected_boxes' && a != 'type' && a != 'file' && a != 'outputs' && a != 'parent') {
                b[a] = temp[a];
            }
        }
    }

    function correct_pipelines() {
        for (var s = 0; s < pipelines.length; ++s) {
            var tp = pipelines[s];
            for (var i = 0; i < tp.length; ++i) {
                recreate_box(tp[i]);
            }
            for (var i = 0; i < tp.length; ++i) {
                if (tp[i].connected_boxes) {
                    for (var j = 0; j < tp[i].connected_boxes.length; ++j) {
                        tp[i].connected_boxes[j] = tp[tp[i].connected_boxes[j]]
                    }
                }
                if (tp[i].outputs) {
                    for (var j = 0; j < tp[i].outputs.length; ++j) {
                        tp[i].outputs[j] = tp[tp[i].outputs[j]];
                    }
                }
                if (tp[i].parent) {
                    tp[i].parent[0] = tp[tp[i].parent[0]];
                }
                if (tp[i].files) {
                    for (var j = 0; j < tp[i].files.length; ++j) {
                        recreate_box(tp[i].files[j]);
                    }
                }
            }

        }

    }

    function load_pipeline(b, e) {
        boxes = pipelines[b.id];
        redraw(e);
    }

/*Retrieve data in json format via a GET request to the server. This is used
anytime there is new data, and initially to populate the table.*/

    function update() {
        conn.request({
            url: '../all/json_pipelines/',
            method: 'GET',
            params: {},
            success: function (responseObject) {
                var json_response = Ext.decode(responseObject.responseText);
                my_pipeline_menu = [];
                pipelines = [];
                var menu = new Ext.menu.Menu({
                    id: 'pipeline_menu',
                    items: []
                });
                for (var i = 0; i < json_response.length; ++i) {
                    menu.add({
                        text: json_response[i].name,
                        id: '' + i,
                        handler: load_pipeline,
                        icon: 'http://famfamfam.com/lab/icons/silk/icons/table.png',
                    });
                    pipelines.push(Ext.decode(json_response[i].pipeline));
                }
                correct_pipelines();
                toolbar.get('load_pipeline').menu.items.get('my_pipelines').menu = menu;
                toolbar.doLayout();
            },
            failure: function () {

            }
        });
        conn.request({
            url: '../all/json/',
            method: 'GET',
            params: {},
            success: function (responseObject) {
                dataArray = Ext.decode(responseObject.responseText); //decodes the response
                reload_data(); //resets the store and grids
                loadMask.hide();
            },
            failure: function () {}
        });
    }
    update();

/*Sets up the stomp connection, subscribes to the 'all' channel, and updates 
whenever any message comes through (whenever files are added, removed, or changed)*/
    stomp = new STOMPClient();
    stomp.onopen = function () {};
    stomp.onclose = function (c) {
        alert('Lost Connection, Code: ' + c);
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
            },
        {
            text: 'Disconnect',
            handler: disconnector,
            id: 'disconnect',
            icon: 'http://famfamfam.com/lab/icons/silk/icons/disconnect.png',
            }, '-',
        {
            text: 'Filter Options',
            menu: [
                {
                text: 'Set Scalar Value',
                handler: set_scalar,
                icon: 'http://famfamfam.com/lab/icons/silk/icons/table_gear.png',
                }
            ],
            id: 'filter_options',
            icon: 'http://famfamfam.com/lab/icons/silk/icons/table_gear.png',
            },
        {
            text: 'Filter Type',
            menu: [
                {
                text: 'Detailed Balance',
                handler: filter_type,
                icon: 'http://famfamfam.com/lab/icons/silk/icons/table_gear.png',
                },
            {
                text: 'Scalar Multiplication',
                handler: filter_type,
                icon: 'http://famfamfam.com/lab/icons/silk/icons/table_gear.png',
                }
            ],
            id: 'filter_type',
            icon: 'http://famfamfam.com/lab/icons/silk/icons/table_gear.png',
            }, '-',
        {
            text: 'Save To Database',
            handler: save,
            id: 'save',
            icon: 'http://famfamfam.com/lab/icons/silk/icons/disk.png',
            },
                    ],
    });

    function set_scalar(b, e) {
        var form = new Ext.form.FormPanel({
            baseCls: 'x-plain',
            layout: 'absolute',
            defaultType: 'textfield',

            items: [{
                x: 0,
                y: 5,
                xtype: 'label',
                text: 'Scalar Value:'},
            {
                x: 80,
                y: 0,
                name: 'scalar',
                anchor: '100%' // anchor width by percentage
                }]
        });
        var win = new Ext.Window({
            title: 'Set Scalar...',
            width: 200,
            height: 100,
            layout: 'fit',
            closeAction: 'hide',
            plain: true,
            items: form,
            buttons: [{
                text: 'Confirm',
                handler: function () {
                    for (var i = 0; i < boxes.length; ++i) {
                        if (boxes[i].selected && boxes[i].outputs) {
                            boxes[i].scalar = parseFloat(form.getForm().getFieldValues().scalar)
                        }
                    }
                    win.hide();
                    redraw(e);
                }},
            {
                text: 'Cancel',
                handler: function () {
                    win.hide();
                    redraw(e);
                }}]
        });
        win.show();

    }

    function filter_type(b, e) {
        var new_text = b.text;
        for (var i = 0; i < boxes.length; ++i) {
            if (boxes[i].selected && boxes[i].outputs) {
                boxes[i].text = new_text;
            }
        }
        redraw(e);
    }

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
        var fcount = true,
            tcount = true;
        var a = null,
            b = null;
        for (var i = 0; i < boxes.length; ++i) {
            if (boxes[i].selected) {
                if (!a) a = boxes[i];
                else if (!b) b = boxes[i];
                else return false;
            }
        }
        if (a === null) {
            return false;
        }
        if (a.operator() && a.can_add() && b !== null && b.dataset()) {
            from = a;
            to = b
        }
        else if (b !== null && a.dataset() && b.operator() && b.can_add()) {
            from = b;
            to = a
        }
        else {
            return false;
        }
/*for (var i = 0; i < boxes.length && fcount < 2 && tcount < 2; ++i) {
            if (boxes[i].selected) {
                if (fcount && boxes[i].operator() && boxes[i].can_add()) {from = boxes[i]; fcount = false;}
                else if (tcount && boxes[i].dataset()) {to = boxes[i]; tcount = false;}
                else return false;
            }
        }*/
        var connected = false;
        for (var j = 0; j < from.connected_boxes.length; ++j) {
            if (from.connected_boxes[j] == to) connected = true;
        }
        for (var j = 0; j < to.connected_boxes.length; ++j) {
            if (to.connected_boxes[j] == from) connected = true;
        }
        return !connected;
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
        if (disconnected() && from.can_add()) {
            if (from.outputs) {
                from.add(to, boxes);
            }
            else {
                from.add(to);
            }
        }
    }




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
    f = boxes;
    var canvas = Ext.get('myCanvas');
    var ctx = canvas.dom.getContext('2d');
    ctx.globalAlpha = 1.0;
    ctx.globalCompositeOperation = 'source-over';

    function redraw(e) {
        var coords = imgCoords(e);
        ctx.clearRect(0, 0, 1000, 1000);

        for (var i = 0; i < boxes.length; ++i) {
            if (boxes[i].color_connections) {
                for (var j = 0; j < boxes[i].connected_boxes.length; ++j) {
                    if (j == 0) connect(ctx, boxes[i], boxes[i].connected_boxes[j], 'rgb(0,0,255)');
                    else if (j == 1) connect(ctx, boxes[i], boxes[i].connected_boxes[j], 'rgb(255,0,0)');
                    else connect(ctx, boxes[i], boxes[i].connected_boxes[j], 'rgb(0,0,255)');
                }
            } else {
                for (var j = 0; j < boxes[i].connected_boxes.length; ++j) {
                    connect(ctx, boxes[i], boxes[i].connected_boxes[j], 'rgb(0,0,0)');
                }
            }
        }
        for (var i = 0; i < boxes.length; ++i) {
            boxes[i].draw(ctx);
        }
        switch (selected) {
        case 'file':
            var fb = new FileBox(coords[0], coords[1]);
            for (var i = 0; i < selectedFiles.length; ++i) {
                fb.files.push(new TextBox({
                    'File Name': selectedFiles[i].data['File Name'],
                    'id': selectedFiles[i].data['id']
                }));
            }
            fb.draw(ctx);

            break;
        case 'plus':
            new PlusBox(coords[0], coords[1], 16, 16).draw(ctx);
            break;
        case 'minus':
            new MinusBox(coords[0], coords[1], 16, 16).draw(ctx);
            break;
        case 'filter':
            new FilterBox(coords[0], coords[1], 'Detailed Balance').draw(ctx);
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
            if (boxes[i].selected && boxes[i].moveable) {
                boxes[i].x += coords[0] - mousemovec[0];
                boxes[i].y += coords[1] - mousemovec[1];
                boxes[i].update(ctx);
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
    var from, to, toSave;

    function savable(e) {
        var coords = imgCoords(e);
        toSave = null;
        for (var i = 0; i < boxes.length; ++i) {
            if (boxes[i].x - boxes[i].width / 2 <= coords[0] && boxes[i].x + boxes[i].width / 2 >= coords[0] && boxes[i].y - boxes[i].height / 2 <= coords[1] && boxes[i].y + boxes[i].height / 2 >= coords[1]) {
                if (boxes[i].dataset()) {
                    toSave = boxes[i];
                    return true;
                }
            }
        }
        return false;
    }

    function mouseUp(e) {
        canvas.un('mousemove', moveSelected);
        if (true) {
            var coords = imgCoords(e);
            switch (selected) {
            case 'plus':
                boxes.push(new PlusBox(coords[0], coords[1], 16, 16));
                break;
            case 'minus':
                boxes.push(new MinusBox(coords[0], coords[1], 16, 16));
                break;
            case 'file':
                var fb = new FileBox(coords[0], coords[1]);
                for (var i = 0; i < selectedFiles.length; ++i) {
                    fb.files.push(new TextBox({
                        'File Name': selectedFiles[i].data['File Name'],
                        'id': selectedFiles[i].data['id']
                    }));
                }
                boxes.push(fb);
                break;
            case 'filter':
                boxes.push(new FilterBox(coords[0], coords[1], 'Detailed Balance'));
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
        }
        if (e.button == 2 || e.button == 1) {
            if (connected()) {
                plMenu.items.get('connect').disable();
                plMenu.items.get('disconnect').enable();
            } else if (disconnected() && from.can_add()) {
                plMenu.items.get('connect').enable();
                plMenu.items.get('disconnect').disable();
            } else {
                plMenu.items.get('disconnect').disable();
                plMenu.items.get('connect').disable();
            }
            if (savable(e)) plMenu.items.get('save').enable();
            else plMenu.items.get('save').disable();
            plMenu.items.get('filter_type').disable();
            plMenu.items.get('filter_options').disable();
            for (var i = 0; i < boxes.length; ++i) {
                if (boxes[i].selected && boxes[i].outputs) {
                    plMenu.items.get('filter_type').enable();
                    plMenu.items.get('filter_options').enable();
                    break;
                }
            }
            plMenu.showAt(e.getXY());
            e.stopEvent();
        }
        redraw(e);
    }

    function mouseDown(e) {
        if (true) {
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
        }
        if (e.button == 2 || e.button == 1) {
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
                    temp.remove(boxes);
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
        } else if (e.getKey() == 67) {
            connector();
            e.stopEvent();
        } else if (e.getKey() == 68) {
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
        collapsible: true,
        width: 500,
        height: 300,
        minSize: 100,
        maxSize: 500,
        id: 'ChartPanel',
        items: [ChartContainer],

    });



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
    }




    var viewport = new Ext.Viewport({
        layout: 'border',
        items: [pipelinePanel, grid, ChartPanel],
    });

}
