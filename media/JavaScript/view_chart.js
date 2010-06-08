var initComplete = false;


function main() {

// Setup the store and its data

var sampleData = [

[ 'Bob', 20, 13.45 ],

[ 'Bill', 40, 12.92],

[ 'Mike', 45, 23.02]

];


var store = new Ext.data.SimpleStore({

fields : [

{ name: 'name', type: 'string' },

{ name: 'hours', type: 'int' },

{ name: 'rate', type: 'float' },

{ name: 'cost', type: 'float' }

],

data: sampleData

});


// Initialize the grid control

var simpleGrid = new Ext.grid.EditorGridPanel({

store: store,

columns: [{

header: 'Name', // Field cannot be edited.

width: 160,

sortable: false,

dataIndex: 'name'

},

{

header: 'Hours', // Field can be edited

width: 75,

sortable: false,

dataIndex: 'hours',

editor: new Ext.form.NumberField({

allowBlank: false,

allowDecimals: false

})

},

{

header: 'Rate', // Field can be edited

width: 75,

sortable: false,

dataIndex: 'rate',

editor: new Ext.form.NumberField({

allowBlank: false,

allowDecimals: true

})

},

{

header: 'Cost', // Calculated field

width: 75,

sortable: false,

renderer: formatCost,

dataIndex: 'cost'

}

],

clicksToEdit: 1,

stripeRows: true,

height: 100,

enableHdMenu: false,

region: 'south'

});

var commonChartStyle = {"margin": "10px 10px 10px 10px"};

// 1: Set up the containers for the charts

var rateContainer = new Ext.Panel({

height: 200,

width: 200,

style: commonChartStyle,

id: 'rateChartContainer'

});

var hoursContainer = new Ext.Panel({

height: 200,

width: 200,

style: commonChartStyle,

id: 'hoursChartContainer'

});

var costContainer = new Ext.Panel({

height: 200,

width: 200,

style: commonChartStyle,

id: 'costChartContainer'

});

var viewPort = new Ext.Panel({

title: 'Chart-Grid Example',

frame: true,

layout: 'border',

renderTo: Ext.getBody(),

height: 400,

width: 674,

items: [{

region: 'center',

border: true,

bodyStyle: 'background-color: white; border: 1px solid #99BBE8',

layout: 'column',

items: [{

title: 'Hours',

width: 220,

items: hoursContainer

},{

title: 'Rate',

width: 220,

items: rateContainer

},{

title: 'Cost',

width: 220,

items: costContainer

}

]

},

simpleGrid]

});

drawCharts(store);

initComplete = true;

}


function drawCharts(store) {

drawChart(store, 'rate', 'rateChartContainer');

drawChart(store, 'hours', 'hoursChartContainer');

drawChart(store, 'cost', 'costChartContainer');

}


function getData(store, nameColumn, dataColumn) {

var dataResults = new Array();

var tickResults = new Array();

// 2: get the chart data

for( var recordIndex = 0; recordIndex < store.getCount(); recordIndex++ ) {

var record = store.getAt(recordIndex);

var tmpData = [(recordIndex+1)*2, record.get(dataColumn)];

var series = {

bars: { show: true },

label: record.get(nameColumn),

data: [ tmpData, tmpData ], // workaround

color: recordIndex

}

dataResults.push( series );

tickResults.push([ ((recordIndex+1)*2)+1, record.get(nameColumn) ]);

}

return {

data:dataResults,

ticks:tickResults

};

}


function drawChart(store, column, chart) {

var chartInfo = getData(store, 'name', column);

// 3: draw the chart in the container

$.plot($("#"+chart),

chartInfo.data,

{

xaxis: {

autoscaleMargin: .25,

ticks: chartInfo.ticks

}

}

);

}


// Formatting function for the cost column

function formatCost(value, metadata, record, rowIndex, colIndex, store) {

var results = getCost(record);

record.set( 'cost', results);

if ( initComplete ) {

// 4: redraw the charts when the data changes

drawCharts(store);

}

return Ext.util.Format.usMoney(results);

}


// Calculates the cost

function getCost(record) {

var hours = record.get('hours');

var rate = record.get('rate');

var results = hours * rate;

return results;

}

