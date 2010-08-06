// Authors: Joe Redmon and Ophir Lifshitz
// view_file.js

/* This is where the fun begins, now we have a Tab panel where you can see both the actual data
displayed in an GridPanel, and the chart of the data, rendered with flot */

var globalPlots = { plot: [], residplot: [] };
var globalDataSeries = { plot: [], residplot: [] };
var globalFunctionSeries = { plot: [], residplot: [] };
var plot;
var residplot;
var stage = 1;

Ext.onReady(onReadyFunction);

function onReadyFunction () {
    loadMask = new Ext.LoadMask(Ext.getBody(), { msg: 'Please wait a moment while the page loads...' } );
    loadMask.show();
    
    Ext.state.Manager.setProvider(new Ext.state.CookieProvider());
    var conn = new Ext.data.Connection();
    var store = new Ext.data.ArrayStore();
    var fieldData = [];
    var gridColumns = [];
    var storeFields = [];
    var metadataObj = {};
    var dataArray = [];
    var iv = 'A4';
    
    // Initialize grid for data view
    var GridPanel = new Ext.grid.GridPanel({
        title:          'Data table',
        
        region:         'center',
        height:         588,
        autoWidth:      true,
        horizontalScroll: true,
        
        store:          store,
        columns:        gridColumns,
        stripeRows:     true,
        
        id:             'GridPanel',
    });
    
    var MetadataStore = new Ext.data.JsonStore({
        data:           [],
        fields:         ['name', 'data'],
    });
    var MetadataGridPanel = new Ext.grid.GridPanel({
        
        store:          MetadataStore,
        columns:        [ { header: 'Name', dataIndex: 'name', width: 164 }, { header: 'Data', id: 'data', dataIndex: 'data', width: 1000 }],
        stripeRows:     true,
        
//        viewConfig:     { forceFit: true },
//        autoExpandColumn: 'data',
//        horizontalScroll: true,

        title:          'Metadata',
        
        onRender:       MetadataGridTooltipRender,
        listeners: {
            render: function (g) {
                g.on("beforetooltipshow", function(grid, row, col) {
                    metadataRecord = MetadataStore.getAt(row);
                    metadataText = metadataRecord.get(metadataRecord.fields.keys[col]);
                    grid.tooltip.body.update(metadataText);
                });
            }
        },

        
        region:         'east',
        collapsible:    true,
        minWidth:       200,
        width: 250,
        maxWidth:       500,
        
        id:             'MetadataGridPanel',
    });
    

    var DataTabPanel = new Ext.Panel({
        height:         588, // why not auto!?
        
        layout:         'border',
        defaults:       { split: true },
        
        id:             'DataTabPanel',
        items:          [ GridPanel, MetadataGridPanel ],
    });

    var GridRowContextMenu = new Ext.menu.Menu({
        id:             'GridRowContextMenu',
        items:          [{
                            text:       'Highlight this point on chart',
                            icon:       '/media/icons/silk/tag_yellow.png',
                            handler:    GridRowContextHighlight,
                        }],
    });
    
    function displayGridRowContextMenu (grid, rowIndex, event) {
        GridRowContextMenu.grid = grid;
        GridRowContextMenu.rowIndex = rowIndex;
        GridRowContextMenu.showAt(event.getXY());
        event.stopEvent();
    }
    function GridRowContextHighlight (menuItem, event) {
        record = menuItem.parentMenu.grid.getStore().getAt(menuItem.parentMenu.rowIndex);
        xData = record.get(xChoice.getValue());
        yData = record.get(yChoice.getValue());
        
        plot.highlight(plot.getData()[0], [xData, yData]);
    }
    
    Ext.ToolTip.prototype.onTargetOver = Ext.ToolTip.prototype.onTargetOver.createInterceptor(function (e) {
        this.baseTarget = e.getTarget();
    });
    Ext.ToolTip.prototype.onMouseMove = Ext.ToolTip.prototype.onMouseMove.createInterceptor(function(e) {
        if (!e.within(this.baseTarget)) {
            this.onTargetOver(e);
            return false;
        }
    });
    function MetadataGridTooltipRender () {
        Ext.grid.GridPanel.prototype.onRender.apply(this, arguments);
        this.addEvents("beforetooltipshow");
        this.tooltip = new Ext.ToolTip({
            renderTo: Ext.getBody(),
            target: this.view.mainBody,
            listeners: {
                beforeshow: function(qt) {
                    var v = this.getView();
    			          var row = v.findRowIndex(qt.baseTarget);
    			          var cell = v.findCellIndex(qt.baseTarget);
    			          this.fireEvent("beforetooltipshow", this, row, cell);
                },
                scope: this,
            }
        });
    }



// [ CHART PANEL ]

    var ChartStatusContainer = new Ext.Container({
//        autoHeight:     true,
        colspan:        3,
        
        id:             'ChartStatusContainer',
        html:           '<p></p>',
    });

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
    var xyCornerContainer = new Ext.Container({
        id:             'xyCornerContainer',
        
        html:           '<p style="letter-spacing: -0.75px; line-height: .85; font-size: .7em;">Mouse: (<span id="MIC-mx"></span>, <span id="MIC-my"></span>)<br/>' +
                        'Page: (<span id="MIC-px"></span>, <span id="MIC-py"></span>)<br />' +
                        '<span id="MIC-d" style="display: none;">Point: (<span id="MIC-dx"></span>, <span id="MIC-dy"></span> &plusmn; <span id="MIC-de"></span>)</p>',
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
    
    LegendDataSeriesStore = new Ext.data.JsonStore({
        data:           globalDataSeries.plot,
        fields:         [ 'label', 'data', 'points', 'lines', 'color' ],
        autoLoad:       true,
    });
    LegendFunctionSeriesStore = new Ext.data.JsonStore({
        data:           globalFunctionSeries.plot,
        fields:         [ 'label', 'data', 'points', 'lines', 'color' ],
        autoLoad:       true,
    });
    var LegendDataSeriesTemplate = new Ext.XTemplate(
        '<h2>Data</h2>',
        '<ul class="legendSeries" id="legendDataSeries">',
        '<tpl for=".">',
            '<li id="legendDataSeries{#}">',
                '<input type="checkbox" name="legendDataSeriesCheck{#}" id="legendDataSeriesCheck{#}" />',
                '<label for="legendDataSeriesCheck{#}">',
                    '<span class="seriesName">',
                        '<span style="-moz-box-shadow: 0 0 0 1px {color}; -webkit-box-shadow: 0 0 0 1px {color}; background-color: {color};"></span>',
                        '{label}',
                    '</span>',
                '</label>',
            '</li>',
        '</tpl></ul>'
    );
    var LegendFunctionSeriesTemplate = new Ext.XTemplate(
        '<h2>Functions</h2>',
        '<ul class="legendSeries" id="legendFunctionSeries">',
        '<tpl for=".">',
            '<li id="legendFunctionSeries{#}">',
                '<input type="checkbox" name="legendFunctionSeriesCheck{#}" id="legendFunctionSeriesCheck{#}" />',
                '<label for="legendFunctionSeriesCheck{#}">',
                    '<span class="seriesName">',
                        '<span style="-moz-box-shadow: 0 0 0 1px {color}; -webkit-box-shadow: 0 0 0 1px {color}; background-color: {color};"></span>',
                        '{label}',
                    '</span>',
                    '<div>',
                    '<tpl if="/*console.log(88, */ curF = globalFunctionSeries.plot[xindex - 1]"></tpl>',
                    // If there is at least one function
                    '<tpl if="(typeof curF.functionInfos != \'undefined\' && curF.functionInfos.length &gt;= 1)">',
                        // If fitting was completed
                        '<tpl if="typeof curF.fitInfo != \'undefined\'">',
                            '<p>&chi;&#178; = {[curF.fitInfo.chisq]}</p>',
                        '</tpl>',
                        // Loop through each of them
                        '<tpl for="curF.functionInfos">',
                            ///'<tpl if="console.log(89,values)"></tpl>',
                            '<dl>',
                                '<dt>{#}. <strong>{functionName}</strong></dt>',
                                '<dd>',
                                // If fitting was completed
                                '<tpl if="typeof values.fitFunctionParams != \'undefined\'">',
                                    ///'<tpl if="console.log(90,fitFunctionParams)"></tpl>',
                                    ///'<tpl if="console.log(90,values)"></tpl>',
                                    '<tpl for="values.fitFunctionParamsArray">',
                                        '<p>{name} = {value} &plusmn; {err}</p>',
                                    '</tpl>',
                                '</tpl>',
                                '</dd>',
                            '</dl>',
                        '</tpl>',
                    '</tpl>',
                    '</div>',
                '</label>',
            '</li>',
        '</tpl></ul>'
    );
    var LegendDataSeriesContainer = new Ext.DataView({
        tpl:            LegendDataSeriesTemplate,
        store:          LegendDataSeriesStore,
        itemSelector:   'li',
    
        id:             'LegendDataSeriesContainer',
        autoWidth:      true,
    });
    var LegendFunctionSeriesContainer = new Ext.DataView({
        tpl:            LegendFunctionSeriesTemplate,
        store:          LegendFunctionSeriesStore,
        itemSelector:   'li',
    
        id:             'LegendFunctionSeriesContainer',
        autoWidth:      true,
    });
    var ChartInfoContainer = new Ext.Container({
//        title:          'Chart information',
        
//        autoHeight:     true,
        rowspan:        3,
        
        id:             'ChartInfoContainer',
        items:          [ LegendDataSeriesContainer, LegendFunctionSeriesContainer ],
    });
    var yResidContainer = new Ext.Container({
        id:             'yResidualsContainer',
    });
    var ResidPlotContainer = new Ext.Container({
        id:             'ResidPlotContainer',
    });
    var ResidChartContainer = new Ext.Container({
        title:          'Residuals',
        
        id:             'ResidChartContainer',
        items:          [ ResidPlotContainer ],
    });



    var PlotContextMenu = new Ext.menu.Menu({
        id:             'PlotContextMenu',
        items:          [{
                            text:       'Zoom reset',
                            icon:       '/media/icons/silk/zoom.png',
                            handler:    zoomPlot,
                            data:       0.0,
                        },
                        {
                            text:       'Zoom in (+25%)',
                            icon:       '/media/icons/silk/zoom_in.png',
                            handler:    zoomPlot,
                            data:       1.25,
                        },
                        {
                            text:       'Zoom out (\u201325%)',
                            icon:       '/media/icons/silk/zoom_out.png',
                            handler:    zoomPlot,
                            data:       0.8,
                        },
                        '-',
                        {
                            id:         'dragCheckZoom',
                            text:       'Drag and select to zoom',
                          //icon:       '/media/icons/silk/magnifier.png',
                          //iconCls:    'icon-radio-unchecked',
                            group:      'dragCheck',
                            checked:    false,
                            checkHandler: dragCheckHandler,
                        },
                        {
                            id:         'dragCheckPan',
                            text:       'Drag to pan',
                          //icon:       'http://sexybuttons.googlecode.com/svn-history/r2/trunk/images/icons/silk/arrow_nsew.png',
                          //iconCls:    'icon-radio-checked',
                            group:      'dragCheck',
                            checked:    true,
                            checkHandler: dragCheckHandler,
                        },
                        '-',
                        {
                            id:         'scaleCheckLog',
                            text:       '<s>Logarithmic scale<\/s>',
                            group:      'scaleCheck',
                            checked:    false,
                            checkHandler: scaleCheckHandler,
                        },
                        {
                            id:         'scaleCheckLinear',
                            text:       '<s>Linear scale<\/s>',
                            group:      'scaleCheck',
                            checked:    false,
                            checkHandler: scaleCheckHandler,
                        }],
    });
    
    function displayPlotContextMenu (event) {
        PlotContextMenu.showAt(event.getXY());
        event.stopEvent();
    }


// [ TOOLS PANEL ]


// TOOLBAR


     FunctionSelectStore = new Ext.data.ArrayStore({
        data:           [ [ 1, 'Linear' ], [ 2, 'Linear drag' ],
                          [ 11, 'Gaussian' ], [ 12, 'Gaussian drag' ],
                          [ 21, 'Lorentzian' ], [ 22, 'Lorentzian drag' ],
                          [ -1, '...' ] ],
        fields:         [ 'id', 'name' ],
        idIndex:        0, // Important: specifies the index of the ID column; used in getById()
    });
     FunctionSelect = new Ext.form.ComboBox({
        fieldLabel:     'Function',
        emptyText:      'Select a function...',
        hiddenName:     'function',
        
        allowBlank:     false,
        
        store:          FunctionSelectStore,
        valueField:     'id',
        displayField:   'name',
        
        typeAhead:      true,
        mode:           'local',
        triggerAction:  'all',
        selectOnFocus:  true,
        width:          125,
        
        id:             'FunctionSelect',
        itemCls:        'formSelect',
    });/*
     CreateFunctionButton = new Ext.Button({
        text:           'Create function',
        type:           'submit',
        handler:        fitFunction,
        
        id:             'CreateFunctionButton',
        cls:            'submitButton',
     });
     AddFunctionToSelectedCurveButton = new Ext.Button({
        text:           'Add function to selected curve',
        type:           'submit',
        handler:        fitFunction,
        
        id:             'AddFunctionToSelectedCurveButton',
        cls:            'submitButton',
    });
    var FitThisSeriesButton = new Ext.Button({
        text:           'Fit this series',
        type:           'submit',
        handler:        fitSeries,
        
        id:             'FitThisSeriesButton',
        cls:            'submitButton strongButton',
    });
    var ClearThisCurveButton = new Ext.Button({
        text:           'Clear this curve',
      //type:           'reset',
        handler:        clearCurve,
        
        id:             'ClearThisCurveButton',
        cls:            'resetButton',
    });*/

// TOOLBAR!



    var NewFunctionButton = new Ext.Button({
        id:           'CreateFunctionButton2',
        text:         'New',
        iconCls:      'icon-function',
        handler:      fitFunction,
        
        arrowAlign:   'right',
        iconAlign:    'left',
        width:        '50',
        
//        menu: [ AddFunctionToSelectedCurveButton ],
    });
    var AddFunctionToSelectedCurveButton = new Ext.Button({
        id:           'AddFunctionToSelectedCurveButton',
        text:         'Add to selected curve',
        handler:      fitFunction,
        iconCls:      'icon-sigma',
    });
    var ClearFunctionButton = new Ext.Button({
        id:           'ClearThisCurveButton2',
        text:         'Clear',
        iconCls:      'icon-cross-circle',
        handler:      clearCurve,
        
        arrowAlign:   'right',
        iconAlign:    'left',
        width:        '50',
    });
    var ParamFunctionButton = new Ext.Button({
        id:           'ParamFunctionButton',
        text:         'Parameters',
        iconCls:      'icon-table-sum',
        handler:      showParamWindow,
        
        arrowAlign:   'right',
        iconAlign:    'left',
        width:        '50',
    });
    var FunctionsButtonGroup = new Ext.ButtonGroup({
        title:  'Functions',
        items: [ FunctionSelect, NewFunctionButton, AddFunctionToSelectedCurveButton, ClearFunctionButton, ParamFunctionButton ]
    });
    
    var FitSeriesButton = new Ext.Button({
        id:           'FitSeriesButton2',
        text:         'Fit series',
        iconCls:      'icon-layer-vector',
        handler:      fitSeries,
        
        cls:          'strongButton',
        arrowAlign:   'right',
        iconAlign:    'left',
        width:        '50',
    });
    var AutoFitSeriesButton = new Ext.Button({
        id:           'AutoFitSeriesButton',
        text:         'AutoFit',
        iconCls:      'icon-wand',
        handler:      autoFitSeries,
        
        cls:          'strongButton',
        arrowAlign:   'right',
        iconAlign:    'left',
        width:        '50',
    });
    var FitButtonGroup = new Ext.ButtonGroup({
        title:  'Fitting',
        items: [ FitSeriesButton, AutoFitSeriesButton ]
    });
    var ChartBar = {
        items: [ FunctionsButtonGroup, FitButtonGroup ]
    };
    


    function fitFunction (button, event) {
        fittingFunction = FunctionSelect.getValue();
        //fittingFunction = record.data.id;
        
        if (fittingFunction === '' || fittingFunction == '-1') {
            Ext.Msg.alert('Form incomplete', 'Please select a function.');
        }
        else {
            var checkedIndices = getCheckedIndices();
            
            if (button.id.indexOf('AddFunctionToSelectedCurve') === 0 && !checkedIndices.functionSeries.length) {
                Ext.Msg.alert('Form incomplete', 'Please select at least one curve to which you would like to add the function.');
            }
            else {
                sendFunction(button, checkedIndices);
            }
        }
    }
    
    function sendFunction(button, checkedIndices) {
        var data = getDataInCols(store, xChoice.getValue(), yChoice.getValue());
        
        var prevFunctions = [];
        if (button.id.indexOf('AddFunctionToSelectedCurve') === 0) {
            for (var checkedFunctionIndex = 0; checkedFunctionIndex < checkedIndices.functionSeries.length; checkedFunctionIndex ++) {
                //console.log('==', selectedFunctionIndex);
                var selectedFunctionIndex = checkedIndices.functionSeries[checkedFunctionIndex];
                var selectedFunctionSeries = globalFunctionSeries.plot[selectedFunctionIndex];
                //console.log('Selected series: ', selectedFunctionSeries);
                prevFunctions = prevFunctions.concat(selectedFunctionSeries.functionInfos);
                //console.log('Length: ', prevFunctions);
                //console.log('==');
                /* { 'functionID':     selectedFunctionSeries.functionID,
                     'functionParams': selectedFunctionSeries.functionParams,
                     'functionIndex':  selectedFunctionIndex }*/
            }
            //console.log(globalFunctionSeries.plot);
            //console.log(prevFunctions);
            replaceIndices = checkedIndices.functionSeries;
        }
        else
            replaceIndices = [ globalFunctionSeries.plot.length ];
        
        var functionID = FunctionSelect.getValue();
        makeFittingRequest({ 'actionID': 1, 'actionName': 'sendData', 'functionID': functionID,
                             'replaceIndices': JSON.stringify(replaceIndices),
                             'data': JSON.stringify(data), 'prevFunctions': JSON.stringify(prevFunctions) }, doFitInstruction);
    }
    
    function getCheckedIndices() {
        var checkedDataSeriesIndices = [];
        $('#legendDataSeries input[type=checkbox]:checked').each(function() {
            if (this.checked) checkedDataSeriesIndices.push($('#legendDataSeries li input').index(this));
        });
        var checkedFunctionSeriesIndices = [];
        $('#legendFunctionSeries input[type=checkbox]:checked').each(function() {
            if (this.checked) checkedFunctionSeriesIndices.push($('#legendFunctionSeries li input').index(this));
        });
        
        var checkedIndices = { dataSeries: checkedDataSeriesIndices, functionSeries: checkedFunctionSeriesIndices };
        return checkedIndices;
    }
    function setCheckedIndices(checkedIndices) {
        $('#legendDataSeries input[type=checkbox]').each(function() {
            $(this).attr('checked', jQuery.inArray($('#legendDataSeries li input').index(this), checkedIndices.dataSeries) !== -1);
        });
        $('#legendFunctionSeries input[type=checkbox]').each(function() {
            $(this).attr('checked', jQuery.inArray($('#legendFunctionSeries li input').index(this), checkedIndices.functionSeries) !== -1);
        });
    }
    
    function fitSeries (button, event) {
        var checkedIndices = getCheckedIndices();

        var allData = [];
        var allFunctionInfos = [];
        for (var checkedDataIndex = 0; checkedDataIndex < checkedIndices.dataSeries.length; checkedDataIndex ++) {
            var checkedDataSeries = globalDataSeries.plot[checkedIndices.dataSeries[checkedDataIndex]];
            var checkedDataSeriesData = dataPointsToCols(checkedDataSeries.data);
            allData.push(checkedDataSeriesData);
        }
        for (var checkedFunctionIndex = 0; checkedFunctionIndex < checkedIndices.functionSeries.length; checkedFunctionIndex ++) {
            var checkedFunctionSeries = globalFunctionSeries.plot[checkedIndices.functionSeries[checkedFunctionIndex]];
            var checkedFunctionSeriesInfos = checkedFunctionSeries.functionInfos;
            allFunctionInfos.push(checkedFunctionSeriesInfos);
        }
      //console.log(allData, allFunctionInfos);
        
        if (allData.length < 1 || allFunctionInfos.length < 1)
            Ext.Msg.alert('Form incomplete', 'Please select at least one data series and at least one function.');
        else {
            makeFittingRequest({ 'actionID': 3, 'actionName': 'sendData', 'replaceIndices': JSON.stringify(checkedIndices.functionSeries),
                                 'allData': JSON.stringify(allData), 'allFunctionInfos': JSON.stringify(allFunctionInfos) }, doFitInstruction);
            updateLegend();
        }
    }
    function autoFitSeries(button, event) {
        var allData = [];
        for (var checkedDataIndex = 0; checkedDataIndex < globalDataSeries.plot.length; checkedDataIndex ++) {
            var checkedDataSeries = globalDataSeries.plot[checkedDataIndex];
            var checkedDataSeriesData = dataPointsToCols(checkedDataSeries.data);
            allData.push(checkedDataSeriesData);
        }

        conn.request({
            url: 'fitting/' + idNum + '/',
            method: 'POST',
            params: { 'actionID': 4, 'actionName': 'sendData', 'allData': JSON.stringify(allData) },
            successFunction: doFitInstruction});
        updateLegend();
    }
    
    function doFitInstruction(responseObject) {
        responseJSON = Ext.decode(responseObject.responseText);
        
        switch (responseJSON['dataType']) {
            case 'askPoint':
                askPoint(responseJSON);
                break;
            case 'askDrag':
                askDrag(responseJSON);
                if (responseJSON.dragMode != 'before')
                    doPlotting(responseJSON);
                break;
            case 'doingDrag':
                doPlotting(responseJSON);
                break;
            case 'doFit':
                doPlotting(responseJSON);
                break;
            default:
                doPlotting(responseJSON);
        }
        allowNextRequest = true;
    }
    function askPoint(responseJSON) {
        updateFittingStatus(responseJSON);
        
        $('#PlotContainer').one('plotclick', function (event, pos, item) {
            updateFittingStatus();
            makeFittingRequest({ 'actionID': 2, 'actionName': 'sendPoint', 'dataType': 'askPoint',
                                 'xPos': pos.x, 'yPos': pos.y, 'xID': responseJSON['xID'], 'yID': responseJSON['yID'] }, doFitInstruction);
        });
    }
    function askDrag(responseJSON) {
        updateFittingStatus(responseJSON);

        $('#PlotContainer').one('dragstart', { 'responseJSON': responseJSON }, onDragStart);
        $('#PlotContainer').bind('drag', function() {}); // To trigger dragstart/dragend events
        $('#PlotContainer').one('dragend', function (event) {
            $('#PlotContainer').unbind('plothover', onDrag);
            updateFittingStatus();
          //console.log('End');
        });
    }
    function onDragStart (event) {
      //console.log('Start');
        
        pos = event2pos(event);
        /*
        makeFittingRequest({ 'actionID': 2, 'actionName': 'sendPoint', 'dataType': 'askDrag',
                             'xPosstart': pos.x, 'yPosstart': pos.y, 'xIDstart': responseJSON['xIDstart'], 'yIDstart': responseJSON['yIDstart'],
                             'xPosend':   pos.x, 'yPosend':   pos.y, 'xIDend':   responseJSON['xIDend'],   'yIDend':   responseJSON['yIDend'] },
                             function() {});*/
        makeFittingRequest({ 'actionID': 2, 'actionName': 'sendPoint', 'dataType': 'askDrag', 'dragMode': 'start',
                             'xPos': pos.x, 'yPos': pos.y, 'xID': responseJSON['xIDstart'], 'yID': responseJSON['yIDstart'] },
                             function() {});
        makeFittingRequest({ 'actionID': 2, 'actionName': 'sendPoint', 'dataType': 'askDrag', 'dragMode': 'start2',
                             'xPos': pos.x + 0.00001, 'yPos': pos.y + 0.00001, 'xID': responseJSON['xIDend'], 'yID': responseJSON['yIDend'] },
                             function() {}); // To prevent undefined on backend
        $('#PlotContainer').bind('plothover', { 'responseJSON': responseJSON }, onDrag);
    }
    function onDrag (event, pos, item) {
//        pos = event2pos(event);
        //console.log(event.data.responseJSON);
        //console.log(responseJSON);
        
        if (allowNextRequest) {
        //  //console.log('Request');
            makeFittingRequest({ 'actionID': 2, 'actionName': 'sendPoint', 'dataType': 'askDrag', 'dragMode': 'during',
                                 'xPos': pos.x, 'yPos': pos.y, 'xID': event.data.responseJSON['xIDend'], 'yID': event.data.responseJSON['yIDend'] },
                                 doFitInstruction);
            allowNextRequest = false;
        }
        //else
        //  //console.log('No request');
    }
    function event2pos (event) {
        var offset = plot.offset(),
            plotOffset = plot.getPlotOffset(),
            axes = plot.getAxes(),
            pos = { pageX: event.pageX, pageY: event.pageY },
            canvasX = event.pageX - offset.left - plotOffset.left,
            canvasY = event.pageY - offset.top - plotOffset.top;
        pos.x = axes.xaxis.c2p(canvasX);
        pos.y = axes.yaxis.c2p(canvasY);
        
        return pos;
    }
    
    function doPlotting (responseJSON) {
        FunctionName = FunctionSelectStore.getById(FunctionSelect.getValue()).data.name;
        if (responseJSON.replaceIndices)
            var functionSeriesReplaceIndices = responseJSON.replaceIndices;
        
      //console.log('Response: ', responseJSON);
      //console.log(FunctionName + ': ', functionSeriesReplaceIndices);
      //console.log('Functions retrieved: ', responseJSON.functionInfos);
        
        
        fitpoints = responseJSON.fit;
        
        newPlotData = {
            label:    xChoice.getValue() + ' vs. ' + yChoice.getValue() + ': Function',
            data:     fitpoints,
            points:   { show: false },
            lines:    { show: true },
            seriesType: 'function',
            
            functionInfos: responseJSON.functionInfos,
        };
        if (responseJSON.hasOwnProperty('fitInfo'))
             newPlotData.fitInfo = responseJSON.fitInfo;

        var plotHoverFunctionSeries = globalFunctionSeries.plot;

        
        residpoints = responseJSON.resid;
        
        newResidPlotData = {
            label:    xChoice.getValue() + ' vs. ' + yChoice.getValue() + ': Resid',
            data:     residpoints,
            points:   { show: true },
            lines:    { show: true },
        };

        var residplotHoverFunctionSeries = globalFunctionSeries.residplot;


        if (functionSeriesReplaceIndices) {
            globalFunctionSeries.plot = removeMultiple(globalFunctionSeries.plot, functionSeriesReplaceIndices);
            globalFunctionSeries.residplot = removeMultiple(globalFunctionSeries.residplot, functionSeriesReplaceIndices);
            
            globalFunctionSeries.plot.splice(functionSeriesReplaceIndices[functionSeriesReplaceIndices.length - 1], 0, newPlotData);
            globalFunctionSeries.residplot.splice(functionSeriesReplaceIndices[functionSeriesReplaceIndices.length - 1], 0, newResidPlotData);
        }
        else {
            globalFunctionSeries.plot.push(newPlotData);
            globalFunctionSeries.residplot.push(newResidPlotData);
        }

        //console.log('ph', plotHoverFunctionSeries);

        //plot = $.plot($('#PlotContainer'), plotHoverFunctionSeries, plotOptions);
        //plot.setData(plotHoverFunctionSeries);
        //plot.setupGrid();
        //plot.draw();


        //console.log('rph', residplotHoverFunctionSeries);

        //residplot = $.plot($('#ResidPlotContainer'), residplotHoverFunctionSeries, residplotOptions);
        //residplot.setData(residplotHoverFunctionSeries);
        //residplot.axis()
        //residplot.setupGrid();
        //residplot.draw();
        
        
                //console.log(plotFunctionSeries, residplotFunctionSeries);
                //console.log(plot.getData(), residplot.getData());
        
        updatePlots('PlotContainer', true); // "true" suppresses plot.setupGrid() so points outside data's y-axis extrema 
    }
    
    function updateFittingStatus(responseJSON) {
        var statusBar = Ext.get('ChartStatusContainer');
        if (responseJSON) {
            statusBar.highlight();
            statusBar.update('<p><strong>' + responseJSON['messageTitle'] + ':</strong> ' + responseJSON['messageText'] + '</p>');
        }
        else {
        //    statusBar.slideUp();
            statusBar.update('<p></p>');
        }
    }
    
    function clearCurve (button, event) {
        var checkedIndices = getCheckedIndices();
        
        if (checkedIndices.functionSeries.length == 0) {
            Ext.Msg.alert('Error in clearing curve', 'Please select at least one curve to clear.');
        }
        else if (checkedIndices.dataSeries.length) {
            Ext.Msg.alert('Error in clearing curve', 'You can\'t clear the data itself, silly!');
        }
        else {
            /*
            Ext.Msg.confirm('Confirm clearing of curves',
                            'Are you sure you want to clear ' + ((checkedIndices.length > 1)
                                                                  ? 'these ' + checkedIndices.functionSeries.length + ' curves?' : 'this curve?'),
                            function (confirm) {
                if (confirm == 'yes') {
            */
                    var newPlotFunctionSeries = [], newResidplotFunctionSeries = [];
                    
                    for (var index = 0; index < globalFunctionSeries.plot.length; index ++) {
                        if (jQuery.inArray(index, checkedIndices.functionSeries) == -1) {
                            newPlotFunctionSeries.push(globalFunctionSeries.plot[index]);
                            newResidplotFunctionSeries.push(globalFunctionSeries.residplot[index]);
                        }
                    }
                    
                    globalFunctionSeries = { plot: newPlotFunctionSeries, residplot: newResidplotFunctionSeries };
                    updatePlots('PlotContainer', true);
            /*
                }
            });
            */
        }
    }

    function makeFittingRequest (params, successFunction) {
        conn.request({
            url: 'fitting/' + idNum + '/',
            method: 'POST',
            params: params,
            success: successFunction,
            failure: function () {
                Ext.Msg.alert('Error: Failed request');
            }
        });
    }
    
    
    
    /*
    Ext.data.Record.create([
       {name: 'firstName', mapping: 'guestName.first'},
       {name: 'secondName', mapping: 'guestName.second'},
   	   {name: 'attendingReception', mapping: 'comingToReception'},
       {name: 'attendingCeremony', mapping: 'comingToCeremony'}
    ]);*/
    
    
/*

    var ParamStore = new Ext.data.JsonStore({
        data:           globalFunctionSeries.plot,
        fields:         ['functionID', 'functionName', 'functionParams'],
        idProperty:     'functionID',
        root:           'functionInfos'
    });/*
    var ParamGridPanel = new Ext.grid.GridPanel({
        store:          ParamStore,
        columns:        [
            {
                id: 'paramName',
                header: 'Name',
                dataIndex: ''
            }
        ],
        title: 'asdf',
    
    
    });
    
*/

    var ParamForm = new Ext.form.FormPanel({
        labelWidth:     30,
        bodyStyle:      'padding: 10px;',
        
        layout: {
            type: 'vbox',
            align: 'stretch',
        },
        
        id:             'ParamForm',
        title:          'Edit parameters',
        
        items: [ { xtype:'textfield', } ]
    
    });
    var ParamWindow = new Ext.Window({
        width:          640,
        height:         460,
        minWidth:       380,
        minHeight:      320,
        
        layout:         'fit',
        collapsible:    true,
        maximizable:    true,
        closeAction:    'hide',
        
        
        id:             'ParamWindow',
        title:          'Function parameters',
        
        items:          [ ParamForm ],
    });
    pw = ParamWindow;

    function showParamWindow (button, event) {
        ParamWindow.show();
    }

/*
    var FittingPanel = new Ext.FormPanel({
        title:          'Fitting tools',
        
        layout:         'form',
        
        defaultType:    'textfield',
        labelWidth:     80,
        defaults:       { anchor: '-20', msgTarget: 'side' },
        
        autoWidth:      true,
        autoHeight:     true,
        bodyStyle:      'padding: 10px;',

        id:             'FittingPanel',
        items:          [ FunctionSelect, CreateFunctionButton, AddFunctionToSelectedCurveButton, FitThisSeriesButton, ClearThisCurveButton ],
        tools:          [ { id: 'gear' }, { id: 'help' } ],
    });
    */
    
    
    
    
// [ TAB PANELS ]
/*
    var ToolsPanel = new Ext.Panel({
        title:          'Tools',
        region:         'east',
        collapsible:    true,
        
        minWidth:       200,
        layout:         'accordion',
        layoutConfig:   { animate: true, },
        
        id:             'ToolsPanel',
        items:          [ FittingPanel ],
    });*/
    
    /* Holds the chart and the two combo boxes */
    var ChartPanel = new Ext.Panel({
        title:          'Chart',
        region:         'center',
        
        layout:         'table',
        layoutConfig:   { columns: 3, tableAttrs: { valign: 'top' } },
        
        minWidth:       755,
        width:          900,
        
        id:             'ChartPanel',
        items:          [ ChartStatusContainer, yChoiceContainer, ChartContainer, ChartInfoContainer, xyCornerContainer, xChoiceContainer, yResidContainer, ResidChartContainer ],
        tools:          [{
                            id: 'refresh',
                            qtip: 'Refresh chart',
                            handler: activateChart,
                        }],
    });
    
    
    
    /* Holds the chart container and the other tool panels */
    var ChartTabPanel = new Ext.Panel({
//      title:          'Chart tab',
//      autoWidth:      true,
        height:         908, //588, // why not auto!?
        
        tbar:           ChartBar,
        
        layout:         'border',
        defaults:       { split: true },
        
        id:             'ChartTabPanel',
        items:          [ ChartPanel ], //ToolsPanel
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
        iconCls:        'data_table',
        items:          [ DataTabPanel ],
    }).show();
    tabs.add({
        listeners:      { activate: function() { activateChart(); } },
        id:             'ChartTab',
        title:          'Chart',
        iconCls:        'chart_curve',
        items:          [ ChartTabPanel ],
    }).show();
    
    tabs.setActiveTab('ChartTab');
    tabs.render();


    GridPanel.on('rowcontextmenu', displayGridRowContextMenu);
    PlotContainer.getEl().on('contextmenu', displayPlotContextMenu);



    /* Draws the chart when the user activates the chart tab. If no choice is specified for the graph, it defaults to A4 and Detector */
    function activateChart() {
        drawChart(store, xChoice.getValue(), yChoice.getValue(), 'PlotContainer');
        //updatePlots('PlotContainer');
    }

    /* When the user selects a new parameter from the comboboxes, the chart is redrawn with that choice in mind */
    function selection(selectedstore, value) {
        initializeData(store, xChoice.getValue(), yChoice.getValue(), 'PlotContainer');
        activateChart();
    }

    /* Retrieve data in json format via a GET request to the server. This is used anytime there is new data, and initially to populate the table. */
    function update() {
        conn.request({
            url: 'json/' + idNum + '/',
            method: 'GET',
            params: {},
            success: function (responseObject) {
                responseJSON = Ext.decode(responseObject.responseText);
                metadataObj = responseJSON.metadata;
                
              //console.log('update', stage);
                // Detect independent variable [Joe]
                if (stage === 1) {
                    yChoice.setValue('Detector');
                    for (var i = 0; i < metadataObj.length; ++ i) {
                        if (metadataObj[i].name == 'Scan') {
                            xChoice.setValue(metadataObj[i].data.split(' ')[0]);
                        }
                    }
                }
                MetadataStore.loadData(metadataObj);
                dataArray = responseJSON.data;
                reloadData();
                initializeData(store, xChoice.getValue(), yChoice.getValue(), true);
                drawChart(store, xChoice.getValue(), yChoice.getValue(), 'PlotContainer');
                loadMask.hide();
                if (stage === 1) {
                    stage = 2;
                }
            },
            failure: function () {
                Ext.Msg.alert('Error', 'Failed JSON request');
            }
        });
    }

    /* Same idea as in all_files.js, when new data comes, we must re-initialize our store to update the plot */
    function reloadData() {
        fieldData = dataArray[0];
      //console.log('reloadData', stage);
        if (stage === 1) {
            xChoice.store = fieldData;
            yChoice.store = fieldData;
            stage = 2;
        }
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
        GridPanel.reconfigure(store, colModel);

        if (tabs.getActiveTab().getId() == 'ChartTab') {
            activateChart();
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

    // }}}}

    /* Gets data from the Store to draw the chart */
    function getData(store, xChoice, yChoice) {
        var dataResults = [];

        for (var recordIndex = 0; recordIndex < store.getCount(); recordIndex ++ ) {
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

        for (var recordIndex = 0; recordIndex < store.getCount(); recordIndex ++ ) {
            var record = store.getAt(recordIndex);

            dataResults.x.push( +record.get(xChoice));
            dataResults.y.push( +record.get(yChoice));
        }
        
        return dataResults;
    }

    /* Gets data from the Store to draw the chart */
    function dataPointsToCols(data) {
        var dataResults = { x: [], y: [], yerr: [] };

        for (var index = 0; index < data.length; index ++ ) {
            dataResults.x.push( +data[index][0] );
            dataResults.y.push( +data[index][1] );
            if (typeof data[index][2] !== 'undefined')
                dataResults.yerr.push( +data[index][2] );
        }
        
        if (dataResults.yerr.length == 0)
            delete dataResults.yerr;
        
        return dataResults;
    }

    function objectToArrayPairs (object) {
        var array = [];
        for (var key in object) {
            if (validation_messages.hasOwnProperty(key)) {
                array.push({ 'name': key, 'value': object[key] });
            }
        }
        return array;
    }


    function updateLegend() {
        var checkedIndices = getCheckedIndices();
    
        // Get data with flot's added properties
        //if (typeof plot !== 'undefined')
        //    globalPlots.plot = plot.getData();
            
        LegendDataSeriesStore.loadData(globalDataSeries.plot);
        LegendFunctionSeriesStore.loadData(globalFunctionSeries.plot);
        
        setCheckedIndices(checkedIndices);
        legendSeriesClick();
        $('.legendSeries input:checkbox').bind('click', legendSeriesClick); // jQuery's .live() should be good
    }

    function legendSeriesClick() {
        checkedIndices = getCheckedIndices();
        
        if (checkedIndices.dataSeries.length) {
            AddFunctionToSelectedCurveButton.disable();
            ClearFunctionButton.disable();
          //console.log(checkedIndices);
            if (checkedIndices.functionSeries.length) {
                FitSeriesButton.enable();
            }
            else {
                FitSeriesButton.disable();
            }
        }
        else {
            FitSeriesButton.disable();
            if (checkedIndices.functionSeries.length >= 1) {               
                AddFunctionToSelectedCurveButton.enable();
                ClearFunctionButton.enable();
            }
            else {
                ClearFunctionButton.disable();
                AddFunctionToSelectedCurveButton.disable();
            }
        }
        //FitSeriesButton.setText('Fit ' + ((checkedIndices.functionSeries.length > 1) ? 'these ' + checkedIndices.functionSeries.length + ' series' : 'this series'));
        //ClearFunctionButton.setText('Clear ' + ((checkedIndices.functionSeries.length > 1) ? 'these ' + checkedIndices.functionSeries.length + ' curves' : 'this curve'));
    }
    
    function initializePlots(chart) {
        var plotContainer = $('#' + chart);

        plotOptions = {
          hooks: { draw: [ updateLegend ] },
          
          legend: { show: false }, // because we have a custom legend
          series: { points: { show: true, radius: 3 } },
  //      selection: { mode: 'xy' },
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


        plot = $.plot(
            plotContainer,
            [], // we add the series later
            plotOptions); // Compass rose for panning
        plot.addRose();

        plotContainer.bind('plothover', function (event, pos, item) {
            $('#MIC-mx').text(pos.x.toPrecision(5));
            $('#MIC-my').text(pos.y.toPrecision(5));
            $('#MIC-px').text(pos.pageX);
            $('#MIC-py').text(pos.pageY);

            if (item) {
                mouseX = item.pageX;
                mouseY = item.pageY;
                
                $('#MIC-dx').text(item.datapoint[0].toPrecision(5));
                $('#MIC-dy').text(item.datapoint[1].toPrecision(5));
                if (item.datapoint[2])
                    $('#MIC-de').text(item.datapoint[2].toPrecision(5));
                $('#MIC-d').css({ display: 'block' }); //, left: mouseX + 3, top: mouseY + 3 });
            }
            else
                $('#MIC-d').css({ display: 'none' });
        });
        
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

    // RESID

        var residplotContainer = $('#Resid' + chart);

        residplotOptions = {
          legend: { show: false }, // because we have a custom legend
          series: { points: { show: true, radius: 3 } },
  //      selection: { mode: 'xy' },
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
        
        residplot = $.plot(
            residplotContainer,
            [],
            residplotOptions);
        
        plotContainer.bind('plotzoom', function (event, plot_, limits) {
            residplot.axis([ limits[0], limits[1], null, null ]);
        });
        plotContainer.bind('plotpan', function (event, plot, ranges) {
            residplot.pan(ranges);
        });
        residplotContainer.bind('plotzoom', function (event, plot_, limits) {
            plot.axis([ limits[0], limits[1], null, null ]);
        });
        residplotContainer.bind('plotpan', function (event, plot, ranges) {
            plot.pan(ranges);
        });
    }

    function initializeData(store, xChoice, yChoice, replaceAll) {
        var plotSeriesData = getData(store, xChoice, yChoice);
        
        var plotSeriesPointsOptions = {
            show: true,
            errorbars: 'y',
            yerr: { show: true, upperCap: '-', lowerCap: '-' },
        };
        var plotDataSeries = {
            label:    xChoice + ' vs. ' + yChoice + ': Series',
            data:     plotSeriesData,
            points:   plotSeriesPointsOptions,
            lines:    { show: false },
            color:    'rgb(0, 0, 0)',
            seriesType: 'data',
        };
        
        var residplotSeriesPointsOptions = {
            show: true,
        };
        var residplotDataSeries = {
            label:    '',
            data:     [],
            points:   residplotSeriesPointsOptions,
            lines:    { show: true },
            color:    'rgb(255, 51, 51)',
        };
        
        if (replaceAll) {
            globalDataSeries.plot = [plotDataSeries];
            globalDataSeries.residplot = [residplotDataSeries];
        }
        else {
            globalDataSeries.plot.push(plotDataSeries);
            globalDataSeries.residplot.push(residplotDataSeries);
        }

      //console.log('initData', stage);
    }
    
    function updatePlots(chart, preventSetupGrid) {
      //console.log('updatePlots', stage);
        
        var plotContainer      = $('#'      + chart);
        var residplotContainer = $('#Resid' + chart);
        
        var updatePlotData = globalDataSeries.plot.concat(globalFunctionSeries.plot);
        var updateResidplotData = globalDataSeries.residplot.concat(globalFunctionSeries.residplot);
        
        plot.setData(updatePlotData);
        residplot.setData(updateResidplotData);
        if (!preventSetupGrid) {
            plot.setupGrid();
            residplot.setupGrid();
        }
        
        //updateGlobals();
        
        plot.draw();
        residplot.draw();
        
        // Copy initial x-axis scale on plot to residplot
        var plotInitialAxesScales = plot.getAxesScales();
        residplot.axis([ plotInitialAxesScales[0], plotInitialAxesScales[1], null, null ]);
    }
    
    function updateGlobals() {
        
        var plotData = plot.getData();
        var residplotData = residplot.getData();
        var newDataSeries = { plot: [], residplot: [] };
        var newFunctionSeries = { plot: [], residplot: [] };
        
      //console.log(plotData);
        for (var index = 0; index < plotData.length; index ++) {
          //console.log(index);
          //console.log(plotData[index]);
            if (plotData[index].seriesType == 'data') {
                newDataSeries.plot.push(plotData[index]);
                newDataSeries.residplot.push(residplotData[index]);
            }
            else if (plotData[index].seriesType == 'function') {
                newFunctionSeries.plot.push(plotData[index]);
                newFunctionSeries.residplot.push(residplotData[index]);            
            }
        }
      //console.log(globalDataSeries);
      //console.log(globalFunctionSeries);
      //console.log(newDataSeries);
      //console.log(newFunctionSeries);
      //console.log(globalDataSeries == newDataSeries);
        globalDataSeries = newDataSeries;
        globalFunctionSeries = newFunctionSeries;
    }
    
    /* Initialize Flot generation, draw the chart with error bars */
    function drawChart(store, xChoice, yChoice, chart) {
  //console.log('drawChart', stage);
        switch (stage) {
            case 1:
                initializePlots(chart);
                break;
            case 2:
                initializeData(store, xChoice, yChoice);
                stage = 3;
                break;
            default:
                updatePlots(chart);
                break;
        }
  //console.log('drawChart', stage);
    }
    
    

    function hypot(x, y) {
      return Math.sqrt(x * x + y * y);
    }

    function zoomPlot (menuItem, event) {
        if (menuItem.data == 0) {
            plot.axis();
            residplot.axis();
        }
        else {
            plot.zoom({ amount: menuItem.data, recenter: true });
            residplot.zoom({ amount: menuItem.data, recenter: true });
        }
    }

    /*
    dragCheckState = 'dragCheckPan';

    function dragCheckHandler(menuItem, checked) {
        if (checked === true) {
            dragCheckState = menuItem.id;
        }
        var iconCls = 'icon-radio-' + ((checked === true) ? '' : 'un') + 'checked';
      //menuItem.setIconClass(iconCls);
    }
    */

    function dragCheckHandler (menuItem, checked) {}

    function scaleCheckHandler (menuItem, checked) {}
    
    function randomColor () {
        var rint = Math.round(0xffffff * Math.random());
        return 'rgb(' + (rint >> 16) + ', ' + (rint >> 8 & 255) + ', ' + (rint & 255) + ')';
    }
    
    function removeMultiple (array, removeIndices) {
        var newArray = [];
        for (var index = 0; index < array.length; index ++) {
            if (jQuery.inArray(index, removeIndices) == -1)
                newArray.push(array[index]);
        }
        return newArray;
    }
    
}
/*
            if (button.id === 'CreateFunctionButton') {
                makeFittingRequest({ 'actionID': 1, 'actionName': 'sendData', 'functionID': FunctionSelect.getValue(),
                                     'data': JSON.stringify(data), 'prevFunctions': JSON.stringify([]) }, doFitInstruction);
            }
            else if (button.id === 'AddFunctionToSelectedCurveButton') {
*/
