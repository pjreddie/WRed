// Authors: Joe Redmon and Ophir Lifshitz
// view_file.js

/* This is where the fun begins, now we have a Tab panel where you can see both the actual data
displayed in an GridPanel, and the chart of the data, rendered with flot */

Ext.onReady(function () {
    loadMask = new Ext.LoadMask(Ext.getBody(), { msg: 'Please wait a moment while the page loads...' } );
    loadMask.show();
    
    Ext.state.Manager.setProvider(new Ext.state.CookieProvider());
    var conn = new Ext.data.Connection();
    var store = new Ext.data.ArrayStore();
    var fieldData = [];
    var gridColumns = [];
    var storeFields = [];
    var dataArray = [];

    // Initialize grid for data view
    var DataTab = new Ext.grid.GridPanel({
        title:          'Data table',
    
        store:          store,
        columns:        gridColumns,
        stripeRows:     true,
        height:         588,
        autoWidth:      true,
        horizontalScroll: true,
        
        id:             'DataTabPanel',
    });
    
    var GridRowContextMenu = new Ext.menu.Menu({
        id:             'GridRowContextMenu',
        items:          [{
                            text:       'Highlight this point on chart',
                            icon:       'http://famfamfam.com/lab/icons/silk/icons/tag_yellow.png',
                            handler:    function() { alert('Not yet...'); }
                        }],
    });
    
    function displayGridRowContextMenu (grid, rowIndex, event) {
        GridRowContextMenu.showAt(event.getXY());
        event.stopEvent();
    }




// [ CHART PANEL ]

    /* ComboBoxes allow user to specify X and Y cooordinates for the graph, they are populated with field data when the file is initially loaded and do not get updated if the file is changed, since it is unlikely that new parameters will be added, even in live data. */
    var xChoice = new Ext.form.ComboBox({
        fieldLabel:     'X axis',
        hiddenName:     'xchoice',
        store:          fieldData,
        typeAhead:      true,
        mode:           'local',
        triggerAction:  'all',
        emptyText:      'Select X axis...',
        selectOnFocus:  true,
        listeners:      { select: { fn: selection } },
        
        id:             'xTitle',
        listClass:      'xChoiceList', /* Apply class to dropdown menu list */
    });
    var yChoice = new Ext.form.ComboBox({
        fieldLabel:     'Y axis',
        hiddenName:     'ychoice',
        store:          fieldData,
        typeAhead:      true,
        mode:           'local',
        triggerAction:  'all',
        emptyText:      'Select Y axis...',
        selectOnFocus:  true,
        listeners:      { select: { fn: selection } },
        
        id:             'yTitle',
        listClass:      'yChoiceList', /* Apply class to dropdown menu list */
    });

    // Comboboxes have their own containers to apply unique styles (i.e., alignment relative to plot)
    var xChoiceContainer = new Ext.Container({
     // width:          500,
        id:             'xChoiceContainer',
        cls:            'ChoiceContainer',
        items:          [ xChoice ],
    });
    var yChoiceContainer = new Ext.Container({
     // height:         500,
        id:             'yChoiceContainer',
        cls:            'ChoiceContainer',
        items:          [ yChoice ],
    });
    
    
    /* Holds the flot plot */
    var PlotContainer = new Ext.Container({
        id:             'PlotContainer',
    });
    
    var ChartContainer = new Ext.Container({
     // height:         500,
        valueField:     'id',
        displayField:   'name',
        autoWidth:      true,
        
        id:             'ChartContainer',
        items:          [ PlotContainer ],
    });
    
    var PlotContextMenu = new Ext.menu.Menu({
        id:             'PlotContextMenu',
        items:          [{
                            text:       '<s>Zoom reset<\/s>',
                            icon:       'http://famfamfam.com/lab/icons/silk/icons/zoom.png',
                            handler:    zoomPlot,
                            data:       0.0,
                        },
                        {
                            text:       'Zoom in (+25%)',
                            icon:       'http://famfamfam.com/lab/icons/silk/icons/zoom_in.png',
                            handler:    zoomPlot,
                            data:       1.25,
                        },
                        {
                            text:       'Zoom out (\u201325%)',
                            icon:       'http://famfamfam.com/lab/icons/silk/icons/zoom_out.png',
                            handler:    zoomPlot,
                            data:       0.8,
                        },
                        '-',
                        {
                            id:         'dragCheckZoom',
                            text:       'Drag and select to zoom',
                          //icon:       'http://famfamfam.com/lab/icons/silk/icons/magnifier.png',
                            iconCls:    'icon-radio-unchecked',
                            group:      'dragCheck',
                            checked:    false,
                            checkHandler: dragCheckHandler,
                        },
                        {
                            id:         'dragCheckPan',
                            text:       'Drag to pan',
                          //icon:       'http://sexybuttons.googlecode.com/svn-history/r2/trunk/images/icons/silk/arrow_nsew.png',
                            iconCls:    'icon-radio-checked',
                            group:      'dragCheck',
                            checked:    true,
                            checkHandler: dragCheckHandler,
                        }],
    });
    
    function displayPlotContextMenu (event) {
        PlotContextMenu.showAt(event.getXY());
        event.stopEvent();
    }



// [ TOOLS PANEL ]

    var FunctionSelectStore = new Ext.data.ArrayStore({
        data:           [ [ 1, 'Gaussian' ], [ -1, '...' ] ],
        fields:         [ 'id', 'name' ],
    });
    var FunctionSelect = new Ext.form.ComboBox({
        fieldLabel:     'Function',
        emptyText:      'Select a fitting function...',
        hiddenName:     'function',
        
        allowBlank:     false,
        anchor:         '-20',
        
        store:          FunctionSelectStore,
        valueField:     'id',
        displayField:   'name',
        
        typeAhead:      true,
        mode:           'local',
        triggerAction:  'all',
        selectOnFocus:  true,
        listeners:      {},
        
        id:             'FunctionSelect',
        itemCls:        'formSelect',
    });
    
    var FitThisSeriesButton = new Ext.Button({
        text:           'Fit this series',
        type:           'submit',
        handler:        fitSeries,
        
        id:             'FitThisSeriesButton',
        cls:            'submitButton',
    });
    var ClearThisCurveButton = new Ext.Button({
        text:           'Clear this curve',
        type:           'reset',
        handler:        clearCurve,
        
        id:             'ClearThisCurveButton',
        cls:            'resetButton',
    });

    function fitSeries (button, event) {
        fittingFunction = FunctionSelect.getValue();
        if (fittingFunction === '' || fittingFunction == '-1')
            Ext.Msg.show({ title: 'Form incomplete', msg: 'Please select a function.', buttons: Ext.Msg.OK, icon: Ext.Msg.ERROR, fn: function () {} } );
        else {
            Ext.Msg.alert('Form complete', 'Submitting function...');
            
            data = getDataInCols(store, xChoice.getValue(), yChoice.getValue());
            makeFittingRequest({ 'actionID': 0, 'actionName': 'sendData', 'x': JSON.stringify(data.x), 'y': JSON.stringify(data.y) },
            function (responseObject) {
                Ext.Msg.alert('Step 1', 'Please click on the peak of the data');
                var clickPos = [];
                $('#PlotContainer').one('plotclick', function (event, pos, item) {
                    makeFittingRequest({ 'actionID': 1, 'actionName': 'sendPeak', 'peakX': pos.x, 'peakY': pos.y },
                    function (responseObject) {
                        Ext.Msg.alert('Step 2', 'Please click on the width of the data');
                        var clickPos = [];
                        $('#PlotContainer').one('plotclick', function (event, pos, item) {
                            makeFittingRequest({ 'actionID': 2, 'actionName': 'sendWidth', 'widthX': pos.x, 'widthY': pos.y },
                            function (responseObject) { alert(responseObject.responseText); }
                            );
                        });
                    });
                });
            });
        }
    }
    function clearCurve (button, event) {


    }

    function makeFittingRequest (params, successFunction) {
        conn.request({
            url: 'fitting/' + idNum + '/',
            method: 'POST',
            params: params,
            success: successFunction,
            failure: function () {
                alert('Error: Failed request');
            }
        });
    }


    var FittingPanel = new Ext.FormPanel({
        title:          'Fitting Tools',
        
        defaultType:    'textfield',
        labelWidth:     80,
        defaults:       { anchor: '-20', msgTarget: 'side' },
        
        autoWidth:      true,
        autoHeight:     true,
        bodyStyle:      'padding: 10px;',

        id:             'FittingPanel',
        items:          [ FunctionSelect, FitThisSeriesButton, ClearThisCurveButton ],
        tools:          [ { id: 'gear' }, { id: 'help' } ],
    });
    
    
    
    
    
// [ TAB PANELS ]

    var ToolsPanel = new Ext.Panel({
        title:          'Tools',
        region:         'east',
        collapsible:    true,
        
        minWidth:       200,
        layout:         'accordion',
        layoutConfig:   { animate: true, },
        
        id:             'ToolsPanel',
        items:          [ FittingPanel ],
    });
    
    /* Holds the chart and the two combo boxes */
    var ChartPanel = new Ext.Panel({
        title:          'Chart',
        region:         'center',
        
        minWidth:       755,
        width:          900,
        
        id:             'ChartPanel',
        items:          [ yChoiceContainer, ChartContainer, xChoiceContainer ],
        tools:          [{
                            id: 'refresh',
                            qtip: 'Refresh chart',
                            handler: activateChart,
                        }],
    });
    
    /* Holds the chart container and the other tool panels */
    var ChartTab = new Ext.Panel({
//      title:          'Chart Tab',
//      autoWidth:      true,
        height:         588, // why not auto!?
        
        layout:         'border',
        defaults:       { split: true },
        
        id:             'ChartTabPanel',
        items:          [ ChartPanel, ToolsPanel ],
    });
    
    

    /* Create and initialize tabs */
    var tabs = new Ext.TabPanel({
       renderTo:        'tabs',
       activeTab:       0,
       defaults:        { autoWidth: true, autoHeight: true },
       layoutOnTabChange: true,
    });
    tabs.add({
        id:             'DataTab',
        title:          'Data',
        items:          [ DataTab ],
    }).show();
    tabs.add({
        listeners:      { activate: activateChart },
        id:             'ChartTab',
        title:          'Chart',
        items:          [ ChartTab ],
    }).show();
    
    tabs.setActiveTab('DataTab');

    tabs.render();
    var first = true;


    DataTab.on('rowcontextmenu', displayGridRowContextMenu);
    PlotContainer.getEl().on('contextmenu', displayPlotContextMenu);



    /* Draws the chart when the user activates the chart tab. If no choice is specified for the graph, it defaults to A4 and Detector */
    function activateChart() {
        if (xChoice.getValue() == '' || yChoice.getValue == '') {
            xChoice.setValue('A4');
            yChoice.setValue('Detector');
        }
        drawChart(store, xChoice.getValue(), yChoice.getValue(), 'PlotContainer');
    }

    /* When the user selects a new parameter from the comboboxes, the chart is redrawn with that choice in mind */
    function selection(selectedstore, value) {
        activateChart();
    }

    /* Retrieve data in json format via a GET request to the server. This is used anytime there is new data, and initially to populate the table. */
    function update() {
        conn.request({
            url: 'json/' + idNum + '/',
            method: 'GET',
            params: {},
            success: function (responseObject) {
                jsonpoints = Ext.decode(responseObject.responseText);
                dataArray = jsonpoints;
                reloadData();
                loadMask.hide();
            },
            failure: function () {
                Ext.Msg.alert('Error', 'Failed JSON request');
            }
        });
    }

    /* Same idea as in all_files.js, when new data comes, we must re-initialize our store to update the plot */
    function reloadData() {
        fieldData = dataArray[0];
        if (first) {
            xChoice.store = fieldData;
            yChoice.store = fieldData;
        }
        first = false;
        dataArray.splice(0, 1);
        gridColumns = [];
        storeFields = [];
        for (var i = 0; i < fieldData.length; ++ i) {
            gridColumns.push({ header: fieldData[i], width: 70, sortable: true, dataIndex: fieldData[i] });
            storeFields.push({ name: fieldData[i] });
        }

        store = new Ext.data.ArrayStore({
            fields: storeFields,
        });

        store.loadData(dataArray);
        colModel = new Ext.grid.ColumnModel({ columns: gridColumns });
        DataTab.reconfigure(store, colModel);

        if (tabs.getActiveTab().getId() == 'chart') {
            activateChart(tabs.getActiveTab());
        }
    }
    
    var jsonpoints = {};

    /* Set up the stomp client, subscribe to channel of individual file ID so that we only receive update information about our specific file. */
    var stomp = new STOMPClient();
    stomp.onopen = function () {};
    stomp.onclose = function (c) {
        Ext.Msg.alert('Error', 'Lost connection, Code: ' + c);
    };
    stomp.onerror = function (error) {
        Ext.Msg.alert('Error', error);
    };
    stomp.onerrorframe = function (frame) {
        Ext.Msg.alert('Error', frame.body);
    };
    stomp.onconnectedframe = function () {
        stomp.subscribe('/updates/files/' + idNum);
    };
    stomp.onmessageframe = function (frame) {
        // Ext.Msg.alert('Success', 'OMG we got updates!!!!1!!!111');
        update();
    };
    stomp.connect('localhost', 61613);
    update();
});

