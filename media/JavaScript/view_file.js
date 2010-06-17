//Author: Joe Redmon
//view_file.js

/*This is where the fun begins, now we have a Tab panel where you can see both the actual data
displayed in an GridPanel, and the chart of the data, rendered with flot*/

Ext.onReady(function(){ 
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

/*ComboBoxes allow user to specify X and Y cooordinates for the graph,
they are populated with field data when the file is initially loaded
and do not get updated if the file is changed, since it is unlikely
that new parameters will be added, even in live data.*/
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
/*Holds the flot plot*/
    var ChartContainer = new Ext.Panel({
        height: 500,
        width: 500,
        style: commonChartStyle,
        id: 'ChartContainer',
    });
/*Holds the chart container and the combo boxes*/
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
/*Draws the chart when the user activates the chart tab. If no choice is specified for the graph,
it defaults to x,y = A4 and Detector*/
function handleActivate(tab){
            if(xChoice.getValue() != "" && yChoice.getValue !="") drawChart(store, xChoice.getValue(), yChoice.getValue(), 'ChartContainer');
            else drawChart(store, 'A4', 'Detector', 'ChartContainer');
}
/*When the user selects a new parameter, the chart is redrawn with that choice in mind*/
function selection(selectedstore, value){
    drawChart(store, xChoice.getValue(), yChoice.getValue(), 'ChartContainer');
}
        tabs.render();
var first = true;
/*Same idea as in all_files.js, when new data comes, we must re-initiallize our store to update the grid/chart/whatever*/
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
/*Retrieve data in json format via a GET request to the server. This is used
anytime there is new data, and initially to populate the table.*/
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
/*Set up the stomp client and subscribe to the channel for our individual file id,
so that we only receive update information about our specific file.*/
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
            //alert('OMG we got updates!!!!1!!!111');
            update();

        };
        stomp.connect('localhost', 61613);
        update();

});
/*Gets data from the Store to draw the chart*/
function getData(store, xcol, ycol) {
    var dataResults = [];

    for( var recordIndex = 0; recordIndex < store.getCount(); recordIndex++ ) {
        var record = store.getAt(recordIndex);
        var data = [record.get(xcol), record.get(ycol), Math.sqrt(record.get(ycol))]; //Error is caculated as sqrts, not included in data file as it should be
        dataResults.push(data);
    }
    return dataResults;
}
/*flot commands for setting up and drawing the chart with error bars*/
function drawChart(store, xcol, ycol, chart) {
    var chartInfo = getData(store, xcol, ycol);
    var data_points = {errorbars: "y",
        yerr: {show:true, upperCap: "-", lowerCap: "-"}};
    var options = {series:{points:{show:true, radius:3}}}
    $.plot($("#"+chart), [{data: chartInfo, points:data_points, lines:{show:false}}], options);
}
