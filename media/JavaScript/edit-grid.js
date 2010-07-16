/*
 * Author: Alex Yee
 *
 * Edit History:
 * 7/12/2010: Created and completed. Created layout, columns, and data sending/receiving/updating. 
 *             Not entirely beautified yet.
 * 7/13/2010: Restructured to give each numberfield (of input) a separate variable so I could
 *             send their given values to the backend for calculations.
 */

Ext.onReady(function () {
    var conn = new Ext.data.Connection();
    
    // ********* START - Creating Column Models *********
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
            header: 'h',
            dataIndex: 'h',
        }, {
            header: 'k',
            dataIndex: 'k',
        }, {
            header: 'l',
            dataIndex: 'l',
        }, {
            header: '2θ',
            dataIndex: 'twotheta',
        }, {
            header: 'θ',
            dataIndex: 'theta',
        }, {
            header: 'ω',
            dataIndex: 'omega',
        }, {
            header: 'χ',
            dataIndex: 'chi',
        }, {
            header: 'φ',
            dataIndex: 'phi',
        },
        ]
    });
    
    //Setting the calculated angle values to uneditable
    cm2.setEditable(3, false);
    cm2.setEditable(4, false);
    cm2.setEditable(5, false);
    cm2.setEditable(6, false);
    cm2.setEditable(7, false);
    // ********* END - Creating Column Models *********
    
    
    var baseData = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ];
    var baseIdealData = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
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
        autoDestroy: false,
        fields: [
        {
            name: 'h',
            type: 'float'
        }, {
            name: 'k',
            type: 'float'
        }, {
            name: 'l',
            type: 'float'
        }, {
            name: 'twotheta',
            type: 'float'
        }, {
            name: 'theta',
            type: 'float',
        }, {
            name: 'omega',
            type: 'float',
        }, {
            name: 'chi',
            type: 'float',
        }, {
            name: 'phi',
            type: 'float',
        },
        ]

    });
    idealDataStore.loadData(baseIdealData);
    
    // ********* START - Defining and assigning variables for the numberfield inputs  *********
    var aField = new Ext.form.NumberField({
        fieldLabel: 'a',
        allowBlank: false,
        decimalPrecision: 10,
        anchor: '-10',
    });
    var bField = new Ext.form.NumberField({
        fieldLabel: 'b',
        allowBlank: false,
        decimalPrecision: 10,
        anchor: '-10',
    });
    var cField = new Ext.form.NumberField({
        fieldLabel: 'c',
        allowBlank: false,
        decimalPrecision: 10,
        anchor: '-10',
    });
    var alphaField = new Ext.form.NumberField({
        fieldLabel: 'α',
        allowBlank: false,
        decimalPrecision: 10,
        anchor: '-10',
    });
    var betaField = new Ext.form.NumberField({
        fieldLabel: 'β',
        allowBlank: false,
        decimalPrecision: 10,
        anchor: '-10',
    });
    var gammaField = new Ext.form.NumberField({
        fieldLabel: 'γ',
        allowBlank: false,
        decimalPrecision: 10,
        anchor: '-10',
    });
    var wavelengthField = new Ext.form.NumberField({
        fieldLabel: 'Wavelength',
        allowBlank: true,
        decimalPrecision: 10,
    });
    
    
    //scattering plane h, k, l numberfields:
    var h1Field = new Ext.form.NumberField({
        fieldLabel: 'h1',
        allowBlank: false,
        decimalPrecision: 10,
        anchor: '-10',
    });
    var k1Field = new Ext.form.NumberField({
        fieldLabel: 'k1',
        allowBlank: false,
        decimalPrecision: 10,
        anchor: '-10',
    });
    var l1Field = new Ext.form.NumberField({
        fieldLabel: 'l1',
        allowBlank: false,
        decimalPrecision: 10,
        anchor: '-10',
    });
    var h2Field = new Ext.form.NumberField({
        fieldLabel: 'h2',
        allowBlank: false,
        decimalPrecision: 10,
        anchor: '-10',
    });
    var k2Field = new Ext.form.NumberField({
        fieldLabel: 'k2',
        allowBlank: false,
        decimalPrecision: 10,
        anchor: '-10',
    });
    var l2Field = new Ext.form.NumberField({
        fieldLabel: 'l2',
        allowBlank: false,
        decimalPrecision: 10,
        anchor: '-10',
    });
    
    // ********* END - Defining and assigning variables for the numberfield inputs  *********  
 
    /*var form1 = new Ext.FormPanel({
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
        bodyStyle: 'padding: 10px;', //padding the edges for aesthetics
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
    });*/
        
    // create the editor grids
    var grid = new Ext.grid.EditorGridPanel({
        store: store,
        cm: cm,
        width: 440,
        height: 145,
        //autoExpandColumn: 'common', // column with this id will be expanded
        title: 'Observations',
        frame: true,
        clicksToEdit: 1,
        bbar: [{
            text: 'Submit',
            handler: submitData,
        }]
    });
    
    var grid2 = new Ext.grid.EditorGridPanel({
        store: idealDataStore,
        cm: cm2,
        width: 539,
        height: 200,
        title: 'Desired Results',
        frame: true,
        clicksToEdit: 1,
        tbar: [{
            text: 'Add New Row',
            handler: addRow,
        }, {
            text: 'Calculate Results',
            handler: calculateResults,
        }]
    });

    // ****************** START - Defining grid button functions ****************** 
    function submitData(button, event) { 
        //Calculates and stores the B and UB matricies when the button 'Submit' is pressed
        params = {'data': [] };

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
        });

        conn.request({
            url: '/WRed/files/calcUBmatrix/',
            method: 'POST',
            params: Ext.encode(params),
            success: function () {
                isUBcalculated = true;
                // update the innerLeftPanel's south panel's title
                southPanel.setTitle('UB Calculated: ' + isUBcalculated);
            },
            failure: function () {
                isUBcalculated = false;
                southPanel.setTitle('UB Calculated: ' + isUBcalculated);
                Ext.Msg.alert('Error: Failed to calculate UB matrix');
            }
        });

    };
    
    function calculateResults(button, event) {
        //Calculates the desired angles when the button 'Calculate Results' is pressed
        params = {'data': [] };
        numrows = idealDataStore.getCount();
        
        //IF it's in the omega mode AND isUBcalculated == true
        if (isUBcalculated && myCombo.getValue() == 'Omega = 0'){

            params['data'].push({
                'wavelength' : wavelengthField.getValue(),
                'numrows' : idealDataStore.getCount(), //gives how many rows
            }); 
            for (var j = 0; j < idealDataStore.getCount(); j++){
                //gets all the data from the Ideal Data table
                var record = idealDataStore.getAt(j)
                params['data'].push(record.data);
            }  
                
             conn.request({
                url: '/WRed/files/omegaZero/',
                method: 'POST',
                params: Ext.encode(params),
                success: successFunction,
                failure: function () {
                    Ext.Msg.alert('Error: Failed request');
                }
            });
        }
            /*for (var i = 0; i < numrows; i++){    
                //gets all the data from one row at a time
                //TODO only get the (h, k, l)
                  
                var record = idealDataStore.getAt(i)
                params['data'].push(record.data);
                
                conn.request({
                    url: '/WRed/files/omegaZero/',
                    method: 'POST',
                    params: Ext.encode(params),
                    success: successFunction(responseObject, i),
                    failure: function () {
                        Ext.Msg.alert('Error: Failed request');
                    }
                });
            }*/
 
        //ELSE IF the combobox is in the scattering plane mode AND isUBcalculated == true
        else if (isUBcalculated && myCombo.getValue() == 'Scattering Plane'){
            params['data'].push({
                'h1'        : h1Field.getValue(),
                'k1'        : k1Field.getValue(),
                'l1'        : l1Field.getValue(),
                'wavelength': wavelengthField.getValue(), //wavelength put on this line to make h/k/l#s easier to read
                'h2'        : h2Field.getValue(),
                'k2'        : k2Field.getValue(),
                'l2'        : l2Field.getValue(),
                'numrows'   : idealDataStore.getCount(), //gives how many rows
            });
            for (var j = 0; j < idealDataStore.getCount(); j++){
                //gets all the data from the Ideal Data table
                //TODO only get the (h, k, l)
                var record = idealDataStore.getAt(j)
                params['data'].push(record.data);
            }

            conn.request({
                url: '/WRed/files/scatteringPlane/',
                method: 'POST',
                params: Ext.encode(params),
                success: successFunction,
                failure: function () {
                    Ext.Msg.alert('Error: Failed request');
                }
            });
        }
        else {
            Ext.Msg.alert('Error: First calculate the UB matrix');
        }
    };
    
    test1 =[];
    function successFunction(responseObject) {
        idealdata = Ext.decode(responseObject.responseText);
        //idealdata = responseObject;
        //print('resp: '+responseObject);
        //idealdata = Ext.decode(responseObject);
        test1 = idealdata;
        //print('test1: ' + test1);
        //console.log(idealdata);

        changes = ['twotheta', 'theta', 'omega', 'chi', 'phi'];
        for (var i = 0; i < idealDataStore.getCount(); i++){
            console.log(i);
            record = idealDataStore.getAt(i); 
            for (var c in changes) {
                fieldName = changes[c];
                record.set(fieldName, idealdata[i][fieldName]);
            }
        }
    }

    function addRow() {
        var input = grid2.getStore().recordType;
        var r = new input({
            h: 0.0,
            k: 0.0,
            l: 0.0,
            twotheta: 0.0,
            theta: 0.0,
            omega: 0.0,
            chi: 0.0,
            phi: 0.0,
        });
        grid2.stopEditing(); 
        idealDataStore.insert(0, r); //adds new row to the top of the table (ie the first row)
        grid2.startEditing(0, 0); //starts editing for first cell of new row
    }
    
    // ****************** END - Defining grid button functions ****************** 
   
   
    //Setting up the ComboBox
    var myComboStore = new Ext.data.ArrayStore({
        data: [[1, 'Omega = 0'], [2, 'Scattering Plane']],
        fields: ['id', 'mode'],
        idIndex: 0, // !!!!!!
    });
    
    var myCombo = new Ext.form.ComboBox ({
        fieldLabel  : 'Select a Mode',
        store       : myComboStore,
        
        displayField: 'mode',
        typeAhead   : true,
        mode        : 'local',
        
        triggerAction:  'all', //Lets you see all drop down options
        selectOnFocus:  true,
        value        : 'Omega = 0',
        
        listeners: {
        // delete the previous query in the beforequery event or set
        // combo.lastQuery = null (this will reload the store the next time it expands)
            beforequery: function(qe){
                //qe.combo.lastQuery = '';
                delete qe.combo.lastQuery;
            }
        }

    });

    // ********* START - Setting up lattice constants GUI  ********* 
    var topFieldset = {
        xtype       : 'fieldset',
        //title       : 'Lattice Constants',
        border      : false,
        defaultType : 'numberfield',
        defaults    : {
            allowBlank : false,
            decimalPrecision: 10,
        },
        items: [
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '115%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items   : [
                            aField
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items       : [
                            bField                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items       : [
                            cField                               
                        ]
                    }, {
                        //Buffer blank space to even out the c inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1,
                    }
                ]
            },
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items   : [
                            alphaField
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items       : [
                            betaField                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items       : [
                            gammaField                               
                        ]
                    }, {
                        //Buffer blank space to even out the gamma inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1,
                    }
                ]
            },
            wavelengthField,
        ]
    };
    // ********* END - Setting up lattice constants GUI  ********* 
    
    // ********* STAR - Setting up scattering plane h/k/l GUI  ********* 
    var bottomFieldset = {
        xtype       : 'fieldset',
        title       : 'Scattering Plane Vectors',
        border      : false,
        defaultType : 'numberfield',
        defaults    : {
            allowBlank : false,
            decimalPrecision: 10,
        },
        items: [
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 15,
                        items   : [
                            h1Field
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 15,
                        items       : [
                            k1Field                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 15,
                        items       : [
                            l1Field                               
                        ]
                    }, {
                        //Buffer blank space to even out the l1 inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1,
                    }
                ]
            },
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 15,
                        items   : [
                            h2Field
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 15,
                        items       : [
                            k2Field                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 15,
                        items       : [
                            l2Field                               
                        ]
                    }, {
                        //Buffer blank space to even out the l2 inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1,
                    }
                ]
            },
            {
                //empty container to allow horizontal inputboxes for h,k,l
                xtype       : 'container',
                border      : false,
                width       : 230,
            } 
        ]
    };
    
    // ********* STAR - Setting up scattering plane h/k/l GUI  ********* 

    var innerRightTopPanel = new Ext.Panel({
        layout: 'border',
        width: 350,
        height: 170,
        border: true,
        items: [{
            title: 'Lattice Constants',
            region: 'center',
            margins: '0 5 0 5', //small margins to the east and west of box
            items: [topFieldset],
        }, {
            title: 'Choose the Mode:',
            region: 'north',
            height: 50,
            margins: '0 5 0 5',
            items: [myCombo],
        }]
    });   
    
    //Tells whether UB matrix has been calculated
    var isUBcalculated = false;
        
    var southPanel = new Ext.Panel ({
        region: 'south',
        height: 25,
        title: 'UB Calculated: '+isUBcalculated,
    });
    
    var innerLeftTopPanel = new Ext.Panel({
        layout: 'border',
        width: 440,
        height: 170,
        items: [{
            region: 'center',
            items: [grid],
        }, 
            southPanel,
        ]
    });

    
    var TopPanel = new Ext.Panel({
        layout: 'table',
        title: 'Known Data',
        width: 790,
        layoutConfig: {
            columns: 2
        },
        items: [innerLeftTopPanel, innerRightTopPanel],
    });

    var BottomPanel = new Ext.Panel({
        layout: 'table',
        title: 'Desired Data',
        width: 790,
        layoutConfig: {
            columns: 2
        },
        items: [bottomFieldset, grid2]
    });

    TopPanel.render('editor-grid');
    BottomPanel.render('result-grid');
    
    /* Testing...
    a1 = {'a': 3, 'b': 4};
    b1 = {'c': 5, 'd': 6};
    arr = [];
    arr.push(a1);
    arr.push(b1);
    */
});
