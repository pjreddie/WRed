/*!
 * Ext JS Library 3.2.1
 * Copyright(c) 2006-2010 Ext JS, Inc.
 * licensing@extjs.com
 * http://www.extjs.com/license
 *
 * Author: Alex Yee
 * Edit History:
 * 7/12/2010: Created and completed. Created layout, columns, and data sending/receiving/updating. 
 *             Not entirely beautified yet.
 * 7/13/2010: Restructured to give each numberfield (of input) a separate variable so I could
 *             send their given values to the backend for calculations.
 */

Ext.onReady(function () {
    var conn = new Ext.data.Connection();

    // ********* END - Defining and assigning variables for the numberfield inputs  *********  
    var cm = new Ext.grid.ColumnModel({
        // specify any defaults for each column
        defaults: {
            sortable: false,
            align: 'right',
            width: 60,
            editor: new Ext.form.NumberField({
                allowBlank: false,
                allowDecimals: true,
                decimalPrecision: 10,

            })
        },
        columns: [
            {
            header: 'h',
            dataIndex: 'h',
            },
        {
            header: 'k',
            dataIndex: 'k',
            },
        {
            header: 'l',
            dataIndex: 'l',
            },
        {
            header: '2θ',
            dataIndex: 'twotheta',
            },
        {
            header: 'θ',
            dataIndex: 'theta',
            },
        {
            header: 'χ',
            dataIndex: 'chi',
            },
        {
            header: 'φ',
            dataIndex: 'phi',
            },
            ]
    });

    var cm2 = new Ext.grid.ColumnModel({
        defaults: {
            sortable: false,
            align: 'right',
            width: 60,
            editor: new Ext.form.NumberField({
                allowBlank: false,
                allowDecimals: true,
                decimalPrecision: 10,

            })
        },
        columns: [
            {
            header: '2θ',
            dataIndex: 'twotheta',
            },
        {
            header: 'θ',
            dataIndex: 'theta',
            },
        {
            header: 'ω',
            dataIndex: 'omega',
            },
        {
            header: 'χ',
            dataIndex: 'chi',
            },
        {
            header: 'φ',
            dataIndex: 'phi',
            },
            ]
    });

    var baseData = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ];
    var baseIdealData = [
        [0.0, 0.0, 0.0, 0.0, 0.0],
        ];

    // create the Data Store
    var store = new Ext.data.ArrayStore({
        // destroy the store if the grid is destroyed
        autoDestroy: true,
        fields: [
        {
            name: 'h',
            type: 'float'},
        {
            name: 'k',
            type: 'float'},
        {
            name: 'l',
            type: 'float'},
        {
            name: 'twotheta',
            type: 'float'},
        {
            name: 'theta',
            type: 'float'},
        {
            name: 'chi',
            type: 'float'},
        {
            name: 'phi',
            type: 'float'},
        ]

    });
    store.loadData(baseData);

    var idealDataStore = new Ext.data.ArrayStore({
        // destroy the store if the grid is destroyed
        autoDestroy: true,
        fields: [
        {
            name: 'twotheta',
            type: 'float'},
        {
            name: 'theta',
            type: 'float'},
        {
            name: 'omega',
            type: 'float'},
        {
            name: 'chi',
            type: 'float'},
        {
            name: 'phi',
            type: 'float'},
        ]

    });
    idealDataStore.loadData(baseIdealData);

    // create the editor grid
    var grid = new Ext.grid.EditorGridPanel({
        store: store,
        cm: cm,
        width: 440,
        height: 200,
        //autoExpandColumn: 'common', // column with this id will be expanded
        title: 'Orientation',
        frame: true,
        clicksToEdit: 1,
        bbar: [{
            text: 'Submit',
            handler: submitData,
            }]
    });

    function submitData(button, event) {
        params = {
            'data': []
        };

        for (var i = 0; i < store.getCount(); i++) {
            var record = store.getAt(i)
            params['data'].push(record.data); //adding table's input to data to be sent to backend
        };
        params['data'].push({
            'a': aField.getValue(),
            'b': bField.getValue(),
            'c': cField.getValue(),
            'alpha': alphaField.getValue(),
            'beta': betaField.getValue(),
            'gamma': gammaField.getValue(),
            'h': hField.getValue(),
            'k': kField.getValue(),
            'l': lField.getValue(),
        });

        //params = {'data': [{'h':1,'k':1,'l':0,'twotheta':0,'theta':0, 'chi':89.62,'phi':0.001},                      
        //                   {'h':0,'k':0,'l':1,'twotheta':0,'theta':0,'chi':-1.286,'phi':131.063}]}
        conn.request({
            url: '/WRed/files/testbob/',
            method: 'POST',
            params: Ext.encode(params),
            success: successFunction,
            failure: function () {
                Ext.Msg.alert('Error: Failed request');
            }
        });

    };

    function successFunction(responseObject) {
        idealdata = Ext.decode(responseObject.responseText);
        console.log(idealdata);

        changes = ['twotheta', 'theta', 'omega', 'chi', 'phi'];
        record = idealDataStore.getAt(0);
        for (var c in changes) {
            fieldName = changes[c];
            record.set(fieldName, idealdata[fieldName]);
        }
    }

    var grid2 = new Ext.grid.EditorGridPanel({
        store: idealDataStore,
        cm: cm2,
        width: 320,
        height: 130,
        //autoExpandColumn: 'common', // column with this id will be expanded
        title: 'Desired Results',
        frame: true,
        clicksToEdit: 1,
    });

    // ********* START - Defining and assigning variables for the numberfield inputs  *********
    var aField = new Ext.form.NumberField({
        fieldLabel: 'a',
        allowBlank: false,
        decimalPrecision: 10,
    });
    var bField = new Ext.form.NumberField({
        fieldLabel: 'b',
        allowBlank: false,
        decimalPrecision: 10,

    });
    var cField = new Ext.form.NumberField({
        fieldLabel: 'c',
        allowBlank: false,
        decimalPrecision: 10,

    });
    var alphaField = new Ext.form.NumberField({
        fieldLabel: 'α',
        allowBlank: false,
        decimalPrecision: 10,

    });
    var betaField = new Ext.form.NumberField({
        fieldLabel: 'β',
        allowBlank: false,
        decimalPrecision: 10,

    });
    var gammaField = new Ext.form.NumberField({
        fieldLabel: 'γ',
        allowBlank: false,
        decimalPrecision: 10,

    });
    //desired h, k, l numberfields:
    var hField = new Ext.form.NumberField({
        fieldLabel: 'h',
        allowBlank: false,
        decimalPrecision: 10,

    });
    var kField = new Ext.form.NumberField({
        fieldLabel: 'k',
        allowBlank: false,
        decimalPrecision: 10,

    });
    var lField = new Ext.form.NumberField({
        fieldLabel: 'l',
        allowBlank: false,
        decimalPrecision: 10,

    });
    // ********* END - Defining and assigning variables for the numberfield inputs  *********  
    // ********* START - Defining and assigning variables for the numberfield inputs  *********  
    var form1 = new Ext.FormPanel({
        items: [
            aField,
            bField,
            cField,
            alphaField,
            betaField,
            gammaField,
            ],
        defaultType: 'numberfield',
        autoWidth: true,
        autoHeight: true,
        title: 'Lattice Constants',
        labelWidth: 30,
        bodyStyle: 'padding: 10px;',
        //padding the edges for aesthetics
    });

    var form2 = new Ext.FormPanel({
        items: [
            hField,
            kField,
            lField,
            ],
        defaultType: 'numberfield',
        autoWidth: true,
        autoHeight: true,
        title: 'Desired Orientation',
        labelWidth: 30,
        height: 130,
        bodyStyle: 'padding: 10px;',

    });

    var TopPanel = new Ext.Panel({
        layout: 'table',
        title: 'Given Data',
        layoutConfig: {
            columns: 2
        },
        items: [grid, form1],
    });

    var BottomPanel = new Ext.Panel({
        layout: 'table',
        title: 'Desired Data',
        layoutConfig: {
            columns: 2
        },
        items: [form2, grid2]
    });

    TopPanel.render('editor-grid');
    BottomPanel.render('result-grid');

});
