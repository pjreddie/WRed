var cstore = new Ext.data.ArrayStore();
function creloadData(response) {
    var pts = response.data;
    var meta = response.metadata;

    if (pts.length == 0) {
        Ext.Msg.alert('Whoops!', 'One or more datafiles is empty!');
        drawChart(cstores, iv, 'Detector', 'ChartContainer');
        return;
    }
    var cfieldData = pts[0];
    pts.splice(0, 1);
    var cgridColumns = [];
    var cstoreFields = [];
    for (var i = 0; i < cfieldData.length; ++i) {
        cgridColumns.push({
            header: cfieldData[i],
            width: 70,
            sortable: true,
            dataIndex: cfieldData[i]
        });
        cstoreFields.push({
            name: cfieldData[i]
        });
    }

    var cstore = new Ext.data.ArrayStore({
        fields: cstoreFields,
    });

    for (var i = 0; i < meta.length; ++i) {
        if (meta[i].name == 'Scan') {
            iv = meta[i].data.split(' ')[0];

        }
    }
    cstore.loadData(pts);
    cstores.push(cstore);
    drawChart(cstores, iv, 'Detector', 'ChartContainer');
}

function getData(store, xChoice, yChoice) {
    var dataResults = [];
    for (var recordIndex = 0; recordIndex < store.getCount(); recordIndex++) {
        var record = store.getAt(recordIndex);
        var data;
        // Calculate error bars with variance if available, else square roots
        if (record.get('_' + yChoice)) {
            data = [+record.get(xChoice), +record.get(yChoice), +Math.sqrt(record.get('_' + yChoice))]; // + to convert string to number
        } else {
            data = [+record.get(xChoice), +record.get(yChoice), +Math.sqrt(record.get(yChoice))]; // + to convert string to number
        }
        dataResults.push(data);
    }

    return dataResults;
} /* Initialize Flot generation, draw the chart with error bars */

function drawChart(stores, xChoice, yChoice, chart) {

    var plotContainer = $('#' + chart);

    plotOptions = {
        series: {
            points: {
                show: true,
                radius: 3
            }
        },
        selection: {
            mode: 'xy'
        },
        crosshair: {
            mode: 'xy'
        },
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
        grid: {
            hoverable: true,
            clickable: true
        },
        //yaxis: { autoscaleMargin: null },
    };
    var seriesPointsOptions = {
        show: true,
        errorbars: 'y',
        yerr: {
            show: true,
            upperCap: '-',
            lowerCap: '-'
        },
    };
    var plotDataSeries = [];

    for (var i = 0; i < stores.length; ++i) {
        var seriesData = getData(stores[i], xChoice, yChoice);
        plotDataSeries.push({
            label: xChoice + ' vs. ' + yChoice + ': Series ' + (i + 1),
            data: seriesData,
            points: seriesPointsOptions,
            lines: {
                show: false
            },
        });
    }

    plot = $.plot(
    plotContainer, plotDataSeries, plotOptions); //.addRose(); // Compass rose for panning
}