/* Gets data from the Store to draw the chart */
function getData(store, xChoice, yChoice) {
    var dataResults = [];

    for (var recordIndex = 0; recordIndex < store.getCount(); recordIndex++ ) {
        var record = store.getAt(recordIndex);
        
        // Calculate error bars with square roots; not included in data file as it should be
        var data = [ +record.get(xChoice), +record.get(yChoice), +Math.sqrt(record.get(yChoice)) ]; // + to convert string to number
        
        dataResults.push(data);
    }
    
    return dataResults;
}

/* Gets data from the Store to draw the chart */
function getDataInCols(store, xChoice, yChoice) {
    var dataResults = { x: [], y: [] };

    for (var recordIndex = 0; recordIndex < store.getCount(); recordIndex++ ) {
        var record = store.getAt(recordIndex);

        dataResults.x.push( +record.get(xChoice));
        dataResults.y.push( +record.get(yChoice));
    }
    
    return dataResults;
}

/* Initialize Flot generation, draw the chart with error bars */
function drawChart(store, xChoice, yChoice, chart) {
    var chartInfo = getData(store, xChoice, yChoice);

    var plotContainer = $('#' + chart);
    
    var datapoints = {
        errorbars: 'y',
        yerr: { show: true, upperCap: '-', lowerCap: '-' },
    };
    
    var options = {
      series: { points: { show: true, radius: 3 } },
      selection: { mode: 'xy' },
      crosshair: { mode: 'xy' },
      zoom: { // plugin
          interactive: true,
          //recenter: true,
          selection: 'xy',
          //trigger: null,
          amount: 1.25,
      },
      pan: { // plugin
          interactive: true,
      },
      grid: { hoverable: true, clickable: true },
      //yaxis: { autoscaleMargin: null },
    };

    var plotData = [{
            label:    xChoice + ' vs. ' + yChoice + ': Series 1',
            data:     chartInfo,
            points:   datapoints,
            lines:    { show: false },
        }];


    plot = $.plot(
        plotContainer,
        plotData,
        options); //.addRose(); // Compass rose for panning


/*
    plotContainer.bind('plothover', function (event, pos, item) {
        dataX = pos.x;
        dataY = pos.y;
        
        if (item) {
            mouseX = item.pageX;
            mouseY = item.pageY;
            
            $('#pX').text(dataX);
            $('#pY').text(dataY);
            
            $('#dX').text(item.datapoint[0]);
            $('#dY').text(item.datapoint[1]);
            $('#dE').text(item.datapoint[2]);
            $('#tt').css({ display: 'block', left: mouseX + 3, top: mouseY + 3 });
        }
        else
            $('#tt').css({ display: 'none' });
    });
    */
    plotContainer.bind('plotclick', function (event, pos, item) {
        var previousPoints = [];
        if (item) {
            plot.highlight(item.series, item.datapoint);
            previousPoints.push(item);
        }
        else {
            for (i in previousPoints)
                plot.unhighlight(previousPoints[i].series, previousPoints[i].datapoint);
            previousPoints = [];
        }
    });
    /*
    plotContainer.bind('plotselected', function (event, ranges) {
        var extension = {};

        if (dragCheckState == 'dragCheckZoom') {
            // clamp the zooming to prevent eternal zoom
            if (ranges.xaxis.to - ranges.xaxis.from < 0.01)
                ranges.xaxis.to = ranges.xaxis.from + 0.01;
            if (ranges.yaxis.to - ranges.yaxis.from < 0.01)
                ranges.yaxis.to = ranges.yaxis.from + 0.01;
            
            
            // do the zooming
            extension = {
                            pan:   { interactive: true },
                            zoom:  { interactive: true  },
                            xaxis: { min: ranges.xaxis.from, max: ranges.xaxis.to },
                            yaxis: { min: ranges.yaxis.from, max: ranges.yaxis.to },
                        };
        }
        else {
            var newXdelta = ranges.xaxis.to - ranges.xaxis.from;
            var newXmin = plot.getAxes().xaxis.min + newXdelta;
            var newXmax = plot.getAxes().xaxis.max + newXdelta;
            var newYdelta = ranges.yaxis.to - ranges.yaxis.from;
            var newYmin = plot.getAxes().yaxis.min + newYdelta;
            var newYmax = plot.getAxes().yaxis.max + newYdelta;
            
            extension = {
                            pan:   { interactive: true  },
                            zoom:  { interactive: true },
                            xaxis: { min: newXmin, max: newXmax },
                            yaxis: { min: newYmin, max: newYmax },
                        };
        }
        plot = $.plot(plotContainer, plotData,
                      $.extend(true, {}, options, extension));
    });*/

}

function zoomPlot (menuItem, event) {
    if (menuItem.data == 0) {
        // something?
    }
    else
        plot.zoom({ amount: menuItem.data, recenter: true });
}

dragCheckState = 'dragCheckPan';

function dragCheckHandler(menuItem, checked) {
    if (checked === true) {
        dragCheckState = menuItem.id;
    }
    var iconCls = 'icon-radio-' + ((checked === true) ? '' : 'un') + 'checked';
    menuItem.setIconClass(iconCls);
}
