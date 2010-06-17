//Author: Joe Redmon
//all_files.js


Ext.onReady(function(){
    var maxvals = [];
    var minvals = [];
/*Handles rendering of ArrayGrid to show range of parameters in data files*/
    function vrange(val, meta, record, rI, cI, store){
        var range = maxvals[cI] - minvals[cI];
        var spl = val.split(',');
        var low = parseFloat(spl[0]);
        var high = parseFloat(spl[1]);
        var roffset = 0;
        var loffset = 0;
        if(range != 0){
        loffset = ((low-minvals[cI])/range)*100-1;
        roffset = ((maxvals[cI]-high)/range) * 100-1;
        }
        var ret = high+low;
        return '<div style="border: 1px red solid;"><div style = "border:1px black solid;background-color:black;height:1.5ex;margin-right:'+roffset+'%; margin-left:'+loffset+'%;"></div></div>';
    }
    var dataArray = [];
    var store = new Ext.data.ArrayStore();
    gridColumns = [];
    var msg = function(title, msg){
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
        width: 500,
        frame: true,
        title: 'File Upload Form',
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
            text: 'Save',
            handler: function(){
                if(fp.getForm().isValid()){
	                fp.getForm().submit({
	                    url: '../forms/upload/',
	                    waitMsg: 'Uploading your file...',
	                    success: function(fp, o){
	                    }
	                });
                }
            }
        },'-',{
            text: 'Reset',
            handler: function(){
                fp.getForm().reset();
            }
        }]
    });
    var rowRightClicked = 0; //variable to store index of row that is right clicked

/*GridPanel that displays the data*/
    var grid = new Ext.grid.GridPanel({
        tbar:[fp,'-'],
        store: store,
        columns: gridColumns,
        stripeRows: true,
        height: 500,
        width: 900,
        title: 'Available Files',    
    });
    grid.on('rowdblclick', function(grid, rowIndex, e){
         window.location = '../' + (store.getAt(rowIndex).get('id'));
    });

/*Menu that shows up on right click to delete a file from the database*/
    var rowMenu = new Ext.menu.Menu({
        id:'rowMenu',
        items:[
            {
                text: 'Delete', handler:deleteRow,
            },
        ],
    });
/*Sends a POST request to server to delete a file*/
    function deleteRow(){
        var conn = new Ext.data.Connection();
        conn.request({
            url: '../forms/delete/',
            method: 'POST',
            params: {'md5': store.getAt(rowRightClicked).get('md5')},
            success: function(responseObject) {
            },
             failure: function() {
             }
        });
    }
    grid.on('rowcontextmenu', function(grid, rowIndex, e){e.stopEvent();rowRightClicked = rowIndex;rowMenu.showAt(e.getXY());});
    grid.render('allfiles');

/*After data is retrieved from server, we have to reinitiallize the Store reconfigure the ArrayGrid
so that the new data is displayed on the page*/
    function reload_data(){
    var fieldData = dataArray[0]; //First row is the parameters of the data file (e.g. ['X', 'Y', 'Z', 'Temp'])
    maxvals = dataArray[1];       //Second row is the max values of the parameters over all files (used for rendering ranges)
    minvals = dataArray[2];       //Third row is min values of parameters
    dataArray.splice(0,3);        //The rest is the actual data
    var gridColumns = [];
    var storeFields = [];
/*The first three parameters (File Name, database ID, and md5 sum) aren't renedered using the
standard renderer and the ID and md5 sum aren't displayed at all, they are only used for server
requests later, so we add them to the Store differently*/
    gridColumns.push({header: fieldData[0], width: 150, sortable: true, dataIndex: fieldData[0]});
    storeFields.push({name: fieldData[0]});
    gridColumns.push({header: fieldData[1], width: 150,hidden:true, sortable: true, dataIndex: fieldData[1]});
    storeFields.push({name: fieldData[1]});
    gridColumns.push({header: fieldData[2], width: 150,hidden:true, sortable: true, dataIndex: fieldData[2]});
    storeFields.push({name: fieldData[2]});
    for(var i = 3; i < fieldData.length; ++i){
        gridColumns.push({header: fieldData[i], width: 100, renderer:vrange, sortable: true, dataIndex: fieldData[i]});
        storeFields.push({name: fieldData[i]});
    }
    store = new Ext.data.ArrayStore({
        fields: storeFields,
    });
    store.loadData(dataArray);
    colModel = new Ext.grid.ColumnModel({columns: gridColumns});
    grid.reconfigure(store, colModel);

    }
/*Retrieve data in json format via a GET request to the server. This is used
anytime there is new data, and initially to populate the table.*/
    function update(){
    var conn = new Ext.data.Connection();
        conn.request({
            url: 'json/',
            method: 'GET',
            params: {},
            success: function(responseObject) {
                dataArray = Ext.decode(responseObject.responseText);//decodes the response
                reload_data();                                      //resets the store and grids
            },
             failure: function() {
             }
        });
    }
    update();

/*Sets up the stomp connection, subscribes to the 'all' channel, and updates 
whenever any message comes through (whenever files are added, removed, or changed)*/
        stomp = new STOMPClient();
        stomp.onopen = function(){};
        stomp.onclose = function(c){
            alert('Lost Connection, Code: ' + c);
        };
        stomp.onerror = function(error){
            alert("Error: " + error);
        };
        stomp.onerrorframe = function(frame){
            alert("Error: " + frame.body);
        };
        stomp.onconnectedframe = function(){
            stomp.subscribe("/updates/files/all");
        };
        stomp.onmessageframe = function(frame){
            update();
        };
        stomp.connect('localhost', 61613);
});

