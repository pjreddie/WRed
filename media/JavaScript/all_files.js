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
        var offset = 0;
        var width = 0;
        if(range != 0){
        loffset = ((low-minvals[cI])/range)*100-1;
        roffset = ((maxvals[cI]-high)/range) * 100-1;
        }
        var ret = high+low;
        return '<div style="border: 1px red solid;"><div style = "border:1px black solid;background-color:black;height:1.5ex;margin-right:'+roffset+'%; margin-left:'+loffset+'%;"></div></div>';
        //return '<div style="border: 1px red solid;padding-left:10px;padding-right:10px"> <div style = "border:1px black solid;background-color:black;"> "" </div> </div>';    
    }
    var dataArray = [];
    function update(){
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
    for(var i = 2; i < fieldData.length; ++i){
        gridColumns.push({header: fieldData[i], width: 100, renderer:vrange, sortable: true, dataIndex: fieldData[i]});
        storeFields.push({name: fieldData[i]});
    }

    var store = new Ext.data.ArrayStore({
        fields: storeFields,
        /*sortType: function(value){
            alert(parseFloat(val.split(',')[0]));
            return parseFloat(val.split(',')[0]);
        },*/
    });
    

    // create the data store

    store.loadData(dataArray);
    // create the Grid
    var grid = new Ext.grid.GridPanel({
        
        store: store,
        columns: gridColumns,
        
        stripeRows: true,
        height: 500,
        width: 900,
        title: 'Array Grid',
        // config options for stateful behavior
        //stateful: true,
        //stateId: 'grid'        
    });
    grid.on('rowdblclick', function(grid, rowIndex, e){window.location = '' + (store.getAt(rowIndex).get('md5'));});
    // render the grid to the specified div in the page
    grid.render('grid-example');
    }
    function cb(data){dataArray = data;update();}
    var jsonpoints = jQuery.getJSON('all/json/', cb);
    
    
});
