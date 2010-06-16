Ext.onReady(function(){
    

    // NOTE: This is an example showing simple state management. During development,
    // it is generally best to disable state management as dynamically-generated ids
    // can change across page loads, leading to unpredictable results.  The developer
    // should ensure that stable state ids are set for stateful components in real apps.    
    Ext.state.Manager.setProvider(new Ext.state.CookieProvider());
    var store = new Ext.data.ArrayStore();
    var fieldData = [];
    var gridColumns = [];
    var storeFields = [];
    var dataArray = [];




var grid = new Ext.grid.GridPanel({
            store: store,
            columns: gridColumns,
            stripeRows: true,
            height: 300,
            autoWidth:true,
            title: 'File Data',
            horizontalScroll: true,        
        });
        var commonChartStyle = {"margin": "10px 10px 10px 10px"};


    var xChoice = new Ext.form.ComboBox({
        fieldLabel: 'X Axis',
        hiddenName: 'xchoice',
        store: fieldData,
        typeAhead: true,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'X Axis...',
        selectOnFocus:true,
        listeners:{select:{fn:selection}},
    });
    var yChoice = new Ext.form.ComboBox({
        fieldLabel: 'Y Axis',
        hiddenName: 'ychoice',
        store:fieldData,
        typeAhead: true,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Y Axis...',
        selectOnFocus:true,
        listeners:{select:{fn:selection}},
    });

    var ChartContainer = new Ext.Panel({
        height: 500,
        width: 500,
        style: commonChartStyle,
        id: 'ChartContainer',
    });
    var ChartTab = new Ext.Panel({
        title:'Chart',
        autoWidth:true,
        autoHeight:true,
        id: 'ChartTab',
        items: [xChoice, yChoice, ChartContainer],
    });
        var tabs = new Ext.TabPanel({
           renderTo: 'tabs',
           activeTab:0,
           defaults:{autoHeight: true, autoWidth: true},
           layoutOnTabChange:true,
        });
    tabs.add({
        id:'file',
        title: "View File",
        items:[grid],
    }).show();
    tabs.add({
        listeners:{activate:handleActivate},
        id:'chart',
        title:"View Chart",
        items:[ChartTab],
    });

function handleActivate(tab){
            if(xChoice.getValue() != "" && yChoice.getValue !="") drawChart(store, xChoice.getValue(), yChoice.getValue(), 'ChartContainer');
            else drawChart(store, 'A4', 'Detector', 'ChartContainer');
}
function selection(selectedstore, value){
    drawChart(store, xChoice.getValue(), yChoice.getValue(), 'ChartContainer');
}
        tabs.render();
var first = true;
    function reloadData(){
        fieldData = dataArray[0];
        if (first){
            xChoice.store = fieldData;
            yChoice.store = fieldData;
        }
        first = false;
        dataArray.splice(0,1);
        gridColumns = [];
        storeFields = [];
        for(var i = 0; i < fieldData.length; ++i){
            gridColumns.push({header: fieldData[i], width: 70, sortable: true, dataIndex: fieldData[i]});
            storeFields.push({name: fieldData[i]});
        }

        store = new Ext.data.ArrayStore({
            fields: storeFields,
        });
    
        store.loadData(dataArray);

        colModel = new Ext.grid.ColumnModel({columns: gridColumns});

            grid.reconfigure(store, colModel);
        if(tabs.getActiveTab().getId() == 'chart'){
            if(xChoice.getValue() != "" && yChoice.getValue !="") drawChart(store, xChoice.getValue(), yChoice.getValue(), 'ChartContainer');
            else drawChart(store, 'A4', 'Detector', 'ChartContainer');
        }
    }

    var jsonpoints = {}
    function update(){
    var conn = new Ext.data.Connection();
        conn.request({
            url: 'json/'+idNum,
            method: 'GET',
            params: {},
            success: function(responseObject) {
                jsonpoints = Ext.decode(responseObject.responseText);
                dataArray = jsonpoints;
                reloadData();
            },
             failure: function() {
                 alert('Failed Request');
             }
        });
}
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
            stomp.subscribe("/updates/files/"+ idNum);
        };
        stomp.onmessageframe = function(frame){
            // Presumably we should only receive message frames with the
            // destination "/topic/shouts" because that's the only destination
            // to which we've subscribed. To handle multiple destinations we
            // would have to check frame.headers.destination.
            // add_message(frame.body);
            //alert('OMG we got updates!!!!1!!!111');
            update();

        };
        stomp.connect('localhost', 61613);
        update();

});
function getData(store, xcol, ycol) {
    var dataResults = [];

    for( var recordIndex = 0; recordIndex < store.getCount(); recordIndex++ ) {
        var record = store.getAt(recordIndex);
        var data = [record.get(xcol), record.get(ycol), Math.sqrt(record.get(ycol))];
        dataResults.push(data);
    }
    return dataResults;
}

function drawChart(store, xcol, ycol, chart) {
    var chartInfo = getData(store, xcol, ycol);
    var data_points = {errorbars: "y",
        yerr: {show:true, upperCap: "-", lowerCap: "-"}};
    // 3: draw the chart in the container
    var options = {series:{points:{show:true, radius:3}}}
    $.plot($("#"+chart), [{data: chartInfo, points:data_points, lines:{show:false}}], options);
}
