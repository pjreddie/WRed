/*!
 * Ext JS Library 3.2.1
 * Copyright(c) 2006-2010 Ext JS, Inc.
 * licensing@extjs.com
 * http://www.extjs.com/license
 */


Ext.onReady(function(){


    // NOTE: This is an example showing simple state management. During development,
    // it is generally best to disable state management as dynamically-generated ids
    // can change across page loads, leading to unpredictable results.  The developer
    // should ensure that stable state ids are set for stateful components in real apps.    
    Ext.state.Manager.setProvider(new Ext.state.CookieProvider());

    var maxvals = [];
    var minvals = [];
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

 var fbutton = new Ext.ux.form.FileUploadField({
        //renderTo: 'uploadfiles',
        buttonOnly: true,
        listeners: {
            'fileselected': function(fb, v){
                var el = Ext.fly('fi-button-msg');
                el.update('<b>Selected:</b> '+v);
                if(!el.isVisible()){
                    el.slideIn('t', {
                        duration: .2,
                        easing: 'easeIn',
                        callback: function(){
                            el.highlight();
                        }
                    });
                }else{
                    el.highlight();
                }
            }
        }
    });

    var fp = new Ext.FormPanel({
        //renderTo: 'uploadfiles',
        //standardSubmit:true,
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
	                        //msg('Success', 'Processed file "'+o.file+'" on the server');
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
    var rowRightClicked = 0;
    var grid = new Ext.grid.GridPanel({
        tbar:[fp,'-'],
        store: store,
        columns: gridColumns,
        stripeRows: true,
        //autoWidth: true,
        height: 500,
        width: 900,
        title: 'Available Files',
        // config options for stateful behavior
        //stateful: true,
        //stateId: 'grid'        
    });
    grid.on('rowdblclick', function(grid, rowIndex, e){
         window.location = '../' + (store.getAt(rowIndex).get('id'));
    });
    var rowMenu = new Ext.menu.Menu({
        id:'rowMenu',
        items:[
            {
                text: 'Delete', handler:deleteRow,
            },
        ],
    });
    function deleteRow(){
        var conn = new Ext.data.Connection();
        conn.request({
            url: '../forms/delete/',
            method: 'POST',
            params: {'md5': store.getAt(rowRightClicked).get('md5')},
            success: function(responseObject) {
                //showHistoryDialog(responseObject.responseText);
            },
             failure: function() {
                 //Ext.Msg.alert('Status', 'Unable to show history at this time. Please try again later.');
             }
        });
    }
    grid.on('rowcontextmenu', function(grid, rowIndex, e){e.stopEvent();rowMenu.showAt(e.getXY());rowRightClicked = rowIndex;});
    grid.render('allfiles');


    function reload_data(){
    var fieldData = dataArray[0];
    maxvals = dataArray[1];
    minvals = dataArray[2];
    dataArray.splice(0,3);
    var gridColumns = [];
    var storeFields = [];
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

    // create the data store

    store.loadData(dataArray);
    colModel = new Ext.grid.ColumnModel({columns: gridColumns});
    grid.reconfigure(store, colModel);

    }

    function update(){
    var conn = new Ext.data.Connection();
        conn.request({
            url: 'json/',
            method: 'GET',
            params: {},
            success: function(responseObject) {
                dataArray = Ext.decode(responseObject.responseText);
                reload_data();
            },
             failure: function() {
             }
        });
    }
    update();



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
            // Presumably we should only receive message frames with the
            // destination "/topic/shouts" because that's the only destination
            // to which we've subscribed. To handle multiple destinations we
            // would have to check frame.headers.destination.
            //add_message(frame.body);
            update();
        };
        stomp.connect('localhost', 61613);
});

