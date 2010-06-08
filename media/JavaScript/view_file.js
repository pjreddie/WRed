Ext.onReady(function(){


    // NOTE: This is an example showing simple state management. During development,
    // it is generally best to disable state management as dynamically-generated ids
    // can change across page loads, leading to unpredictable results.  The developer
    // should ensure that stable state ids are set for stateful components in real apps.    
    Ext.state.Manager.setProvider(new Ext.state.CookieProvider());

    var dataArray = [];
    function update(){
        var fieldData = dataArray[0];
        dataArray.splice(0,1);
        var gridColumns = [];
        var storeFields = [];
        for(var i = 0; i < fieldData.length; ++i){
            gridColumns.push({header: fieldData[i], width: 70, sortable: true, dataIndex: fieldData[i]});
            storeFields.push({name: fieldData[i]});
        }

        var store = new Ext.data.ArrayStore({
            fields: storeFields,
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
            stateful: true,
            stateId: 'grid'        
        });
    
        // render the grid to the specified div in the page
        grid.render('grid-example');
    }
    function cb(data){
        dataArray = data;
        update();
    }
    var jsonpoints = jQuery.getJSON('files/json/ee4fea29545cbcd1079d955aeb90740e', cb);
    
    
});
